import os
import re
import socket
import struct
import subprocess
import time
from datetime import datetime, timezone
from functools import wraps
from pathlib import Path

from flask import Flask, jsonify, render_template, request, Response

app = Flask(__name__)

RCON_HOST = os.environ.get("RCON_HOST", "minecraft-server")
RCON_PORT = int(os.environ.get("RCON_PORT", 25575))
RCON_PASSWORD = os.environ.get("RCON_PASSWORD", "mcusiman123")
DASHBOARD_USER = os.environ.get("DASHBOARD_USER", "admin")
DASHBOARD_PASSWORD = os.environ.get("DASHBOARD_PASSWORD", "admin123")
MINECRAFT_DIR = os.environ.get("MINECRAFT_DIR", "/data")
LOGS_DIR = os.path.join(MINECRAFT_DIR, "logs")
BACKUPS_DIR = os.path.join(MINECRAFT_DIR, "backups")
WORLD_DIR = os.path.join(MINECRAFT_DIR, "world")


def rcon_send(command):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect((RCON_HOST, RCON_PORT))

        req_id = int(time.time())

        def send_packet(pkt_type, payload):
            body = payload.encode("utf-8") + b"\x00\x00"
            length = struct.pack("<i", 10 + len(payload))
            sock.sendall(length + struct.pack("<ii", req_id, pkt_type) + body)

        def recv_response():
            data = sock.recv(4)
            if len(data) < 4:
                return None
            resp_len = struct.unpack("<i", data)[0]
            resp = b""
            while len(resp) < resp_len:
                chunk = sock.recv(resp_len - len(resp))
                if not chunk:
                    break
                resp += chunk
            if len(resp) >= 8:
                _, pkt_type = struct.unpack("<ii", resp[:8])
                body = resp[8:-2].decode("utf-8", errors="replace")
                return body
            return None

        send_packet(3, RCON_PASSWORD)
        auth_resp = recv_response()
        send_packet(2, command)
        result = recv_response()

        sock.close()
        return result or ""
    except Exception as e:
        return f"RCON Error: {e}"


def get_container_stats():
    try:
        out = subprocess.run(
            ["docker", "stats", "minecraft-tlaucer-server",
             "--no-stream", "--format",
             "{{.CPUPerc}}|{{.MemPerc}}|{{.MemUsage}}|{{.NetIO}}|{{.PIDs}}"],
            capture_output=True, text=True, timeout=5
        )
        if not out.stdout.strip():
            return None
        parts = out.stdout.strip().split("|")
        if len(parts) >= 5:
            return {
                "cpu": parts[0],
                "mem_percent": parts[1],
                "mem_usage": parts[2],
                "net_io": parts[3],
                "pids": parts[4],
            }
    except Exception:
        pass
    return None


def check_auth(username, password):
    return username == DASHBOARD_USER and password == DASHBOARD_PASSWORD


def authenticate():
    return Response("Auth required", 401,
                    {"WWW-Authenticate": 'Basic realm="Dashboard"'})


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


def get_server_status():
    response = rcon_send("list")
    if response.startswith("RCON Error"):
        return {"online": False, "error": response}

    players = []
    m = re.search(r"There are (\d+) of a max of \d+ players online: (.*)", response)
    if m:
        player_data = m.group(2).strip()
        if player_data:
            players = [p.strip() for p in player_data.split(",") if p.strip()]

    return {"online": True, "players": players, "player_count": len(players), "raw": response}


def get_world_size():
    path = Path(WORLD_DIR)
    if path.exists():
        total = sum(f.stat().st_size for f in path.rglob("*") if f.is_file())
        return f"{total / 1024 / 1024:.1f} MB"
    return "N/A"


def get_motd():
    props = Path(MINECRAFT_DIR) / "server.properties"
    motd = "Minecraft Server"
    if props.exists():
        for line in props.read_text().splitlines():
            if line.startswith("motd="):
                motd = line.split("=", 1)[1].strip()
                break
    return motd


@app.route("/")
def index():
    return render_template("index.html", motd=get_motd())


@app.route("/logs")
def logs_page():
    return render_template("logs.html")


@app.route("/rcon")
@requires_auth
def rcon_page():
    return render_template("rcon.html")


@app.route("/backups")
@requires_auth
def backups_page():
    return render_template("backups.html")


@app.route("/api/status")
def api_status():
    status = get_server_status()
    stats = get_container_stats()
    return jsonify({
        "server": status,
        "container": stats,
        "world_size": get_world_size(),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })


@app.route("/api/logs")
def api_logs():
    tail = request.args.get("tail", 50, type=int)
    level = request.args.get("level", "").lower()
    search = request.args.get("search", "").lower()

    log_file = Path(LOGS_DIR) / "latest.log"
    if not log_file.exists():
        return jsonify({"lines": [], "error": "No log file"})

    try:
        lines = log_file.read_text().splitlines()
        if level:
            lines = [l for l in lines if f"[{level.upper()}]" in l]
        if search:
            lines = [l for l in lines if search in l.lower()]
        lines = lines[-tail:]
        return jsonify({"lines": lines, "total": len(lines)})
    except Exception as e:
        return jsonify({"lines": [], "error": str(e)})


@app.route("/api/rcon", methods=["POST"])
@requires_auth
def api_rcon():
    data = request.get_json()
    if not data or "command" not in data:
        return jsonify({"error": "No command"}), 400
    cmd = data["command"].strip()
    if not cmd:
        return jsonify({"error": "Empty command"}), 400

    dangerous = any(cmd.lower().startswith(d) for d in
                    ["stop", "ban", "kick", "op", "deop", "whitelist"])
    response = rcon_send(cmd)
    return jsonify({"response": response, "command": cmd, "dangerous": dangerous})


@app.route("/api/backups", methods=["GET"])
@requires_auth
def api_list_backups():
    bdir = Path(BACKUPS_DIR)
    if not bdir.exists():
        return jsonify({"backups": []})
    backups = []
    for f in sorted(bdir.iterdir(), key=lambda x: x.stat().st_mtime, reverse=True):
        if f.is_file() and f.suffix == ".gz":
            backups.append({
                "name": f.name,
                "size": f"{f.stat().st_size / 1024 / 1024:.1f} MB",
                "date": datetime.fromtimestamp(f.stat().st_mtime, tz=timezone.utc).isoformat(),
            })
    return jsonify({"backups": backups})


@app.route("/api/backups", methods=["POST"])
@requires_auth
def api_create_backup():
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    dest = Path(BACKUPS_DIR) / f"world-{ts}.tar.gz"
    try:
        Path(BACKUPS_DIR).mkdir(parents=True, exist_ok=True)
        subprocess.run(
            ["tar", "-czf", str(dest), "-C", str(Path(WORLD_DIR).parent), "world"],
            capture_output=True, timeout=120
        )
        return jsonify({"status": "success", "name": dest.name,
                        "size": f"{dest.stat().st_size / 1024 / 1024:.1f} MB"})
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


@app.route("/api/backups/<name>", methods=["DELETE"])
@requires_auth
def api_delete_backup(name):
    p = Path(BACKUPS_DIR) / name
    if p.exists():
        p.unlink()
        return jsonify({"status": "deleted"})
    return jsonify({"error": "Not found"}), 404


@app.route("/api/health")
def api_health():
    return jsonify({"status": "ok"})

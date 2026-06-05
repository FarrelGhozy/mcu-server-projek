import os
import subprocess
import time
from datetime import datetime
from functools import wraps
from pathlib import Path

from flask import Flask, jsonify, render_template, request, Response
from mcrcon import MCRcon

app = Flask(__name__)

# Config
RCON_HOST = os.environ.get("RCON_HOST", "minecraft-server")
RCON_PORT = int(os.environ.get("RCON_PORT", 25575))
RCON_PASSWORD = os.environ.get("RCON_PASSWORD", "mcusiman123")
DASHBOARD_USER = os.environ.get("DASHBOARD_USER", "admin")
DASHBOARD_PASSWORD = os.environ.get("DASHBOARD_PASSWORD", "admin123")
MINECRAFT_DIR = os.environ.get("MINECRAFT_DIR", "/data")
LOGS_DIR = os.environ.get("LOGS_DIR", os.path.join(MINECRAFT_DIR, "logs"))
BACKUPS_DIR = os.environ.get("BACKUPS_DIR", os.path.join(MINECRAFT_DIR, "backups"))
WORLD_DIR = os.environ.get("WORLD_DIR", os.path.join(MINECRAFT_DIR, "world"))


def rcon_command(command):
    try:
        with MCRcon(RCON_HOST, RCON_PASSWORD, port=RCON_PORT) as mcr:
            return mcr.command(command)
    except Exception as e:
        return f"Error: {e}"


def check_auth(username, password):
    return username == DASHBOARD_USER and password == DASHBOARD_PASSWORD


def authenticate():
    return Response(
        "Authentication required", 401,
        {"WWW-Authenticate": 'Basic realm="Dashboard Login"'}
    )


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


def get_container_stats():
    try:
        result = subprocess.run(
            ["docker", "stats", "minecraft-tlaucer-server",
             "--no-stream", "--format",
             "{{.CPUPerc}}|{{.MemPerc}}|{{.MemUsage}}|{{.NetIO}}|{{.PIDs}}"],
            capture_output=True, text=True, timeout=5
        )
        parts = result.stdout.strip().split("|")
        if len(parts) == 5:
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


def get_server_status():
    response = rcon_command("list")
    if response.startswith("Error"):
        return {"online": False, "error": response}

    players = []
    if ":" in response:
        parts = response.split(":")
        if len(parts) > 1:
            player_part = parts[1].strip()
            if player_part:
                players = [p.strip() for p in player_part.split(",") if p.strip()]

    return {
        "online": True,
        "players": players,
        "player_count": len(players),
        "raw": response,
    }


def get_world_size():
    path = Path(WORLD_DIR)
    if path.exists():
        total = sum(f.stat().st_size for f in path.rglob("*") if f.is_file())
        return f"{total / 1024 / 1024:.1f} MB"
    return "N/A"


@app.route("/")
def index():
    return render_template("index.html")


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
    world_size = get_world_size()

    result = {
        "server": status,
        "container": stats,
        "world_size": world_size,
        "timestamp": datetime.now().isoformat(),
    }
    return jsonify(result)


@app.route("/api/logs")
def api_logs():
    tail = request.args.get("tail", 50, type=int)
    level = request.args.get("level", "").lower()
    search = request.args.get("search", "").lower()

    latest_log = Path(LOGS_DIR) / "latest.log"
    if not latest_log.exists():
        return jsonify({"lines": [], "error": "No log file found"})

    try:
        with open(latest_log, "r") as f:
            lines = f.readlines()

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
        return jsonify({"error": "No command provided"}), 400

    command = data["command"].strip()
    if not command:
        return jsonify({"error": "Empty command"}), 400

    dangerous = ["stop", "ban", "kick", "op", "deop", "whitelist"]
    is_dangerous = any(command.lower().startswith(d) for d in dangerous)

    response = rcon_command(command)
    return jsonify({
        "response": response,
        "command": command,
        "dangerous": is_dangerous,
    })


@app.route("/api/backups", methods=["GET"])
@requires_auth
def api_list_backups():
    backup_dir = Path(BACKUPS_DIR)
    if not backup_dir.exists():
        return jsonify({"backups": []})

    backups = []
    for f in sorted(backup_dir.iterdir(), key=lambda x: x.stat().st_mtime, reverse=True):
        if f.is_file() and f.suffix == ".gz":
            backups.append({
                "name": f.name,
                "size": f"{f.stat().st_size / 1024 / 1024:.1f} MB",
                "date": datetime.fromtimestamp(f.stat().st_mtime).isoformat(),
            })

    return jsonify({"backups": backups})


@app.route("/api/backups", methods=["POST"])
@requires_auth
def api_create_backup():
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_path = Path(BACKUPS_DIR) / f"world-{timestamp}.tar.gz"

    try:
        Path(BACKUPS_DIR).mkdir(parents=True, exist_ok=True)
        subprocess.run(
            ["tar", "-czf", str(backup_path), "-C", str(Path(WORLD_DIR).parent), "world"],
            capture_output=True, text=True, timeout=120
        )
        return jsonify({
            "status": "success",
            "name": backup_path.name,
            "size": f"{backup_path.stat().st_size / 1024 / 1024:.1f} MB",
        })
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


@app.route("/api/backups/<name>", methods=["DELETE"])
@requires_auth
def api_delete_backup(name):
    backup_path = Path(BACKUPS_DIR) / name
    if backup_path.exists():
        backup_path.unlink()
        return jsonify({"status": "deleted"})
    return jsonify({"error": "File not found"}), 404


@app.route("/api/motd")
def api_motd():
    status = get_server_status()
    if not status["online"]:
        return jsonify({"motd": "Server Offline", "version": "N/A"})

    props_path = Path(MINECRAFT_DIR) / "server.properties"
    motd = "Minecraft Server"
    version = "Unknown"

    if props_path.exists():
        with open(props_path) as f:
            for line in f:
                if line.startswith("motd="):
                    motd = line.split("=", 1)[1].strip()
                if line.startswith("max-players="):
                    version = f"Paper (max {line.split('=')[1].strip()} players)"

    return jsonify({
        "motd": motd,
        "version": "Paper 26.1.2",
        "online": status["online"],
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

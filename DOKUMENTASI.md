# 📋 Dokumentasi Teknis — Tlaucer Minecraft Server

## Arsitektur Sistem

```
Internet
    │
    ├── Cloudflare Tunnel (remote managed)
    │     ├── mcu.utc.web.id → TCP:8443  → Minecraft Server
    │     └── admin.mcu.utc.web.id → HTTP:5000  → Dashboard
    │
    ├── Docker Container: minecraft-tlaucer-server
    │     └── Port: 8443 (host) → 25565 (container)
    │                           └── Minecraft Paper 1.21.11 (offline-mode)
    │
    └── Docker Container: minecraft-dashboard
          └── Port: 5000 (host)
                └── Flask Dashboard (Python)
```

## Spesifikasi

| Item | Detail |
|------|--------|
| **Host** | Linux (Docker) |
| **Container Minecraft** | `itzg/minecraft-server:latest` |
| **Container Dashboard** | `python:3.12-slim` (Flask + Gunicorn) |
| **Server Type** | Paper 1.21.11 |
| **Memory** | 4GB (4096M) |
| **Host Ports** | 8443 (Minecraft) · 5000 (Dashboard) |
| **Mode** | Offline (Tlaucer) |
| **Domain** | mcu.utc.web.id (Minecraft) |
| **Dashboard** | admin.mcu.utc.web.id |
| **Directory** | `/home/ghozy/Server-Tlaucer` |

## Management Commands

### Server Lifecycle
```bash
cd /home/ghozy/Server-Tlaucer

# Start all services
docker compose up -d

# Stop
docker compose stop

# Restart
docker compose restart

# Rebuild & start (after code changes)
docker compose up -d --build

# View logs
docker compose logs -f minecraft-server
docker compose logs -f dashboard
docker compose logs --tail=50 minecraft-server
```

### RCON Console
```bash
docker compose exec minecraft-server rcon-cli
```

**RCON Credentials:**
- Password: `mcusiman123`
- Port internal: 25575

### Monitoring
```bash
# Container stats
docker stats minecraft-tlaucer-server

# Check ports
ss -tlnp | grep -E "8443|5000"

# API test
curl http://localhost:5000/api/status
curl http://localhost:5000/api/health
```

## File Structure
```
/home/ghozy/Server-Tlaucer/
├── docker-compose.yml       # Konfigurasi Docker
├── .env                     # Environment variables
├── AGENTS.md                # Panduan untuk AI agents
├── PLANNING.md              # Planning dokumen
├── README.md                # Panduan untuk pemain
├── DOKUMENTASI.md           # Dokumentasi teknis
├── server.properties        # Config server Minecraft
├── eula.txt                 # EULA (已同意)
├── world/                   # World data
├── plugins/                 # Plugin folder
├── logs/                    # Log files
├── backups/                 # Backup world
└── dashboard/               # Dashboard aplikasi
    ├── Dockerfile
    ├── requirements.txt
    ├── app.py               # Flask app
    ├── templates/           # HTML templates
    └── static/              # CSS & JS
```

## Dashboard

### Akses
- **URL:** `https://admin.mcu.utc.web.id` (via Cloudflare Tunnel)
- **Login:** `admin` / `admin123`
- **Auto-refresh:** 5 detik (dashboard), 10 detik (logs)

### Fitur
| Halaman | URL | Auth | Fungsi |
|---------|-----|------|--------|
| Dashboard | `/` | Tidak | Status server, player, resource |
| Logs | `/logs` | Tidak | Live logs dengan filter & search |
| RCON | `/rcon` | Basic Auth | Kirim command ke server |
| Backups | `/backups` | Basic Auth | List, create, delete backup |

### API Endpoints
| Endpoint | Method | Auth | Response |
|----------|--------|------|----------|
| `/api/status` | GET | Tidak | Server status, player, container stats |
| `/api/logs?tail=50&level=&search=` | GET | Tidak | Log entries |
| `/api/rcon` | POST | Basic Auth | Execute RCON command |
| `/api/backups` | GET | Basic Auth | List backups |
| `/api/backups` | POST | Basic Auth | Create backup |
| `/api/backups/<name>` | DELETE | Basic Auth | Delete backup |
| `/api/health` | GET | Tidak | Health check |

## Backup

### Via Dashboard
1. Buka `admin.mcu.utc.web.id/backups`
2. Klik **"Create Backup"**
3. Backup tersimpan di `backups/` folder

### Manual
```bash
cd /home/ghozy/Server-Tlaucer
docker compose stop
# Backup world
tar -czf backups/world-$(date +%Y%m%d-%H%M%S).tar.gz world
docker compose up -d
```

### Restore
```bash
cd /home/ghozy/Server-Tlaucer
docker compose stop
rm -rf world
tar -xzf backups/world-20250605-*.tar.gz
docker compose up -d
```

### Auto Backup (Crontab)
```bash
crontab -e
# Backup jam 2 pagi, hapus backup >7 hari:
0 2 * * * cd /home/ghozy/Server-Tlaucer && tar -czf backups/world-$(date +\%Y\%m\%d).tar.gz world && find backups -name "world-*.tar.gz" -mtime +7 -delete
```

## Menambah Plugin

### Via Download Langsung
```bash
cd /home/ghozy/Server-Tlaucer
wget <url-plugin> -O plugins/<nama>.jar
docker compose restart minecraft-server
```

### Via docker-compose.yml
```yaml
environment:
  PLUGINS: "https://url-plugin1.jar|https://url-plugin2.jar"
```
Lalu rebuild: `docker compose up -d --build`

## Troubleshooting

### Server tidak bisa start?
```bash
docker compose logs minecraft-server --tail=50
```

### Dashboard error?
```bash
docker compose logs dashboard --tail=50
```

### Player tidak bisa connect?
```bash
# Cek port
ss -tlnp | grep 8443

# Cek server log
docker compose logs --tail=20 minecraft-server

# Cek tunnel
sudo systemctl status cloudflared
```

### Container restart loop?
- Naikkan memory di `.env`
- Cek port conflict: `ss -tlnp | grep -E "8443|5000"`

## Cloudflare Tunnel

Config dikelola via **Cloudflare Zero Trust Dashboard**:
1. Buka [Cloudflare Dashboard](https://dash.cloudflare.com/) → **Zero Trust** → **Networks** → **Tunnels**
2. Pilih tunnel → **Edit** → **Public Hostname**

### Public Hostnames yang harus ada:
| Hostname | Service | Tujuan |
|----------|---------|--------|
| `mcu.utc.web.id` | `tcp://localhost:8443` | Minecraft |
| `admin.mcu.utc.web.id` | `http://localhost:5000` | Dashboard |

### Restart Tunnel
```bash
sudo systemctl restart cloudflared
```

### Cek Status
```bash
sudo systemctl status cloudflared
sudo journalctl -u cloudflared -f  # Live logs
```

## Konfigurasi Penting

### server.properties
```properties
online-mode=false
enforce-secure-profile=false
server-port=25565
enable-rcon=true
rcon.password=mcusiman123
max-players=20
pvp=true
difficulty=normal
gamemode=survival
```

### docker-compose.yml
```yaml
services:
  minecraft-server:
    image: itzg/minecraft-server:latest
    ports: ["8443:25565"]
    environment:
      EULA: "TRUE"
      ONLINE_MODE: "false"
      TYPE: "PAPER"
      MEMORY: "4096M"
      RCON_PASSWORD: "mcusiman123"
    volumes: [".:/data"]

  dashboard:
    build: ./dashboard
    ports: ["5000:5000"]
    environment:
      RCON_PASSWORD: "mcusiman123"
      DASHBOARD_USER: "admin"
      DASHBOARD_PASSWORD: "admin123"
    volumes:
      - .:/data:ro
      - /var/run/docker.sock:/var/run/docker.sock:ro
```

### Environment Variables
| Variable | Default | Fungsi |
|----------|---------|--------|
| MEMORY | 4096M | RAM Minecraft |
| MAX_PLAYERS | 20 | Max player |
| RCON_PASSWORD | mcusiman123 | Password RCON |
| DASHBOARD_USER | admin | Login dashboard |
| DASHBOARD_PASSWORD | admin123 | Password dashboard |

---

**Dibuat:** Juni 2026
**Minecraft:** mcu.utc.web.id:8443
**Dashboard:** admin.mcu.utc.web.id

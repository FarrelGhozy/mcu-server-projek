# AGENTS.md — Minecraft Tlaucer Server

## Project Info
- **Server:** Minecraft Paper (offline-mode/Tlaucer)
- **Setup:** Docker Compose
- **Ports:** 8443 (Minecraft) · 5000 (Dashboard)
- **Domain:** mcu.utc.web.id
- **Dashboard:** admin.mcu.utc.web.id (via Cloudflare Tunnel)
- **Directory:** `/home/ghozy/Server-Tlaucer`
- **Memory:** 4GB (4096M)

## Commands

### Start All Services
```bash
cd /home/ghozy/Server-Tlaucer
docker compose up -d
docker compose logs -f
```

### Start / Stop / Restart
```bash
docker compose up -d       # Start
docker compose stop        # Stop
docker compose restart     # Restart
docker compose up -d --build  # Rebuild & start (after code changes)
```

### View Logs
```bash
docker compose logs -f minecraft-server   # Minecraft logs
docker compose logs -f dashboard          # Dashboard logs
docker compose logs --tail=50 minecraft-server
```

### RCON Console
```bash
# Via CLI
docker compose exec minecraft-server rcon-cli

# Via Dashboard
# Buka admin.mcu.utc.web.id/rcon di browser (login: admin / admin123)
```

Useful RCON commands:
- `say <message>` — broadcast
- `list` — players online
- `save-all` — force save world
- `stop` — stop server
- `op <player>` — give operator
- `gamemode <0/1/2/3> <player>` — change gamemode
- `time set day/night` — set waktu
- `weather clear/rain/thunder` — set cuaca

### Resource Monitor
```bash
docker stats minecraft-tlaucer-server
# Atau lihat di Dashboard (admin.mcu.utc.web.id)
```

### Backup World
```bash
# Manual
tar -czf backups/world-$(date +%Y%m%d-%H%M%S).tar.gz world

# Via Dashboard
# Buka admin.mcu.utc.web.id/backups → klik "Create Backup"
```

### Add Plugin
```bash
wget <plugin-url> -O plugins/<plugin-name>.jar
docker compose restart minecraft-server
```

### Dashboard API (internal)
```bash
curl http://localhost:5000/api/status      # JSON status
curl http://localhost:5000/api/logs        # JSON logs
curl http://localhost:5000/api/health      # Health check
```

## RCON Info
- **Password:** mcusiman123
- **Port:** 25575 (internal container)
- **Function:** Remote console via CLI atau Dashboard

## Dashboard Info
- **URL:** admin.mcu.utc.web.id
- **Login:** admin / admin123
- **Fitur:** Status server, player list, live logs, RCON console, backup manager
- **Auto-refresh:** 5 detik (dashboard), 10 detik (logs)

## Cloudflare Tunnel
Config di Cloudflare Zero Trust Dashboard (remote managed):
```yaml
Public Hostnames:
  - mcu.utc.web.id → tcp://localhost:8443   # Minecraft
  - admin.mcu.utc.web.id → http://localhost:5000  # Dashboard
```

## Connection Info
- **Minecraft:** `mcu.utc.web.id:8443` (Tlaucer, offline mode)
- **Dashboard:** `https://admin.mcu.utc.web.id` (browser)

## Environment File
File `.env` berisi konfigurasi yang bisa diubah tanpa edit docker-compose.yml.

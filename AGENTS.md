# AGENTS.md — Minecraft Tlaucer Server

## Project Info
- **Server:** Minecraft Paper (offline-mode/Tlaucer)
- **Setup:** Docker Compose
- **Port:** 1350 (host) → 25565 (container)
- **Domain:** mcu.utc.web.id
- **Directory:** `/home/ghozy/Server-Tlaucer`
- **Memory:** 4GB (4096M)

## Commands

### Start Server
```bash
cd /home/ghozy/Server-Tlaucer
docker compose up -d
docker compose logs -f
```

### Stop Server
```bash
docker compose stop
```

### Restart Server
```bash
docker compose restart
```

### View Logs
```bash
docker compose logs -f minecraft-server
docker compose logs --tail=50 minecraft-server
```

### RCON Console (Remote Console)
```bash
docker compose exec minecraft-server rcon-cli
```
Useful RCON commands:
- `say <message>` — broadcast message
- `list` — see online players
- `save-all` — force save world
- `stop` — stop server
- `op <player>` — give operator
- `gamemode <0/1/2/3> <player>` — change gamemode

### Resource Monitor
```bash
docker stats minecraft-server
```

### Backup World
```bash
tar -czf backups/world-$(date +%Y%m%d-%H%M%S).tar.gz world
```

### Add Plugin
```bash
wget <plugin-url> -O plugins/<plugin-name>.jar
docker compose restart minecraft-server
```

## RCON Info
- **Password:** mcusiman123
- **Port:** 25575 (internal container)
- **Function:** Remote console untuk manage server tanpa perlu masuk game

## Cloudflare Tunnel
Ingress rule di `/etc/cloudflared/config.yml`:
```yaml
ingress:
  - hostname: mcu.utc.web.id
    service: tcp://localhost:1350
  - service: http_status:404
```
Restart: `sudo systemctl restart cloudflared`

## Environment File
File `.env` berisi konfigurasi yang bisa diubah tanpa edit docker-compose.yml.

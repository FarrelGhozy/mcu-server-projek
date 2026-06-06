# AGENTS.md — Minecraft Home Server (Tlaucer)

## Project Info
- **Server:** Minecraft Forge 1.20.1 + Mekanism + JEI + Veinst VeinMiner + JourneyMap (offline-mode/Tlaucer)
- **Setup:** Docker Compose
- **Port:** 25565 (Minecraft) · 25575 (RCON)
- **Akses:** IP Lokal Server (contoh: `192.168.x.x:25565`)
- **Directory:** `/home/ghozy/Server-Tlaucer`
- **Memory:** 4GB (4096M)

## Commands

### Start / Stop / Restart
```bash
docker compose up -d             # Start
docker compose stop               # Stop
docker compose restart            # Restart
docker compose up -d --build      # Rebuild & start (after config changes)
```

### View Logs
```bash
docker compose logs -f minecraft-server
docker compose logs --tail=50 minecraft-server
```

### RCON Console
```bash
docker compose exec minecraft-server rcon-cli
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
docker stats minecraft-home-server
```

### Backup World
```bash
tar -czf backups/world-$(date +%Y%m%d-%H%M%S).tar.gz world
```

### Add Mod
```bash
# Taruh file .jar mod Forge 1.20.1 di folder mods/
cp /path/to/mod.jar /home/ghozy/Server-Tlaucer/mods/
docker compose restart minecraft-server
```

## RCON Info
- **Password:** mcusiman123
- **Port:** 25575 (internal container)
- **Function:** Remote console via CLI

## Connection Info
- **Minecraft:** `{IP_SERVER}:25565` (Tlaucer, offline mode)
- Cek IP server: `ip a | grep 192.168`

## Catatan Penting
- Server ini untuk **jaringan lokal** — semua pemain harus dalam Wi-Fi/network yang sama
- Setiap client **wajib pasang mod yang sama** di folder `.minecraft/mods/`
- Mod hanya untuk Forge **1.20.1** — cek kompatibilitas sebelum download
- File `.env` berisi konfigurasi yang bisa diubah tanpa edit docker-compose.yml
- Server akan terus berkembang — dokumentasi akan diupdate bertahap

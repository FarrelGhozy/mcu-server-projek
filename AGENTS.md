# AGENTS.md — Minecraft Home Server (Tlaucer)

## Project Info
- **Server:** Minecraft Forge 1.20.1 + Mekanism + JEI + Veinst VeinMiner + JourneyMap + GraveStone (offline-mode/Tlaucer)
- **Setup:** Docker Compose
- **Port:** 200 (Minecraft) · 25575 (RCON)
- **Akses:** `localhost:200` (dari host server) · pemain lain pakai IP server (`hostname -I`)
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
# Cara cepat: auto-download semua mod (9 file) dari link resmi ke folder mods/
bash download_mod.sh <folder>     # Linux/macOS  (tanpa argumen = folder mods/ di folder script)
download_mod.bat <folder>         # Windows      (klik 2× jika tanpa folder custom)

# Atau manual: taruh file .jar mod Forge 1.20.1 di folder mods/ server
cp /path/to/mod.jar /home/ghozy/Server-Tlaucer/mods/
docker compose restart minecraft-server
```

## RCON Info
- **Password:** mcusiman123
- **Port:** 25575 (internal container)
- **Function:** Remote console via CLI

## Connection Info
- **Minecraft** (Tlaucer, offline mode):
  - Dalam kampus UNIDA: `172.20.20.200:200`
  - Luar kampus UNIDA (dari mana saja): `103.195.19.115:200`
  - Host server: `localhost:200`
- Cek IP LAN server: `hostname -I` · Cek IP publik: `curl ifconfig.me`

## Catatan Penting
- Akses server: dalam kampus UNIDA `172.20.20.200:200`, luar kampus `103.195.19.115:200`, host `localhost:200` — pemain wajib bisa menjangkau alamat tersebut
- Setiap client **wajib pasang mod yang sama** di folder `.minecraft/mods/`
- Mod hanya untuk Forge **1.20.1** — cek kompatibilitas sebelum download
- File `.env` berisi konfigurasi yang bisa diubah tanpa edit docker-compose.yml
- Server akan terus berkembang — dokumentasi akan diupdate bertahap

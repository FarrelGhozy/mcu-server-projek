# PLANNING.md — Minecraft Home Server (Tlaucer)

## Status: Aktif — Tahap Lokal

### Arsitektur Saat Ini
```
[ Laptop Player 1 ] ───┐
[ Laptop Player 2 ] ───┼── (Jaringan Lokal / Wi-Fi) ──► [ Ubuntu Server ]
[ Laptop Player 3 ] ───┘                                   │
                                                      ┌─────────────────┐
                                                      │ Forge 1.20.1    │
                                                      │ + Mekanism      │
                                                      │ + JEI           │
                                                      │ + Veinst        │
                                                      └─────────────────┘
```

### ✅ Sudah Berjalan
- [x] Docker Compose setup
- [x] Forge 1.20.1
- [x] Port 25565 (Minecraft)
- [x] RCON (port 25575)
- [x] Offline-mode (Tlaucher)
- [x] Clean start (world baru)
- [x] Folder `mods/` siap pakai
- [x] Mekanism (Core + Generators + Tools)
- [x] Architectury API + Cloth Config API (dependensi)
- [x] JEI (Just Enough Items)
- [x] Veinst VeinMiner (shift + mine)

### 📌 Rencana Selanjutnya (bertahap)
- [ ] Tambah mod-mod lain sesuai kebutuhan (sudah: Mekanism, JEI, Veinst)
- [ ] Optimasi performa (kalau ada lag)
- [ ] Whitelist / permission system
- [ ] Backup otomatis (cron job)
- [ ] Dashboard monitoring (future)
- [ ] Cloudflare Tunnel (future — akses remote)

## Keterangan

### docker-compose.yml (current)
```yaml
services:
  minecraft-server:
    image: itzg/minecraft-server:latest
    container_name: minecraft-home-server
    ports:
      - "25565:25565"
    environment:
      EULA: "TRUE"
      ONLINE_MODE: "false"
      TYPE: "FORGE"
      VERSION: "1.20.1"
      MEMORY: "4096M"
      JVM_OPTS: "-Xmx4096M -Xms2048M"
      DIFFICULTY: "2"
      GAMEMODE: "0"
      PVP: "true"
      ALLOW_FLIGHT: "false"
      MAX_PLAYERS: "20"
      ENABLE_RCON: "true"
      RCON_PASSWORD: "mcusiman123"
      RCON_PORT: "25575"
    volumes:
      - /home/ghozy/Server-Tlaucer:/data
    restart: unless-stopped
```

### .env
```
MINECRAFT_DIR=/home/ghozy/Server-Tlaucer
CONTAINER_NAME=minecraft-home-server
MEMORY=4096M
MAX_PLAYERS=20
RCON_PASSWORD=mcusiman123
DIFFICULTY=2
GAMEMODE=0
HOST_PORT=25565
MINECRAFT_VERSION=1.20.1
SERVER_TYPE=FORGE
```

## Catatan
- Dokumentasi akan selalu diupdate sesuai perkembangan server
- Setiap fase baru akan ditambahkan ke rencana di atas
- Prioritaskan kestabilan sebelum nambah fitur baru

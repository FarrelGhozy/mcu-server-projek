# Dokumentasi Teknis — Tlaucer Minecraft Home Server

## Arsitektur Sistem

```
[ Laptop Player 1 ] ───┐
[ Laptop Player 2 ] ───┼── (Jaringan Lokal / Wi-Fi) ──► [ Ubuntu Server ]
[ Laptop Player 3 ] ───┘                                   │
                                                     ┌─────────────────┐
                                                     │ Forge 1.20.1    │
                                                     │ + Mekanism      │
                                                     │ + JEI           │
                                                      │ + Veinst     │
                                                      └─────────────────┘
```

## Spesifikasi

| Item | Detail |
|------|--------|
| **Host** | Linux (Docker) |
| **Container** | `itzg/minecraft-server:latest` |
| **Server Type** | Forge 1.20.1 + Mekanism + JEI + Veinst + JourneyMap + GraveStone |
| **Memory** | 4GB (4096M) |
| **Port** | 200 (host) → 25565 (container) |
| **Mode** | Offline (Tlaucer) |
| **Directory** | `/home/ghozy/Server-Tlaucer` |
| **Mods** | Mekanism + Generators + Tools + JEI + Veinst + JourneyMap + GraveStone |

## Management Commands

## Management Commands

### Server Lifecycle
```bash
cd /home/ghozy/Server-Tlaucer

# Start
docker compose up -d

# Stop
docker compose stop

# Restart
docker compose restart

# Rebuild & start (after config changes)
docker compose up -d --build

# View logs
docker compose logs -f minecraft-server
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
docker stats minecraft-home-server
ss -tlnp | grep :200
```

## File Structure
```
/home/ghozy/Server-Tlaucer/
├── docker-compose.yml       # Konfigurasi Docker
├── .env                     # Environment variables
├── AGENTS.md                # Panduan AI agents
├── PLANNING.md              # Rencana pengembangan
├── README.md                # Panduan pemain
├── DOKUMENTASI.md           # Dokumentasi teknis
├── server.properties        # Config server Minecraft
├── eula.txt                 # EULA
├── mods/                    # Mod server (Forge 1.20.1)
│   ├── Mekanism-1.20.1-10.4.16.80.jar
│   ├── MekanismGenerators-1.20.1-10.4.16.80.jar
│   ├── MekanismTools-1.20.1-10.4.16.80.jar
│   ├── architectury-9.2.14-forge.jar
│   ├── cloth-config-11.1.136-forge.jar
│   ├── jei-1.20.1-forge-15.20.0.130.jar
│   ├── veinst_veinminer-1.3.0-1.20.1.jar
│   └── journeymap-1.20.1-5.10.3-forge.jar
├── config/                  # Config mod (auto-generated)
├── defaultconfigs/          # Default config mod
├── libraries/               # Library Forge
├── versions/                # Version metadata
├── world/                   # World data
├── logs/                    # Log files
└── backups/                 # Backup world
```

## Konfigurasi Penting

### server.properties
```properties
online-mode=false
enforce-secure-profile=false
server-port=25565
enable-rcon=true
rcon.password=mcusiman123
max-players=30
pvp=true
difficulty=normal
gamemode=survival
```

### docker-compose.yml
```yaml
services:
  minecraft-server:
    image: itzg/minecraft-server:latest
    container_name: minecraft-home-server
    ports:
      - "200:25565"
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
      MAX_PLAYERS: "30"
      ENABLE_RCON: "true"
      RCON_PASSWORD: "mcusiman123"
      RCON_PORT: "25575"
    volumes:
      - /home/ghozy/Server-Tlaucer:/data
    restart: unless-stopped
```

## Akses Jaringan (Cara Join)

Server bisa diakses dari 3 lokasi:

| Lokasi Pemain | Alamat Server | Keterangan |
|---|---|---|
| **Dalam kampus UNIDA** | `172.20.20.200:200` | WiFi / kabel jaringan kampus (IP LAN server) |
| **Luar kampus UNIDA** | `103.195.19.115:200` | Internet bebas — bisa diakses **dari mana saja** (IP publik server) |
| **Host server** | `localhost:200` | Langsung dari mesin server |

**Catatan penting:**
- IP publik `103.195.19.115` butuh **port forwarding** di router (port 200 → `172.20.20.200:200`) — sudah dikonfigurasi
- Kalau IP publik berubah (dinamis), cek alamat terbaru: `curl ifconfig.me`
- IP LAN bisa berubah tergantung DHCP kampus; pastikan IP server di-reserve/di-static
- Semua pemain tetap wajib pasang **mod yang sama + Forge 1.20.1** dari lokasi mana pun

## Backup

### Manual
```bash
cd /home/ghozy/Server-Tlaucer
docker compose stop
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
0 2 * * * cd /home/ghozy/Server-Tlaucer && tar -czf backups/world-$(date +\%Y\%m\%d).tar.gz world && find backups -name "world-*.tar.gz" -mtime +7 -delete
```

## Kustomisasi Tampilan Server

Server biar gak "kosong" di multiplayer list ada 2 hal: **icon** + **deskripsi (MOTD)**.

### Ganti Icon Server
1. Siapkan gambar **persegi 64×64** format **PNG**
2. Timpa file: `cp /path/ke/gambar.png /home/ghozy/Server-Tlaucer/server-icon.png`
   - Nama file **wajib** `server-icon.png` (jangan diubah)
3. Restart server: `docker compose restart minecraft-server`
4. Icon langsung muncul di samping nama server di multiplayer list

### Ganti Deskripsi (MOTD)
Bisa lewat 2 cara (pilih salah satu):

**Cara A — env di `docker-compose.yml`** (lebih awet, dipakai ulang tiap recreate):
```yaml
MOTD: "§l§bMCU · §r§fMinicraft UNIDA\n§7Forge 1.20.1 · Mekanism + JEI + Veinst + JourneyMap + GraveStone\n§fPVP aktif · §eMax 30 · §b§llocalhost:2000"
```
Lalu: `docker compose up -d` (recreate supaya env kebaca)

**Cara B — langsung di `server.properties`:**
```properties
motd=§l§bMCU · §r§fMinicraft UNIDA\n§7Forge 1.20.1 · Mekanism + JEI + Veinst + JourneyMap + GraveStone\n§fPVP aktif · §eMax 30 · §b§llocalhost:2000
```
Lalu: `docker compose restart minecraft-server`

### Kode Warna MOTD
| Kode | Warna | | Kode | Gaya |
|------|-------|-|------|------|
| `§a` | Hijau | | `§l` | Bold |
| `§e` | Kuning | | `§o` | Italic |
| `§b` | Aqua | | `§n` | Underline |
| `§7` | Abu-abu | | `§r` | Reset |
| `§f` | Putih | | `\n` | Baris baru |

> Kode warna bisa digabung, contoh: `§l§a` = hijau tebal. Setiap ganti icon/MOTD wajib restart server biar kebaca.

## Menambah Mod Baru

1. Download file `.jar` mod Forge 1.20.1 dari CurseForge/Modrinth
2. Taruh di folder `mods/`:
   ```bash
   cp /path/to/mod.jar /home/ghozy/Server-Tlaucer/mods/
   ```
3. Restart server:
   ```bash
   docker compose restart minecraft-server
   ```
4. Client laptop juga wajib pasang mod yang sama

## Troubleshooting

### Server tidak bisa start?
```bash
docker compose logs minecraft-server --tail=50
```

### Player tidak bisa connect?
```bash
# Cek IP server (untuk pemain lain; host sendiri pakai localhost)
hostname -I

# Cek port
ss -tlnp | grep :200

# Cek server log
docker compose logs --tail=20 minecraft-server
```

### Cara Pakai Mod

**Veinst VeinMiner**:
- **Controls → Key Binds → Cari "Veinminer" → Set "Veinminer Key"** (misal: `V`, `G`, `~`)
- **Hold tombol itu + mine** — vein mining tanpa enchant
- Support batu, ore, kayu, dan semua block
- Bisa diatur via tombol "Veinminer Menu Key"

**JourneyMap**:
- Tekan `J` — fullscreen map
- Tekan `B` — set waypoint
- Minimap pojok kanan atas (otomatis)
- Lihat posisi teman di peta

**JEI** (Just Enough Items):
- `R` = lihat recipe item
- `U` = lihat kegunaan item
- Search bar di kiri untuk cari item

**LightAura** (client-only):
- Pasang di laptop masing-masing (tidak di server)
- Otomatis: cahaya sekitar player di kegelapan

### Mod tidak terload?
- Cek log: `docker compose logs minecraft-server | grep -i error`
- Pastikan file `.jar` ada di folder `mods/`
- Pastikan versi mod untuk Forge 1.20.1
- Pastikan dependensi mod ikut terinstall

---

**Dibuat:** Juni 2026
**Server:** Lokal — akses lewat `localhost:200` dari host; pemain lain pakai IP server (`hostname -I`)

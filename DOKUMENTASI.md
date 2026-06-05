# 📋 Dokumentasi Teknis — Tlaucer Minecraft Server

## Arsitektur Sistem

```
Internet
    │
    ├── Cloudflare (mcu.utc.web.id)
    │     └── TCP Tunnel → localhost:1350
    │
    └── Docker Container (minecraft-tlaucer-server)
          └── Port: 1350 (host) → 25565 (container)
                └── Minecraft Paper 26.1.2 (offline-mode)
```

## Spesifikasi

| Item | Detail |
|------|--------|
| **Host** | Linux (Docker) |
| **Container Image** | `itzg/minecraft-server:latest` |
| **Server Type** | Paper 26.1.2 |
| **Memory** | 4GB (4096M) |
| **Host Port** | 1350 |
| **Container Port** | 25565 |
| **Mode** | Offline (Tlaucer) |
| **Domain** | mcu.utc.web.id |
| **Directory** | `/home/ghozy/Server-Tlaucer` |

## Management Commands

### Server Lifecycle
```bash
# Start server
cd /home/ghozy/Server-Tlaucer && docker compose up -d

# Stop server
docker compose stop

# Restart server
docker compose restart

# View logs (real-time)
docker compose logs -f

# View last 50 lines
docker compose logs --tail=50
```

### RCON Console
```bash
docker compose exec minecraft-server rcon-cli
```
Setelah masuk RCON, kamu bisa pakai commands berikut:

| Command | Fungsi |
|---------|--------|
| `say <pesan>` | Broadcast pesan ke semua player |
| `list` | Lihat player online |
| `save-all` | Force save world |
| `stop` | Stop server |
| `op <player>` | Beri operator ke player |
| `deop <player>` | Cabut operator |
| `gamemode 0 <player>` | Survival mode |
| `gamemode 1 <player>` | Creative mode |
| `gamemode 2 <player>` | Adventure mode |
| `gamemode 3 <player>` | Spectator mode |
| `tp <player> <target>` | Teleport player |
| `kick <player>` | Kick player |
| `ban <player>` | Ban player |
| `pardon <player>` | Unban player |
| `whitelist add <player>` | Tambah ke whitelist |
| `time set day/night` | Set waktu |
| `weather clear/rain/thunder` | Set cuaca |

**RCON Credentials:**
- Password: `mcusiman123`
- Port internal: 25575

### Monitoring
```bash
# Resource usage
docker stats minecraft-tlaucer-server

# Container status
docker compose ps

# Port check
ss -tlnp | grep 1350
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
└── bukkit.yml, spigot.yml, paper.yml, etc.
```

## Backup

### Manual Backup
```bash
cd /home/ghozy/Server-Tlaucer
tar -czf backups/world-$(date +%Y%m%d-%H%M%S).tar.gz world
```

### Restore Backup
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
# Tambah baris ini (backup jam 2 pagi setiap hari, hapus backup >7 hari):
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
Edit environment di `docker-compose.yml`:
```yaml
environment:
  PLUGINS: "https://url-plugin1.jar|https://url-plugin2.jar"
```
Lalu:
```bash
docker compose up -d
```

## Troubleshooting

### Container restart terus?
```bash
docker compose logs minecraft-server --tail=50
```
Cek error message, biasanya karena:
- Kurang memory → naikkan `MEMORY` di `.env`
- Port conflict → cek `ss -tlnp | grep 1350`
- EULA belum diset → cek `eula.txt`

### Player tidak bisa connect?
```bash
# Cek port
ss -tlnp | grep 1350

# Cek log server
docker compose logs --tail=20 minecraft-server

# Cek DNS
nslookup mcu.utc.web.id
```

### Server lambat?
- Naikkan alokasi memory di `docker-compose.yml`
- Kurangi `max-players`
- Set `view-distance=6` di `server.properties`
- Tambah plugin performance (seperti Spark)

## Cloudflare Tunnel

### Setup via Dashboard
1. Buka [Cloudflare Dashboard](https://dash.cloudflare.com/) → **Zero Trust** → **Networks** → **Tunnels**
2. Pilih tunnel yang sudah ada
3. **Edit** → **Public Hostname** → **Add**
4. Isi:
   - Subdomain: `mcu`
   - Domain: `utc.web.id`
   - Service: `TCP` → `localhost:1350`
5. **Save**

### Restart Tunnel
```bash
sudo systemctl restart cloudflared
```

### Cek Status Tunnel
```bash
sudo systemctl status cloudflared
```

## Konfigurasi Penting

### server.properties (sudah dioptimasi)
```properties
online-mode=false           # Offline mode untuk Tlaucer
enforce-secure-profile=false # Penting untuk offline mode
server-port=25565
enable-rcon=true
rcon.password=mcusiman123
max-players=20
pvp=true
difficulty=normal
gamemode=survival
```

### Environment Variables
| Variable | Value | Fungsi |
|----------|-------|--------|
| MEMORY | 4096M | Alokasi RAM |
| TYPE | PAPER | Server type |
| ONLINE_MODE | false | Offline mode |
| ENABLE_RCON | true | Remote console |
| MAX_PLAYERS | 20 | Max player |
| DIFFICULTY | 2 (normal) | Difficulty |

---

**Dibuat:** Juni 2026
**Domain:** mcu.utc.web.id:1350

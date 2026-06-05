# PLANNING.md — Minecraft Tlaucer Server

## Architecture
```
Host Machine (mcu.utc.web.id)
    │
    ├── Cloudflare Tunnel (cloudflared)
    │     └── TCP:1350 → localhost:1350
    │
    └── Docker Container (minecraft-tlaucer-server)
          └── Port: 1350 (host) → 25565 (container)
                └── Minecraft Paper Server (offline-mode)
```

## Setup Phases

### ✅ Phase 1: Prerequisites
- Docker 28.2.2 ✅
- Docker Compose v2.37.1 ✅
- Cloudflared installed & active ✅
- Port 1350 available ✅
- Directory /home/ghozy/Server-Tlaucer ready ✅

### ✅ Phase 2: Configuration Files
- [x] docker-compose.yml
- [x] .env
- [x] AGENTS.md
- [x] PLANNING.md

### 🔄 Phase 3: Server Initialization
- [ ] First run (generate default files)
- [ ] Configure server.properties (online-mode=false)
- [ ] Accept EULA

### ⏳ Phase 4: Cloudflare Tunnel
- [ ] Update /etc/cloudflared/config.yml with ingress rule
- [ ] Restart cloudflared service
- [ ] Verify DNS resolution

### ⏳ Phase 5: Final Verification
- [ ] Docker container running
- [ ] Port 1350 binding
- [ ] Local connection test
- [ ] Remote connection test via Tlaucer

## Configuration Details

### docker-compose.yml
```yaml
version: '3.9'
services:
  minecraft-server:
    image: itzg/minecraft-server:latest
    container_name: minecraft-tlaucer-server
    ports:
      - "1350:25565"
    environment:
      EULA: "TRUE"
      ONLINE_MODE: "false"
      TYPE: "PAPER"
      VERSION: "latest"
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
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:25575"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

### .env
```
MINECRAFT_DIR=/home/ghozy/Server-Tlaucer
CONTAINER_NAME=minecraft-tlaucer-server
MEMORY=4096M
MAX_PLAYERS=20
RCON_PASSWORD=mcusiman123
DIFFICULTY=2
GAMEMODE=0
```

## Notes
- RCON (Remote Console): allows server management via CLI without logging into the game
- Tlaucer = offline-mode client, uses `online-mode=false`
- Cloudflare Tunnel handles DDoS protection and hides real IP
- Plugins can be added later without rebuilding container

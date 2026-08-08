#!/usr/bin/env bash
# download_mod.sh - download semua mod client server (Forge 1.20.1) dari link resmi
# Cara pakai: bash download_mod.sh [folder_tujuan]  (default: mods/ di folder script)
# Butuh: curl (Debian/Ubuntu: sudo apt install curl)
set -euo pipefail
TARGET="${1:-$(cd "$(dirname "$0")" && pwd)/mods}"
mkdir -p "$TARGET"
MODS=(
  "Mekanism-1.20.1-10.4.16.80.jar" "https://cdn.modrinth.com/data/Ce6I4WUE/versions/uxe1WQp4/Mekanism-1.20.1-10.4.16.80.jar"  # Mekanism Core
  "MekanismGenerators-1.20.1-10.4.16.80.jar" "https://cdn.modrinth.com/data/OFVYKsAk/versions/Th4Czz4N/MekanismGenerators-1.20.1-10.4.16.80.jar"  # Mekanism Generators
  "MekanismTools-1.20.1-10.4.16.80.jar" "https://cdn.modrinth.com/data/tqQpq1lt/versions/VzpFbUpF/MekanismTools-1.20.1-10.4.16.80.jar"  # Mekanism Tools
  "architectury-9.2.14-forge.jar" "https://cdn.modrinth.com/data/lhGA9TYQ/versions/1MKTLiiG/architectury-9.2.14-forge.jar"  # Architectury API
  "cloth-config-11.1.136-forge.jar" "https://cdn.modrinth.com/data/9s6osm5g/versions/t8TXrZvZ/cloth-config-11.1.136-forge.jar"  # Cloth Config API
  "jei-1.20.1-forge-15.20.0.130.jar" "https://cdn.modrinth.com/data/u6dRKJwZ/versions/RTFeXsvE/jei-1.20.1-forge-15.20.0.130.jar"  # JEI
  "veinst_veinminer-1.3.0-1.20.1.jar" "https://edge.forgecdn.net/files/8128/571/veinst_veinminer-1.3.0-1.20.1.jar"  # Veinst VeinMiner
  "journeymap-1.20.1-5.10.3-forge.jar" "https://cdn.modrinth.com/data/lfHFW1mp/versions/r7FWVNCs/journeymap-1.20.1-5.10.3-forge.jar"  # JourneyMap
  "gravestone-forge-1.20.1-1.0.35.jar" "https://cdn.modrinth.com/data/RYtXKJPr/versions/q9kZE5Xo/gravestone-forge-1.20.1-1.0.35.jar"  # GraveStone
  "create-1.20.1-6.0.8.jar" "https://cdn.modrinth.com/data/LNytGWDc/versions/8amzvn9x/create-1.20.1-6.0.8.jar"  # Create
  "garnished-2.1.7.b+1.20.1-neoforged.jar" "https://cdn.modrinth.com/data/6e2SlzR4/versions/tO2irH8t/garnished-2.1.7.b%2B1.20.1-neoforged.jar"  # Create Garnished
)
ok=0; gagal=0; n=${#MODS[@]}
for (( i=0; i<n; i+=2 )); do
  f="${MODS[$i]}"; u="${MODS[$((i+1))]}"
  printf "  * %-38s ... " "$f"
  if curl -fsSL --retry 3 -A "hermes-agent/1.0" -o "$TARGET/$f" "$u" 2>/dev/null; then
    sz=$(stat -c%s "$TARGET/$f" 2>/dev/null); [ -z "$sz" ] && sz=$(stat -f%z "$TARGET/$f" 2>/dev/null)
    if [ "${sz:-0}" -gt 100000 ]; then echo "OK ($sz)"; ok=$((ok+1)); else echo "kecil, hapus"; rm -f "$TARGET/$f"; gagal=$((gagal+1)); fi
  else
    echo "GAGAL"; rm -f "$TARGET/$f" 2>/dev/null || true; gagal=$((gagal+1))
  fi
done
echo "=== Selesai: $ok OK, $gagal gagal -> $(cd "$TARGET" && pwd)"

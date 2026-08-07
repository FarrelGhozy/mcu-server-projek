#!/usr/bin/env bash
# ==================================================================
# download_mod.sh - Minecraft), server MCU (Forge 1.20.1)
# Cara pakai (Linux/macOS):
#   bash download_mod.sh                -> simpan ke ./mods
#   bash download_mod.sh <folder_path>  -> simpan ke folder tertentu
# Butuh: curl  (Debian/Ubuntu: sudo apt install curl)
# ==================================================================
set -euo pipefail
TARGET="${1:-$(cd "$(dirname "$0")" && pwd)/mods}"
mkdir -p "$TARGET"

# Baca daftar mod: "nama-file|url-lengkap"
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
)

ok=0; gagal=0
n=${#MODS[@]}
for (( i=0; i<n; i+=2 )); do
  f="${MODS[$i]}"; u="${MODS[$((i+1))]}"
  printf "  \\u2588 %-38s ... " "$f"
  if curl -fsSL --retry 3 -A "hermes-agent/1.0" -o "$TARGET/$f" "$u" 2>/dev/null; then
    sz=$(stat -c%s "$TARGET/$f" 2>/dev/null)
    [ -z "$sz" ] && sz=$(stat -f%z "$TARGET/$f" 2>/dev/null)
    if [ "${sz:-0}" -gt 100000 ]; then echo "OK ($sz bytes)"; ok=$((ok+1)); else echo "gagal (ukuran kecil)"; rm -f "$TARGET/$f"; gagal=$((gagal+1)); fi
  else
    echo "GAGAL"; rm -f "$TARGET/$f" 2>/dev/null || true; gagal=$((gagal+1))
  fi
done
echo
echo "=== Selesai: $ok mod berhasil, $gagal gagal ==="
echo "File tersimpan di: $(cd "$TARGET" && pwd)"
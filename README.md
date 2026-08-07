# Minecraft Home Server — Tlaucer

Selamat datang di server Minecraft lokal! Server ini pakai **Forge 1.20.1 + Mekanism + JEI + Veinst VeinMiner + GraveStone**. Semua pemain harus pasang mod yang sama biar bisa join.

## Cara Join

### 1. Install TLauncher & Forge 1.20.1
- Download TLauncher dari [tlauncher.org](https://tlauncher.org/en/)
- Buka TLauncher → pilih **Forge 1.20.1** di daftar versi → klik Install
- (Opsional) Bisa pilih **ForgeOptiFine 1.20.1** biar lebih ringan

### 2. Download & Pasang Mod
Download semua file `.jar` berikut, lalu pindahkan ke folder `mods` di laptop kamu. Ada **2 cara**: otomatis (disarankan) atau manual.

#### 🚀 Cara A — Otomatis: pakai script dari repo
Repo ini berisi script buat **download SEMUA mod sekaligus** dari link resmi (Modrinth/CurseForge):

| OS | Script | Cara pakai |
|---|---|---|
| **Linux / macOS** | `download_mod.sh` | `bash download_mod.sh` |
| **Windows** | `download_mod.bat` | klik 2×, atau ketik `download_mod.bat` di cmd |

**Cara pakai:**
- **Windows** → copy `download_mod.bat` ke folder mana saja → **klik 2×**. Script otomatis bikin folder `mods/` di sebelahnya & download semua mod ke situ. Butuh `curl` (udah bawaan Windows 10/11; kalau gak ada, script otomatis pakai PowerShell).
- **Linux** → copy `download_mod.sh` → `bash download_mod.sh`. File ke-download ke folder `mods/` di folder script. Mau taruh di folder lain? `bash download_mod.sh /path/folder`.
- Script nunjuk status tiap mod (`OK`/`GAGAL`). Setelah semua OK, pindahin file ke folder `mods` TLauncher (langkah di bawah).

**Cara akses folder mods:**
1. Buka TLauncher
2. Klik ikon folder () di pojok kanan bawah
3. Cari folder **`mods`** (buat baru kalo belum ada)
4. Copy semua file `.jar` dari hasil script ke dalam folder `mods/`

#### 🐢 Cara B — Manual: download satu-satu

**Download Links (Forge 1.20.1):**

| Mod | File | Link Download |
|-----|------|---------------|
| **Mekanism Core** | `Mekanism-1.20.1-10.4.16.80.jar` | [Download](https://cdn.modrinth.com/data/Ce6I4WUE/versions/uxe1WQp4/Mekanism-1.20.1-10.4.16.80.jar) |
| **Mekanism Generators** | `MekanismGenerators-1.20.1-10.4.16.80.jar` | [Download](https://cdn.modrinth.com/data/OFVYKsAk/versions/Th4Czz4N/MekanismGenerators-1.20.1-10.4.16.80.jar) |
| **Mekanism Tools** | `MekanismTools-1.20.1-10.4.16.80.jar` | [Download](https://cdn.modrinth.com/data/tqQpq1lt/versions/VzpFbUpF/MekanismTools-1.20.1-10.4.16.80.jar) |
| **Architectury API** | `architectury-9.2.14-forge.jar` | [Download](https://cdn.modrinth.com/data/lhGA9TYQ/versions/1MKTLiiG/architectury-9.2.14-forge.jar) |
| **Cloth Config API** | `cloth-config-11.1.136-forge.jar` | [Download](https://cdn.modrinth.com/data/9s6osm5g/versions/t8TXrZvZ/cloth-config-11.1.136-forge.jar) |
| **JEI** | `jei-1.20.1-forge-15.20.0.130.jar` | [Download](https://cdn.modrinth.com/data/u6dRKJwZ/versions/RTFeXsvE/jei-1.20.1-forge-15.20.0.130.jar) |
| **Veinst VeinMiner** | `veinst_veinminer-1.3.0-1.20.1.jar` | [Download](https://edge.forgecdn.net/files/8128/571/veinst_veinminer-1.3.0-1.20.1.jar) |
| **JourneyMap** | `journeymap-1.20.1-5.10.3-forge.jar` | [Download](https://cdn.modrinth.com/data/lfHFW1mp/versions/r7FWVNCs/journeymap-1.20.1-5.10.3-forge.jar) |
| **GraveStone** | `gravestone-forge-1.20.1-1.0.35.jar` | [Download](https://cdn.modrinth.com/data/RYtXKJPr/versions/q9kZE5Xo/gravestone-forge-1.20.1-1.0.35.jar) |

> **Wajib download SEMUA file di atas.** Kalo kurang satu, game bisa crash atau koneksi ditolak.
>
> **LightAura** (client-only — optional, tidak perlu di server) | `LightAura-8.2.0.jar` | [Download](https://cdn.modrinth.com/data/MNQ8PfgX/versions/Aa16E33Q/LightAura-8.2.0.jar)

### 3. Cara Pakai Mod Penting

**Veinst VeinMiner**:
- ⚠️ **Wajib punya enchant `` \"Veinmining\" ``** di tool kamu (bisa lewat tabel enchant / buku / villager). Config server `maxBlocksBase=0` → **tanpa enchant, vein mining = 0 blok (gak jalan!)**. Maks level 5, ~50 blok/level.
- Tahan **Veinminer Key** (default: `` ` ``) sambil mine — vein mining blok yang nyambung.
- **Hanya bisa vein mining: BIJIH (ore, pakai belatik) + LOG KAYU (pakai kapak)** — sesuai config server (`#c:ores`, `#forge:ores`, `#minecraft:logs`). Batu biasa/tanah TIDAK ke-vein.
- Ganti tombol: **Controls → Key Binds → cari "Veinminer"** → set "Veinminer Key" & "Veinminer Menu Key".
- Buka menu setting via **"Veinminer Menu Key"** (default: `]`) — buat toggle alat & jumlah blok.

**JourneyMap**:
- Tekan `J` — buka fullscreen map
- Tekan `B` — set waypoint di lokasi saat ini
- Minimap otomatis muncul di pojok atas kanan
- Lihat posisi teman di peta (real-time)

**JEI** (Just Enough Items):
- Tekan `R` di atas item untuk lihat recipe
- Tekan `U` di atas item untuk lihat kegunaan
- Bisa nyari item di panel kiri

### 4. Join Server
1. Buka Minecraft dari TLauncher (pastiin pilih **Forge 1.20.1**)
2. Multiplayer → Direct Connection (atau Add Server)
3. Masukkan alamat server **sesuai lokasi kamu**:

| Lokasi Kamu | Alamat Server |
|---|---|
| **Di dalam kampus UNIDA** (Wi-Fi / kabel kampus) | **`172.20.20.200:200`** |
| **Di luar kampus UNIDA** (internet bebas, dari mana saja) | **`103.195.19.115:200`** |
| **Di laptop/server host itu sendiri** | `localhost:200` |

4. Klik Join Server

> 💡 Mau share cara join ke temen? Ada file undangan siap-pakai di repo ini: **`UNDANGAN.md`** — tinggal share.

### Info Server
| Info | Detail |
|------|--------|
| **Address** | `172.20.20.200:200` (kampus UNIDA) · `103.195.19.115:200` (luar kampus) |
| **Version** | Forge **1.20.1** |
| **Mode** | Survival |
| **Difficulty** | Normal |
| **Max Players** | 30 |
| **PVP** | Aktif |
| **Mods** | Mekanism + Generators + Tools + JEI + Veinst + JourneyMap + GraveStone |

### Aturan Server
1. Jangan cheat / x-ray
2. Jangan grief bangunan orang
3. Jangan toxic di chat
4. Boleh PVP dengan persetujuan
5. Nikmati!

### 💬 Grup WhatsApp
Punya pertanyaan, masukan, atau laporan? **Gabung grup WhatsApp server:**
👉 **https://chat.whatsapp.com/JeH2ir0wN5QLCTI8eUOSyQ**

---

**Host:** `172.20.20.200:200` (kampus UNIDA) · `103.195.19.115:200` (luar kampus) · `localhost:200` (host)

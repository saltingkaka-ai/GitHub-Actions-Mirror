# 🪞 File Mirror GitHub Actions

Mirror file dari berbagai hosting ke GitHub Actions dengan satu command.

## 🚀 Quick Start

1. Fork repo ini
2. Setup GitHub Secrets:
   - `PIXELDRAIN_APIKEY` (Wajib jika ingin mirror ke PixelDrain)
   - `GOFILE_APIKEY` (Opsional, GoFile bisa tanpa APIKEY)
3. Trigger workflow dengan URL file yang ingin di-mirror

## ✅ Status Hosting

| Hosting | Status | Keterangan |
|---------|--------|------------|
| AnonFiles | ⬜ | anonfiles.com, anonfile.com |
| BayFiles | ⬜ | bayfiles.com |
| ZippyShare | ⬜ | zippyshare.com |
| MediaFire | ⬜ | mediafire.com |
| Google Drive | ⬜ | drive.google.com |
| Dropbox | ⬜ | dropbox.com |
| Mega.nz | ⬜ | mega.nz |
| PixelDrain | ⬜ | pixeldrain.com |
| GoFile | ⬜ | gofile.io |
| Direct Link | ⬜ | URL langsung (.zip, .mp4, dll) |

**Keterangan:**
- ✅ = Berfungsi & tested
- ⚠️ = Partial/terkadang error
- ❌ = Belum support/Broken
- ⬜ = Dalam pengembangan

## ✅ Status Mirror To

| Hosting | Status | Keterangan | Limit Ukuran File |
|---------|--------|------------|------------|
| PixelDrain | ⬜ | Butuh APIKEY | 20GB (Free) |
| GoFile | ⬜ | Tidak butuh APIKEY | Unlimited |

**Keterangan:**
- ✅ = Berfungsi & tested
- ⚠️ = Partial/terkadang error
- ❌ = Belum support/Broken
- ⬜ = Dalam pengembangan

## 📋 Cara Pakai

### Manual Trigger
1. Fork repo ini
2. Setup GitHub Secrets (jika perlu)
3. Go to **Actions** tab
4. Pilih workflow **"File Mirror"**
5. Klik **"Run workflow"**
6. Masukkan URL dan nama file (opsional)
7. Pilih file hosting tujuan (PixelDrain/GoFile)
8. Klik **"Run"** dan tunggu proses selesai

### Auto-detect
Script otomatis mendeteksi hosting dari URL — tidak perlu setting manual.

## 🔧 Tambah Hosting Baru

1. Buat file di `.github/scripts/files-hosting/namahosting.py`
2. Inherit class `BaseHostingHandler`
3. Implement method `get_direct_link()`
4. Done — auto-detected!

```python
class NewHostingHandler(BaseHostingHandler):
    HOSTING_NAME = "newhosting"
    DOMAINS = ["newhosting.com"]
    
    def get_direct_link(self, url: str) -> str:
        # parsing logic here
        return direct_url
```

## 🤝 Kontribusi
- Fork repo ini
- Buat branch baru untuk fitur/hosting baru
- Submit pull request dengan penjelasan dan contoh URL

## 📄 License
MIT License © 2024 [@profambatukam]

## 📞 Contact
- Telegram : @profambatukam
# 🪞 File Mirror GitHub Actions

Mirror file dari berbagai hosting ke GitHub Actions dengan satu command.

## 🚀 Quick Start

```yaml
- uses: actions/checkout@v4
- run: python .github/scripts/main.py "URL_FILE_HOSTING" "nama_file.zip"
```

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
| Direct Link | ⬜ | URL langsung (.zip, .mp4, dll) |

**Keterangan:**
- ✅ = Berfungsi & tested
- ⚠️ = Partial/terkadang error
- ❌ = Belum support/Broken
- ⬜ = Dalam pengembangan

## 📋 Cara Pakai

### Manual Trigger
1. Go to **Actions** tab
2. Pilih workflow **"File Mirror"**
3. Klik **"Run workflow"**
4. Masukkan URL dan nama file (opsional)

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
# Tracker Lokasi (Demo Lab) — CLI + Website Permission Lokasi

Tool edukasi/lab: website meminta izin geolokasi browser (Geolocation API) dengan consent user,
lalu menyimpan data ke SQLite lokal. CLI dipakai lihat data.

## Install (Linux/Kali)
```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv
cd "melacak orang lewat"
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run
```bash
# Server web
python3 cli.py serve
# akses: http://IP-KALI:5000  (atau http://localhost:5000)
# Lihat data
python3 cli.py list
python3 cli.py stats
# Hapus data
python3 cli.py clear
```

## API
- `GET /` website
- `POST /api/location` simpan lokasi
- `GET /api/visits` daftar JSON

## Notes
- Hanya lokasi yang user setujui di browser.
- Untuk HTTPS (permission lokasi di beberapa browser mobile) pakai reverse proxy / ngrok.
- Data: tracker.db (SQLite).

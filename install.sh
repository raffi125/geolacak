#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
echo "[*] Update packages..."
sudo apt-get update -y
echo "[*] Install python3 + venv..."
sudo apt-get install -y python3 python3-pip python3-venv
echo "[*] Create venv..."
python3 -m venv venv
source venv/bin/activate
echo "[*] Install requirements..."
pip install --upgrade pip
pip install -r requirements.txt
echo "[+] Done. Run: ./run.sh"

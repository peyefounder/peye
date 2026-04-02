# 🔥 PEYE Simple Scann Vuln Site

<p align="center">
  <img src="peye.png" alt="PEYE Logo" width="200">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Version-9.0-red?style=for-the-badge&logo=github">
  <img src="https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python">
  <img src="https://img.shields.io/badge/License-Custom-yellow?style=for-the-badge&logo=legal">
  <img src="https://img.shields.io/badge/Platform-Linux%20%7C%20Termux%20%7C%20Windows-lightgrey?style=for-the-badge&logo=linux">
</p>

---

## 📌 Tentang PEYE

**PEYE** adalah tools scanner vuln yang sederhana

| Fitur | Keterangan |
|-------|-------------|
| 🔍 **XSS Scanner** | Cross-Site Scripting detection |
| 🗄️ **SQLi Scanner** | SQL Injection detection |
| 📁 **LFI Scanner** | Local File Inclusion |
| 💻 **CMD Injection** | Command Injection detection |
| 📂 **Dir Bruteforce** | Directory discovery |
| 🌐 **Subdomain Scan** | Subdomain enumeration |
| 🎯 **Dork Search** | Google Dorking |
| 🖥️ **Tech Detection** | CMS, JS, Server detection |
| 💥 **DoS Attack** | 15+ attack methods |

> ⚠️ **Peringatan**: Tools ini HANYA untuk testing pada sistem yang Anda miliki atau memiliki izin eksplisit!

---

## 📦 Installation

### 🔹 Linux (Debian/Ubuntu/Kali)

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python & pip
sudo apt install python3 python3-pip git -y

# Clone repository
git clone https://github.com/peye/peye.git
cd peye

# Install dependencies
pip3 install cloudscraper dnspython requests

# Jalankan
python3 peye.py

<p align="center">
  <img src="icon.png" width="180">
</p>

<h1 align="center">⚡ Haywire</h1>

Built for players who want tighter control over matchmaking regions in fog-heavy competitive environments.

**Haywire** is a Windows utility that lets you control AWS GameLift routing by blocking or allowing specific AWS regions using Windows Firewall rules.

It gives you control over matchmaking regions for games that use AWS infrastructure.

---

## 🚀 Features

- 🌍 Select AWS regions to block
- ⚙️ Live AWS IP range fetching
- 🧠 PySide6 GUI
- 📊 Built-in log console
- 🔐 Automatic admin elevation (UAC prompt)
- 📦 Easy PyInstaller packaging

---

## ⚠️ Important Warning

Do NOT block `us-east-1 (N. Virginia)` unless you understand the consequences.

This region is heavily used for AWS routing and matchmaking. Blocking it may cause:
- Failed matchmaking
- Long queue times
- Connection issues

---

## 🖥️ How It Works

1. Fetches AWS IP ranges from official AWS JSON feed  
2. Filters them by selected regions  
3. Writes IPs to a temporary file  
4. Applies Windows Firewall outbound block rules  
5. Removes/replaces rules when updated  

---

## 🧱 Requirements

- Python 3.10+
- PySide6
- requests
- Windows OS

Install dependencies:

pip install PySide6 requests

---

## ▶️ Run from source

python app.py

Must be run as Administrator.

---

## 📦 Build executable

pyinstaller --onefile --noconsole --name Haywire --icon icon.ico app.py

Output:

dist/Haywire.exe

---

## 🧠 Tech Stack

- Python  
- PySide6 (Qt GUI)  
- Windows Firewall (PowerShell)  
- AWS IP Ranges API  

---

## 📁 Project Structure

Haywire/
│── app.py
│── icon.ico
│── README.md
│── .gitignore
│
├── build/
├── dist/
└── __pycache__/

---

## ⚙️ Permissions

Requires Administrator privileges for:
- Creating firewall rules
- Modifying outbound network access

UAC prompt appears on launch.

---

## 💡 Disclaimer

Haywire is a network utility tool.  
It is not affiliated with or endorsed by any game or developer.
This tool modifies system firewall rules. Use responsibly.


---

## 🧪 Future Ideas

- Region presets (Asia / EU / NA)
- Ping-based auto routing
- System tray mode
- Dark UI overhaul
- Installer wizard

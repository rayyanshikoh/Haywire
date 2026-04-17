<p align="center">
  <img src="assets/icon.png" width="180">
</p>

<h1 align="center">⚡ Haywire</h1>

<p align="center">
Built for players who want tighter control over matchmaking regions in fog-heavy competitive environments.
</p>

---

Haywire applies Windows Firewall rules to block AWS GameLift regions and influence matchmaking routing.

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

## 📸 Preview

<p align="center">
  <img src="assets/screenshot.png" width="800">
</p>

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

### 🔐 Safety Note

Haywire is fully open-source and does not contain any malicious code.  
You can review the source code before running it.

## ▶️ How to Run

### Option 1: Download Release (Recommended)

1. Go to the Releases page or click this <a href="https://github.com/rayyanshikoh/Haywire/releases">link</a>
2. Download the latest Haywire.exe  
3. Extract if zipped  
4. Double-click Haywire.exe  
5. Allow Administrator access (UAC prompt)

> Admin permission is required for firewall modifications.

#### 🛠️ Troubleshooting

- If no regions apply → Run as Administrator
- If app doesn’t start → Check Windows Defender SmartScreen
- If rules don’t apply → Restart app as admin


#### 🛡️ Windows SmartScreen Warning

When running Haywire for the first time, Windows SmartScreen may show a warning like:

> “Windows protected your PC”

This happens because Haywire is not digitally signed (common for open-source tools).

##### ▶️ How to run anyway:

1. Click **More info**
2. Click **Run anyway**

##### ⚠️ Why this happens

SmartScreen flags new or unsigned applications that don’t yet have a download reputation. This is normal for:

- Open-source tools
- Indie applications
- Newly released software

---

### Option 2: Run from Source

Install dependencies:

pip install PySide6 requests

Run:

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
│── icon.png
│── README.md
│── .gitignore
│── LICENSE
│
├── build/
├── dist/
└── __pycache__/

---

## ⚙️ Permissions

Requires Administrator privileges for:

- Creating firewall rules  
- Modifying outbound network access  

A UAC prompt appears on launch.

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

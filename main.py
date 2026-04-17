import sys
import ctypes
import requests
import subprocess
import tempfile
import os

from PySide6.QtGui import QIcon

from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QCheckBox,
    QPushButton, QLabel, QTextEdit, QScrollArea,
    QFrame, QMessageBox
)

ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("haywire.app")

# -----------------------------
# UAC / Admin elevation
# -----------------------------
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, " ".join(sys.argv), None, 1
    )
    sys.exit()

# -----------------------------
# Regions
# -----------------------------
REGIONS = {
    "us-east-1": "US East (N. Virginia)",
    "us-east-2": "US East (Ohio)",
    "us-west-1": "US West (N. California)",
    "us-west-2": "US West (Oregon)",
    "ca-central-1": "Canada (Central)",
    "sa-east-1": "South America (São Paulo)",
    "eu-west-1": "Europe (Ireland)",
    "eu-west-2": "Europe (London)",
    "eu-central-1": "Europe (Frankfurt am Main)",
    "eu-north-1": "Europe (Stockholm)",
    "eu-west-3": "Europe (Paris)",
    "eu-south-1": "Europe (Milan)",
    "ap-northeast-1": "Asia Pacific (Tokyo)",
    "ap-northeast-2": "Asia Pacific (Seoul)",
    "ap-northeast-3": "Asia Pacific (Osaka)",
    "ap-south-1": "Asia Pacific (Mumbai)",
    "ap-southeast-1": "Asia Pacific (Singapore)",
    "ap-southeast-2": "Asia Pacific (Sydney)",
    "ap-east-1": "Asia Pacific (Hong Kong)",
    "af-south-1": "Africa (Cape Town)",
    "me-south-1": "Middle East (Bahrain)"
}

RULE_NAME = "AWS Region Blocker"


# -----------------------------
# App
# -----------------------------
class FirewallApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Haywire - DBD Region Firewall Blocker")
        self.setMinimumSize(600, 750)
        self.setWindowIcon(QIcon("icon.ico"))

        self.checkboxes = {}

        layout = QVBoxLayout()

        # -----------------------------
        # Warning (IMPORTANT NOTE ONLY)
        # -----------------------------
        warning = QLabel(
            "⚠ NOTE: us-east-1 (N. Virginia) is a major AWS routing region.\n"
            "Blocking it may cause matchmaking issues or prevent game connections. \n"
        )
        warning.setStyleSheet("color: orange; font-weight: bold;")
        layout.addWidget(warning)

        warning2 = QLabel(
            "⚠ NOTE: Addresses for DBD servers may unexpectedly change. \n"
            "It is advisable to run this program once every week or so"
        )
        warning2.setStyleSheet("color: red; font-weight: bold;")
        layout.addWidget(warning2)

        title = QLabel("Select AWS regions to BLOCK")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)

        # -----------------------------
        # Scrollable region list
        # -----------------------------
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        container = QFrame()
        vbox = QVBoxLayout(container)

        for code, name in REGIONS.items():
            cb = QCheckBox(name)
            self.checkboxes[code] = cb
            vbox.addWidget(cb)

        scroll.setWidget(container)
        layout.addWidget(scroll)

        # -----------------------------
        # Buttons
        # -----------------------------
        self.btn_apply = QPushButton("Apply Block")
        self.btn_apply.clicked.connect(self.apply_block)

        self.btn_remove = QPushButton("Remove Block")
        self.btn_remove.clicked.connect(self.remove_block)

        layout.addWidget(self.btn_apply)
        layout.addWidget(self.btn_remove)

        # -----------------------------
        # Log console
        # -----------------------------
        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)
        layout.addWidget(self.log_box)

        self.setLayout(layout)

    # -----------------------------
    # Logger
    # -----------------------------
    def log(self, msg):
        self.log_box.append(str(msg))

    # -----------------------------
    # Apply firewall block
    # -----------------------------
    def apply_block(self):
        selected = [c for c, cb in self.checkboxes.items() if cb.isChecked()]

        if not selected:
            QMessageBox.warning(self, "Warning", "Select at least one region")
            return

        try:
            self.log("Fetching AWS IP ranges...")

            data = requests.get(
                "https://ip-ranges.amazonaws.com/ip-ranges.json"
            ).json()

            ranges = [
                p["ip_prefix"]
                for p in data["prefixes"]
                if p["region"] in selected
            ]

            self.log(f"Selected regions: {selected}")
            self.log(f"Total IPs: {len(ranges)}")

            if not ranges:
                self.log("No IPs found")
                return

            # Write to temp file (avoids command size limit)
            tmp = tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".txt")
            tmp.write("\n".join(ranges))
            tmp.close()

            self.log(f"Temp file: {tmp.name}")

            ps_script = f"""
$ips = Get-Content "{tmp.name}"

Get-NetFirewallRule -DisplayName "{RULE_NAME}" -ErrorAction SilentlyContinue | Remove-NetFirewallRule

New-NetFirewallRule `
-DisplayName "{RULE_NAME}" `
-Direction Outbound `
-Action Block `
-RemoteAddress $ips `
-Profile Any
"""

            self.log("Running PowerShell...")

            result = subprocess.run(
                ["powershell", "-ExecutionPolicy", "Bypass", "-Command", ps_script],
                capture_output=True,
                text=True
            )

            self.log(result.stdout if result.stdout else "No output")
            self.log(result.stderr if result.stderr else "No errors")

            if result.returncode == 0:
                self.log("SUCCESS: Rule applied")
            else:
                self.log("FAILED")

            os.remove(tmp.name)

        except Exception as e:
            self.log(f"ERROR: {e}")

    # -----------------------------
    # Remove rule
    # -----------------------------
    def remove_block(self):
        self.log("Removing rule...")

        ps_script = f"""
Get-NetFirewallRule -DisplayName "{RULE_NAME}" -ErrorAction SilentlyContinue | Remove-NetFirewallRule
"""

        subprocess.run(
            ["powershell", "-ExecutionPolicy", "Bypass", "-Command", ps_script],
            capture_output=True,
            text=True
        )

        self.log("Rule removed (if existed)")


# -----------------------------
# Run
# -----------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.ico"))
    window = FirewallApp()
    window.show()
    sys.exit(app.exec())
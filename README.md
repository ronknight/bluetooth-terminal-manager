# <h1 align="center">📶Bluetooth Terminal Manager</h1>

<h4 align="center">A powerful Python-based Bluetooth device management CLI tool with advanced scanning and device management capabilities.</h4>

<p align="center">
<a href="https://twitter.com/PinoyITSolution"><img src="https://img.shields.io/twitter/follow/PinoyITSolution?style=social"></a>
<a href="https://github.com/ronknight?tab=followers"><img src="https://img.shields.io/github/followers/ronknight?style=social"></a>
<a href="https://github.com/ronknight/ronknight/stargazers"><img src="https://img.shields.io/github/stars/BEPb/BEPb.svg?logo=github"></a>
<a href="https://github.com/ronknight/ronknight/network/members"><img src="https://img.shields.io/github/forks/BEPb/BEPb.svg?color=blue&logo=github"></a>
<a href="https://youtube.com/@PinoyITSolution"><img src="https://img.shields.io/youtube/channel/subscribers/UCeoETAlg3skyMcQPqr97omg"></a>
<a href="https://github.com/ronknight/bluetooth-terminal-manager/issues"><img src="https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat"></a>
<a href="https://github.com/ronknight/bluetooth-terminal-manager/blob/master/LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg"></a>
<a href="#"><img src="https://img.shields.io/badge/Made%20with-Python-1f425f.svg"></a>
<a href="https://github.com/ronknight"><img src="https://img.shields.io/badge/Made%20with%20%F0%9F%A4%8D%20by%20-%20Ronknight%20-%20red"></a>
</p>

<p align="center">
  <a href="#requirements">Requirements</a> •
  <a href="#features">Features</a> •
  <a href="#installation">Installation</a> •
  <a href="#usage">Usage</a> •
  <a href="#diagrams">Diagrams</a>
</p>

---

## 📋 Requirements

- Python 3.7+
- Bluetooth adapter
- Windows/Linux/macOS

## ⚡ Features

- Advanced device scanning with multiple modes (quick, normal, deep)
- Visual signal strength indicators
- Device connection management
- Detailed device information display
- Known devices management
- Colorful terminal output
- Continuous scanning mode

## 🚀 Installation

```bash
# Clone the repository
git clone https://github.com/ronknight/bluetooth-terminal-manager.git

# Install dependencies
pip install -r requirements.txt
```

## 💻 Usage

```bash
# Scan for devices
python cli.py scan

# Scan with options
python cli.py scan --duration 30 --mode deep --continuous

# Get device info
python cli.py info <device-address>

# Connect to device
python cli.py connect <device-address>

# List known devices
python cli.py known-devices

# Forget a device
python cli.py forget <device-address>
```

## 📊 Diagrams

### Project Architecture

```mermaid
graph TD
    A[CLI Interface] --> B[Bluetooth Manager]
    B --> C[Device Scanner]
    B --> D[Connection Handler]
    B --> E[Device Storage]
    C --> F[BLE Device Discovery]
    D --> G[Device Connection]
    D --> H[Device Disconnection]
    E --> I[Known Devices JSON]
    style A fill:#f9f,stroke:#333,stroke-width:2px
    style B fill:#bbf,stroke:#333,stroke-width:2px
```

### Scan Workflow

```mermaid
sequenceDiagram
    participant User
    participant CLI
    participant BluetoothManager
    participant BleakScanner
    
    User->>CLI: scan command
    CLI->>BluetoothManager: scan_devices()
    BluetoothManager->>BleakScanner: start()
    BleakScanner-->>BluetoothManager: device detected
    BluetoothManager-->>CLI: device info
    CLI-->>User: formatted output
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

<p align="center">Made with ❤️ by Ronknight</p>

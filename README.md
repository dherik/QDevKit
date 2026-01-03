<div align="center">
  <h1>QDevKit - Developer Utilities Application</h1>

  Development tools at your fingertips
</div>

<div align="center">
  <a href="https://github.com/dherik/QDevKit/actions/workflows/ci.yml" title="CI">
    <img src="https://github.com/dherik/QDevKit/actions/workflows/ci.yml/badge.svg" alt="CI status"/>
  </a>
  <a href="#license">
    <img src="https://img.shields.io/badge/License-GPL--3.0-blue.svg" alt="GPL 3 License">
  </a>
  <br />
  <a href="#features">Features</a> ·
  <a href="#download">Download</a> ·
  <a href="#building-from-source">Build</a> ·
  <a href="#license">License</a>
</div>

---

A Qt-based desktop application for developers with various conversion and utility tools.

<img width="1130" height="855" alt="image" src="https://github.com/user-attachments/assets/ea83cb02-5b6b-4195-a078-4ce6a90d2e6d" />

## Features

- **JSON Formatter** - Format, validate, and minify JSON data
- **Base64 Encoder/Decoder** - Encode and decode Base64 strings
- **UUID Generator** - Generate UUID v4 (random) and v7 (time-ordered)
- **JWT Decoder** - Decode and inspect JSON Web Tokens
- **URL Encoder/Decoder** - Encode and decode URL strings
- **Timestamp Converter** - Convert between Unix timestamps and datetime strings
- **Hash Generator** - Generate MD5, SHA1, SHA256, SHA512 hashes

## Download

### Linux (AppImage)

Download the latest AppImage from [Releases](https://github.com/dherik/QDevKit/releases):

```bash
wget https://github.com/dherik/QDevKit/releases/download/v1.1.0/QDevKit-1.1.0-linux-x86_64.AppImage
chmod +x QDevKit-1.1.0-linux-x86_64.AppImage
./QDevKit-1.1.0-linux-x86_64.AppImage
```

The AppImage works on most Linux distributions without installation.

## Building from Source

### Requirements

- Python 3.8 or higher
- PySide6
- PyJWT

### Installation

1. Clone the repository:
```bash
git clone https://github.com/dherik/QDevKit.git
cd QDevKit
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Application

```bash
python main.py
```

## Building Distributables

### Build Executable

```bash
pip install -r requirements-dev.txt
python build.py
```

This creates a standalone executable in `dist/QDevKit/`.

### Build AppImage (Linux only)

```bash
python build.py --appimage
```

This creates an AppImage in `dist/` that can be distributed.

## Project Structure

```
qdevtools/
├── main.py                      # Application entry point
├── build.py                     # Build script
├── QDevKit.spec                 # PyInstaller configuration
├── requirements.txt             # Runtime dependencies
├── requirements-dev.txt         # Build dependencies
├── ui/
│   ├── __init__.py
│   └── main_window.py          # Main window with sidebar
├── tools/
│   ├── __init__.py
│   ├── json_formatter.py       # JSON formatter tool
│   ├── base64_tool.py          # Base64 encoder/decoder
│   ├── uuid_generator.py       # UUID v4/v7 generator
│   ├── jwt_decoder.py          # JWT decoder
│   ├── url_encoder.py          # URL encoder/decoder
│   └── timestamp_converter.py  # Timestamp converter
└── build/
    └── linux/
        └── appimage/           # AppImage build scripts
```

## Adding New Tools

1. Create a new file in the `tools/` directory
2. Inherit from `QWidget`
3. Implement your tool's UI
4. Import and add it to the tools list in `ui/main_window.py`

Example:
```python
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

class MyTool(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("My Custom Tool"))
```

Then add to `main_window.py`:
```python
from tools.my_tool import MyTool

# In add_tools() method:
tools = [
    # ... existing tools ...
    ("My Tool", MyTool),
]
```

## Dependencies

- **PySide6** - Qt6 Python bindings (LGPL licensed)
- **PyJWT** - JWT decoding support
- **PyInstaller** - For building executables (development only)

## License

This project is licensed under the GNU General Public License v3.0 or later.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

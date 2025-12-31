# QDevTools - Developer Utilities Application

A Qt-based desktop application for developers with various conversion and utility tools.

## Features

- **JSON Formatter** - Format, validate, and minify JSON data
- **Base64 Encoder/Decoder** - Encode and decode Base64 strings
- **UUID Generator** - Generate UUID v4 (random) and v7 (time-ordered)
- **JWT Decoder** - Decode and inspect JSON Web Tokens
- **URL Encoder/Decoder** - Encode and decode URL strings
- **Timestamp Converter** - Convert between Unix timestamps and datetime strings

## Installation

1. Install Python 3.8 or higher

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

```bash
python main.py
```

Or make it executable (Linux/Mac):
```bash
chmod +x main.py
./main.py
```

## Project Structure

```
qdevtools/
├── main.py                      # Application entry point
├── requirements.txt             # Python dependencies
├── ui/
│   ├── __init__.py
│   └── main_window.py          # Main window with sidebar
└── tools/
    ├── __init__.py
    ├── json_formatter.py       # JSON formatter tool
    ├── base64_tool.py          # Base64 encoder/decoder
    ├── uuid_generator.py       # UUID v4/v7 generator
    ├── jwt_decoder.py          # JWT decoder
    ├── url_encoder.py          # URL encoder/decoder
    └── timestamp_converter.py  # Timestamp converter
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

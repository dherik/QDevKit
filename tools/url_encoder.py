"""
URL Encoder/Decoder Tool
"""

from urllib.parse import quote, unquote
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton,
    QLabel, QRadioButton, QButtonGroup, QCheckBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class UrlEncoderTool(QWidget):
    """Tool for URL encoding and decoding"""

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        """Setup the URL encoder/decoder UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        # Title
        title = QLabel("URL Encoder / Decoder")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        layout.addWidget(title)

        description = QLabel(
            "Encode or decode URL strings. Handle special characters for safe URL usage."
        )
        description.setStyleSheet("color: #666;")
        layout.addWidget(description)

        # Mode selection
        mode_layout = QHBoxLayout()
        mode_label = QLabel("Mode:")
        mode_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        mode_layout.addWidget(mode_label)

        self.mode_group = QButtonGroup()
        self.encode_radio = QRadioButton("Encode")
        self.encode_radio.setChecked(True)
        self.decode_radio = QRadioButton("Decode")

        self.mode_group.addButton(self.encode_radio, 1)
        self.mode_group.addButton(self.decode_radio, 2)

        mode_layout.addWidget(self.encode_radio)
        mode_layout.addWidget(self.decode_radio)
        mode_layout.addStretch()
        layout.addLayout(mode_layout)

        # Options
        options_layout = QHBoxLayout()
        self.safe_chars_cb = QCheckBox("Plus for spaces")
        self.safe_chars_cb.setToolTip("Use '+' for spaces instead of %20 (encoding only)")
        self.safe_chars_cb.setChecked(False)
        options_layout.addWidget(self.safe_chars_cb)
        options_layout.addStretch()
        layout.addLayout(options_layout)

        # Input section
        input_label = QLabel("Input:")
        input_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        layout.addWidget(input_label)

        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText("Enter URL or text to encode/decode...")
        self.input_text.setMinimumHeight(120)
        self.input_text.setFont(QFont("Consolas", 10))
        layout.addWidget(self.input_text)

        # Buttons
        button_layout = QHBoxLayout()

        self.convert_btn = QPushButton("Convert")
        self.convert_btn.clicked.connect(self.convert)
        self.convert_btn.setMinimumHeight(35)
        button_layout.addWidget(self.convert_btn)

        self.swap_btn = QPushButton("Swap Input/Output")
        self.swap_btn.clicked.connect(self.swap)
        self.swap_btn.setMinimumHeight(35)
        button_layout.addWidget(self.swap_btn)

        self.clear_btn = QPushButton("Clear")
        self.clear_btn.clicked.connect(self.clear_all)
        self.clear_btn.setMinimumHeight(35)
        button_layout.addWidget(self.clear_btn)

        layout.addLayout(button_layout)

        # Output section
        output_label = QLabel("Output:")
        output_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        layout.addWidget(output_label)

        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setMinimumHeight(120)
        self.output_text.setFont(QFont("Consolas", 10))
        layout.addWidget(self.output_text)

        # Status bar
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color: #666; padding: 5px;")
        layout.addWidget(self.status_label)

        layout.addStretch()

        # Apply button styles
        self.apply_button_styles()

    def apply_button_styles(self):
        """Apply styles to buttons"""
        button_style = """
            QPushButton {
                background-color: #0078d4;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #106ebe;
            }
            QPushButton:pressed {
                background-color: #005a9e;
            }
            QPushButton#swapButton {
                background-color: #5c2d91;
            }
            QPushButton#swapButton:hover {
                background-color: #44226b;
            }
            QPushButton#clearButton {
                background-color: #d13438;
            }
            QPushButton#clearButton:hover {
                background-color: #a92a2d;
            }
        """
        self.convert_btn.setStyleSheet(button_style)
        self.swap_btn.setStyleSheet(button_style.replace("QPushButton", "QPushButton#swapButton"))
        self.clear_btn.setStyleSheet(button_style.replace("QPushButton", "QPushButton#clearButton"))

    def convert(self):
        """Perform encode or decode based on selected mode"""
        input_data = self.input_text.toPlainText()

        if not input_data:
            self.status_label.setText("⚠️  Please enter text to convert")
            self.status_label.setStyleSheet("color: #f0ad4e; padding: 5px;")
            return

        try:
            if self.encode_radio.isChecked():
                # Encode
                if self.safe_chars_cb.isChecked():
                    # Use '+' for spaces
                    encoded = quote(input_data, safe='')
                    encoded = encoded.replace('%20', '+')
                else:
                    encoded = quote(input_data, safe='')

                self.output_text.setPlainText(encoded)
                input_len = len(input_data)
                output_len = len(encoded)
                self.status_label.setText(
                    f"✅ Encoded {input_len} chars → {output_len} chars"
                )
            else:
                # Decode
                if self.safe_chars_cb.isChecked():
                    # First replace '+' with spaces
                    input_data = input_data.replace('+', ' ')
                decoded = unquote(input_data)
                self.output_text.setPlainText(decoded)
                input_len = len(input_data)
                output_len = len(decoded)
                self.status_label.setText(
                    f"✅ Decoded {input_len} chars → {output_len} chars"
                )
            self.status_label.setStyleSheet("color: #28a745; padding: 5px;")
        except Exception as e:
            self.output_text.setPlainText("")
            self.status_label.setText(f"❌ Error: {str(e)}")
            self.status_label.setStyleSheet("color: #dc3545; padding: 5px;")

    def swap(self):
        """Swap input and output"""
        output_data = self.output_text.toPlainText()
        if output_data:
            self.input_text.setPlainText(output_data)

    def clear_all(self):
        """Clear all fields"""
        self.input_text.clear()
        self.output_text.clear()
        self.status_label.setText("")

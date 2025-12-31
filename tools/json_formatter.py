"""
JSON Formatter Tool
"""

import json
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton,
    QLabel, QCheckBox, QFrame
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class JsonFormatterTool(QWidget):
    """Tool for formatting and validating JSON"""

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        """Setup the JSON formatter UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        # Title
        title = QLabel("JSON Formatter & Validator")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        layout.addWidget(title)

        description = QLabel(
            "Format, validate, and minify JSON data. Copy formatted JSON to clipboard."
        )
        description.setStyleSheet("color: #666;")
        layout.addWidget(description)

        # Input section
        input_label = QLabel("Input JSON:")
        input_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        layout.addWidget(input_label)

        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText("Paste your JSON here...")
        self.input_text.setMinimumHeight(200)
        self.input_text.setFont(QFont("Consolas", 10))
        layout.addWidget(self.input_text)

        # Buttons
        button_layout = QHBoxLayout()

        self.format_btn = QPushButton("Format")
        self.format_btn.clicked.connect(self.format_json)
        self.format_btn.setMinimumHeight(35)
        button_layout.addWidget(self.format_btn)

        self.minify_btn = QPushButton("Minify")
        self.minify_btn.clicked.connect(self.minify_json)
        self.minify_btn.setMinimumHeight(35)
        button_layout.addWidget(self.minify_btn)

        self.clear_btn = QPushButton("Clear")
        self.clear_btn.clicked.connect(self.clear_all)
        self.clear_btn.setMinimumHeight(35)
        button_layout.addWidget(self.clear_btn)

        layout.addLayout(button_layout)

        # Options
        options_layout = QHBoxLayout()

        self.sort_keys_cb = QCheckBox("Sort Keys")
        options_layout.addWidget(self.sort_keys_cb)

        self.indent_2_cb = QCheckBox("2-space indent")
        self.indent_2_cb.setChecked(True)
        options_layout.addWidget(self.indent_2_cb)

        options_layout.addStretch()
        layout.addLayout(options_layout)

        # Output section
        output_label = QLabel("Output:")
        output_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        layout.addWidget(output_label)

        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setMinimumHeight(200)
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
            QPushButton#clearButton {
                background-color: #d13438;
            }
            QPushButton#clearButton:hover {
                background-color: #a92a2d;
            }
        """
        self.format_btn.setStyleSheet(button_style)
        self.minify_btn.setStyleSheet(button_style)
        self.clear_btn.setStyleSheet(button_style.replace("QPushButton", "QPushButton#clearButton"))

    def format_json(self):
        """Format the JSON input"""
        input_data = self.input_text.toPlainText().strip()

        if not input_data:
            self.status_label.setText("⚠️  Please enter JSON data")
            self.status_label.setStyleSheet("color: #f0ad4e; padding: 5px;")
            return

        try:
            data = json.loads(input_data)
            indent = 2 if self.indent_2_cb.isChecked() else 4
            formatted = json.dumps(
                data,
                indent=indent,
                sort_keys=self.sort_keys_cb.isChecked(),
                ensure_ascii=False
            )
            self.output_text.setPlainText(formatted)
            self.status_label.setText("✅ JSON formatted successfully")
            self.status_label.setStyleSheet("color: #28a745; padding: 5px;")
        except json.JSONDecodeError as e:
            self.output_text.setPlainText("")
            self.status_label.setText(f"❌ Invalid JSON: {str(e)}")
            self.status_label.setStyleSheet("color: #dc3545; padding: 5px;")

    def minify_json(self):
        """Minify the JSON input"""
        input_data = self.input_text.toPlainText().strip()

        if not input_data:
            self.status_label.setText("⚠️  Please enter JSON data")
            self.status_label.setStyleSheet("color: #f0ad4e; padding: 5px;")
            return

        try:
            data = json.loads(input_data)
            minified = json.dumps(data, separators=(',', ':'), ensure_ascii=False)
            self.output_text.setPlainText(minified)
            self.status_label.setText("✅ JSON minified successfully")
            self.status_label.setStyleSheet("color: #28a745; padding: 5px;")
        except json.JSONDecodeError as e:
            self.output_text.setPlainText("")
            self.status_label.setText(f"❌ Invalid JSON: {str(e)}")
            self.status_label.setStyleSheet("color: #dc3545; padding: 5px;")

    def clear_all(self):
        """Clear all text fields"""
        self.input_text.clear()
        self.output_text.clear()
        self.status_label.setText("")

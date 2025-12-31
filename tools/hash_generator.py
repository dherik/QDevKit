"""
Hash Generator Tool
"""

import hashlib
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton,
    QLabel, QRadioButton, QButtonGroup, QFrame
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class HashGeneratorTool(QWidget):
    """Tool for generating cryptographic hashes"""

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        """Setup the Hash Generator UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        # Title
        title = QLabel("Hash Generator")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        layout.addWidget(title)

        description = QLabel(
            "Generate cryptographic hashes from text using MD5, SHA1, SHA256, or SHA512 algorithms."
        )
        description.setStyleSheet("color: #666;")
        layout.addWidget(description)

        # Input section
        input_label = QLabel("Input Text:")
        input_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        layout.addWidget(input_label)

        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText("Enter text to hash...")
        self.input_text.setMinimumHeight(120)
        self.input_text.setFont(QFont("Consolas", 10))
        layout.addWidget(self.input_text)

        # Algorithm selection
        algo_layout = QHBoxLayout()
        algo_label = QLabel("Algorithm:")
        algo_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        algo_layout.addWidget(algo_label)

        self.algo_group = QButtonGroup()
        self.md5_radio = QRadioButton("MD5")
        self.sha1_radio = QRadioButton("SHA1")
        self.sha1_radio.setChecked(True)  # Default
        self.sha256_radio = QRadioButton("SHA256")
        self.sha512_radio = QRadioButton("SHA512")

        self.algo_group.addButton(self.md5_radio, 1)
        self.algo_group.addButton(self.sha1_radio, 2)
        self.algo_group.addButton(self.sha256_radio, 3)
        self.algo_group.addButton(self.sha512_radio, 4)

        algo_layout.addWidget(self.md5_radio)
        algo_layout.addWidget(self.sha1_radio)
        algo_layout.addWidget(self.sha256_radio)
        algo_layout.addWidget(self.sha512_radio)
        algo_layout.addStretch()
        layout.addLayout(algo_layout)

        # Buttons
        button_layout = QHBoxLayout()

        self.generate_btn = QPushButton("Generate Hash")
        self.generate_btn.clicked.connect(self.generate_hash)
        self.generate_btn.setMinimumHeight(35)
        button_layout.addWidget(self.generate_btn)

        self.copy_btn = QPushButton("Copy to Clipboard")
        self.copy_btn.clicked.connect(self.copy_hash)
        self.copy_btn.setMinimumHeight(35)
        button_layout.addWidget(self.copy_btn)

        self.clear_btn = QPushButton("Clear")
        self.clear_btn.clicked.connect(self.clear_all)
        self.clear_btn.setMinimumHeight(35)
        button_layout.addWidget(self.clear_btn)

        layout.addLayout(button_layout)

        # Output section
        output_label = QLabel("Hash:")
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
            QPushButton#copyButton {
                background-color: #107c10;
            }
            QPushButton#copyButton:hover {
                background-color: #0c5c0c;
            }
            QPushButton#clearButton {
                background-color: #d13438;
            }
            QPushButton#clearButton:hover {
                background-color: #a92a2d;
            }
        """
        self.generate_btn.setStyleSheet(button_style)
        self.copy_btn.setStyleSheet(button_style.replace("QPushButton", "QPushButton#copyButton"))
        self.clear_btn.setStyleSheet(button_style.replace("QPushButton", "QPushButton#clearButton"))

    def get_selected_algorithm(self):
        """Get the selected hash algorithm"""
        checked = self.algo_group.checkedId()
        if checked == 1:
            return "MD5"
        elif checked == 2:
            return "SHA1"
        elif checked == 3:
            return "SHA256"
        elif checked == 4:
            return "SHA512"
        return "SHA1"  # Default

    def generate_hash(self):
        """Generate hash from input text"""
        input_data = self.input_text.toPlainText()

        if not input_data:
            self.status_label.setText("⚠️  Please enter text to hash")
            self.status_label.setStyleSheet("color: #f0ad4e; padding: 5px;")
            return

        try:
            algorithm = self.get_selected_algorithm()

            if algorithm == "MD5":
                hash_obj = hashlib.md5()
            elif algorithm == "SHA1":
                hash_obj = hashlib.sha1()
            elif algorithm == "SHA256":
                hash_obj = hashlib.sha256()
            elif algorithm == "SHA512":
                hash_obj = hashlib.sha512()
            else:
                hash_obj = hashlib.sha256()

            hash_obj.update(input_data.encode('utf-8'))
            hash_hex = hash_obj.hexdigest()

            self.output_text.setPlainText(hash_hex)

            # Show hash info
            char_count = len(input_data)
            self.status_label.setText(
                f"✅ {algorithm} hash generated ({char_count} chars → {len(hash_hex)} chars)"
            )
            self.status_label.setStyleSheet("color: #28a745; padding: 5px;")

        except Exception as e:
            self.output_text.setPlainText("")
            self.status_label.setText(f"❌ Error: {str(e)}")
            self.status_label.setStyleSheet("color: #dc3545; padding: 5px;")

    def copy_hash(self):
        """Copy hash to clipboard"""
        hash_text = self.output_text.toPlainText()
        if hash_text:
            self.output_text.selectAll()
            self.output_text.copy()
            self.status_label.setText("✅ Hash copied to clipboard")
            self.status_label.setStyleSheet("color: #28a745; padding: 5px;")

    def clear_all(self):
        """Clear all fields"""
        self.input_text.clear()
        self.output_text.clear()
        self.status_label.setText("")

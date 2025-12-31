"""
UUID Generator Tool
Supports UUID v4 and v7
"""

import uuid
import time
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QRadioButton, QButtonGroup, QSpinBox, QTextEdit, QCheckBox
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QFontMetrics


class UuidGeneratorTool(QWidget):
    """Tool for generating UUID v4 and v7"""

    def __init__(self):
        super().__init__()
        self.generated_uuids = []
        self.setup_ui()

    def setup_ui(self):
        """Setup the UUID generator UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        # Title
        title = QLabel("UUID Generator")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        layout.addWidget(title)

        description = QLabel(
            "Generate UUIDs (Universally Unique Identifiers). "
            "v4 is random-based, v7 is time-ordered."
        )
        description.setStyleSheet("color: #666;")
        layout.addWidget(description)

        # UUID Version selection
        version_layout = QHBoxLayout()
        version_label = QLabel("UUID Version:")
        version_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        version_layout.addWidget(version_label)

        self.version_group = QButtonGroup()
        self.v4_radio = QRadioButton("v4 (Random)")
        self.v4_radio.setChecked(True)
        self.v7_radio = QRadioButton("v7 (Time-ordered)")

        self.version_group.addButton(self.v4_radio, 4)
        self.version_group.addButton(self.v7_radio, 7)

        version_layout.addWidget(self.v4_radio)
        version_layout.addWidget(self.v7_radio)
        version_layout.addStretch()
        layout.addLayout(version_layout)

        # Quantity and options
        options_layout = QHBoxLayout()

        quantity_label = QLabel("Quantity:")
        quantity_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        options_layout.addWidget(quantity_label)

        self.quantity_spin = QSpinBox()
        self.quantity_spin.setMinimum(1)
        self.quantity_spin.setMaximum(1000)
        self.quantity_spin.setValue(1)
        self.quantity_spin.setFixedWidth(80)
        options_layout.addWidget(self.quantity_spin)

        self.uppercase_cb = QCheckBox("Uppercase")
        options_layout.addWidget(self.uppercase_cb)

        self.without_dashes_cb = QCheckBox("Remove dashes")
        options_layout.addWidget(self.without_dashes_cb)

        options_layout.addStretch()
        layout.addLayout(options_layout)

        # Generate button
        generate_layout = QHBoxLayout()

        self.generate_btn = QPushButton("Generate UUIDs")
        self.generate_btn.clicked.connect(self.generate_uuids)
        self.generate_btn.setMinimumHeight(40)
        generate_layout.addWidget(self.generate_btn)

        self.copy_btn = QPushButton("Copy All")
        self.copy_btn.clicked.connect(self.copy_all)
        self.copy_btn.setMinimumHeight(40)
        generate_layout.addWidget(self.copy_btn)

        self.clear_btn = QPushButton("Clear")
        self.clear_btn.clicked.connect(self.clear_all)
        self.clear_btn.setMinimumHeight(40)
        generate_layout.addWidget(self.clear_btn)

        layout.addLayout(generate_layout)

        # Output section
        output_label = QLabel("Generated UUIDs:")
        output_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        layout.addWidget(output_label)

        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setMinimumHeight(300)
        self.output_text.setFont(QFont("Consolas", 11))
        self.output_text.setPlaceholderText("Click 'Generate UUIDs' to create UUIDs...")
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

    def generate_uuid_v4(self):
        """Generate UUID v4 (random)"""
        return uuid.uuid4()

    def generate_uuid_v7(self):
        """
        Generate UUID v7 (time-ordered)
        UUID v7 is a draft standard for time-based UUIDs
        Format: XXXXXXXX-XXXX-7XXX-YXXX-XXXXXXXXXXXX
        where:
        - 48 bits: Unix timestamp in milliseconds
        - 4 bits: version (7)
        - 12 bits: random (sub-millisecond precision + counter)
        - 2 bits: variant
        - 62 bits: random
        """
        # Get current time in milliseconds since Unix epoch
        timestamp_ms = int(time.time() * 1000)

        # 48-bit timestamp (will be valid until year 10889)
        timestamp_bytes = timestamp_ms.to_bytes(6, byteorder='big')

        # Random bytes for the rest
        random_bytes = bytes([
            # First 2 random bits + 4 bits version (7) + 12 random bits
            (random_byte := uuid.uuid4().bytes[6]) & 0x0F | 0x70,
            uuid.uuid4().bytes[7],
            # Variant bits + random
            uuid.uuid4().bytes[8] & 0x3F | 0x80,
            uuid.uuid4().bytes[9],
            uuid.uuid4().bytes[10],
            uuid.uuid4().bytes[11],
            uuid.uuid4().bytes[12],
            uuid.uuid4().bytes[13],
            uuid.uuid4().bytes[14],
            uuid.uuid4().bytes[15]
        ])

        # Combine timestamp + version + variant + random
        uuid_bytes = timestamp_bytes + random_bytes

        # Format as UUID
        return uuid.UUID(bytes=uuid_bytes)

    def generate_uuids(self):
        """Generate UUIDs based on selected options"""
        quantity = self.quantity_spin.value()
        version = 7 if self.v7_radio.isChecked() else 4
        uppercase = self.uppercase_cb.isChecked()
        without_dashes = self.without_dashes_cb.isChecked()

        self.generated_uuids = []

        try:
            for _ in range(quantity):
                if version == 4:
                    generated_uuid = self.generate_uuid_v4()
                else:
                    generated_uuid = self.generate_uuid_v7()

                uuid_str = str(generated_uuid)

                if uppercase:
                    uuid_str = uuid_str.upper()

                if without_dashes:
                    uuid_str = uuid_str.replace('-', '')

                self.generated_uuids.append(uuid_str)

            # Display results
            self.output_text.setPlainText('\n'.join(self.generated_uuids))

            self.status_label.setText(
                f"✅ Generated {quantity} UUID v{version}{'(s)' if quantity > 1 else ''}"
            )
            self.status_label.setStyleSheet("color: #28a745; padding: 5px;")

        except Exception as e:
            self.status_label.setText(f"❌ Error: {str(e)}")
            self.status_label.setStyleSheet("color: #dc3545; padding: 5px;")

    def copy_all(self):
        """Copy all generated UUIDs to clipboard"""
        if self.generated_uuids:
            clipboard = self.output_text.textCursor()
            self.output_text.selectAll()
            self.output_text.copy()
            self.status_label.setText(f"✅ Copied {len(self.generated_uuids)} UUID(s) to clipboard")
            self.status_label.setStyleSheet("color: #28a745; padding: 5px;")

    def clear_all(self):
        """Clear all fields"""
        self.generated_uuids = []
        self.output_text.clear()
        self.status_label.setText("")

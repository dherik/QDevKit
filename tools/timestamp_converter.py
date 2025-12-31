"""
Timestamp Converter Tool
"""

from datetime import datetime, timezone
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QLineEdit, QTextEdit, QRadioButton, QButtonGroup, QFrame
)
from PySide6.QtCore import Qt, QDateTime
from PySide6.QtGui import QFont


class TimestampConverter(QWidget):
    """Tool for converting between timestamps and datetime strings"""

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        """Setup the timestamp converter UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        # Title
        title = QLabel("Timestamp Converter")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        layout.addWidget(title)

        description = QLabel(
            "Convert between Unix timestamps (seconds/milliseconds) and human-readable dates."
        )
        description.setStyleSheet("color: #666;")
        layout.addWidget(description)

        # Current timestamp display
        current_frame = QFrame()
        current_frame.setStyleSheet("""
            QFrame {
                background-color: #f5f5f5;
                border-radius: 5px;
                padding: 10px;
            }
        """)
        current_layout = QVBoxLayout(current_frame)

        current_label = QLabel("Current Timestamp:")
        current_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        current_layout.addWidget(current_label)

        self.current_timestamp_label = QLabel("")
        self.current_timestamp_label.setFont(QFont("Consolas", 11))
        current_layout.addWidget(self.current_timestamp_label)

        layout.addWidget(current_frame)

        # Conversion mode
        mode_layout = QHBoxLayout()
        mode_label = QLabel("Convert:")
        mode_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        mode_layout.addWidget(mode_label)

        self.mode_group = QButtonGroup()
        self.to_date_radio = QRadioButton("Timestamp → Date")
        self.to_date_radio.setChecked(True)
        self.to_timestamp_radio = QRadioButton("Date → Timestamp")

        self.mode_group.addButton(self.to_date_radio, 1)
        self.mode_group.addButton(self.to_timestamp_radio, 2)

        mode_layout.addWidget(self.to_date_radio)
        mode_layout.addWidget(self.to_timestamp_radio)
        mode_layout.addStretch()
        layout.addLayout(mode_layout)

        # Input section
        input_label = QLabel("Input:")
        input_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        layout.addWidget(input_label)

        self.input_text = QLineEdit()
        self.input_text.setPlaceholderText("Enter timestamp or date...")
        self.input_text.setFont(QFont("Consolas", 10))
        self.input_text.setMinimumHeight(35)
        layout.addWidget(self.input_text)

        # Timestamp unit selection (for timestamp to date)
        unit_layout = QHBoxLayout()
        unit_label = QLabel("Timestamp Unit:")
        unit_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        unit_layout.addWidget(unit_label)

        self.unit_group = QButtonGroup()
        self.seconds_radio = QRadioButton("Seconds")
        self.seconds_radio.setChecked(True)
        self.milliseconds_radio = QRadioButton("Milliseconds")

        self.unit_group.addButton(self.seconds_radio, 1)
        self.unit_group.addButton(self.milliseconds_radio, 2)

        unit_layout.addWidget(self.seconds_radio)
        unit_layout.addWidget(self.milliseconds_radio)
        unit_layout.addStretch()
        layout.addLayout(unit_layout)

        # Buttons
        button_layout = QHBoxLayout()

        self.convert_btn = QPushButton("Convert")
        self.convert_btn.clicked.connect(self.convert)
        self.convert_btn.setMinimumHeight(35)
        button_layout.addWidget(self.convert_btn)

        self.now_btn = QPushButton("Insert Current Time")
        self.now_btn.clicked.connect(self.insert_current_time)
        self.now_btn.setMinimumHeight(35)
        button_layout.addWidget(self.now_btn)

        self.clear_btn = QPushButton("Clear")
        self.clear_btn.clicked.connect(self.clear_all)
        self.clear_btn.setMinimumHeight(35)
        button_layout.addWidget(self.clear_btn)

        layout.addLayout(button_layout)

        # Output section
        output_label = QLabel("Result:")
        output_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        layout.addWidget(output_label)

        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setMinimumHeight(150)
        self.output_text.setFont(QFont("Consolas", 10))
        layout.addWidget(self.output_text)

        # Status bar
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color: #666; padding: 5px;")
        layout.addWidget(self.status_label)

        layout.addStretch()

        # Apply button styles
        self.apply_button_styles()

        # Update current timestamp
        self.update_current_timestamp()

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
            QPushButton#nowButton {
                background-color: #107c10;
            }
            QPushButton#nowButton:hover {
                background-color: #0c5c0c;
            }
            QPushButton#clearButton {
                background-color: #d13438;
            }
            QPushButton#clearButton:hover {
                background-color: #a92a2d;
            }
        """
        self.convert_btn.setStyleSheet(button_style)
        self.now_btn.setStyleSheet(button_style.replace("QPushButton", "QPushButton#nowButton"))
        self.clear_btn.setStyleSheet(button_style.replace("QPushButton", "QPushButton#clearButton"))

    def update_current_timestamp(self):
        """Update the current timestamp display"""
        now = datetime.now(timezone.utc)
        timestamp_sec = int(now.timestamp())
        timestamp_ms = int(now.timestamp() * 1000)

        display_text = f"Seconds: {timestamp_sec} | Milliseconds: {timestamp_ms}"
        self.current_timestamp_label.setText(display_text)

    def convert(self):
        """Perform the conversion"""
        input_data = self.input_text.text().strip()

        if not input_data:
            self.status_label.setText("⚠️  Please enter a value to convert")
            self.status_label.setStyleSheet("color: #f0ad4e; padding: 5px;")
            return

        try:
            if self.to_date_radio.isChecked():
                # Timestamp to Date
                try:
                    timestamp = float(input_data)
                except ValueError:
                    raise ValueError("Invalid timestamp format")

                # Check if milliseconds or seconds
                if self.milliseconds_radio.isChecked():
                    # Milliseconds
                    if timestamp > 9999999999999:  # Too large
                        raise ValueError("Timestamp value is too large")
                    dt = datetime.fromtimestamp(timestamp / 1000, tz=timezone.utc)
                    unit = "milliseconds"
                else:
                    # Seconds
                    dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
                    unit = "seconds"

                # Format output
                result_lines = [
                    f"Input: {input_data} ({unit})",
                    "",
                    f"UTC: {dt.strftime('%Y-%m-%d %H:%M:%S')} UTC",
                    f"ISO 8601: {dt.isoformat()}",
                    f"RFC 2822: {dt.strftime('%a, %d %b %Y %H:%M:%S GMT')}",
                    "",
                    "Additional formats:",
                    f"  {dt.strftime('%Y-%m-%d')}",
                    f"  {dt.strftime('%d/%m/%Y %H:%M:%S')}",
                    f"  {dt.strftime('%A, %B %d, %Y')}",
                ]

                self.output_text.setPlainText('\n'.join(result_lines))
                self.status_label.setText("✅ Converted timestamp to date")
                self.status_label.setStyleSheet("color: #28a745; padding: 5px;")

            else:
                # Date to Timestamp
                # Try common date formats
                formats = [
                    '%Y-%m-%d %H:%M:%S',
                    '%Y-%m-%d',
                    '%Y/%m/%d %H:%M:%S',
                    '%Y/%m/%d',
                    '%d/%m/%Y %H:%M:%S',
                    '%d/%m/%Y',
                    '%d-%m-%Y %H:%M:%S',
                    '%d-%m-%Y',
                    '%B %d, %Y %H:%M:%S',
                    '%B %d, %Y',
                ]

                dt = None
                for fmt in formats:
                    try:
                        dt = datetime.strptime(input_data, fmt)
                        break
                    except ValueError:
                        continue

                if dt is None:
                    # Try ISO format
                    try:
                        dt = datetime.fromisoformat(input_data.replace('Z', '+00:00'))
                    except ValueError:
                        raise ValueError(
                            "Could not parse date. Try formats like: "
                            "2024-01-15, 2024-01-15 14:30:00, or ISO 8601"
                        )

                # Make timezone-aware if not
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=timezone.utc)

                # Calculate timestamps
                timestamp_sec = int(dt.timestamp())
                timestamp_ms = int(dt.timestamp() * 1000)

                result_lines = [
                    f"Input: {input_data}",
                    "",
                    f"Seconds: {timestamp_sec}",
                    f"Milliseconds: {timestamp_ms}",
                    "",
                    f"UTC: {dt.strftime('%Y-%m-%d %H:%M:%S')} UTC",
                    f"ISO 8601: {dt.isoformat()}",
                ]

                self.output_text.setPlainText('\n'.join(result_lines))
                self.status_label.setText("✅ Converted date to timestamp")
                self.status_label.setStyleSheet("color: #28a745; padding: 5px;")

        except Exception as e:
            self.output_text.clear()
            self.status_label.setText(f"❌ Error: {str(e)}")
            self.status_label.setStyleSheet("color: #dc3545; padding: 5px;")

    def insert_current_time(self):
        """Insert current time/date based on mode"""
        now = datetime.now(timezone.utc)

        if self.to_date_radio.isChecked():
            # Insert current timestamp
            self.input_text.setText(str(int(now.timestamp())))
        else:
            # Insert current date
            self.input_text.setText(now.strftime('%Y-%m-%d %H:%M:%S'))

    def clear_all(self):
        """Clear all fields"""
        self.input_text.clear()
        self.output_text.clear()
        self.status_label.setText("")

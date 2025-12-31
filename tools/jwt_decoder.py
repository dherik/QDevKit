"""
JWT Decoder Tool
"""

import json
import base64
import hashlib
from datetime import datetime
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton,
    QLabel, QGroupBox, QScrollArea
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class JwtDecoderTool(QWidget):
    """Tool for decoding JWT tokens"""

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        """Setup the JWT decoder UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        # Title
        title = QLabel("JWT Decoder")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        layout.addWidget(title)

        description = QLabel(
            "Decode JSON Web Tokens (JWT) to view header and payload contents. "
            "No signature verification is performed."
        )
        description.setStyleSheet("color: #666;")
        layout.addWidget(description)

        # Input section
        input_label = QLabel("JWT Token:")
        input_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        layout.addWidget(input_label)

        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText("Paste your JWT token here...")
        self.input_text.setMaximumHeight(100)
        self.input_text.setFont(QFont("Consolas", 10))
        layout.addWidget(self.input_text)

        # Buttons
        button_layout = QHBoxLayout()

        self.decode_btn = QPushButton("Decode")
        self.decode_btn.clicked.connect(self.decode_jwt)
        self.decode_btn.setMinimumHeight(35)
        button_layout.addWidget(self.decode_btn)

        self.clear_btn = QPushButton("Clear")
        self.clear_btn.clicked.connect(self.clear_all)
        self.clear_btn.setMinimumHeight(35)
        button_layout.addWidget(self.clear_btn)

        button_layout.addStretch()
        layout.addLayout(button_layout)

        # Create scroll area for results
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)

        # Results container
        results_widget = QWidget()
        results_layout = QVBoxLayout(results_widget)

        # Header section
        self.header_group = self.create_section("Header", "")
        results_layout.addWidget(self.header_group)

        # Payload section
        self.payload_group = self.create_section("Payload", "")
        results_layout.addWidget(self.payload_group)

        # Signature section
        self.signature_group = self.create_section("Signature", "")
        results_layout.addWidget(self.signature_group)

        # Token info section
        self.info_group = self.create_info_section()
        results_layout.addWidget(self.info_group)

        results_layout.addStretch()
        scroll.setWidget(results_widget)

        layout.addWidget(scroll, 1)

        # Status bar
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color: #666; padding: 5px;")
        layout.addWidget(self.status_label)

        # Apply button styles
        self.apply_button_styles()

    def create_section(self, title, content):
        """Create a collapsible group box section"""
        group = QGroupBox(title)
        group.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        layout = QVBoxLayout(group)

        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        text_edit.setMaximumHeight(150)
        text_edit.setFont(QFont("Consolas", 9))
        text_edit.setPlainText(content)

        layout.addWidget(text_edit)
        return group

    def create_info_section(self):
        """Create token information section"""
        group = QGroupBox("Token Information")
        group.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        layout = QVBoxLayout(group)

        self.info_label = QLabel("No token decoded yet")
        self.info_label.setWordWrap(True)
        self.info_label.setFont(QFont("Arial", 9))

        layout.addWidget(self.info_label)
        return group

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
        self.decode_btn.setStyleSheet(button_style)
        self.clear_btn.setStyleSheet(button_style.replace("QPushButton", "QPushButton#clearButton"))

    def base64_decode(self, data):
        """Base64 decode with padding fix"""
        # Add padding if needed
        missing_padding = len(data) % 4
        if missing_padding:
            data += '=' * (4 - missing_padding)

        return base64.urlsafe_b64decode(data)

    def decode_jwt(self):
        """Decode the JWT token"""
        token = self.input_text.toPlainText().strip()

        if not token:
            self.status_label.setText("⚠️  Please enter a JWT token")
            self.status_label.setStyleSheet("color: #f0ad4e; padding: 5px;")
            return

        try:
            parts = token.split('.')

            if len(parts) != 3:
                raise ValueError("Invalid JWT format. Expected 3 parts separated by dots.")

            # Decode header
            header_decoded = self.base64_decode(parts[0])
            header_json = json.loads(header_decoded)
            header_formatted = json.dumps(header_json, indent=2)

            # Update header section
            self.update_section_text(self.header_group, header_formatted)

            # Decode payload
            payload_decoded = self.base64_decode(parts[1])
            payload_json = json.loads(payload_decoded)
            payload_formatted = json.dumps(payload_json, indent=2)

            # Update payload section
            self.update_section_text(self.payload_group, payload_formatted)

            # Signature (can't decode, just show)
            signature = parts[2]
            self.update_section_text(self.signature_group, signature)

            # Extract token information
            info_text = self.extract_token_info(header_json, payload_json)
            self.info_label.setText(info_text)

            self.status_label.setText("✅ JWT decoded successfully")
            self.status_label.setStyleSheet("color: #28a745; padding: 5px;")

        except Exception as e:
            self.status_label.setText(f"❌ Error: {str(e)}")
            self.status_label.setStyleSheet("color: #dc3545; padding: 5px;")

    def update_section_text(self, group, text):
        """Update the text content of a section"""
        text_edit = group.findChild(QTextEdit)
        if text_edit:
            text_edit.setPlainText(text)

    def extract_token_info(self, header, payload):
        """Extract and display token information"""
        info_lines = []

        # Algorithm
        alg = header.get('alg', 'N/A')
        typ = header.get('typ', 'N/A')
        info_lines.append(f"<b>Algorithm:</b> {alg} | <b>Type:</b> {typ}")

        # Issuer
        if 'iss' in payload:
            info_lines.append(f"<b>Issuer:</b> {payload['iss']}")

        # Subject
        if 'sub' in payload:
            info_lines.append(f"<b>Subject:</b> {payload['sub']}")

        # Audience
        if 'aud' in payload:
            info_lines.append(f"<b>Audience:</b> {payload['aud']}")

        # Expiration
        if 'exp' in payload:
            exp_timestamp = payload['exp']
            exp_datetime = datetime.fromtimestamp(exp_timestamp)
            info_lines.append(f"<b>Expires:</b> {exp_datetime.strftime('%Y-%m-%d %H:%M:%S')}")

        # Not Before
        if 'nbf' in payload:
            nbf_timestamp = payload['nbf']
            nbf_datetime = datetime.fromtimestamp(nbf_timestamp)
            info_lines.append(f"<b>Not Before:</b> {nbf_datetime.strftime('%Y-%m-%d %H:%M:%S')}")

        # Issued At
        if 'iat' in payload:
            iat_timestamp = payload['iat']
            iat_datetime = datetime.fromtimestamp(iat_timestamp)
            info_lines.append(f"<b>Issued At:</b> {iat_datetime.strftime('%Y-%m-%d %H:%M:%S')}")

        # JWT ID
        if 'jti' in payload:
            info_lines.append(f"<b>JWT ID:</b> {payload['jti']}")

        return '<br>'.join(info_lines)

    def clear_all(self):
        """Clear all fields"""
        self.input_text.clear()
        self.update_section_text(self.header_group, "")
        self.update_section_text(self.payload_group, "")
        self.update_section_text(self.signature_group, "")
        self.info_label.setText("No token decoded yet")
        self.status_label.setText("")

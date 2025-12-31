"""
Main Window for QDevKit
"""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QListWidget, QStackedWidget,
    QListWidgetItem, QLabel, QFrame
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont

from tools.json_formatter import JsonFormatterTool
from tools.base64_tool import Base64Tool
from tools.uuid_generator import UuidGeneratorTool
from tools.jwt_decoder import JwtDecoderTool
from tools.url_encoder import UrlEncoderTool
from tools.timestamp_converter import TimestampConverter
from tools.hash_generator import HashGeneratorTool


class MainWindow(QMainWindow):
    """Main application window"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("QDevKit - Developer Utilities")
        self.setMinimumSize(900, 600)
        self.resize(1000, 700)

        self.setup_ui()

    def setup_ui(self):
        """Setup the main window UI"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Create sidebar for tool selection
        self.sidebar = self.create_sidebar()
        main_layout.addWidget(self.sidebar)

        # Create stacked widget for tools
        self.tool_stack = QStackedWidget()
        main_layout.addWidget(self.tool_stack, 1)  # Give stretch factor

        # Add tools
        self.add_tools()

    def create_sidebar(self):
        """Create the sidebar with tool list"""
        sidebar = QFrame()
        sidebar.setFrameShape(QFrame.Shape.StyledPanel)
        sidebar.setFixedWidth(220)
        sidebar.setStyleSheet("""
            QFrame {
                background-color: #2b2b2b;
                border-right: 1px solid #3d3d3d;
            }
        """)

        layout = QHBoxLayout(sidebar)
        layout.setContentsMargins(0, 0, 0, 0)

        self.tool_list = QListWidget()
        self.tool_list.setStyleSheet("""
            QListWidget {
                background-color: #2b2b2b;
                border: none;
                color: #ffffff;
                font-size: 13px;
                outline: none;
            }
            QListWidget::item {
                padding: 12px 15px;
                border-bottom: 1px solid #3d3d3d;
            }
            QListWidget::item:selected {
                background-color: #0078d4;
                color: #ffffff;
            }
            QListWidget::item:hover {
                background-color: #3d3d3d;
            }
        """)

        # Header
        header = QListWidgetItem()
        header.setText("  DEVELOPER TOOLS")
        header.setFlags(Qt.ItemFlag.NoItemFlags)
        header.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        self.tool_list.addItem(header)

        layout.addWidget(self.tool_list)

        return sidebar

    def add_tools(self):
        """Add all tools to the window"""
        tools = [
            ("JSON Formatter", JsonFormatterTool),
            ("Base64 Encode/Decode", Base64Tool),
            ("UUID Generator", UuidGeneratorTool),
            ("JWT Decoder", JwtDecoderTool),
            ("URL Encoder/Decoder", UrlEncoderTool),
            ("Timestamp Converter", TimestampConverter),
            ("Hash Generator", HashGeneratorTool),
        ]

        for tool_name, tool_class in tools:
            # Add to list
            item = QListWidgetItem()
            item.setText(tool_name)
            self.tool_list.addItem(item)

            # Create tool widget and add to stack
            tool_widget = tool_class()
            self.tool_stack.addWidget(tool_widget)

        # Connect selection change
        self.tool_list.currentRowChanged.connect(self.on_tool_selected)

        # Select first tool (skip header)
        self.tool_list.setCurrentRow(1)

    def on_tool_selected(self, index):
        """Handle tool selection from sidebar"""
        if index > 0:  # Skip header
            self.tool_stack.setCurrentIndex(index - 1)

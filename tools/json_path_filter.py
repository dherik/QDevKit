"""
JSON Path Filter Tool
"""

import json
from functools import partial
from pathlib import Path
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton,
    QLabel, QGroupBox, QComboBox, QGridLayout, QFrame, QLineEdit, QScrollArea, QSizePolicy
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QCursor
from jsonpath_ng import parse
from jsonpath_ng.exceptions import JsonPathParserError


class JsonPathFilterTool(QWidget):
    """Tool for filtering JSON data using JSONPath expressions"""

    def __init__(self):
        super().__init__()
        self.history = []
        self.max_history = 20
        self.history_file = Path.home() / '.qdevkit_jsonpath_history.json'
        self.load_history()
        self.setup_ui()

    def setup_ui(self):
        """Setup the JSON Path Filter UI"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Create scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        # Create scroll content widget
        scroll_content = QWidget()
        layout = QVBoxLayout(scroll_content)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(8)

        # Title
        title = QLabel("JSON Path Filter")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        layout.addWidget(title)

        description = QLabel(
            "Filter JSON data using JSONPath expressions. Extract specific nodes, arrays, or filtered results."
        )
        description.setStyleSheet("color: #666;")
        description.setWordWrap(True)
        layout.addWidget(description)

        # Input section
        input_label = QLabel("Input JSON:")
        input_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        layout.addWidget(input_label)

        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText("Paste your JSON here...")
        self.input_text.setMinimumHeight(120)
        self.input_text.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.input_text.setFont(QFont("Consolas", 10))
        layout.addWidget(self.input_text)

        # Expression input section
        expr_label = QLabel("JSONPath Expression:")
        expr_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        layout.addWidget(expr_label)

        expr_layout = QHBoxLayout()
        self.expr_input = QLineEdit()
        self.expr_input.setPlaceholderText("$")
        self.expr_input.setFont(QFont("Consolas", 10))
        expr_layout.addWidget(self.expr_input)

        self.apply_expr_btn = QPushButton("Apply")
        self.apply_expr_btn.clicked.connect(self.filter_json)
        self.apply_expr_btn.setMinimumHeight(30)
        self.apply_expr_btn.setMinimumWidth(70)
        expr_layout.addWidget(self.apply_expr_btn)

        layout.addLayout(expr_layout)

        # Quick Examples section - more compact
        examples_group = QGroupBox("Quick Examples (click to use)")
        examples_layout = QGridLayout()
        examples_layout.setSpacing(3)
        examples_layout.setContentsMargins(8, 12, 8, 8)

        examples = [
            ("$.items[*]", "All items"),
            ("$.user.name", "Field"),
            ("$.users[0]", "Index"),
            ("$.users[?(@.age > 25)]", "Filter"),
            ("$..[name, email]", "Multi"),
            ("$", "Root"),
        ]

        for i, (expr, desc) in enumerate(examples):
            row = i // 2
            col = (i % 2) * 2
            example_btn = QPushButton(f"{expr}")
            example_btn.setToolTip(desc)
            example_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            example_btn.clicked.connect(partial(self.use_example, expr))
            examples_layout.addWidget(example_btn, row, col)

            desc_label = QLabel(desc)
            desc_label.setStyleSheet("color: #666; font-size: 10px;")
            examples_layout.addWidget(desc_label, row, col + 1)

        examples_group.setLayout(examples_layout)
        layout.addWidget(examples_group)

        # History section
        history_label = QLabel("Recent Expressions:")
        history_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        layout.addWidget(history_label)

        self.history_combo = QComboBox()
        self.history_combo.setMaximumHeight(28)
        self.history_combo.currentTextChanged.connect(self.on_history_selected)
        layout.addWidget(self.history_combo)

        # Update history combo
        self.update_history_ui()

        # Buttons
        button_layout = QHBoxLayout()

        self.filter_btn = QPushButton("Apply Filter")
        self.filter_btn.clicked.connect(self.filter_json)
        self.filter_btn.setMinimumHeight(32)
        button_layout.addWidget(self.filter_btn)

        self.copy_btn = QPushButton("Copy Result")
        self.copy_btn.clicked.connect(self.copy_result)
        self.copy_btn.setMinimumHeight(32)
        button_layout.addWidget(self.copy_btn)

        self.clear_btn = QPushButton("Clear")
        self.clear_btn.clicked.connect(self.clear_all)
        self.clear_btn.setMinimumHeight(32)
        button_layout.addWidget(self.clear_btn)

        layout.addLayout(button_layout)

        # Output section
        output_label = QLabel("Filtered Result:")
        output_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        layout.addWidget(output_label)

        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setMinimumHeight(120)
        self.output_text.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.output_text.setFont(QFont("Consolas", 10))
        layout.addWidget(self.output_text)

        # Status bar
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color: #666; padding: 5px;")
        layout.addWidget(self.status_label)

        # Set scroll content
        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area)

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
        self.filter_btn.setStyleSheet(button_style)
        self.apply_expr_btn.setStyleSheet(button_style)
        self.copy_btn.setStyleSheet(button_style.replace("QPushButton", "QPushButton#copyButton"))
        self.clear_btn.setStyleSheet(button_style.replace("QPushButton", "QPushButton#clearButton"))

        # Example buttons style
        example_style = """
            QPushButton {
                background-color: #f5f5f5;
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 6px 10px;
                font-size: 11px;
                font-family: Consolas;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #e5e5e5;
                border-color: #0078d4;
            }
        """
        # Apply to all child buttons in the examples group
        for child in self.findChildren(QPushButton):
            if child not in [self.filter_btn, self.apply_expr_btn, self.copy_btn, self.clear_btn]:
                child.setStyleSheet(example_style)

    def filter_json(self):
        """Execute JSONPath filter on input JSON"""
        input_data = self.input_text.toPlainText().strip()
        expression = self.expr_input.text().strip()

        if not input_data:
            self.status_label.setText("⚠️  Please enter JSON data")
            self.status_label.setStyleSheet("color: #f0ad4e; padding: 5px;")
            return

        if not expression:
            self.status_label.setText("⚠️  Please enter a JSONPath expression")
            self.status_label.setStyleSheet("color: #f0ad4e; padding: 5px;")
            return

        try:
            # Parse JSON
            data = json.loads(input_data)

            # Parse JSONPath expression
            try:
                jsonpath_expr = parse(expression)
            except JsonPathParserError as e:
                self.output_text.setPlainText("")
                self.status_label.setText(f"❌ Invalid JSONPath: {str(e)}")
                self.status_label.setStyleSheet("color: #dc3545; padding: 5px;")
                return

            # Execute filter
            matches = jsonpath_expr.find(data)

            if not matches:
                self.output_text.setPlainText("[]")
                self.status_label.setText("ℹ️  No matches found for this expression")
                self.status_label.setStyleSheet("color: #17a2b8; padding: 5px;")
            else:
                # Extract values
                results = [match.value for match in matches]

                # Format output
                if len(results) == 1:
                    # Single match - display directly
                    formatted = json.dumps(results[0], indent=2, ensure_ascii=False)
                    match_info = "1 match"
                else:
                    # Multiple matches - display as array
                    formatted = json.dumps(results, indent=2, ensure_ascii=False)
                    match_info = f"{len(results)} matches"

                self.output_text.setPlainText(formatted)
                self.status_label.setText(f"✅ Found {match_info}")
                self.status_label.setStyleSheet("color: #28a745; padding: 5px;")

                # Add to history on success
                self.add_to_history(expression)

        except json.JSONDecodeError as e:
            self.output_text.setPlainText("")
            self.status_label.setText(f"❌ Invalid JSON: {str(e)}")
            self.status_label.setStyleSheet("color: #dc3545; padding: 5px;")
        except Exception as e:
            self.output_text.setPlainText("")
            self.status_label.setText(f"❌ Error: {str(e)}")
            self.status_label.setStyleSheet("color: #dc3545; padding: 5px;")

    def use_example(self, expression):
        """Insert example expression into input field"""
        self.expr_input.setText(expression)
        self.status_label.setText(f"ℹ️  Example loaded: {expression}")
        self.status_label.setStyleSheet("color: #17a2b8; padding: 5px;")

    def add_to_history(self, expression):
        """Add expression to history with LRU eviction"""
        # Remove if already exists
        if expression in self.history:
            self.history.remove(expression)

        # Add to front
        self.history.insert(0, expression)

        # Trim to max
        if len(self.history) > self.max_history:
            self.history = self.history[:self.max_history]

        # Update UI and save
        self.update_history_ui()
        self.save_history()

    def update_history_ui(self):
        """Update the history combo box"""
        self.history_combo.clear()
        self.history_combo.addItem("-- Select recent expression --")
        for expr in self.history:
            self.history_combo.addItem(expr)

    def on_history_selected(self, text):
        """Handle history selection"""
        if text and not text.startswith("--"):
            self.expr_input.setText(text)

    def load_history(self):
        """Load history from JSON file"""
        try:
            if self.history_file.exists():
                with open(self.history_file, 'r') as f:
                    data = json.load(f)
                    if isinstance(data, dict) and 'history' in data:
                        self.history = data['history']
                    elif isinstance(data, list):
                        self.history = data
        except (json.JSONDecodeError, IOError):
            # Start with empty history if file is corrupted
            self.history = []

    def save_history(self):
        """Save history to JSON file"""
        try:
            data = {
                'version': 1,
                'history': self.history
            }
            with open(self.history_file, 'w') as f:
                json.dump(data, f, indent=2)
        except IOError:
            # Silently fail if we can't save history
            pass

    def copy_result(self):
        """Copy filtered result to clipboard"""
        result_text = self.output_text.toPlainText()
        if result_text:
            self.output_text.selectAll()
            self.output_text.copy()
            self.status_label.setText("✅ Result copied to clipboard")
            self.status_label.setStyleSheet("color: #28a745; padding: 5px;")

    def clear_all(self):
        """Clear all fields"""
        self.input_text.clear()
        self.expr_input.setText("")
        self.output_text.clear()
        self.status_label.setText("")

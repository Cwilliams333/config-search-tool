#!/usr/bin/env python3
import sys
import os
import subprocess
import json
import re
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QComboBox, QLineEdit, 
                             QPushButton, QRadioButton, QButtonGroup, QTextEdit, 
                             QGroupBox, QTabWidget, QSplitter, QFileDialog,
                             QStatusBar, QMessageBox, QFrame, QProgressDialog)
from PyQt5.QtCore import Qt, QProcess, QTimer, QDateTime
from PyQt5.QtGui import QFont, QColor, QPalette, QTextCursor

class ConfigSearchApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Store directory paths
        self.directories = {
            "DUT Parameters": "/var/db/fusion/test_parameters/test_parameter_configs/dut_parameters",
            "DUT Configurations": "/var/db/fusion/dut_configurations",
            "Legacy Parameters": "/etc/brb-mes/_legacy_profiles/core/dut_parameters",
            "Legacy Configurations": "/etc/brb-mes/_legacy_dut_configurations",
            "Trades Parameters": "/etc/brb-mes/_legacy_profiles/trades/dut_parameters",
            "Custom Directory": ""
        }
        
        # Fallback model database - will be loaded from file if exists
        self.model_database = {
            "Encore_VZW": "TCL 40XE 5G",
            "Fun": "Orbic Fun Pro 5G",
            "JOY2": "Orbic Joy 2",
            "KY22M-RG100": "DuraForce Pro 3",
            "OnePlus8VZW": "OnePLus 8",
            "Ruby_VZW": "TCL 50 XL",
            "Style": "Orbic Style 5G",
            "Trophy": "Orbic Trophy 5G UW",
            "Wa42xuq": "Galaxy A42 5G",
            "Wa71": "A71",
            "X800": "XP Pro 5G",
            "a01q": "Galaxy A01",
            "a02q": "Galaxy A02",
            "a03su": "Galaxy A03s",
            "a10e": "A10e",
            "a11q": "A11",
            "a13": "A13",
            "a15x": "Galaxy A15 5G",
            "a16x": "Galaxy A16 5G",
            "a20p": "A20",
            "a21": "A21",
            "a23xq": "Galaxy A23 5G UW",
            "a36xq": "Galaxy A36 5G",
            "a42xuq": "Galaxy A42 5G",
            "a50": "A50",
            "a51": "A51",
            "a51xq": "A51 5G",
            "a53x": "Galaxy A53 5G",
            "a54x": "Galaxy A54 5G",
            "a71xq": "A71",
            "aito": "motorola razr 2025",
            "akita": "Pixel 8a",
            "b0q": "Galaxy S22 Ultra",
            "b2q": "Galaxy Z Flip3 5G",
            "b4q": "Galaxy Z Flip4 5G",
            "b5q": "Galaxy Z Flip5 5G",
            "b6q": "Galaxy Z Flip6 5G",
            "b7s": "Galaxy Z Flip 7",
            "berlna": "Moto Edge 2021 (XT-2141)",
            "beyond0q": "Samsung S10e",
            "beyond1q": "Samsung S10",
            "beyond2q": "S10+",
            "beyondxq": "Samsung S10 5G",
            "bluejay": "Pixel 6a",
            "blueline": "Pixel 3",
            "bonito": "Pixel 3a XL",
            "borneo": "Moto G Power (2021)",
            "boston": "moto g stylus - 2024",
            "bramble": "Pixel 4a 5G",
            "burton": "Moto Edge Plus",
            "c1q": "Galaxy Note 20 5G",
            "c2q": "Galaxy Note 20 Ultra 5G",
            "caiman": "Pixel 9 Pro",
            "channel": "moto g(7) play",
            "cheetah": "Pixel 7 Pro",
            "coral": "Pixel 4 XL",
            "crosshatch": "Pixel 3 XL",
            "crownqltesq": "Galaxy Note9",
            "crownqlteue": "Galaxy Note9",
            "d1q": "Galaxy Note 10",
            "d2q": "Galaxy Note 10+",
            "d2xq": "Galaxy Note 10 5G",
            "dm1q": "Galaxy S23",
            "dm2q": "Galaxy S23+",
            "dm3q": "Galaxy S23 Ultra",
            "dream2qltesq": "Galaxy S8+",
            "dreamqltesq": "Galaxy S8",
            "e1q": "Galaxy S24",
            "e2q": "Galaxy S24+",
            "e3q": "Galaxy S24 Ultra",
            "flame": "Pixel 4",
            "foles": "moto z4",
            "g0q": "Galaxy S22+",
            "greatqlte": "Galaxy Note8",
            "guamna": "Moto G Play (2021)",
            "hero2qltevzw": "Galaxy S7 Edge",
            "heroqltevzw": "Galaxy S7",
            "hiphi": "motorola edge plus 5G UW (2022)",
            "husky": "Pixel 8 Pro",
            "iPhone10,1": "iPhone 8",
            "iPhone10,2": "iPhone 8 Plus",
            "iPhone10,3": "iPhone X",
            "iPhone10,5": "iPhone 8 Plus",
            "iPhone10,6": "iPhone X",
            "iPhone11,2": "iPhone XS",
            "iPhone11,6": "iPhone XS Max",
            "iPhone11,8": "iPhone XR",
            "iPhone12,1": "iPhone 11",
            "iPhone12,3": "iPhone 11 Pro",
            "iPhone12,5": "iPhone 11 Pro Max",
            "iPhone12,8": "iPhone SE 2",
            "iPhone13,1": "iPhone 12 Mini",
            "iPhone13,2": "iPhone 12",
            "iPhone13,3": "iPhone 12 Pro",
            "iPhone13,4": "iPhone 12 Pro Max",
            "iPhone14,2": "iPhone 13 Pro",
            "iPhone14,3": "iPhone 13 Pro Max",
            "iPhone14,4": "iPhone 13 Mini",
            "iPhone14,5": "iPhone 13",
            "iPhone14,6": "iPhone SE 3",
            "iPhone14,7": "iPhone 14",
            "iPhone14,8": "iPhone 14 Plus",
            "iPhone15,2": "iPhone 14 Pro",
            "iPhone15,3": "iPhone 14 Pro Max",
            "iPhone15,4": "iPhone 15",
            "iPhone15,5": "iPhone 15 Plus",
            "iPhone16,1": "iPhone 15 Pro",
            "iPhone16,2": "iPhone 15 Pro Max",
            "iPhone17,1": "iPhone 16 Pro",
            "iPhone17,2": "iPhone 16 Pro Max",
            "iPhone17,3": "iPhone 16",
            "iPhone17,4": "iPhone 16 Plus",
            "iPhone17,5": "iPhone 16e",
            "iPhone7,1": "iPhone 6 Plus",
            "iPhone7,2": "iPhone 6",
            "iPhone8,1": "iPhone 6S",
            "iPhone8,2": "iPhone 6S Plus",
            "iPhone8,4": "iPhone SE",
            "iPhone9,1": "iPhone 7",
            "iPhone9,2": "iPhone 7 Plus",
            "iPhone9,3": "iPhone 7",
            "iPhone9,4": "iPhone 7 Plus",
            "j3popltevzw": "J327",
            "j3topeltevzw": "J337",
            "j7popltevzw": "Galaxy J727",
            "j7topeltevzw": "Galaxy J737",
            "kievv": "Motorola One 5G UW ace",
            "kltevzw": "Galaxy S5",
            "komodo": "Pixel 9 Pro XL",
            "lynx": "Pixel 7a",
            "maui": "Motorolla XT2271-1PP",
            "messi": "Moto XT1929",
            "nairo": "Moto one 5G",
            "nobleltevzw": "Galaxy Note 5",
            "o1q": "Galaxy S21",
            "oriole": "Pixel 6",
            "p3q": "S21 Ultra 5G",
            "pa1q": "Galaxy S25",
            "pa2q": "Galaxy S25+",
            "pa3q": "Galaxy S25 Ultra",
            "panther": "Pixel 7",
            "psq": "Galaxy S25 Edge",
            "q7q": "Galaxy Z Fold7",
            "r0q": "Galaxy S22 Ultra",
            "r11q": "Galaxy S23 FE",
            "r12s": "Galaxy S24 FE",
            "r8q": "Galaxy S20 FE 5G UW",
            "r9q": "Galaxy S20 FE 5G UW",
            "raven": "Pixel 6 Pro",
            "redfin": "Pixel 5",
            "sargo": "Pixel 3a",
            "shiba": "Pixel 8",
            "sofia": "XT2041-7",
            "sofiap": "XT2043-5",
            "star2qltesq": "Galaxy S9+",
            "star2qlteue": "Galaxy S9+",
            "starqltesq": "Galaxy S9",
            "starqlteue": "Galaxy S9",
            "sunfish": "Pixel 4a 5G",
            "t2q": "Galaxy S21+",
            "tegu": "Google Pixel 9a",
            "tesla": "Moto edge+ 5G UW (2022)",
            "tokay": "Pixel 9",
            "tonga": "Moto G Power 2022",
            "x1q": "S20 5G UW",
            "xcoverpro": "X Cover Pro",
            "y2q": "S20+ 5G",
            "z3q": "S20 Ultra 5G",
            "zerofltevzw": "Galaxy S6",
            "zeroltevzw": "Galaxy S7 Edge"
        }

        
        # Path to model database file
        self.model_db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "model_database.json")
        
        # Load model database from file if it exists
        self.load_model_database()
        
        # Store model information
        self.models = []  # Will contain tuples of (model_code, market_name)
        
        # UI setup
        self.setWindowTitle("Configuration Search Tool - Dark Mode")
        self.setMinimumSize(900, 600)
        self.setup_ui()
        
        # Process initialization
        self.process = QProcess()
        self.process.readyReadStandardOutput.connect(self.handle_stdout)
        self.process.readyReadStandardError.connect(self.handle_stderr)
        self.process.finished.connect(self.process_finished)
        
        # Buffer for process output
        self.stdout_buffer = ""
        self.stderr_buffer = ""
        
        # History
        self.search_history = []
        
        # Load models for initial directory
        self.update_models_list()
        
    def load_model_database(self):
        """Load model database from JSON file if it exists"""
        try:
            if os.path.exists(self.model_db_path):
                with open(self.model_db_path, 'r') as f:
                    loaded_db = json.load(f)
                    # Merge with existing database, keeping existing entries
                    self.model_database.update(loaded_db)
                print(f"Loaded {len(loaded_db)} model names from database file")
        except Exception as e:
            print(f"Error loading model database: {str(e)}")
            
    def save_model_database(self):
        """Save model database to JSON file"""
        try:
            with open(self.model_db_path, 'w') as f:
                json.dump(self.model_database, f, indent=4)
            print(f"Saved {len(self.model_database)} model names to database file")
        except Exception as e:
            print(f"Error saving model database: {str(e)}")
        
    def setup_ui(self):
        # Main layout
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        
        # Tabs
        tabs = QTabWidget()
        main_layout.addWidget(tabs)
        
        # Search tab
        search_tab = QWidget()
        search_layout = QVBoxLayout()
        search_tab.setLayout(search_layout)
        tabs.addTab(search_tab, "Search")
        
        # Directory selection
        dir_group = QGroupBox("Directory Selection")
        dir_layout = QVBoxLayout()
        dir_group.setLayout(dir_layout)
        
        self.dir_combo = QComboBox()
        for name in self.directories.keys():
            self.dir_combo.addItem(name)
        self.dir_combo.currentTextChanged.connect(self.handle_dir_change)
        
        self.custom_dir_path = QLineEdit()
        self.custom_dir_path.setPlaceholderText("Enter custom directory path...")
        self.custom_dir_path.setEnabled(False)
        self.custom_dir_path.editingFinished.connect(self.handle_custom_dir_change)
        
        browse_button = QPushButton("Browse...")
        browse_button.clicked.connect(self.browse_directory)
        
        dir_path_layout = QHBoxLayout()
        dir_path_layout.addWidget(self.custom_dir_path)
        dir_path_layout.addWidget(browse_button)
        
        dir_layout.addWidget(self.dir_combo)
        dir_layout.addLayout(dir_path_layout)
        
        # Search criteria
        criteria_group = QGroupBox("Search Criteria")
        criteria_layout = QVBoxLayout()
        criteria_group.setLayout(criteria_layout)
        
        # Model search
        model_layout = QHBoxLayout()
        model_label = QLabel("Model:")
        self.model_combo = QComboBox()
        self.model_combo.setEditable(True)  # Allow manual entry for flexibility
        self.model_combo.setInsertPolicy(QComboBox.NoInsert)  # Don't add text to list
        self.model_combo.setMinimumWidth(350)  # Make it wide enough for model names
        model_layout.addWidget(model_label, 1)
        model_layout.addWidget(self.model_combo, 4)
        
        # Refresh models button
        refresh_models_button = QPushButton("Refresh Models")
        refresh_models_button.clicked.connect(self.update_models_list)
        model_layout.addWidget(refresh_models_button)
        
        # Section search
        section_layout = QHBoxLayout()
        section_label = QLabel("Section:")
        self.section_input = QLineEdit()
        self.section_input.setPlaceholderText("e.g., CameraRearPhoto (case sensitive)")
        section_layout.addWidget(section_label, 1)
        section_layout.addWidget(self.section_input, 4)
        
        # Query search
        query_layout = QHBoxLayout()
        query_label = QLabel("Query:")
        self.query_input = QLineEdit()
        self.query_input.setPlaceholderText("e.g., EnableTopBar = True")
        query_layout.addWidget(query_label, 1)
        query_layout.addWidget(self.query_input, 4)
        
        criteria_layout.addLayout(model_layout)
        criteria_layout.addLayout(section_layout)
        criteria_layout.addLayout(query_layout)
        
        # Search button
        search_button = QPushButton("Search")
        search_button.setMinimumHeight(40)
        search_button.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
        search_button.clicked.connect(self.perform_search)
        
        # Clear button
        clear_button = QPushButton("Clear")
        clear_button.setMinimumHeight(40)
        clear_button.clicked.connect(self.clear_search)
        
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(search_button)
        buttons_layout.addWidget(clear_button)
        
        # Results area
        results_group = QGroupBox("Results")
        results_layout = QVBoxLayout()
        results_group.setLayout(results_layout)
        
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        self.results_text.setFont(QFont("Monospace", 10))
        # Enable HTML for rich text display
        self.results_text.setAcceptRichText(True)
        
        results_layout.addWidget(self.results_text)
        
        # Add all components to the search tab
        search_layout.addWidget(dir_group)
        search_layout.addWidget(criteria_group)
        search_layout.addLayout(buttons_layout)
        search_layout.addWidget(results_group)
        
        # History tab
        history_tab = QWidget()
        history_layout = QVBoxLayout()
        history_tab.setLayout(history_layout)
        tabs.addTab(history_tab, "History")
        
        self.history_text = QTextEdit()
        self.history_text.setReadOnly(True)
        
        clear_history_button = QPushButton("Clear History")
        clear_history_button.clicked.connect(self.clear_history)
        
        history_layout.addWidget(self.history_text)
        history_layout.addWidget(clear_history_button)
        
        # Model Database tab
        db_tab = QWidget()
        db_layout = QVBoxLayout()
        db_tab.setLayout(db_layout)
        tabs.addTab(db_tab, "Model Database")
        
        self.db_text = QTextEdit()
        self.db_text.setPlaceholderText("# Model Database\nAdd model mappings in format:\nmodel_code = Market Name\n\nFor example:\na01q = Galaxy A01")
        
        save_db_button = QPushButton("Save Database")
        save_db_button.clicked.connect(self.save_db_from_text)
        
        db_layout.addWidget(self.db_text)
        db_layout.addWidget(save_db_button)
        
        # Update the database text
        self.update_db_text()
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
        
    def update_db_text(self):
        """Update the database text editor with current model mappings"""
        content = "# Model Database\n# Format: model_code = Market Name\n\n"
        for model_code, market_name in sorted(self.model_database.items()):
            content += f"{model_code} = {market_name}\n"
        self.db_text.setText(content)
        
    def save_db_from_text(self):
        """Parse and save the model database from the text editor"""
        try:
            text = self.db_text.toPlainText()
            new_db = {}
            
            for line in text.split('\n'):
                line = line.strip()
                # Skip comments and empty lines
                if not line or line.startswith('#'):
                    continue
                    
                if '=' in line:
                    parts = line.split('=', 1)
                    model_code = parts[0].strip()
                    market_name = parts[1].strip()
                    if model_code and market_name:
                        new_db[model_code] = market_name
            
            # Update the database
            self.model_database = new_db
            self.save_model_database()
            
            # Refresh the model list
            self.update_models_list()
            
            QMessageBox.information(self, "Success", f"Saved {len(new_db)} model mappings to database")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save database: {str(e)}")
        
    def handle_dir_change(self, text):
        # Enable/disable custom directory input
        is_custom = text == "Custom Directory"
        self.custom_dir_path.setEnabled(is_custom)
        
        # Update models list
        self.update_models_list()
        
    def handle_custom_dir_change(self):
        # When custom directory path changes, update the models list
        if self.dir_combo.currentText() == "Custom Directory":
            directory = self.custom_dir_path.text()
            if directory and os.path.isdir(directory):
                self.directories["Custom Directory"] = directory
                self.update_models_list()
        
    def browse_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if directory:
            self.custom_dir_path.setText(directory)
            # Update the custom directory in our dictionary
            self.directories["Custom Directory"] = directory
            # Update models list
            self.update_models_list()
            
    def update_models_list(self):
        """Scan the selected directory and update the models dropdown"""
        self.model_combo.clear()
        self.models = []
        
        # Get current directory path
        dir_name = self.dir_combo.currentText()
        if dir_name == "Custom Directory":
            directory = self.custom_dir_path.text()
            if not directory or not os.path.isdir(directory):
                self.status_bar.showMessage("Invalid directory path")
                return
        else:
            directory = self.directories[dir_name]
            
        # Check if directory exists
        if not os.path.isdir(directory):
            self.status_bar.showMessage(f"Directory not found: {directory}")
            return
            
        # Progress dialog
        progress = QProgressDialog("Loading models...", "Cancel", 0, 100, self)
        progress.setWindowModality(Qt.WindowModal)
        progress.show()
        
        try:
            # Get all .ini files
            ini_files = [f for f in os.listdir(directory) if f.endswith('.ini')]
            
            # Process each file
            for idx, file in enumerate(ini_files):
                progress.setValue(int((idx / len(ini_files)) * 100))
                if progress.wasCanceled():
                    break
                    
                model_code = os.path.splitext(file)[0]  # Remove .ini extension
                
                # Look up the model name in our database
                market_name = self.model_database.get(model_code, "")
                
                # Create display name
                if market_name:
                    display_name = f"{market_name} ({model_code})"
                else:
                    display_name = model_code
                    
                self.models.append((model_code, display_name))
                
            # Sort models by display name
            self.models.sort(key=lambda x: x[1])
            
            # Add "All Models" option at the top
            self.model_combo.addItem("All Models")
            
            # Add models to dropdown
            for model_code, display_name in self.models:
                self.model_combo.addItem(display_name, model_code)
                
            self.status_bar.showMessage(f"Loaded {len(self.models)} models")
            
        except Exception as e:
            self.status_bar.showMessage(f"Error loading models: {str(e)}")
            
        finally:
            progress.setValue(100)
            
    def perform_search(self):
        # Get selected model
        selected_index = self.model_combo.currentIndex()
        model = ""
        
        if selected_index > 0:  # Not "All Models"
            model = self.model_combo.itemData(selected_index)
        elif selected_index == 0:  # "All Models"
            model = ""
        else:  # Custom text entered
            # Try to extract model code from the entered text if it matches our pattern
            entered_text = self.model_combo.currentText()
            if "(" in entered_text and ")" in entered_text:
                model = entered_text.split("(")[1].split(")")[0]
            else:
                model = entered_text
                
        # Check if at least one search criterion is provided
        if not any([model, self.section_input.text(), self.query_input.text()]):
            QMessageBox.warning(self, "Warning", "Please provide at least one search criterion (Model, Section, or Query).")
            return
            
        # Clear previous results
        self.results_text.clear()
        
        # Clear output buffers
        self.stdout_buffer = ""
        self.stderr_buffer = ""
        
        # Get selected directory
        dir_name = self.dir_combo.currentText()
        if dir_name == "Custom Directory":
            directory = self.custom_dir_path.text()
            if not directory:
                QMessageBox.warning(self, "Warning", "Please specify a custom directory path.")
                return
            if not os.path.isdir(directory):
                QMessageBox.critical(self, "Error", f"Directory does not exist: {directory}")
                return
        else:
            directory = self.directories[dir_name]
            
        # Build command arguments
        args = []
        
        # Find script path - for now assuming it's in the same directory
        script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "configSearchTool.sh")
        
        # Verify the script exists
        if not os.path.isfile(script_path):
            error_msg = f"Error: Script not found at {script_path}"
            self.results_text.append(error_msg)
            self.status_bar.showMessage(error_msg)
            return
        
        # Add directory option
        dir_option = None
        if dir_name == "DUT Parameters":
            dir_option = "1"
        elif dir_name == "DUT Configurations":
            dir_option = "2"
        elif dir_name == "Legacy Parameters":
            dir_option = "3"
        elif dir_name == "Legacy Configurations":
            dir_option = "4"
        elif dir_name == "Trades Parameters":
            dir_option = "5"
            
        if dir_option:
            args.extend(["-d", dir_option])
        else:
            # Custom directory path
            args.extend(["-d", directory])
        
        if model:
            args.extend(["-m", model])
            
        section = self.section_input.text()
        if section:
            args.extend(["-s", section])
            
        query = self.query_input.text()
        if query:
            args.extend(["-z", query])
            
        # Record in history
        timestamp = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")
        model_display = self.model_combo.currentText() if model else "All Models"
        
        search_params = f"Time: {timestamp}\n"
        search_params += f"Directory: {dir_name} ({directory})\n"
        search_params += f"Model: {model_display}\n"
        if section:
            search_params += f"Section: {section}\n"
        if query:
            search_params += f"Query: {query}\n"
        search_params += "-------------------------------\n"
        
        self.search_history.append(search_params)
        self.update_history()
        
        # Set status
        self.status_bar.showMessage("Searching...")
        
        # Start the process
        try:
            # Set the working directory to the script's directory
            self.process.setWorkingDirectory(os.path.dirname(script_path))
            
            # Start the process
            self.process.start(script_path, args)
        except Exception as e:
            error_msg = f"Failed to start search: {str(e)}"
            QMessageBox.critical(self, "Error", error_msg)
            self.status_bar.showMessage("Search failed")
            
    def process_ansi_output(self, text):
        """
        Process ANSI colored output and convert to HTML
        This function directly formats specific patterns to ensure consistent display
        """
        # Replace any existing HTML-like content
        text = text.replace('&', '&amp;')
        text = text.replace('<', '&lt;')
        text = text.replace('>', '&gt;')
        
        # Replace ANSI color codes with HTML span tags
        color_mapping = {
            '\033[0;32m': '<span style="color: #00BB00;">',  # Green
            '\033[0;31m': '<span style="color: #FF0000;">',  # Red
            '\033[0;33m': '<span style="color: #BBBB00;">',  # Yellow
            '\033[0;34m': '<span style="color: #0000BB;">',  # Blue
            '\033[0m': '</span>',  # Reset
        }
        
        for ansi_code, html_tag in color_mapping.items():
            text = text.replace(ansi_code, html_tag)
        
        # Strip any remaining ANSI codes
        text = re.sub(r'\033\[\d+(?:;\d+)*m', '', text)
        
        # Special formatting for common patterns
        
        # Format checkmarks and X marks
        text = re.sub(r'(✓ [^:]+: Section \[[^\]]+\] found)', 
                    r'<span style="color: #00BB00;">\1</span>', 
                    text)
        text = re.sub(r'(✗ [^:]+: [^\n]+)', 
                    r'<span style="color: #FF0000;">\1</span>', 
                    text)
        
        # Format section headers
        text = re.sub(r'(Search Parameters:|Search Results:|Summary:)', 
                    r'<span style="color: #0000BB;">\1</span>', 
                    text)
        
        # Format values in square brackets
        text = re.sub(r'\[([^\]]+)\]', 
                    r'<span style="color: #BBBB00;">[\1]</span>', 
                    text)
        
        # Format directory paths
        text = re.sub(r'(Directory: )([^\n]+)', 
                    r'\1<span style="color: #BBBB00;">\2</span>', 
                    text)
        
        # Format numbers in summary
        text = re.sub(r'(Total files searched: )(\d+)', 
                    r'\1<span style="color: #BBBB00;">\2</span>', 
                    text)
        text = re.sub(r'(Files with match: )(\d+)', 
                    r'\1<span style="color: #BBBB00;">\2</span>', 
                    text)
        
        # Format the dashed lines
        text = re.sub(r'(-{40,})', 
                    r'<hr style="border: none; border-top: 1px dashed #666; margin: 5px 0;">', 
                    text)
        
        # Ensure all spans are closed
        if text.count('<span') > text.count('</span>'):
            text += '</span>' * (text.count('<span') - text.count('</span>'))
        
        # Convert newlines to HTML line breaks with proper spacing
        # First split the text into lines
        lines = text.split('\n')
        
        # Create a proper HTML structure with monospace font and pre-formatted text
        html = '<pre style="margin: 0; font-family: monospace; white-space: pre;">'
        
        # Process each line individually
        for line in lines:
            # Skip lines that have been converted to <hr> elements
            if '<hr' in line:
                html += line
                continue
            
            # Add each line with its content
            html += line + '\n'
        
        # Close the pre tag
        html += '</pre>'
        
        # Replace any double newlines
        html = html.replace('\n\n', '\n')
        
        return html

    def handle_stdout(self):
        """Handle standard output from the process"""
        # Read all available data
        data = self.process.readAllStandardOutput().data().decode()
        
        # Append to buffer
        self.stdout_buffer += data
        
        # Process and display the output
        formatted_data = self.process_ansi_output(self.stdout_buffer)
        
        # Update the display with formatted output
        self.results_text.clear()
        self.results_text.setHtml(formatted_data)
        
        # Scroll to the beginning
        self.results_text.moveCursor(QTextCursor.Start)
        
    def handle_stderr(self):
        """Handle standard error from the process"""
        # Read all available data
        data = self.process.readAllStandardError().data().decode()
        
        # Append to buffer
        self.stderr_buffer += data
        
        # Process and display the output (including both stdout and stderr)
        combined_output = self.stdout_buffer + self.stderr_buffer
        formatted_data = self.process_ansi_output(combined_output)
        
        # Update the display with formatted output
        self.results_text.clear()
        self.results_text.setHtml(formatted_data)
        
        # Scroll to the beginning
        self.results_text.moveCursor(QTextCursor.Start)
        
    def process_finished(self, exit_code, exit_status):
        """Handle process completion"""
        if exit_code == 0:
            self.status_bar.showMessage("Search completed successfully")
        else:
            self.status_bar.showMessage(f"Search failed with exit code {exit_code}")
            
        # Final formatting pass to ensure everything is displayed properly
        formatted_data = self.process_ansi_output(self.stdout_buffer + self.stderr_buffer)
        self.results_text.clear()
        self.results_text.setHtml(formatted_data)
        
        # Scroll to the beginning to show the search parameters
        self.results_text.moveCursor(QTextCursor.Start)
            
    def clear_search(self):
        self.model_combo.setCurrentIndex(0)  # Reset to "All Models"
        self.section_input.clear()
        self.query_input.clear()
        self.results_text.clear()
        self.status_bar.showMessage("Ready")
        
    def update_history(self):
        self.history_text.clear()
        for i, search in enumerate(reversed(self.search_history), 1):
            self.history_text.append(f"Search #{i}\n{search}\n")
            
    def clear_history(self):
        self.search_history = []
        self.history_text.clear()

def apply_dark_style(app):
    app.setStyle("Fusion")
    
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.WindowText, Qt.white)
    dark_palette.setColor(QPalette.Base, QColor(35, 35, 35))
    dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ToolTipBase, QColor(25, 25, 25))
    dark_palette.setColor(QPalette.ToolTipText, Qt.white)
    dark_palette.setColor(QPalette.Text, Qt.white)
    dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ButtonText, Qt.white)
    dark_palette.setColor(QPalette.BrightText, Qt.red)
    dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.HighlightedText, QColor(35, 35, 35))
    dark_palette.setColor(QPalette.Active, QPalette.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.Disabled, QPalette.ButtonText, Qt.darkGray)
    dark_palette.setColor(QPalette.Disabled, QPalette.WindowText, Qt.darkGray)
    dark_palette.setColor(QPalette.Disabled, QPalette.Text, Qt.darkGray)
    dark_palette.setColor(QPalette.Disabled, QPalette.Light, QColor(53, 53, 53))
    
    app.setPalette(dark_palette)

def main():
    app = QApplication(sys.argv)
    
    # Apply dark theme
    apply_dark_style(app)
    
    window = ConfigSearchApp()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

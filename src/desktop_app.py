"""
Desktop Application Launcher for Voice Cloner
PyQt6-based GUI with professional branding
"""
import sys
import os
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QProgressBar, QComboBox, QSpinBox, QDoubleSpinBox,
    QTabWidget, QTextEdit, QFileDialog, QMessageBox, QStatusBar, QMenuBar,
    QMenu, QListWidget, QListWidgetItem, QStackedWidget
)
from PyQt6.QtGui import QIcon, QPixmap, QFont, QColor
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QSize
from src.orchestrator import VoiceClonerOrchestrator
from src.utils.logger import logger


class WorkerThread(QThread):
    """Worker thread for long-running operations"""
    progress = pyqtSignal(str)
    finished = pyqtSignal(bool)
    error = pyqtSignal(str)

    def __init__(self, task_name, *args, **kwargs):
        super().__init__()
        self.task_name = task_name
        self.args = args
        self.kwargs = kwargs
        self.orchestrator = VoiceClonerOrchestrator()

    def run(self):
        try:
            if self.task_name == "detect":
                success = self.orchestrator.run_phase_1_environment_detection()
            elif self.task_name == "setup":
                success = self.orchestrator.run_phase_2_environment_setup()
            elif self.task_name == "preprocess":
                success = self.orchestrator.run_phase_3_audio_preprocessing(self.args[0])
            elif self.task_name == "train":
                success = self.orchestrator.run_phase_4_model_training(
                    epochs=self.kwargs.get("epochs"),
                    batch_size=self.kwargs.get("batch_size"),
                    learning_rate=self.kwargs.get("learning_rate"),
                )
            elif self.task_name == "infer":
                success = self.orchestrator.run_phase_5_voice_inference(
                    self.args[0], self.args[1],
                    pitch_shift=self.kwargs.get("pitch_shift", 0),
                    f0_method=self.kwargs.get("f0_method", "crepe"),
                )
            else:
                success = False

            self.finished.emit(success)
        except Exception as e:
            self.error.emit(str(e))
            self.finished.emit(False)


class VoiceClonerDesktopApp(QMainWindow):
    """Main desktop application window"""

    def __init__(self):
        super().__init__()
        self.orchestrator = VoiceClonerOrchestrator()
        self.worker_thread = None
        self.init_ui()

    def init_ui(self):
        """Initialize user interface"""
        self.setWindowTitle("🎤 Voice Cloner Pro")
        self.setWindowIcon(self.load_logo())
        self.setGeometry(100, 100, 1000, 700)
        self.setStyleSheet(self.get_stylesheet())

        # Create menu bar
        self.create_menu_bar()

        # Create main widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # Create layout
        layout = QHBoxLayout()

        # Left sidebar with navigation
        self.create_sidebar(layout)

        # Right content area
        self.stacked_widget = QStackedWidget()
        self.create_pages()
        layout.addWidget(self.stacked_widget, 1)

        main_widget.setLayout(layout)

        # Status bar
        self.statusBar().showMessage("Ready")

    def create_menu_bar(self):
        """Create menu bar"""
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("File")
        file_menu.addAction("Exit", self.close)

        # Help menu
        help_menu = menubar.addMenu("Help")
        help_menu.addAction("About", self.show_about)
        help_menu.addAction("Documentation", self.open_documentation)

    def create_sidebar(self, layout):
        """Create left sidebar navigation"""
        sidebar_widget = QWidget()
        sidebar_layout = QVBoxLayout()
        sidebar_widget.setFixedWidth(200)
        sidebar_widget.setStyleSheet("background-color: #1e1e1e; border-right: 1px solid #3e3e3e;")

        # Logo
        logo_label = QLabel()
        logo_pixmap = self.load_logo().pixmap(QSize(150, 150))
        logo_label.setPixmap(logo_pixmap)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sidebar_layout.addWidget(logo_label)

        # Navigation buttons
        self.nav_buttons = {}
        pages = [
            ("🏠 Home", "home"),
            ("🔧 Setup", "setup"),
            ("🎵 Preprocess", "preprocess"),
            ("🧠 Train", "train"),
            ("🎙️ Infer", "infer"),
            ("⚙️ Settings", "settings"),
        ]

        for label, page_id in pages:
            btn = QPushButton(label)
            btn.setStyleSheet(self.get_button_style())
            btn.clicked.connect(lambda checked, p=page_id: self.show_page(p))
            self.nav_buttons[page_id] = btn
            sidebar_layout.addWidget(btn)

        sidebar_layout.addStretch()

        # Status indicator
        status_label = QLabel("Status: Ready")
        status_label.setStyleSheet("color: #00ff00; font-weight: bold;")
        sidebar_layout.addWidget(status_label)

        sidebar_widget.setLayout(sidebar_layout)
        layout.addWidget(sidebar_widget)

    def create_pages(self):
        """Create content pages"""
        # Home page
        self.stacked_widget.addWidget(self.create_home_page())

        # Setup page
        self.stacked_widget.addWidget(self.create_setup_page())

        # Preprocess page
        self.stacked_widget.addWidget(self.create_preprocess_page())

        # Train page
        self.stacked_widget.addWidget(self.create_train_page())

        # Infer page
        self.stacked_widget.addWidget(self.create_infer_page())

        # Settings page
        self.stacked_widget.addWidget(self.create_settings_page())

    def create_home_page(self):
        """Create home page"""
        widget = QWidget()
        layout = QVBoxLayout()

        title = QLabel("🎤 Voice Cloner Pro")
        title.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        layout.addWidget(title)

        description = QLabel(
            "Welcome to Voice Cloner Pro!\n\n"
            "Clone your voice and create AI-powered vocal tracks for music production.\n\n"
            "Quick Start:\n"
            "1. Setup your environment\n"
            "2. Preprocess your vocal recordings\n"
            "3. Train your custom voice model\n"
            "4. Convert any singing input to your voice\n\n"
            "Ready to begin? Click 'Setup' in the sidebar!"
        )
        description.setStyleSheet("font-size: 14px; line-height: 1.5;")
        layout.addWidget(description)

        # Quick actions
        quick_start_btn = QPushButton("🚀 Quick Start Setup")
        quick_start_btn.setStyleSheet(self.get_button_style(primary=True))
        quick_start_btn.clicked.connect(lambda: self.show_page("setup"))
        layout.addWidget(quick_start_btn)

        layout.addStretch()
        widget.setLayout(layout)
        return widget

    def create_setup_page(self):
        """Create setup page"""
        widget = QWidget()
        layout = QVBoxLayout()

        title = QLabel("🔧 Environment Setup")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        layout.addWidget(title)

        # Detection section
        layout.addWidget(QLabel("Step 1: Detect Environment"))
        detect_btn = QPushButton("🔍 Detect System")
        detect_btn.clicked.connect(self.run_detection)
        layout.addWidget(detect_btn)

        # Setup section
        layout.addWidget(QLabel("Step 2: Setup Environment"))
        setup_btn = QPushButton("⚙️ Install & Setup")
        setup_btn.clicked.connect(self.run_setup)
        layout.addWidget(setup_btn)

        # Progress
        self.setup_progress = QProgressBar()
        self.setup_progress.setVisible(False)
        layout.addWidget(self.setup_progress)

        # Log output
        self.setup_log = QTextEdit()
        self.setup_log.setReadOnly(True)
        layout.addWidget(self.setup_log)

        layout.addStretch()
        widget.setLayout(layout)
        return widget

    def create_preprocess_page(self):
        """Create preprocessing page"""
        widget = QWidget()
        layout = QVBoxLayout()

        title = QLabel("🎵 Audio Preprocessing")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        layout.addWidget(title)

        # Input directory selection
        layout.addWidget(QLabel("Select vocal recordings directory:"))
        dir_layout = QHBoxLayout()
        self.preprocess_dir_input = QLabel("No directory selected")
        dir_btn = QPushButton("📁 Browse")
        dir_btn.clicked.connect(self.select_preprocessing_dir)
        dir_layout.addWidget(self.preprocess_dir_input)
        dir_layout.addWidget(dir_btn)
        layout.addLayout(dir_layout)

        # Process button
        process_btn = QPushButton("🔄 Process Audio")
        process_btn.clicked.connect(self.run_preprocessing)
        layout.addWidget(process_btn)

        # Progress
        self.preprocess_progress = QProgressBar()
        self.preprocess_progress.setVisible(False)
        layout.addWidget(self.preprocess_progress)

        # Log
        self.preprocess_log = QTextEdit()
        self.preprocess_log.setReadOnly(True)
        layout.addWidget(self.preprocess_log)

        layout.addStretch()
        widget.setLayout(layout)
        return widget

    def create_train_page(self):
        """Create training page"""
        widget = QWidget()
        layout = QVBoxLayout()

        title = QLabel("🧠 Model Training")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        layout.addWidget(title)

        # Training parameters
        params_layout = QHBoxLayout()

        params_layout.addWidget(QLabel("Epochs:"))
        self.epochs_spinbox = QSpinBox()
        self.epochs_spinbox.setValue(100)
        self.epochs_spinbox.setRange(1, 1000)
        params_layout.addWidget(self.epochs_spinbox)

        params_layout.addWidget(QLabel("Batch Size:"))
        self.batch_size_spinbox = QSpinBox()
        self.batch_size_spinbox.setValue(16)
        self.batch_size_spinbox.setRange(1, 128)
        params_layout.addWidget(self.batch_size_spinbox)

        params_layout.addWidget(QLabel("Learning Rate:"))
        self.lr_spinbox = QDoubleSpinBox()
        self.lr_spinbox.setValue(0.0001)
        self.lr_spinbox.setDecimals(6)
        params_layout.addWidget(self.lr_spinbox)

        params_layout.addStretch()
        layout.addLayout(params_layout)

        # Train button
        train_btn = QPushButton("▶️ Start Training")
        train_btn.setStyleSheet(self.get_button_style(primary=True))
        train_btn.clicked.connect(self.run_training)
        layout.addWidget(train_btn)

        # Progress
        self.train_progress = QProgressBar()
        self.train_progress.setVisible(False)
        layout.addWidget(self.train_progress)

        # Log
        self.train_log = QTextEdit()
        self.train_log.setReadOnly(True)
        layout.addWidget(self.train_log)

        layout.addStretch()
        widget.setLayout(layout)
        return widget

    def create_infer_page(self):
        """Create inference page"""
        widget = QWidget()
        layout = QVBoxLayout()

        title = QLabel("🎙️ Voice Conversion")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        layout.addWidget(title)

        # Input file selection
        layout.addWidget(QLabel("Input vocal file:"))
        input_layout = QHBoxLayout()
        self.infer_input = QLabel("No file selected")
        input_btn = QPushButton("📁 Browse")
        input_btn.clicked.connect(self.select_infer_input)
        input_layout.addWidget(self.infer_input)
        input_layout.addWidget(input_btn)
        layout.addLayout(input_layout)

        # Output file
        layout.addWidget(QLabel("Output file:"))
        output_layout = QHBoxLayout()
        self.infer_output = QLabel("No file selected")
        output_btn = QPushButton("📁 Browse")
        output_btn.clicked.connect(self.select_infer_output)
        output_layout.addWidget(self.infer_output)
        output_layout.addWidget(output_btn)
        layout.addLayout(output_layout)

        # Conversion parameters
        params_layout = QHBoxLayout()
        params_layout.addWidget(QLabel("Pitch Shift:"))
        self.pitch_shift_spinbox = QSpinBox()
        self.pitch_shift_spinbox.setValue(0)
        self.pitch_shift_spinbox.setRange(-12, 12)
        params_layout.addWidget(self.pitch_shift_spinbox)

        params_layout.addWidget(QLabel("F0 Method:"))
        self.f0_method_combo = QComboBox()
        self.f0_method_combo.addItems(["crepe", "dio", "harvest"])
        params_layout.addWidget(self.f0_method_combo)

        params_layout.addStretch()
        layout.addLayout(params_layout)

        # Convert button
        convert_btn = QPushButton("🎵 Convert Voice")
        convert_btn.setStyleSheet(self.get_button_style(primary=True))
        convert_btn.clicked.connect(self.run_inference)
        layout.addWidget(convert_btn)

        # Progress
        self.infer_progress = QProgressBar()
        self.infer_progress.setVisible(False)
        layout.addWidget(self.infer_progress)

        # Log
        self.infer_log = QTextEdit()
        self.infer_log.setReadOnly(True)
        layout.addWidget(self.infer_log)

        layout.addStretch()
        widget.setLayout(layout)
        return widget

    def create_settings_page(self):
        """Create settings page"""
        widget = QWidget()
        layout = QVBoxLayout()

        title = QLabel("⚙️ Settings")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        layout.addWidget(title)

        # Application info
        info_text = QTextEdit()
        info_text.setReadOnly(True)
        info_text.setText(
            "Voice Cloner Pro v0.1.0\n\n"
            "System Information:\n"
            f"- Python: 3.8-3.10\n"
            f"- Platform: Windows/Linux/macOS\n"
            f"- GPU Support: NVIDIA CUDA\n\n"
            "Documentation:\n"
            "- README.md - Project overview\n"
            "- SETUP_GUIDE.md - Installation help\n"
            "- USER_GUIDE.md - Usage guide\n"
            "- FL_STUDIO_GUIDE.md - FL Studio integration\n\n"
            "License: MIT\n"
            "Status: Production Ready"
        )
        layout.addWidget(info_text)

        # Buttons
        btn_layout = QHBoxLayout()
        doc_btn = QPushButton("📚 Open Documentation")
        doc_btn.clicked.connect(self.open_documentation)
        btn_layout.addWidget(doc_btn)

        about_btn = QPushButton("ℹ️ About")
        about_btn.clicked.connect(self.show_about)
        btn_layout.addWidget(about_btn)

        btn_layout.addStretch()
        layout.addLayout(btn_layout)

        layout.addStretch()
        widget.setLayout(layout)
        return widget

    # Helper methods
    def load_logo(self):
        """Load application logo"""
        # Create a placeholder icon if logo file doesn't exist
        return QIcon()

    def get_stylesheet(self):
        """Get application stylesheet"""
        return """
            QMainWindow {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            QLabel {
                color: #ffffff;
            }
            QPushButton {
                background-color: #0d47a1;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1565c0;
            }
            QPushButton:pressed {
                background-color: #0d3d91;
            }
            QTextEdit {
                background-color: #1e1e1e;
                color: #00ff00;
                border: 1px solid #3e3e3e;
                font-family: Courier;
            }
            QProgressBar {
                border: 1px solid #3e3e3e;
                border-radius: 4px;
                text-align: center;
                background-color: #1e1e1e;
            }
            QProgressBar::chunk {
                background-color: #00ff00;
            }
            QComboBox, QSpinBox, QDoubleSpinBox {
                background-color: #1e1e1e;
                color: #ffffff;
                border: 1px solid #3e3e3e;
                padding: 4px;
            }
        """

    def get_button_style(self, primary=False):
        """Get button style"""
        if primary:
            return """
                QPushButton {
                    background-color: #00cc00;
                    color: black;
                    border: none;
                    padding: 10px;
                    border-radius: 4px;
                    font-weight: bold;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background-color: #00ff00;
                }
                QPushButton:pressed {
                    background-color: #00aa00;
                }
            """
        return """
            QPushButton {
                background-color: #0d47a1;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1565c0;
            }
        """

    def show_page(self, page_id):
        """Show page by ID"""
        page_map = {"home": 0, "setup": 1, "preprocess": 2, "train": 3, "infer": 4, "settings": 5}
        self.stacked_widget.setCurrentIndex(page_map.get(page_id, 0))

    def run_detection(self):
        """Run environment detection"""
        self.setup_log.append("🔍 Starting environment detection...\n")
        self.setup_progress.setVisible(True)
        self.setup_progress.setValue(50)

        success = self.orchestrator.run_phase_1_environment_detection()

        if success:
            self.setup_log.append("\n✅ Environment detection passed!")
        else:
            self.setup_log.append("\n❌ Environment detection failed!")

        self.setup_progress.setValue(100)

    def run_setup(self):
        """Run environment setup"""
        self.setup_log.append("⚙️ Starting environment setup...\nThis may take 10-20 minutes...\n")
        self.setup_progress.setVisible(True)
        self.setup_progress.setValue(0)

        success = self.orchestrator.run_phase_2_environment_setup()

        if success:
            self.setup_log.append("\n✅ Environment setup completed!")
            self.setup_progress.setValue(100)
        else:
            self.setup_log.append("\n❌ Environment setup failed!")

    def select_preprocessing_dir(self):
        """Select preprocessing directory"""
        dir_path = QFileDialog.getExistingDirectory(self, "Select vocal recordings directory")
        if dir_path:
            self.preprocess_dir_input.setText(dir_path)

    def run_preprocessing(self):
        """Run audio preprocessing"""
        dir_path = self.preprocess_dir_input.text()
        if dir_path == "No directory selected":
            QMessageBox.warning(self, "Error", "Please select a directory first")
            return

        self.preprocess_log.append("🎵 Starting audio preprocessing...\n")
        self.preprocess_progress.setVisible(True)
        self.preprocess_progress.setValue(50)

        success = self.orchestrator.run_phase_3_audio_preprocessing(dir_path)

        if success:
            self.preprocess_log.append("\n✅ Preprocessing completed!")
            self.preprocess_progress.setValue(100)
        else:
            self.preprocess_log.append("\n❌ Preprocessing failed!")

    def run_training(self):
        """Run model training"""
        self.train_log.append("🧠 Starting model training...\n")
        self.train_progress.setVisible(True)
        self.train_progress.setValue(10)

        success = self.orchestrator.run_phase_4_model_training(
            epochs=self.epochs_spinbox.value(),
            batch_size=self.batch_size_spinbox.value(),
            learning_rate=self.lr_spinbox.value(),
        )

        if success:
            self.train_log.append("\n✅ Training started! Monitor progress in terminal.")
            self.train_progress.setValue(100)
        else:
            self.train_log.append("\n❌ Training failed!")

    def select_infer_input(self):
        """Select inference input file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select input vocal file", filter="Audio Files (*.wav *.mp3 *.flac)"
        )
        if file_path:
            self.infer_input.setText(file_path)

    def select_infer_output(self):
        """Select inference output file"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Select output file", filter="WAV Files (*.wav)"
        )
        if file_path:
            self.infer_output.setText(file_path)

    def run_inference(self):
        """Run voice inference"""
        input_file = self.infer_input.text()
        output_file = self.infer_output.text()

        if input_file == "No file selected" or output_file == "No file selected":
            QMessageBox.warning(self, "Error", "Please select both input and output files")
            return

        self.infer_log.append("🎙️ Starting voice conversion...\n")
        self.infer_progress.setVisible(True)
        self.infer_progress.setValue(50)

        success = self.orchestrator.run_phase_5_voice_inference(
            input_file,
            output_file,
            pitch_shift=self.pitch_shift_spinbox.value(),
            f0_method=self.f0_method_combo.currentText(),
        )

        if success:
            self.infer_log.append(f"\n✅ Conversion completed!")
            self.infer_log.append(f"Output saved to: {output_file}")
            self.infer_progress.setValue(100)
        else:
            self.infer_log.append("\n❌ Conversion failed!")

    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(
            self,
            "About Voice Cloner Pro",
            "Voice Cloner Pro v0.1.0\n\n"
            "AI-powered voice cloning for music production\n"
            "Using SO-VITS-SVC technology\n\n"
            "© 2025 Voice Cloner\n"
            "MIT License"
        )

    def open_documentation(self):
        """Open documentation"""
        doc_path = Path(__file__).parent.parent / "README.md"
        os.startfile(str(doc_path)) if sys.platform == "win32" else os.system(f"open {doc_path}")


def main():
    """Main entry point"""
    app = QApplication(sys.argv)
    window = VoiceClonerDesktopApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

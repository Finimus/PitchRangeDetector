"""
Pitch Range Detector - Analiză gamă vocală / instrument offline
Application for detecting and analyzing pitch range from audio files
"""

import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QFileDialog, 
                             QGroupBox, QMessageBox, QProgressBar)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QPalette, QColor
from audio_analyzer import AudioAnalyzer


class AnalysisThread(QThread):
    """Background thread for audio analysis to keep UI responsive"""
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)
    
    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path
        
    def run(self):
        try:
            analyzer = AudioAnalyzer()
            results = analyzer.analyze_audio(self.file_path)
            self.finished.emit(results)
        except Exception as e:
            self.error.emit(str(e))


class PitchRangeDetectorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.audio_file_path = None
        self.analysis_thread = None
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Pitch Range Detector - Analiză Gamă Vocală")
        self.setGeometry(100, 100, 700, 600)
        self.setMinimumSize(650, 550)
        
        # Set modern color scheme
        self.set_dark_theme()
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title_label = QLabel("🎵 Pitch Range Detector")
        title_font = QFont("Segoe UI", 20, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Subtitle
        subtitle_label = QLabel("Analiză gamă vocală și instrument - Offline")
        subtitle_font = QFont("Segoe UI", 10)
        subtitle_label.setFont(subtitle_font)
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet("color: #888888;")
        main_layout.addWidget(subtitle_label)
        
        main_layout.addSpacing(10)
        
        # File selection section
        file_group = QGroupBox("Fișier Audio")
        file_group.setFont(QFont("Segoe UI", 11, QFont.Bold))
        file_layout = QVBoxLayout()
        
        # File info label
        self.file_label = QLabel("Niciun fișier selectat")
        self.file_label.setFont(QFont("Segoe UI", 10))
        self.file_label.setWordWrap(True)
        self.file_label.setStyleSheet("padding: 10px; background-color: #2d2d2d; border-radius: 5px;")
        file_layout.addWidget(self.file_label)
        
        # Open file button
        self.open_button = QPushButton("📂 Deschide Fișier Audio")
        self.open_button.setFont(QFont("Segoe UI", 11))
        self.open_button.setMinimumHeight(45)
        self.open_button.setStyleSheet("""
            QPushButton {
                background-color: #0078d4;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #1084d8;
            }
            QPushButton:pressed {
                background-color: #006cbe;
            }
        """)
        self.open_button.clicked.connect(self.open_file)
        file_layout.addWidget(self.open_button)
        
        file_group.setLayout(file_layout)
        main_layout.addWidget(file_group)
        
        # Analyze button
        self.analyze_button = QPushButton("🔍 Analizează")
        self.analyze_button.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.analyze_button.setMinimumHeight(50)
        self.analyze_button.setEnabled(False)
        self.analyze_button.setStyleSheet("""
            QPushButton {
                background-color: #107c10;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover:enabled {
                background-color: #128a12;
            }
            QPushButton:pressed:enabled {
                background-color: #0e6e0e;
            }
            QPushButton:disabled {
                background-color: #3d3d3d;
                color: #666666;
            }
        """)
        self.analyze_button.clicked.connect(self.analyze_audio)
        main_layout.addWidget(self.analyze_button)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setMinimumHeight(8)
        self.progress_bar.setMaximum(0)  # Indeterminate progress
        main_layout.addWidget(self.progress_bar)
        
        # Results section
        results_group = QGroupBox("Rezultate Analiză")
        results_group.setFont(QFont("Segoe UI", 11, QFont.Bold))
        results_layout = QVBoxLayout()
        results_layout.setSpacing(10)
        
        # Result labels
        self.min_freq_label = self.create_result_label("Frecvența minimă: —")
        self.max_freq_label = self.create_result_label("Frecvența maximă: —")
        self.median_freq_label = self.create_result_label("Frecvența mediană: —")
        self.note_range_label = self.create_result_label("Gama în note: —")
        self.confidence_label = self.create_result_label("Nivel de încredere: —")
        
        results_layout.addWidget(self.min_freq_label)
        results_layout.addWidget(self.max_freq_label)
        results_layout.addWidget(self.median_freq_label)
        results_layout.addWidget(self.note_range_label)
        results_layout.addWidget(self.confidence_label)
        
        results_group.setLayout(results_layout)
        main_layout.addWidget(results_group)
        
        main_layout.addStretch()
        
        # About button
        self.about_button = QPushButton("ℹ️ Despre")
        self.about_button.setFont(QFont("Segoe UI", 10))
        self.about_button.setMinimumHeight(35)
        self.about_button.setStyleSheet("""
            QPushButton {
                background-color: #2d2d2d;
                color: white;
                border: 1px solid #3d3d3d;
                border-radius: 5px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #3d3d3d;
            }
            QPushButton:pressed {
                background-color: #252525;
            }
        """)
        self.about_button.clicked.connect(self.show_about)
        main_layout.addWidget(self.about_button)

        # Footer
        footer_label = QLabel("© 2025 – Finimus | Pitch Range Detector 🎶")
        footer_label.setFont(QFont("Segoe UI", 8))
        footer_label.setAlignment(Qt.AlignCenter)
        footer_label.setStyleSheet("color: #666666;")
        main_layout.addWidget(footer_label)
        
        central_widget.setLayout(main_layout)
        
    def set_dark_theme(self):
        """Apply dark theme to the application"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
            }
            QWidget {
                background-color: #1e1e1e;
                color: #ffffff;
            }
            QGroupBox {
                border: 2px solid #3d3d3d;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 5px 10px;
                color: #ffffff;
            }
            QProgressBar {
                border: none;
                border-radius: 4px;
                background-color: #2d2d2d;
            }
            QProgressBar::chunk {
                background-color: #0078d4;
                border-radius: 4px;
            }
        """)
        
    def create_result_label(self, text):
        """Create a styled label for results"""
        label = QLabel(text)
        label.setFont(QFont("Segoe UI", 11))
        label.setStyleSheet("""
            padding: 12px;
            background-color: #252525;
            border-radius: 5px;
            border-left: 4px solid #0078d4;
        """)
        return label
        
    def open_file(self):
        """Open file dialog to select audio file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Selectează Fișier Audio",
            "",
            "Audio Files (*.wav *.mp3 *.ogg *.flac);;All Files (*.*)"
        )
        
        if file_path:
            self.audio_file_path = file_path
            file_name = os.path.basename(file_path)
            self.file_label.setText(f"📄 {file_name}\n{file_path}")
            self.analyze_button.setEnabled(True)
            self.clear_results()
            
    def analyze_audio(self):
        """Start audio analysis in background thread"""
        if not self.audio_file_path:
            return
            
        # Disable controls during analysis
        self.analyze_button.setEnabled(False)
        self.open_button.setEnabled(False)
        self.progress_bar.setVisible(True)
        
        # Start analysis thread
        self.analysis_thread = AnalysisThread(self.audio_file_path)
        self.analysis_thread.finished.connect(self.on_analysis_finished)
        self.analysis_thread.error.connect(self.on_analysis_error)
        self.analysis_thread.start()
        
    def on_analysis_finished(self, results):
        """Handle analysis completion"""
        # Re-enable controls
        self.analyze_button.setEnabled(True)
        self.open_button.setEnabled(True)
        self.progress_bar.setVisible(False)
        
        # Display results
        self.min_freq_label.setText(
            f"Frecvența minimă: {results['min_freq']:.2f} Hz — {results['min_note']}"
        )
        self.max_freq_label.setText(
            f"Frecvența maximă: {results['max_freq']:.2f} Hz — {results['max_note']}"
        )
        self.median_freq_label.setText(
            f"Frecvența mediană: {results['median_freq']:.2f} Hz — {results['median_note']}"
        )
        self.note_range_label.setText(
            f"Gama în note: {results['min_note']} — {results['max_note']}"
        )
        self.confidence_label.setText(
            f"Nivel de încredere: {results['confidence']:.1f}%"
        )
        
    def on_analysis_error(self, error_message):
        """Handle analysis errors"""
        self.analyze_button.setEnabled(True)
        self.open_button.setEnabled(True)
        self.progress_bar.setVisible(False)
        
        QMessageBox.critical(
            self,
            "Eroare la Analiză",
            f"A apărut o eroare la procesarea fișierului:\n\n{error_message}"
        )
        
    def clear_results(self):
        """Clear all result labels"""
        self.min_freq_label.setText("Frecvența minimă: —")
        self.max_freq_label.setText("Frecvența maximă: —")
        self.median_freq_label.setText("Frecvența mediană: —")
        self.note_range_label.setText("Gama în note: —")
        self.confidence_label.setText("Nivel de încredere: —")

    def show_about(self):
        """Show About dialog with application information"""
        about_text = """
<div style='text-align: center;'>
<h2>Pitch Range Detector 🎶</h2>
<p style='font-size: 11pt;'><b>Versiune: 1.0</b></p>
</div>

<p style='font-size: 10pt;'>
<b>Descoperă cu precizie gama ta vocală sau instrumentală!</b><br><br>
Încarcă un fișier audio, apasă „Analizează” și vizualizează notele extreme,
frecvențele și intervalul muzical.
</p>

<p style='font-size: 10pt;'>
Aplicația funcționează complet <b>offline</b> și este creată special pentru
cântăreți, profesori de muzică și ingineri de sunet care doresc o analiză
rapidă și intuitivă.
</p>

<p style='font-size: 10pt;'>
Dezvoltată cu pasiune în Python ❤️
</p>

<hr>

<p style='font-size: 9pt;'>
<b>Funcționalitate:</b><br>
Tool offline pentru analiza de pitch și determinarea gamei vocale/instrumentale.
</p>

<p style='font-size: 9pt;'>
<b>Tehnologii utilizate:</b><br>
• Framework: PyQt5<br>
• Analiză audio: Librosa<br>
• Formate compatibile: WAV, MP3, FLAC, OGG
</p>

<hr>

<p style='font-size: 9pt; text-align: center;'>
<b>Open-source | Creat de Finimus</b><br>
🌐 <a href='https://github.com/Finimus'>github.com/Finimus</a>
</p>

<p style='font-size: 8pt; text-align: center; color: #888888;'>
© 2025 – Finimus
</p>
        """

        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Despre Pitch Range Detector")
        msg_box.setTextFormat(Qt.RichText)
        msg_box.setText(about_text)
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Modern look on all platforms
    
    window = PitchRangeDetectorApp()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

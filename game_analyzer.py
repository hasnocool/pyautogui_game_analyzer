import sys
import pyautogui
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QColor, QPixmap, QImage
import mss

class GameAnalyzer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyAutoGUI Game Analyzer")
        self.setGeometry(100, 100, 400, 300)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Create labels for displaying information
        self.mouse_pos_label = QLabel("Mouse Position: ")
        self.rgb_label = QLabel("RGB Value: ")
        self.hex_label = QLabel("Hex Value: ")
        self.resolution_label = QLabel("Screen Resolution: ")
        self.color_preview = QLabel()
        self.color_preview.setFixedSize(50, 50)
        self.screenshot_preview = QLabel()
        self.screenshot_preview.setFixedSize(200, 200)

        # Create buttons
        self.start_button = QPushButton("Start")
        self.stop_button = QPushButton("Stop")
        self.screenshot_button = QPushButton("Take Screenshot")

        # Add widgets to layout
        layout.addWidget(self.mouse_pos_label)
        layout.addWidget(self.rgb_label)
        layout.addWidget(self.hex_label)
        layout.addWidget(self.resolution_label)
        layout.addWidget(self.color_preview)
        layout.addWidget(self.screenshot_preview)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        button_layout.addWidget(self.screenshot_button)
        layout.addLayout(button_layout)

        # Connect buttons to functions
        self.start_button.clicked.connect(self.start_analysis)
        self.stop_button.clicked.connect(self.stop_analysis)
        self.screenshot_button.clicked.connect(self.take_screenshot)

        # Set up timer for updating information
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_info)

        # Initialize mss for faster screenshots
        self.sct = mss.mss()

        # Display initial screen resolution
        screen_size = pyautogui.size()
        self.resolution_label.setText(f"Screen Resolution: {screen_size.width}x{screen_size.height}")

    def start_analysis(self):
        self.timer.start(100)  # Update every 100 ms
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)

    def stop_analysis(self):
        self.timer.stop()
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)

    def update_info(self):
        # Get mouse position
        x, y = pyautogui.position()
        self.mouse_pos_label.setText(f"Mouse Position: ({x}, {y})")

        # Get pixel color at mouse position
        pixel_color = pyautogui.pixel(x, y)
        r, g, b = pixel_color
        self.rgb_label.setText(f"RGB Value: ({r}, {g}, {b})")

        # Convert RGB to Hex
        hex_color = '#{:02x}{:02x}{:02x}'.format(r, g, b)
        self.hex_label.setText(f"Hex Value: {hex_color}")

        # Update color preview
        self.color_preview.setStyleSheet(f"background-color: {hex_color};")

        # Update screenshot preview
        self.update_screenshot_preview(x, y)

    def update_screenshot_preview(self, x, y):
        # Capture a small area around the mouse cursor
        width, height = 100, 100
        left = max(x - width // 2, 0)
        top = max(y - height // 2, 0)
        screenshot = self.sct.grab({"left": left, "top": top, "width": width, "height": height})

        # Convert to QImage and display
        image = QImage(screenshot.rgb, screenshot.width, screenshot.height, QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(image)
        self.screenshot_preview.setPixmap(pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio))

    def take_screenshot(self):
        screenshot = pyautogui.screenshot()
        screenshot.save("game_screenshot.png")
        self.screenshot_preview.setPixmap(QPixmap("game_screenshot.png").scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GameAnalyzer()
    window.show()
    sys.exit(app.exec())

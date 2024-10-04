from PySide6 import QtCore, QtWidgets, QtGui
from pathlib import Path
import sys, os

class QT_IMGVWR(QtWidgets.QMainWindow):
    
    def __init__(self) -> None:
        super().__init__()

        # app window
        self.setWindowTitle("QT_IMGVWR")
        self.setGeometry(100, 100, 800, 800)

        # central widget
        self.central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QtWidgets.QVBoxLayout(self.central_widget)

        self.image_label = QtWidgets.QLabel("No image loaded")
        self.image_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.image_label)

        # image vars
        self.images = []
        self.folder_path = None
        self.image_index = 0
        self.init_image_data()

        # window options
        self.fill_window: bool = False
        self.full_screen: bool = True

    def init_image_data(self, folder_path: Path | None) -> None:
        self.folder_path = folder_path
        self.image_index = 0
        self.images.clear()
        if self.folder_path:
            self.images = [
                f for f in os.listdir(self.folder_path)
                if f.lower().endswith(('.png', '.gif', '.jpeg', '.jpg'))
                ]
            # if self.images

    def toggle_fill_window(self) -> None:
        self.fill_window = not self.fill_window

    def toggle_full_screen(self) -> None:
        self.full_screen = not self.full_screen

    def load_image(self, image_path: Path) -> None:
        image_path_str = str(image_path)
        pixmap = QtGui.QPixmap(image_path_str)
        if pixmap.isNull():
            print(f"Failed to load image {image_path}")
            self.image_label.setText("Failed to load image")
        else:
            self.image_label.setPixmap(pixmap)
            self.image_label.setScaledContents(True)

    def get_current_image_path(self) -> Path:
        return Path(self.folder_path) / self.images[self.image_index]

    def prev_image(self) -> None:
        if self.images:
            self.image_index = (self.image_index - 1) % len(self.images)
            self.load_image(self.get_current_image_path())

    def next_image(self) -> None:
        if self.images:
            self.image_index = (self.image_index + 1) % len(self.images)
            self.load_image(self.get_current_image_path())

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        if event.key() == QtCore.Qt.Key.Key_Left:
            self.prev_image()
        elif event.key() == QtCore.Qt.Key.Key_Right:
            self.next_image()

    def open(self) -> Path:
        pass

app = QtWidgets.QApplication(sys.argv)
window = QT_IMGVWR()
window.show()

test_image_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/data/1281384394853.jpg"
window.load_image(test_image_path)

sys.exit(app.exec())
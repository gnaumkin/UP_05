import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMessageBox
from PyQt5.QtCore import Qt, QTimer, QRect
from PyQt5.QtGui import QPixmap, QImage
from PIL import Image

def load_icon(image_path, size=40):
    image = Image.open(image_path).resize((size, size))
    return image

class DinosaurGame(QWidget):
    def __init__(self):
        super().__init__()

        self.setGeometry(100, 100, 800, 300)
        self.setWindowTitle('Dinosaur Game')

        self.dino_label = QLabel(self)
        dino_icon = load_icon(r'C:\UP05\UP_05\dino_icon.png')
        self.dino_label.setPixmap(self.image_to_pixmap(dino_icon))

        self.ground_label = QLabel(self)
        ground_icon = load_icon(r'C:\UP05\UP_05\ground_icon.png')
        self.ground_label.setPixmap(self.image_to_pixmap(ground_icon))

        self.cactus_label = QLabel(self)
        cactus_icon = load_icon(r'C:\UP05\UP_05\cactus_icon.png')
        self.cactus_label.setPixmap(self.image_to_pixmap(cactus_icon))

        self.pterodactyl_label = QLabel(self)
        pterodactyl_icon = load_icon(r'C:\UP05\UP_05\pterodactyl_icon.png')
        self.pterodactyl_label.setPixmap(self.image_to_pixmap(pterodactyl_icon))

        self.dino_label.setGeometry(50, 200, 40, 40)
        self.ground_label.setGeometry(0, 240, 800, 60)
        self.cactus_label.setGeometry(800, 200, 40, 40)
        self.pterodactyl_label.setGeometry(300, 100, 50, 50)

        self.dino_jump = False
        self.jump_height = 120
        self.jump_step = 10
        self.dino_speed = 5
        self.speed_increase_interval = 1000
        self.speed_increase_factor = 0.1

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_game)
        self.timer.start(20)

        self.speed_increase_timer = QTimer(self)
        self.speed_increase_timer.timeout.connect(self.increase_speed)
        self.speed_increase_timer.start(self.speed_increase_interval)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.move_pterodactyl)
        self.timer.start(50)

        self.score = 0
        self.score_label = QLabel('Score: 0', self)
        self.score_label.setGeometry(10, 10, 100, 30)

        self.show()

    def increase_speed(self):
        self.dino_speed += int(self.dino_speed * self.speed_increase_factor)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space and not self.dino_jump:
            self.dino_jump = True
        elif event.key() == Qt.Key_Control:
            self.duck()
    def check_collision(self):
        dino_rect = QRect(self.dino_label.x() + 5, self.dino_label.y() + 5, self.dino_label.width() - 10,
                          self.dino_label.height() - 10)
        cactus_rect = QRect(self.cactus_label.x() + 5, self.cactus_label.y() + 5, self.cactus_label.width() - 10,
                            self.cactus_label.height() - 10)

        if dino_rect.intersects(cactus_rect):
            self.timer.stop()
            QMessageBox.information(self, 'Game Over', 'You collided with the cactus! Game Over.')
            self.close()

    def update_game(self):
        dino_y = self.dino_label.y()

        if self.dino_jump:
            dino_y -= self.jump_step
            self.jump_step -= 1

            if dino_y >= 200:
                self.dino_jump = False
                dino_y = 200
                self.jump_step = 12

        cactus_x = self.cactus_label.x()
        cactus_x -= self.dino_speed

        if cactus_x < 0:
            cactus_x = 800
        self.increase_score()
        self.dino_label.move(50, dino_y)
        self.cactus_label.move(cactus_x, 200)

        self.check_collision()

    def image_to_pixmap(self, image):
        width, height = image.size
        image = image.convert("RGBA")
        byte_array = image.tobytes("raw", "RGBA")
        pixmap = QPixmap.fromImage(QImage(byte_array, width, height, QImage.Format_RGBA8888))
        return pixmap

    def increase_score(self):
      self.score += 1
      self.score_label.setText(f'Score: {self.score}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = DinosaurGame()
    sys.exit(app.exec_())
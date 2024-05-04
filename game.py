import sys

import self
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMessageBox
from PyQt5.QtCore import Qt, QTimer, QRect
from PyQt5.QtGui import QPixmap, QImage
from PIL import Image
import random
import os

def load_icon(image_path, size=40):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(script_dir, image_path)
    image = Image.open(image_path).resize((size, size))
    return image

class DinosaurGame(QWidget):
    def __init__(self):
        super().__init__()

        self.setGeometry(100, 100, 800, 300)
        self.setWindowTitle('Dinosaur Game')

        self.dino_label = QLabel(self)
        dino_icon = load_icon('dino_icon.png')
        self.dino_label.setPixmap(self.image_to_pixmap(dino_icon))

        self.ground_label = QLabel(self)
        ground_icon = load_icon(r'C:\UP05\UP_05\ground_icon.png')
        self.ground_label.setPixmap(self.image_to_pixmap(ground_icon))

        self.cactuses = []
        for _ in range(3):
            cactus_label = QLabel(self)
            cactus_icon = load_icon(r'C:\UP05\UP_05\cactus_icon.png')
        self.cactuses = []
        for _ in range(3):
            cactus_label = QLabel(self)
            cactus_icon = load_icon('cactus_icon.png')
            cactus_label.setPixmap(self.image_to_pixmap(cactus_icon))
            self.cactuses.append(cactus_label)

        self.pterodactyl_label = QLabel(self)
        pterodactyl_icon = load_icon('pterodactyl_icon.png')
        self.pterodactyl_label.setPixmap(self.image_to_pixmap(pterodactyl_icon))

        self.pterodactyl_label.setGeometry(800, 100, 50, 50)
        self.dino_label.setGeometry(50, 200, 40, 40)
        self.ground_label.setGeometry(0, 240, 800, 60)

        for i, cactus in enumerate(self.cactuses):
            cactus.setGeometry(800 + i * 300, 200, 40, 40)

        self.pterodactyl_label.setGeometry(800, 100, 50, 50)

        for i, cactus in enumerate(self.cactuses):
            cactus.setGeometry(800 + i * 300, 100, 40, 40)

        self.pterodactyl_label.setGeometry(500, 100, 40, 40)

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

        self.pterodactyl_timer = QTimer(self)  # Один QTimer для птеродактиля
        self.pterodactyl_timer.timeout.connect(self.move_pterodactyl)
        self.pterodactyl_timer.start(1000)  # Появление птеродактиля через 2 секунды после старта игры
        self.pterodactyl_timer = QTimer(self)
        self.pterodactyl_timer.timeout.connect(self.move_pterodactyl)
        self.pterodactyl_timer.start(1000)

        self.score = 1
        self.score_label = QLabel('Score: 0', self)
        self.score_label.setGeometry(10, 10, 100, 30)

        self.ground_x = 0

        # Тут 2 копии земли дабы она двигалась
        self.ground_label1 = QLabel(self)
        self.ground_label2 = QLabel(self)

        ground_icon = load_icon('ground_icon.png')
        window_width = 800
        num_ground_icons = window_width // ground_icon.size[0] + 1

        combined_ground_image = Image.new('RGBA', (window_width * 2, ground_icon.size[1]))
        for i in range(num_ground_icons * 2):
            combined_ground_image.paste(ground_icon, (i * ground_icon.size[0], 0))

        self.ground_label1.setPixmap(self.image_to_pixmap(combined_ground_image))
        self.ground_label2.setPixmap(self.image_to_pixmap(combined_ground_image))

        self.ground_label1.setGeometry(0, 240, window_width, 5)
        self.ground_label2.setGeometry(window_width, 240, window_width, 5)

        self.show()

    def increase_speed(self):
        self.dino_speed += int(self.dino_speed * self.speed_increase_factor)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space and not self.dino_jump:
            self.dino_jump = True
            self.jump_step = 12

    def check_collision(self):
        dino_rect = QRect(self.dino_label.x() + 5, self.dino_label.y() + 5, self.dino_label.width() - 10,
                          self.dino_label.height() - 10)

        for cactus in self.cactuses:
            cactus_rect = QRect(cactus.x() + 5, cactus.y() + 5, cactus.width() - 10, cactus.height() - 10)
            if dino_rect.intersects(cactus_rect):
                self.timer.stop()
                QMessageBox.information(self, 'Game Over', 'Тебя схавал дядюшка кактус!')
                self.close()

        pterodactyl_rect = QRect(self.pterodactyl_label.x() + 5, self.pterodactyl_label.y() + 5,
                                 self.pterodactyl_label.width() - 10, self.pterodactyl_label.height() - 10)
        if dino_rect.intersects(pterodactyl_rect):
            self.timer.stop()
            QMessageBox.information(self, 'Game Over', 'Тебя поцеловал птеродактиль!')
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

        for cactus in self.cactuses:
            cactus_x = cactus.x()
            cactus_x -= self.dino_speed

            if cactus_x < 0:
                cactus_x = 800 + random.randint(100, 300)
            cactus.move(cactus_x, 200)

        self.increase_score()
        self.dino_label.move(50, dino_y)


        self.move_pterodactyl()
        self.increase_score()
        self.dino_label.move(50, dino_y)
        self.move_ground()
        self.check_collision()

    def move_pterodactyl(self):
        current_x = self.pterodactyl_label.x()
        new_x = current_x - self.dino_speed
        if new_x < -self.pterodactyl_label.width():
            new_x = self.width()
            new_y = random.randint(50, 150)
            self.pterodactyl_label.move(new_x, new_y)
            if not hasattr(self, 'ptero_y'):
                self.ptero_y = random.randint(50, 150)
            new_y = self.ptero_y + 50
        else:
            new_y = self.pterodactyl_label.y()
        self.pterodactyl_label.move(new_x, new_y)
        self.check_collision_with_pterodactyl(new_x, new_y)

    def move_ground(self):
        # Обновляем позицию земельки
        self.ground_x -= self.dino_speed
        if self.ground_x <= -800:
            self.ground_x = 0
        self.ground_label1.move(self.ground_x, 240)
        self.ground_label2.move(self.ground_x + 800, 240)

    def check_collision_with_pterodactyl(self, ptero_x, ptero_y):
        dino_rect = QRect(self.dino_label.x(), self.dino_label.y(), self.dino_label.width(), self.dino_label.height())
        pterodactyl_rect = QRect(ptero_x, ptero_y, self.pterodactyl_label.width(), self.pterodactyl_label.height())
        if dino_rect.intersects(pterodactyl_rect):
            self.timer.stop()
            QMessageBox.information(self, 'Game Over', 'Тебя поцеловал птеродактиль!')
            self.close()

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
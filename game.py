import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QStackedWidget, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt, QTimer, QRect
from PyQt5.QtGui import QPixmap, QImage, QFont, QIcon
from PIL import Image
import random
import os

def load_icon(image_path, size=40):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(script_dir, image_path)
    image = Image.open(image_path).resize((size, size))
    return image

class MainMenu(QWidget):
    def __init__(self, start_game_callback):
        super().__init__()
        self.start_game_callback = start_game_callback

        layout = QVBoxLayout()
        self.setLayout(layout)

        title_label = QLabel('Dinosaur Game', self)
        title_font = QFont()
        title_font.setFamily("Unispace")
        title_font.setPointSize(24)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        layout.addSpacerItem(QSpacerItem(0, 30, QSizePolicy.Minimum, QSizePolicy.Expanding))

        start_button = QPushButton('Начать игру', self)
        start_button.setFont(QFont("Unispace", 18))
        start_button.setFixedSize(200, 50)
        start_button.clicked.connect(self.start_game)
        layout.addWidget(start_button, alignment=Qt.AlignCenter)

        layout.addSpacerItem(QSpacerItem(0, 30, QSizePolicy.Minimum, QSizePolicy.Expanding))

    def start_game(self):
        self.start_game_callback()

class GameOverMenu(QWidget):
    def __init__(self, main_menu_callback, score):
        super().__init__()
        self.main_menu_callback = main_menu_callback
        self.setWindowIcon(QIcon('ikonka.ico'))

        layout = QVBoxLayout()
        self.setLayout(layout)

        score_label = QLabel(f'Набрано очков: {score}', self)
        score_label.setFont(QFont("Unispace", 18))
        score_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(score_label)

        layout.addSpacerItem(QSpacerItem(0, 30, QSizePolicy.Minimum, QSizePolicy.Expanding))

        main_menu_button = QPushButton('Главное меню', self)
        main_menu_button.setFont(QFont("Arial", 18))
        main_menu_button.setFixedSize(200, 50)
        main_menu_button.clicked.connect(self.main_menu)
        main_menu_button.move(290, 150)
        layout.addWidget(main_menu_button, alignment=Qt.AlignCenter)

    def main_menu(self):
        self.main_menu_callback()

class DinosaurGame(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 800, 300)
        self.setFixedSize(800, 300)
        self.setWindowTitle('Dinosaur Game')
        self.setWindowIcon(QIcon('ikonka.ico'))

        self.stack = QStackedWidget(self)
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.stack)

        self.game_widget = QWidget()
        self.game_layout = QVBoxLayout(self.game_widget)
        self.stack.addWidget(self.game_widget)

        self.main_menu = MainMenu(self.start_game)
        self.stack.addWidget(self.main_menu)

        self.game_over_menu = None

        self.init_game_ui()

        self.stack.setCurrentWidget(self.main_menu)

    def init_game_ui(self):
        self.dino_label = QLabel(self.game_widget)
        self.dino_icon1 = load_icon('dinoicon1.png')
        self.dino_icon2 = load_icon('dinoicon2.png')
        self.dino_label.setPixmap(self.image_to_pixmap(self.dino_icon1))

        self.down_dino_icon = load_icon('dinodownicon.png')
        self.default_dino_icon = self.dino_icon1

        self.obstacles = []
        self.obstacle_min_distance = 300

        self.dino_label.setGeometry(50, 200, 40, 40)

        self.dino_jump = False
        self.dino_crouch = False
        self.jump_height = 120
        self.jump_step = 12
        self.dino_speed = 5
        self.max_dino_speed = self.dino_speed * 1.5

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_game)

        self.obstacle_spawn_timer = QTimer(self)
        self.obstacle_spawn_timer.timeout.connect(self.spawn_obstacle)

        self.score = 0
        self.score_label = QLabel('Очки: 0', self.game_widget)
        self.score_label.setGeometry(10, 10, 100, 30)

        font = QFont()
        font.setFamily("Unispace")
        font.setPointSize(13)
        font.setBold(True)
        self.score_label.setFont(font)

        self.ground_x = 0

        self.ground_label1 = QLabel(self.game_widget)
        self.ground_label2 = QLabel(self.game_widget)

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

        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(self.animate_dino)
        self.current_dino_icon = 1

    def start_game(self):
        self.reset_game()
        self.stack.setCurrentWidget(self.game_widget)
        self.timer.start(20)
        self.obstacle_spawn_timer.start(2000)
        self.animation_timer.start(200)

    def reset_game(self):
        self.score = 0
        self.dino_jump = False
        self.dino_crouch = False
        self.jump_step = 12
        self.dino_label.move(50, 200)
        self.dino_label.setPixmap(self.image_to_pixmap(self.default_dino_icon))

        for obstacle in self.obstacles:
            obstacle.hide()
        self.obstacles.clear()

        self.score_label.setText('Очки: 0')
        self.dino_speed = 5  # Reset speed

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space and not self.dino_jump and not self.dino_crouch:
            self.dino_jump = True
        elif event.key() == Qt.Key_Down:
            self.dino_crouch = True
            self.dino_label.setPixmap(self.image_to_pixmap(self.down_dino_icon))

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Down:
            self.dino_crouch = False
            self.dino_label.setPixmap(self.image_to_pixmap(self.default_dino_icon))

    def check_collision(self):
        dino_rect = QRect(self.dino_label.x() + 5, self.dino_label.y() + 5, self.dino_label.width() - 10,
                          self.dino_label.height() - 10)

        if self.dino_crouch:
            dino_rect = QRect(self.dino_label.x() + 10, self.dino_label.y() + 20, self.dino_label.width() - 20,
                              self.dino_label.height() - 20)

        for obstacle in self.obstacles:
            obstacle_rect = QRect(obstacle.x() + 5, obstacle.y() + 5, obstacle.width() - 10, obstacle.height() - 10)
            if dino_rect.intersects(obstacle_rect):
                self.timer.stop()
                self.obstacle_spawn_timer.stop()
                self.animation_timer.stop()
                self.show_game_over_menu()

    def show_game_over_menu(self):
        self.game_over_menu = GameOverMenu(self.show_main_menu, self.score)
        self.stack.addWidget(self.game_over_menu)
        self.stack.setCurrentWidget(self.game_over_menu)

    def update_game(self):
        dino_y = self.dino_label.y()

        if self.dino_jump:
            dino_y -= self.jump_step
            self.jump_step -= 1

            if dino_y >= 200:
                self.dino_jump = False
                dino_y = 200
                self.jump_step = 12

        for obstacle in self.obstacles:
            obstacle_x = obstacle.x()
            obstacle_x -= self.dino_speed

            if obstacle_x < -40:
                obstacle.hide()
                self.obstacles.remove(obstacle)
            else:
                obstacle.move(obstacle_x, obstacle.y())

        self.increase_score()
        self.dino_label.move(50, dino_y)
        self.move_ground()
        self.check_collision()

    def spawn_obstacle(self):
        if self.obstacles and 800 - self.obstacles[-1].x() < self.obstacle_min_distance:
            return

        if random.choice([True, False]):
            obstacle_label = QLabel(self.game_widget)
            obstacle_icon = load_icon('cactusicon.png')
            obstacle_label.setPixmap(self.image_to_pixmap(obstacle_icon))
            obstacle_label.setGeometry(800, 200, 40, 40)
        else:
            obstacle_label = QLabel(self.game_widget)
            obstacle_icon = load_icon('pteroicon.png')
            obstacle_label.setPixmap(self.image_to_pixmap(obstacle_icon))
            obstacle_label.setGeometry(800, 175, 40, 40)

        self.obstacles.append(obstacle_label)
        obstacle_label.show()

    def move_ground(self):
        self.ground_x -= self.dino_speed
        if self.ground_x <= -800:
            self.ground_x = 0
        self.ground_label1.move(self.ground_x, 240)
        self.ground_label2.move(self.ground_x + 800, 240)

    def image_to_pixmap(self, image):
        width, height = image.size
        image = image.convert("RGBA")
        byte_array = image.tobytes("raw", "RGBA")
        pixmap = QPixmap.fromImage(QImage(byte_array, width, height, QImage.Format_RGBA8888))
        return pixmap

    def increase_score(self):
        self.score += 1
        self.score_label.setText(f'Очки: {self.score}')

    def show_main_menu(self):
        self.stack.setCurrentWidget(self.main_menu)

    def restart_game(self):
        self.reset_game()
        self.stack.setCurrentWidget(self.game_widget)
        self.timer.start(20)
        self.obstacle_spawn_timer.start(2000)
        self.animation_timer.start(200)

    def animate_dino(self):
        if not self.dino_jump and not self.dino_crouch:
            if self.current_dino_icon == 1:
                self.dino_label.setPixmap(self.image_to_pixmap(self.dino_icon2))
                self.current_dino_icon = 2
            else:
                self.dino_label.setPixmap(self.image_to_pixmap(self.dino_icon1))
                self.current_dino_icon = 1

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = DinosaurGame()
    game.show()
    sys.exit(app.exec_())
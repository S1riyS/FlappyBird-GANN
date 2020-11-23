import sys

from PyQt5 import uic, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QSpinBox, QCheckBox


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("settings.ui", self)
        self.setWindowTitle("Настройки")
        self.startButton.clicked.connect(self.start)
        self.birdsCount.valueChanged.connect(self.set_correct_values)

    def set_correct_values(self):
        self.crossCount.setMaximum(self.birdsCount.value())

    def start(self):
        try:
            self.close()

            from Game import GameController

            controller = GameController(
                bird_count=self.birdsCount.value(),
                mutation_chance=self.mutationChance.value(),
                cross_count=self.crossCount.value(),
                tower_dist=self.dist.value(),
                tower_interval=self.interval.value(),
                is_random_generated=self.checkBox.isChecked(),
            )
            controller.start_game()

        except Exception as e:
            print(e)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())

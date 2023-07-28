from PyQt6.QtCore import QPropertyAnimation, QRect, QTimer
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtGui import QMovie, QIcon
from PyQt6.QtTest import QTest
from PyQt6.uic import loadUi
from afk_resources import *
from PyQt6 import QtCore
import keyboard
import psutil
import sys
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class SplashScreen(QMainWindow):
	# window
	def __init__(self):
		super().__init__()

		loadUi(resource_path("Anti-AFK.ui"), self)
		self.setFixedSize(400, 300)
		self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
		self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
		self.setWindowIcon(QIcon(resource_path("./resources/icon.ico")))
		
		self.loading_icon = QMovie(resource_path("./resources/loading.gif"))
		self.loading.setMovie(self.loading_icon)
		self.loading_icon.start()

		self.anti_afk.stateChanged.connect(self.checkBox)
		self.anti_afk.pressed.connect(self.checkBox_pressed)
		self.anti_afk_pressed = False
		self.anti_afk_status = "deactivated"

		self.anti_afk.setStyleSheet("""QCheckBox::indicator {
										width: 30px;
										height: 30px;
										image: url(":/resources/resources/uncheck.png")
									}""")

		self.exit_app.clicked.connect(self.exit_app_)
		self.exit_app.pressed.connect(self.exit_app_pressed)
		self.always_on_top.clicked.connect(self.always_on_top_check)
		self.always_on_top.pressed.connect(self.always_on_top_check_pressed)
		self.setWindowFlag(QtCore.Qt.WindowType.WindowStaysOnTopHint, False)
		self.always_on_top_ = False

		self.updatingText = QtCore.QTimer(self)
		self.updatingText.timeout.connect(self.update_loading)
		self.updatingText.start(400)
		self.loading_count = 1
		self.stop_updating_text = False

		self.check_for_roblox_ = QtCore.QTimer(self)
		self.check_for_roblox_.timeout.connect(self.check_for_roblox)
		self.check_for_roblox_.start(3000)

		self.roblox_pid = 0

	def exit_app_(self):
		self.close()
	
	def always_on_top_check(self):
		self.always_on_top_ = not self.always_on_top_
		
		self.setWindowFlag(QtCore.Qt.WindowType.WindowStaysOnTopHint, self.always_on_top_)

		if self.always_on_top_ == False:
			self.move(self.frameGeometry().center())
			self.anti_afk_pressed = False
		else:
			self.move(0, 0)

		self.show()

	def checkBox(self, state):
		if state == 2:
			self.anti_afk_status = "activating"
			self.run_anti_afk_current = 0
			self.run_anti_afk_second = 0
			self.run_anti_afk_minute = 0
			self.run_anti_afk_hour = 0

			self.anti_afk.setStyleSheet("""QCheckBox::indicator {
											width: 30px;
											height: 30px;
											image: url(":/resources/resources/check_activating.png")
										}""")

			self.status.setText("STATUS: <strong>activating in 3</strong>")
			self.setWindowTitle("Anti-AFK - Activating in 3")
			QTest.qWait(1000)
			if self.anti_afk_status == "deactivated":
				return
			self.status.setText("STATUS: <strong>activating in 2</strong>")
			self.setWindowTitle("Anti-AFK - Activating in 2")
			QTest.qWait(1000)
			if self.anti_afk_status == "deactivated":
				return
			self.status.setText("STATUS: <strong>activating in 1</strong>")
			self.setWindowTitle("Anti-AFK - Activating in 1")
			QTest.qWait(1000)
			if self.anti_afk_status == "deactivated":
				return
			
			self.status.setText("STATUS: <strong>activated.</strong>")
			self.anti_afk_status = "activated"
			self.setWindowTitle("Anti-AFK - Activated")

			self.anti_afk.setStyleSheet("""QCheckBox::indicator {
											width: 30px;
											height: 30px;
											image: url(":/resources/resources/check.png")
										}""")

			self.run_anti_afk_ = QtCore.QTimer(self)
			self.run_anti_afk_.timeout.connect(self.run_anti_afk)
			self.run_anti_afk_.start()
		else:
			self.anti_afk.setStyleSheet("""QCheckBox::indicator {
											width: 30px;
											height: 30px;
											image: url(":/resources/resources/uncheck.png")
										}""")

			self.anti_afk_status = "deactivated"
			if self.run_anti_afk_hour == 0 and self.run_anti_afk_minute == 0 and self.run_anti_afk_second == 0:
				self.status.setText("STATUS: <strong>not active</strong>")
				self.setWindowTitle("Anti-AFK - Not active")
			else:
				if self.run_anti_afk_minute == 0 and self.run_anti_afk_hour == 0:
					self.status.setText(f"STATUS: <strong>deactivated. You've been AFK for {self.run_anti_afk_second}s</strong>")
					self.setWindowTitle(f"Anti-AFK - Deactivated. {self.run_anti_afk_second}s")
				elif self.run_anti_afk_minute > 0 and self.run_anti_afk_hour == 0:
					self.status.setText(f"STATUS: <strong>deactivated. You've been AFK for {self.run_anti_afk_minute}m {self.run_anti_afk_second}s</strong>")
					self.setWindowTitle(f"Anti-AFK - Deactivated. {self.run_anti_afk_minute}m {self.run_anti_afk_second}s")
				elif self.run_anti_afk_minute > 0 and self.run_anti_afk_hour > 0:
					self.status.setText(f"STATUS: <strong>deactivated. You've been AFK for {self.run_anti_afk_hour}h {self.run_anti_afk_minute}m {self.run_anti_afk_second}s</strong>")
					self.setWindowTitle(f"Anti-AFK - Deactivated. {self.run_anti_afk_hour}h {self.run_anti_afk_minute}m {self.run_anti_afk_second}s")

	def run_anti_afk(self):
		if self.run_anti_afk_second in [0, 10, 20, 30, 40, 50]:
			if self.run_anti_afk_current == 0:
				keyboard.press("a")
				self.run_anti_afk_current += 1
			elif self.run_anti_afk_current == 1:
				keyboard.press("s")
				self.run_anti_afk_current += 1
			elif self.run_anti_afk_current == 2:
				keyboard.press("d")
				self.run_anti_afk_current += 1
			elif self.run_anti_afk_current == 3:
				keyboard.press("w")
				self.run_anti_afk_current = 0

		QTest.qWait(1000)
		keyboard.release("a")
		keyboard.release("s")
		keyboard.release("d")
		keyboard.release("w")
		keyboard.release("space")

		self.run_anti_afk_second += 1

		if self.run_anti_afk_second == 30:
			keyboard.press("space")

		if self.run_anti_afk_second >= 60:
			self.run_anti_afk_second = 0
			self.run_anti_afk_minute += 1
			if self.run_anti_afk_minute >= 60:
				self.run_anti_afk_minute = 0
				self.run_anti_afk_hour += 1

		if self.anti_afk_status == "deactivated":
			self.run_anti_afk_.stop()
			return

		if self.run_anti_afk_minute == 0 and self.run_anti_afk_hour == 0:
			self.status.setText(f"STATUS: <strong>activated. You've been AFK for {self.run_anti_afk_second}s</strong>")
			self.setWindowTitle(f"Anti-AFK - Activated. {self.run_anti_afk_second}s")
		elif self.run_anti_afk_minute > 0 and self.run_anti_afk_hour == 0:
			self.status.setText(f"STATUS: <strong>activated. You've been AFK for {self.run_anti_afk_minute}m {self.run_anti_afk_second}s</strong>")
			self.setWindowTitle(f"Anti-AFK - Activated. {self.run_anti_afk_minute}m {self.run_anti_afk_second}s")
		elif self.run_anti_afk_minute > 0 and self.run_anti_afk_hour > 0:
			self.status.setText(f"STATUS: <strong>activated. You've been AFK for {self.run_anti_afk_hour}h {self.run_anti_afk_minute}m {self.run_anti_afk_second}s</strong>")
			self.setWindowTitle(f"Anti-AFK - Activated. {self.run_anti_afk_hour}h {self.run_anti_afk_minute}m {self.run_anti_afk_second}s")

	def checkBox_pressed(self):
		self.anti_afk_pressed = True

		if self.anti_afk_status == "deactivated":
			self.anti_afk.setStyleSheet("""QCheckBox::indicator {
											width: 30px;
											height: 30px;
											image: url(":/resources/resources/press_activating.png")
										}""")
		elif self.anti_afk_status == "activating":
			self.anti_afk.setStyleSheet("""QCheckBox::indicator {
											width: 30px;
											height: 30px;
											image: url(":/resources/resources/press_activating.png")
										}""")
		elif self.anti_afk_status == "activated":
			self.anti_afk.setStyleSheet("""QCheckBox::indicator {
											width: 30px;
											height: 30px;
											image: url(":/resources/resources/press.png")
										}""")

	def exit_app_pressed(self):
		self.anti_afk_pressed = True

	def always_on_top_check_pressed(self):
		self.anti_afk_pressed = True

	# dragging window
	def mousePressEvent(self, event):
		self.dragPos = event.globalPosition().toPoint()

	def mouseReleaseEvent(self, event):
		if self.anti_afk_pressed == True and self.always_on_top_ == False:
			self.anti_afk_pressed = False

	def mouseMoveEvent(self, event):
		if self.anti_afk_pressed == True: return
		self.move(self.pos() + event.globalPosition().toPoint() - self.dragPos )
		self.dragPos = event.globalPosition().toPoint()
		event.accept()

	# updating loading text
	def update_loading(self):
		self.loading_count = (self.loading_count + 1) % 4
		self.updated_loading_text = "Waiting for <strong>ROBLOX</strong> to open" + "." * self.loading_count
		self.loading_text.setText(self.updated_loading_text)
		self.setWindowTitle("Anti-AFK - Waiting for ROBLOX to open" + "." * self.loading_count)

		if self.stop_updating_text == True:
			self.loading_text.setText("<strong>ROBLOX</strong> is now opened. Please wait.")
			self.setWindowTitle("Anti-AFK - ROBLOX is now opened. Please wait.")
			self.stop_updating_text = False
			self.updatingText.stop()

	# check for roblox on startup
	def check_for_roblox(self):
		for process in psutil.process_iter(["pid", "name"]):
			if process.info['name'] == "RobloxPlayerBeta.exe":
				self.roblox_pid = process.pid
				QTimer.singleShot(1500, self.splashAnim)
				self.check_for_roblox_.stop()
	
	def splashAnim(self):
		self.stop_updating_text = True

		# loading icon shrinks
		self.loading_animation = QPropertyAnimation(self.loading, b"geometry")
		self.loading_animation.setDuration(400)
		self.loading_animation.setStartValue(QRect(170, 210, 41, 41))
		self.loading_animation.setEndValue(QRect(190, 230, 0, 0))
		self.loading_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
		self.loading_animation.start()

		QTest.qWait(150)

		# loading icon changes to rocket
		self.loading_icon = QMovie(resource_path("./resources/loaded.gif"))
		self.loading.setMovie(self.loading_icon)
		self.loading_icon.start()

		# loading icon expands
		self.loading_animation = QPropertyAnimation(self.loading, b"geometry")
		self.loading_animation.setDuration(400)
		self.loading_animation.setStartValue(QRect(190, 230, 0, 0))
		self.loading_animation.setEndValue(QRect(170, 210, 41, 41))
		self.loading_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)
		self.loading_animation.start()

		QTest.qWait(1000)

		# rocket takes off
		self.loading_animation = QPropertyAnimation(self.loading, b"geometry")
		self.loading_animation.setDuration(3000)
		self.loading_animation.setStartValue(QRect(170, 210, 41, 41))
		self.loading_animation.setEndValue(QRect(380, 0, 41, 41))
		self.loading_animation.setEasingCurve(QtCore.QEasingCurve.Type.InBack)
		self.loading_animation.start()

		self.frame.setStyleSheet("""QFrame {
			   							background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.499955, fy:0.5, stop:0 rgba(115, 122, 185, 255), stop:1 rgba(56, 58, 89, 255));
										color: rgb(255, 255, 255);
			   							border-radius: 10px;
			   						}""")
		
		QTest.qWait(1000)

		# title frame goes up
		self.title_frame_animation = QPropertyAnimation(self.title_frame, b"geometry")
		self.title_frame_animation.setDuration(1000)
		self.title_frame_animation.setStartValue(QRect(0, 80, 381, 91))
		self.title_frame_animation.setEndValue(QRect(0, 30, 381, 91))
		self.title_frame_animation.setEasingCurve(QtCore.QEasingCurve.Type.InBack)
		self.title_frame_animation.start()

		self.always_on_top.setGeometry(QRect(340, 50, 25, 25))

		# loading frame goes down
		self.loading_frame_animation = QPropertyAnimation(self.loading_frame, b"geometry")
		self.loading_frame_animation.setDuration(1000)
		self.loading_frame_animation.setStartValue(QRect(0, 180, 381, 81))
		self.loading_frame_animation.setEndValue(QRect(0, 280, 381, 91))
		self.loading_frame_animation.setEasingCurve(QtCore.QEasingCurve.Type.InQuad)
		self.loading_frame_animation.start()

		QTest.qWait(1500)

		self.setWindowTitle("Anti-AFK - Ready to use.")

		# main frame goes to the center
		self.main_frame_animation = QPropertyAnimation(self.main_frame, b"geometry")
		self.main_frame_animation.setDuration(1000)
		self.main_frame_animation.setStartValue(QRect(-320, 110, 321, 111))
		self.main_frame_animation.setEndValue(QRect(30, 110, 321, 111))
		self.main_frame_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutBack)
		self.main_frame_animation.start()

		self.check_if_roblox_is_closed_ = QtCore.QTimer(self)
		self.check_if_roblox_is_closed_.timeout.connect(self.check_if_roblox_is_closed)
		self.check_if_roblox_is_closed_.start()

	def check_if_roblox_is_closed(self):
		if psutil.pid_exists(self.roblox_pid):
			process = psutil.Process(self.roblox_pid)
			if process.name() == "RobloxPlayerBeta.exe":
				return
		
		self.loading_text.setText("Waiting for <strong>ROBLOX</strong> to open")
		self.setWindowTitle("Anti-AFK - Waiting for ROBLOX to open.")

		self.loading_icon = QMovie(resource_path("./resources/loading.gif"))
		self.loading.setMovie(self.loading_icon)
		self.loading_icon.start()

		self.always_on_top.setGeometry(QRect(305, 15, 25, 25))
		self.loading.setGeometry(QRect(170, 210, 41, 41))
		self.title_frame.setGeometry(QRect(0, 80, 381, 91))
		self.loading_frame.setGeometry(QRect(0, 180, 381, 81))
		self.main_frame.setGeometry(QRect(-320, 110, 321, 111))

		self.frame.setStyleSheet("""QFrame {
			   							background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.499955, fy:0.5, stop:0 rgba(88, 93, 141, 255), stop:1 rgba(56, 58, 89, 255));
										color: rgb(255, 255, 255);
			   							border-radius: 10px;
			   						}""")
	
		self.updatingText = QtCore.QTimer(self)
		self.updatingText.timeout.connect(self.update_loading)
		self.updatingText.start(400)
		self.loading_count = 1
		self.stop_updating_text = False

		self.check_for_roblox_ = QtCore.QTimer(self)
		self.check_for_roblox_.timeout.connect(self.check_for_roblox)
		self.check_for_roblox_.start(3000)

		self.roblox_pid = 0

		self.anti_afk.setChecked = False
		self.anti_afk.setStyleSheet("""QCheckBox::indicator {
										width: 30px;
										height: 30px;
										image: url(":/resources/resources/uncheck.png")
									}""")
		
		self.check_if_roblox_is_closed_.stop()

# launch app
if __name__ == "__main__":
	splash = QApplication(sys.argv)
	window = SplashScreen()
	window.show()
	sys.exit(splash.exec())
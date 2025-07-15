import sys
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QMessageBox, \
    QScrollArea, QFrame, QWidget, QTextEdit
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QPalette, QColor, QIcon
import os


class StatusWindow(QDialog):
    update_signal = pyqtSignal(str)  # 信号：更新状态文本

    def __init__(self, parent=None):
        super().__init__(parent)
        icon_path = resource_path("Threadsicon.ico")
        self.setWindowIcon(QIcon(icon_path))
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)  # 无边框
        self.setFixedSize(400, 550)  # 固定大小
        self.initUI()
        self.update_signal.connect(self.update_status)
        # 设置窗口位置到右上角（距离边缘10像素）
        self.setGeometryToTopRight()

    # 新增方法：设置窗口到右上角
    def setGeometryToTopRight(self):
        screen_geometry = QApplication.desktop().availableGeometry()
        x = screen_geometry.width() - self.width() - 10  # 距离右边10像素
        y = 10  # 距离顶部10像素
        self.move(x, y)

    def initUI(self):
        # 主布局
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # 标题栏
        title_bar = QHBoxLayout()
        self.title_label = QLabel("執行任務狀態", self)
        self.title_label.setFont(QFont("微軟雅黑", 12, QFont.Bold))
        self.title_label.setStyleSheet("color: white;")
        title_bar.addWidget(self.title_label)
        title_bar.addStretch(1)

        # 最小化按钮
        min_button = QPushButton("-", self)
        min_button.setFixedSize(24, 24)
        min_button.setFont(QFont("微軟雅黑", 12))
        min_button.clicked.connect(self.showMinimized)
        title_bar.addWidget(min_button)

        # 关闭按钮
        close_button = QPushButton("×", self)
        close_button.setFixedSize(24, 24)
        close_button.setFont(QFont("微軟雅黑", 12))
        close_button.clicked.connect(self.close)
        close_button.setStyleSheet("""
            QPushButton:hover {
                background-color: red;
            }
        """)
        title_bar.addWidget(close_button)

        layout.addLayout(title_bar)
        # 创建滚动区域
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)  # 无边框
        scroll_area.setStyleSheet("background-color: #252525; border: none;")

        # 创建内容容器
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(5, 5, 5, 5)
        content_layout.setAlignment(Qt.AlignTop)

        # 状态文本区域
        self.status_textedit = QTextEdit()
        self.status_textedit.setReadOnly(True)
        self.status_textedit.setFont(QFont("微軟雅黑", 10))
        self.status_textedit.setStyleSheet("""
                    QTextEdit {
                        color: #7FFFD4;
                        background-color: #252525;
                        border: none;
                    }
                """)
        self.status_textedit.append("准备开始任务...")
        content_layout.addWidget(self.status_textedit)
        # 设置滚动区域的内容
        scroll_area.setWidget(content_widget)

        # 添加到主布局
        layout.addWidget(scroll_area)  # 替换原来的 status_label

        self.setLayout(layout)

        # 设置暗色主题
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(25, 25, 25))
        self.setPalette(palette)
    def closeEvent(self, event):
        """重写关闭事件，发出关闭信号"""
        reply = QMessageBox.question(
            self, "關閉確認", "確認要關閉腳本程序嗎？",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.window_closed.emit()
            super().closeEvent(event)
        else:
            event.ignore()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.dragPosition)
            event.accept()

    # def update_status(self, text):
    #     """更新状态文本"""
    #     self.status_label.setText(text)

    def update_status(self, text):
        """更新状态文本，追加并滚动到底部"""
        # 追加新状态
        self.status_textedit.append(text)

        # 滚动到底部
        scrollbar = self.status_textedit.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

        # 确保立即显示更新
        QApplication.processEvents()

def resource_path(relative_path):
    """获取资源的绝对路径"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
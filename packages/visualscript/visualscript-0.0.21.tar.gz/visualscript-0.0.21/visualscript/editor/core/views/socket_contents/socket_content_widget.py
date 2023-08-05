from collections import OrderedDict
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QGraphicsProxyWidget
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt

class SocketContentWidget(QWidget):
    def __init__(self, model, parent=None):
        super().__init__(parent)
        self.model = model
        self.socket = model.parent

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.setLayout(self.layout)

        socket_graphics = self.socket.graphics
        socket_radius = socket_graphics.radius
        self.shape = [0, socket_radius * 2]

        self.isConnected = False

        self.label = None

        self.posX = 2 * socket_radius
        self.posY = 0

        self.setAttribute(Qt.WA_TranslucentBackground)

        proxy_widget = QGraphicsProxyWidget(socket_graphics)
        proxy_widget.setWidget(self)

    def updateName(self, new_name):
        if new_name and not self.label:
            self.label = QLabel()
            if not self.socket.is_input:
                self.label.setAlignment(Qt.AlignRight | Qt.AlignCenter)
            self.addWidget(self.label)
        if self.label:
            self.label.setText(new_name)
            bounding_rect = self.label.fontMetrics().boundingRect(self.label.text())
            self.shape = [bounding_rect.width(), max(bounding_rect.height(), self.shape[1])]
            self.update_geometry()
            self.socket.node.graphics.update_sockets_pos()

    def update_geometry(self):
        # if not self.socket.is_input:
        #     self.posX = -abs(self.posX) - self.shape[0]
        self.posY = -self.shape[1]//2
        if self.socket.is_input:
            self.setGeometry(self.posX, self.posY, *self.shape)
        else:
            self.setGeometry(-self.posX - self.shape[0], self.posY, *self.shape)

    def addWidget(self, widget):
        widget.setStyleSheet(f"background: {self.socket.node.graphics.background_color}; color: white")
        self.layout.addWidget(widget)
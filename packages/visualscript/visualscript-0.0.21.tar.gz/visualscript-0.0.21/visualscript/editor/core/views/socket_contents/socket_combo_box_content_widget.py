from PyQt5.QtWidgets import QComboBox
from visualscript.editor.core.views.socket_contents.socket_content_widget import SocketContentWidget


class SocketComboBoxContentWidget(SocketContentWidget):
    def __init__(self, model, parent=None):
        self.combo_box = None
        self.combo_box_width = 80
        super(SocketComboBoxContentWidget, self).__init__(model, parent)
        self.init_combo_box()

    def load_value(self, value):
        if self.combo_box.findText(value) == -1:
            self.combo_box.addItem(value)
        self.combo_box.setCurrentText(value)
        # print(self.combo_box.currentText())

    def get_value(self):
        return self.combo_box.currentText()

    def init_combo_box(self):
        label_width = 0 if self.label is None else self.label.fontMetrics().boundingRect(self.label.text()).width()
        self.combo_box = QComboBox()
        self.combo_box.setFixedSize(self.combo_box_width, 24)
        self.shape = [label_width + self.combo_box_width, 24]
        self.update_geometry()
        self.layout.addWidget(self.combo_box)

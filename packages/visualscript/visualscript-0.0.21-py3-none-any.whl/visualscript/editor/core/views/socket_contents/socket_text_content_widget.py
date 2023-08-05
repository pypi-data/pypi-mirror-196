from PyQt5.QtWidgets import QTextEdit
from visualscript.editor.core.views.socket_contents.socket_content_widget import SocketContentWidget


class SocketTextContentWidget(SocketContentWidget):
    def __init__(self, model, parent=None):
        self.editText = None
        self.editText_width = 80
        self.initial_text = "Hello" if model.parent.data_type == str else "None"
        super(SocketTextContentWidget, self).__init__(model, parent)
        self.init_edit_text()

    def load_value(self, value):
        self.editText.setText(value)

    def get_value(self):
        return self.editText.toPlainText()

    def init_edit_text(self):
        label_width = 0 if self.label is None else self.label.fontMetrics().boundingRect(self.label.text()).width()
        self.editText = QTextEdit(self.initial_text)
        self.editText.setFixedSize(self.editText_width, 24)
        self.editText.focusOutEvent = self.onEditTextFocusOutEvent
        self.shape = [label_width + self.editText_width, 24]
        self.update_geometry()
        self.layout.addWidget(self.editText)

    def onEditTextFocusOutEvent(self, event):
        QTextEdit.focusOutEvent(self.editText, event)
        current_text = self.editText.toPlainText()
        if current_text != self.initial_text:
            self.initial_text = current_text
            self.socket.node.update()
            self.socket.node.scene.history.storeHistory("Changed text value to %s" % current_text)
from visualscript.editor.core.models.serializable import Serializable
from visualscript.editor.core.views.socket_contents.socket_content_widget import SocketContentWidget


class SocketContent(Serializable):
    default_graphics = SocketContentWidget
    def __init__(self, parent, graphics=None, name=''):
        super().__init__()
        self.parent = parent
        if graphics:
            self.graphics = graphics(self)
        else:
            self.graphics = self.default_graphics(self)
        self.graphics.updateName(name)

    def updateName(self, new_name):
        self.graphics.updateName(new_name)

    def on_connect(self):
        pass

    def on_disconnect(self):
        pass

    def get_value(self):
        return None

    def deserialize(self, data, hashmap={}, restore_id=True):
        return True
from collections import OrderedDict
from visualscript.editor.core.models.socket_contents.socket_content import SocketContent
from visualscript.editor.core.views.socket_contents.socket_text_content_widget import SocketTextContentWidget

class SocketTextContent(SocketContent):
    default_graphics = SocketTextContentWidget

    def get_value(self):
        return self.graphics.get_value()

    def serialize(self):
        return OrderedDict([('text', self.get_value())])

    def deserialize(self, data, hashmap={}, restore_id=True):
        self.graphics.load_value(data['text'])
        return True

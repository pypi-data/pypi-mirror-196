from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from visualscript.editor.config import *
from visualscript.editor.core.utils import dumpException


class NodeBrowser(QTreeWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.categories = {}
        self.initUI()

    def initUI(self):
        self.setIconSize(QSize(32, 32))
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setDragEnabled(True)
        self.header().hide()
        self.addMyItems()

    def mouseDoubleClickEvent(self, event):
        super().mouseDoubleClickEvent(event)
        item = self.currentItem()
        if item and not item.childCount():
            scene = self.window().parent().scene
            if scene:
                self.instantiate_node(scene, item)
                self.window().hide()

    def addMyItems(self):
        keys = list(CLASS_REGISTRY.keys())
        keys.sort()
        for key in keys:
            node = get_class_from_name(key)
            self.addMyItem(node.title, node.category, node.__name__)

    def addMyItem(self, name, category, class_name):
        if category == "Abstract":
            return
        if self.categories.__contains__(category):
            parent = self.categories[category]
        else:
            parent = self.addCategoriesItems(self, category)
        item = QTreeWidgetItem(parent, [name])
        pixmap = QPixmap(".")
        item.setIcon(0, QIcon(pixmap))
        item.setSizeHint(0, QSize(16, 16))

        item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsDragEnabled)

        item.setData(Qt.UserRole, 0, pixmap)
        item.setData(Qt.UserRole + 1, 0, class_name)

    def addCategoriesItems(self, parent, category):
        subcategory = category.split(";")[-1]
        separator_index = len(category) - len(subcategory)
        if separator_index != 0:
            parent = self.addCategoriesItems(parent, category[:(separator_index - 1)])
        item = QTreeWidgetItem(parent, [subcategory])
        item.setFlags(Qt.ItemIsEnabled)
        self.categories[category] = item
        return item

    def startDrag(self, *args, **kwargs):
        try:
            item = self.currentItem()
            class_name = item.data(Qt.UserRole + 1, 0)
            if not class_name:
                return

            pixmap = QPixmap(item.data(Qt.UserRole, 0))


            itemData = QByteArray()
            dataStream = QDataStream(itemData, QIODevice.WriteOnly)
            dataStream << pixmap

            dataStream.writeQString(class_name)

            mimeData = QMimeData()
            mimeData.setData(LISTBOX_MIMETYPE, itemData)

            drag = QDrag(self)
            drag.setMimeData(mimeData)
            drag.setHotSpot(QPoint(pixmap.width() // 2, pixmap.height() // 2))
            drag.setPixmap(pixmap)

            drag.exec_(Qt.MoveAction)

        except Exception as e: dumpException(e)

    def instantiate_node(self, scene, item):
        class_name = item.data(Qt.UserRole + 1, 0)
        node = get_class_from_name(class_name)(scene=scene)
        node_pos = scene.graphics.views()[0].last_scene_mouse_position
        node.graphics.setPos(node_pos)
        scene.history.storeHistory("Created node %s" % node.__class__.__name__)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    NodeBrowser().show()
    sys.exit(app.exec_())
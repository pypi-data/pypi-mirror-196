import inspect, types, builtins
import threading

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from visualscript.editor.nodes.variable import VariableNode
from visualscript.editor.nodes.call_function import CallFunctionNode

from visualscript.editor.config import *
from visualscript.editor.core.utils import dumpException


class AttributeBrowser(QTreeWidget):
    SUBMODULES, MAGIC_FUNCTIONS, FUNCTIONS, MAGIC_VARIABLES, VARIABLES, CLASSES = \
        "Submodules", "__MagicFunctions__", "Functions", "__MagicVariables__", "Variables", "Classes"

    FUNCTION_NODE, VARIABLE_NODE, CONSTRUCTOR_NODE = CallFunctionNode, VariableNode, VariableNode

    def __init__(self, module, parent=None):
        super().__init__(parent)
        self.reference_dictionary = {}
        self.module = None
        self.items_count = 0
        self.parent_items = {}
        self.reload(module)
        self.initUI()

    def setup_parent_items(self):
        parent_items = {}
        for item_type in (self.MAGIC_FUNCTIONS, self.MAGIC_VARIABLES, self.CLASSES, self.FUNCTIONS, self.SUBMODULES, self.VARIABLES):
            item = QTreeWidgetItem(self, [item_type])
            item.setFlags(Qt.ItemIsEnabled)
            parent_items[item_type] = item
        return parent_items

    def initUI(self):
        self.setIndentation(7)
        self.setIconSize(QSize(32, 32))
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setDragEnabled(True)
        self.header().hide()

    def reload(self, new_opened_module):
        if new_opened_module:
                self.module = new_opened_module
                if not hasattr(self.module, '__dict__'):
                    self.clear()
                    return
                self.items_count = len(self.module.__dict__)
                self.clear()
                self.parent_items = self.setup_parent_items()
                self.addItems(self, self.module)
                # threading.Thread(target=self.addItems).start()
        else:
            self.clear()

    def mouseDoubleClickEvent(self, event):
        super().mouseDoubleClickEvent(event)
        if event.button() == Qt.LeftButton:
            item = self.currentItem()
            if item and not item.childCount():
                scene = self.window().getActiveWorkspace().scene
                if scene:
                    self.instantiate_node(scene, item)

    def addItems(self, parent, module, level=0, parent_modules=None):
        if level > 10:
            return
        if not module:
            return
        if parent_modules is None:
            parent_modules = []

        magic_function_item, magic_variable_item, submodule_item, class_item, function_item, variable_item = [None] * 6

        if level == 0:
            parent_modules.append(module)
            submodule_item = QTreeWidgetItem(parent, [self.SUBMODULES])
            submodule_item.setFlags(Qt.ItemIsEnabled)
            item = QTreeWidgetItem(submodule_item, ["builtins"])
            item.setFlags(Qt.ItemIsEnabled)
            self.addItems(item, builtins, level + 1, parent_modules)

        keys = list(module.__dict__.keys())
        submodules = []
        for key in keys:
            try:
                if parent_modules.__contains__(module.__dict__[key]):
                    continue
            except:
                continue
            if inspect.ismodule(module.__dict__[key]):
                submodules.append(key)
                parent_modules.append(module.__dict__[key])
                continue
            elif callable(getattr(module, key)):
                if hasattr(getattr(module, key), 'mro'):
                    class_name = self.CONSTRUCTOR_NODE.__name__
                    if not class_item:
                        if level == 0:
                            class_item = self.parent_items[self.CLASSES]
                        else:
                            class_item = QTreeWidgetItem(parent, [self.CLASSES])
                            class_item.setFlags(Qt.ItemIsEnabled)
                    parent_item = class_item
                else:
                    class_name = self.FUNCTION_NODE.__name__
                    if key.startswith("__"):
                        if not magic_function_item:
                            if level == 0:
                                magic_function_item = self.parent_items[self.MAGIC_FUNCTIONS]
                            else:
                                magic_function_item = QTreeWidgetItem(parent, [self.MAGIC_FUNCTIONS])
                                magic_function_item.setFlags(Qt.ItemIsEnabled)
                        parent_item = magic_variable_item
                    else:
                        if not function_item:
                            if level == 0:
                                function_item = self.parent_items[self.FUNCTIONS]
                            else:
                                function_item = QTreeWidgetItem(parent, [self.FUNCTIONS])
                                function_item.setFlags(Qt.ItemIsEnabled)
                        parent_item = function_item
            else:
                class_name = self.VARIABLE_NODE.__name__
                if key.startswith("__"):
                    if not magic_variable_item:
                        if level == 0:
                            magic_variable_item = self.parent_items[self.MAGIC_VARIABLES]
                        else:
                            magic_variable_item = QTreeWidgetItem(parent, [self.MAGIC_VARIABLES])
                            magic_variable_item.setFlags(Qt.ItemIsEnabled)
                    parent_item = magic_variable_item
                else:
                    if not variable_item:
                        if level == 0:
                            variable_item = self.parent_items[self.VARIABLES]
                        else:
                            variable_item = QTreeWidgetItem(parent, [self.VARIABLES])
                            variable_item.setFlags(Qt.ItemIsEnabled)
                    parent_item = variable_item
            item = QTreeWidgetItem(parent_item, [key])
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsDragEnabled)
            item.setData(Qt.UserRole + 1, 0, class_name)
            self.reference_dictionary[key] = module.__dict__[key]

        for submodule in submodules:
            item = QTreeWidgetItem(submodule_item, [submodule])
            item.setFlags(Qt.ItemIsEnabled)
            self.addItems(item, module.__dict__[submodule], level + 1, parent_modules)

        if level == 0:
            self.sortItems(0, Qt.AscendingOrder)

            if self.parent():
                self.parent().filter_tree()

    def startDrag(self, *args, **kwargs):
        try:
            item = self.currentItem()
            class_name = item.data(Qt.UserRole + 1, 0)
            pixmap = QPixmap(item.data(Qt.UserRole, 0))

            title = item.text(0)

            itemData = QByteArray()
            dataStream = QDataStream(itemData, QIODevice.WriteOnly)
            dataStream << pixmap

            dataStream.writeQString(class_name)

            while item.parent().parent():
                item = item.parent().parent()
                title = f"{item.text(0)}.{title}"

            dataStream.writeQString(title)

            mimeData = QMimeData()
            mimeData.setData(LISTBOX_MIMETYPE, itemData)

            drag = QDrag(self)
            drag.setMimeData(mimeData)
            drag.setHotSpot(QPoint(pixmap.width() // 2, pixmap.height() // 2))
            drag.setPixmap(pixmap)

            drag.exec_(Qt.MoveAction)

        except Exception as e:
            dumpException(e)

    def instantiate_node(self, scene, item):
        class_name = item.data(Qt.UserRole + 1, 0)
        title = item.text(0)

        while item.parent().parent():
            item = item.parent().parent()
            title = f"{item.text(0)}.{title}"

        if not class_name:
            print("This type of attribute/method is not handled yet")
            return

        node = get_class_from_name(class_name)(scene=scene, title=title)
        node.generate_sockets()
        scene.history.storeHistory("Created node %s" % node.__class__.__name__)

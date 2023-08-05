import dis, types, inspect
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTreeWidgetItem
from visualscript.editor.config import get_class_from_name
from visualscript.editor.core.models.element_browsers.attribute_browser import AttributeBrowser
from visualscript.editor.nodes.attribute import AttributeNode
from visualscript.editor.nodes.call_method import CallMethodNode

class InheritedAttibutesBrowser(AttributeBrowser):
    FUNCTION_NODE, VARIABLE_NODE, CONSTRUCTOR_NODE = CallMethodNode, AttributeNode, AttributeNode

    def __init__(self, socket, parent=None):
        self.start_socket = socket
        super().__init__(parent=parent, module=socket.data_type)

    def setup_parent_items(self):
        pass

    def addItems(self, parent, scope, level=0, parent_modules=[]):
        if level > 3:
            return

        # input_values = []
        # for i in range(1, len(self.start_socket.node.inputs)):
        #     value = None
        #     input_node = self.start_socket.node.get_input_node(i)
        #     if input_node:
        #         value = input_node.get_value()
        #     input_values.append(value)

        keys = dir(scope)

        #checking attributes defined in __init__ only if that function isn't a wrapper_descriptor
        if not isinstance(scope.__init__, type(int.__init__)):
            try:
                for instruction in dis.Bytecode(self.start_socket.data_type.__init__):
                    if instruction.opname == "STORE_ATTR":
                        value = instruction.argval
                        if value == 'overriden_args':
                            continue
                        if not keys.__contains__(value):
                            keys.append(value)
            except TypeError as e:
                pass

        magic_method_item, magic_variable_item, submodule_item, class_item, method_item, variable_item = [None] * 6
        for key in keys:
            parent_item = None
            class_name = None
            if scope.__dict__ and scope.__dict__.__contains__(key):
                if parent_modules.__contains__(scope.__dict__[key]):
                    continue
                if inspect.ismodule(scope.__dict__[key]):
                    if not submodule_item:
                        submodule_item = QTreeWidgetItem(parent, [self.SUBMODULES])
                        submodule_item.setFlags(Qt.ItemIsEnabled)
                    parent_item = submodule_item
                    item = QTreeWidgetItem(parent_item, [key])
                    item.setFlags(Qt.ItemIsEnabled)
                    self.addItems(item, scope.__dict__[key], level + 1, parent_modules)
                    continue
            if parent_item is None:
                if hasattr(scope, key) and callable(getattr(scope, key)):
                    if hasattr(getattr(scope, key), 'mro'):
                        class_name = self.CONSTRUCTOR_NODE.__name__
                        if not class_item:
                            class_item = QTreeWidgetItem(parent, [self.CLASSES])
                            class_item.setFlags(Qt.ItemIsEnabled)
                        parent_item = class_item
                    else:
                        class_name = self.FUNCTION_NODE.__name__
                        if key.startswith("__"):
                            if not magic_method_item:
                                magic_method_item = QTreeWidgetItem(parent, [self.MAGIC_FUNCTIONS])
                                magic_method_item.setFlags(Qt.ItemIsEnabled)
                            parent_item = magic_method_item
                        else:
                            if not method_item:
                                method_item = QTreeWidgetItem(parent, [self.FUNCTIONS])
                                method_item.setFlags(Qt.ItemIsEnabled)
                            parent_item = method_item
                else:
                    class_name = self.VARIABLE_NODE.__name__
                    if key.startswith("__"):
                        if not magic_variable_item:
                            magic_variable_item = QTreeWidgetItem(parent, [self.MAGIC_VARIABLES])
                            magic_variable_item.setFlags(Qt.ItemIsEnabled)
                        parent_item = magic_variable_item
                    else:
                        if not variable_item:
                            variable_item = QTreeWidgetItem(parent, [self.VARIABLES])
                            variable_item.setFlags(Qt.ItemIsEnabled)
                        parent_item = variable_item
            item = QTreeWidgetItem(parent_item, [key])
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsDragEnabled)
            item.setData(Qt.UserRole + 1, 0, class_name)
            if self.start_socket.data_type.__dict__.__contains__(key):
                self.reference_dictionary[key] = self.start_socket.data_type.__dict__[key]
            else:
                self.reference_dictionary[key] = key

    def mouseDoubleClickEvent(self, event):
        item = self.currentItem()
        if item and not item.childCount():
            scene = self.start_socket.node.scene
            if scene:
                self.instantiate_node(scene, item)
                self.window().hide()

    def instantiate_node(self, scene, item):
        class_name = item.data(Qt.UserRole + 1, 0)
        title = item.text(0)

        while item.parent().parent():
            item = item.parent().parent()
            title = f"{item.text(0)}.{title}"

        node = get_class_from_name(class_name)(scene=scene, title=title)
        node.generate_sockets()

        node_pos = scene.graphics.views()[0].last_scene_mouse_position
        node.graphics.setPos(node_pos)
        node.connect_parent(self.start_socket)

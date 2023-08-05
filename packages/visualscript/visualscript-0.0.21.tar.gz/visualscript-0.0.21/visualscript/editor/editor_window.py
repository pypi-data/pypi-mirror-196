import os, json

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from visualscript.editor.core.utils import dumpException
from visualscript.editor.workspace_window import WorkspaceWindow

class EditorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.running = False
        self.initUI()

    def initUI(self):
        style = """QFrame,QDialog,QMainWindow{background:#474747}QSplitter,QMainWindow::separator{background:#474747}QStatusBar{background:#474747;color:#ccc}QTabWidget{border:0}QTabBar{background:#474747;color:#ccc}QMdiArea QTabBar,QMdiArea QTabWidget,QMdiArea QTabWidget::pane,QMdiArea QTabWidget::tab-bar,QMdiArea QTabBar::tab{height:17px}QMdiArea QTabBar::tab:top:!selected,QMdiArea QTabBar::tab:top:selected,QMdiArea QTabBar::tab:top:!selected:hover{border-top-left-radius:4px;border-top-right-radius:4px;padding:2px 8px;padding-top:0;padding-bottom:3px;min-width:8ex;border:1px solid #333;border-bottom:0}QMdiArea QTabBar::tab:top:!selected,QMdiArea QTabBar::tab:top:!selected:hover{background:qlineargradient(x1 : 0,y1 : 0,x2 : 0,y2 : 1,stop : 0 #6d6d6d,stop : .1 #474747,stop : .89 #3f3f3f,stop : 1 #3f3f3f)}QMdiArea QTabBar::tab:top:selected{background:qlineargradient(x1 : 0,y1 : 0,x2 : 0,y2 : 1,stop : 0 #878787,stop : .1 #545454,stop : .89 #474747,stop : 1 #474747)}QMdiArea QTabBar::tab:top:!selected:hover{background:qlineargradient(x1 : 0,y1 : 0,x2 : 0,y2 : 1,stop : 0 #727272,stop : .1 #4c4c4c,stop : .89 #444,stop : 1 #444)}QMdiArea QTabBar QToolButton{background:qlineargradient(x1 : 0,y1 : 0,x2 : 0,y2 : 1,stop : 0 #878787,stop : .1 #616161,stop : .89 #4f4f4f,stop : 1 #4f4f4f);border:1px solid #333;border-radius:0}QMdiArea QTabBar QToolButton::left-arrow{image:url(':icons/small_arrow_left-light.png")}QMdiArea QTabBar QToolButton::right-arrow{image:url(":icons/small_arrow_right-light.png")}QMdiArea QTabBar::close-button:selected{image:url(":icons/tab_close_btn.png");subcontrol-origin:border;subcontrol-position:right bottom}QMdiArea QTabBar::close-button:!selected{image:url(":icons/tab_close_nonselected_btn.png")}QMdiSubWindow{border-style:solid;background:#616161}QTabBar::tab:selected,QTabBar::tab:hover{color:#eee}QDockWidget{color:#ddd;font-weight:bold;titlebar-close-icon:url(":icons/docktitle-close-btn-light.png");titlebar-normal-icon:url(":icons/docktitle-normal-btn-light.png")}QDockWidget::title{background:qlineargradient(x1 : 0,y1 : 0,x2 : 0,y2 : 1,stop : 0 #3b3b3b,stop : 1 #2e2e2e);padding-top:4px;padding-right:22px;font-weight:bold}QDockWidget::close-button,QDockWidget::float-button{subcontrol-position:top right;subcontrol-origin:margin;text-align:center;icon-size:16px;width:14px;position:absolute;top:0;bottom:0;left:0;right:4px}QDockWidget::close-button{right:4px}QDockWidget::float-button{right:18px}QToolButton{background:#474747;color:#eee}QToolBar,QMenuBar{background:#474747}QMenuBar::item{spacing:3px;padding:3px 5px;color:#eee;background:transparent}QMenuBar::item:selected,QMenuBar::item:pressed{background:#4f9eee}QMenu{background:#474747;border:1px solid #2e2e2e}QMenu::item{background:#474747;color:#eee}QMenu::item:selected{background:#616161}QMenu::active{background:#616161;color:#eee}QMenu::separator{height:1px;background:#2e2e2e}QMenu::disabled,QMenu::item:disabled{color:#6e6e6e}QListView{background-color:#555;alternate-background-color:#434343}QListView::item{height:22px;color:#e6e6e6}QListView::item:hover{background:#6e6e6e}QListView::item::active:hover{color:#fff}QListView::item:selected,QListView::item::active:selected{color:#fff;background:qlineargradient(x1 : 0,y1 : 0,x2 : 0,y2 : 1,stop : 0 #4f9eee,stop : 1 #2084ea);border:0}QTreeView{background-color:#555;alternate-background-color:#434343}QTreeView::item{height:22px;color:#e6e6e6}QTreeView::item:hover{background:#6e6e6e}QTreeView::item::active:hover{color:#fff}QTreeView::item:selected,QTreeView::item::active:selected{color:#fff;background:qlineargradient(x1 : 0,y1 : 0,x2 : 0,y2 : 1,stop : 0 #4f9eee,stop : 1 #2084ea);border:0}QPushButton{color:#e6e6e6;background:#555;border-color:#141414}QLabel{color:#e6e6e6}QLineEdit,QTextEdit{color:#e6e6e6;background:#5a5a5a}QLineEdit{border:1px solid #3a3a3a;border-radius:2px;padding:1px 2px}QDMNodeContentWidget{background:transparent;}QDMNodeContentWidget QFrame{background:transparent}QDMNodeContentWidget QTextEdit{background:#666}QDMNodeContentWidget QLabel{color:#e0e0e0}QGraphicsView{selection-background-color:#fff}"""
        QApplication.instance().setStyleSheet(style)

        self.empty_icon = QIcon(".")

        self.mdiArea = QMdiArea()
        self.mdiArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mdiArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mdiArea.setViewMode(QMdiArea.TabbedView)
        self.mdiArea.setDocumentMode(True)
        self.mdiArea.setTabsClosable(True)
        self.mdiArea.setTabsMovable(True)
        self.setCentralWidget(self.mdiArea)

        self.mdiArea.subWindowActivated.connect(self.updateMenus)
        self.windowMapper = QSignalMapper(self)
        self.windowMapper.mapped[QWidget].connect(self.setActiveSubWindow)
        self.createAttributeBrowser()
        self.setShortcutEnabled(True)

        self.createActions()
        self.createMenus()
        self.createToolBars()
        self.createStatusBar()
        self.updateMenus()

        self.setWindowTitle("Models Circuit Editor")
        self.show()

    def createAttributeBrowser(self):
        from visualscript.editor.core.models.properties_widget import PropertiesWidget
        self.attributeBrowser = PropertiesWidget()
        self.attributeDock = QDockWidget()
        self.attributeDock.setWindowTitle("Attributes Window")
        self.attributeDock.setWidget(self.attributeBrowser)
        self.attributeDock.setFloating(False)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.attributeDock)

    def closeEvent(self, event):
        self.mdiArea.closeAllSubWindows()
        if self.mdiArea.currentSubWindow():
            event.ignore()
        else:
            event.accept()

    def createActions(self):
        self.actNew = QAction('&New', self, shortcut='Ctrl+N', statusTip="Create new graph", triggered=self.onFileNew)
        self.actOpen = QAction('&Open', self, shortcut='Ctrl+O', statusTip="Open file", triggered=self.onFileOpen)
        self.actSave = QAction('&Save', self, shortcut='Ctrl+S', statusTip="Save file", triggered=self.onFileSave)
        self.actSaveAs = QAction('Save &As...', self, shortcut='Ctrl+Shift+S', statusTip="Save file as...", triggered=self.onFileSaveAs)
        self.actExit = QAction('E&xit', self, shortcut='Ctrl+Q', statusTip="Exit application", triggered=self.close)

        self.actUndo = QAction('&Undo', self, shortcut='Ctrl+Z', statusTip="Undo last operation", triggered=self.onEditUndo)
        self.actRedo = QAction('&Redo', self, shortcut='Ctrl+Y', statusTip="Redo last operation", triggered=self.onEditRedo)
        self.actCut = QAction('Cu&t', self, shortcut='Ctrl+X', statusTip="Cut to clipboard", triggered=self.onEditCut)
        self.actCopy = QAction('&Copy', self, shortcut='Ctrl+C', statusTip="Copy to clipboard", triggered=self.onEditCopy)
        self.actPaste = QAction('&Paste', self, shortcut='Ctrl+V', statusTip="Paste from clipboard", triggered=self.onEditPaste)
        self.actDelete = QAction('&Delete', self, shortcut='Del', statusTip="Delete selected items", triggered=self.onEditDelete)

        self.actClose = QAction("Cl&ose", self, statusTip="Close the active window", triggered=self.mdiArea.closeActiveSubWindow)
        self.actCloseAll = QAction("Close &All", self, statusTip="Close all the windows", triggered=self.mdiArea.closeAllSubWindows)
        self.actTile = QAction("&Tile", self, statusTip="Tile the windows", triggered=self.mdiArea.tileSubWindows)
        self.actCascade = QAction("&Cascade", self, statusTip="Cascade the windows", triggered=self.mdiArea.cascadeSubWindows)
        self.actNext = QAction("Ne&xt", self, shortcut=QKeySequence.NextChild, statusTip="Move the focus to the next window", triggered=self.mdiArea.activateNextSubWindow)
        self.actPrevious = QAction("Pre&vious", self, shortcut=QKeySequence.PreviousChild, statusTip="Move the focus to the previous window", triggered=self.mdiArea.activatePreviousSubWindow)

        self.actSeparator = QAction(self)
        self.actSeparator.setSeparator(True)

    def getActiveWorkspace(self) -> WorkspaceWindow:
        active_workspace = self.mdiArea.activeSubWindow()
        if active_workspace:
            return active_workspace.widget()
        return None

    def isModified(self):
        return self.getActiveWorkspace().scene.isModified()

    def maybeSave(self):
        if not self.isModified():
            return True

        res = QMessageBox.warning(self, "About to lose your work?",
                "The document has been modified.\n Do you want to save your changes?",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
              )

        if res == QMessageBox.Save:
            return self.onFileSave()
        elif res == QMessageBox.Cancel:
            return False

        return True

    def onScenePosChanged(self, x, y):
        self.status_mouse_pos.setText("Scene Pos: [%d, %d]" % (x, y))

    def onFileNew(self):
        try:
            subwnd = self.createMdiChild()
            subwnd.widget().fileNew()
            subwnd.showMaximized()
            self.getActiveWorkspace().view.scenePosChanged.connect(self.onScenePosChanged)
        except Exception as e:
            dumpException(e)

    def onFileOpen(self, file_paths=None):
        if not file_paths:
            file_paths, _ = QFileDialog.getOpenFileNames(self, 'Open graph from file',
                                                         filter=self.tr("Python Scripts (*.py *.vpy)"))

        for path in file_paths:
            path = os.path.join(os.curdir, path)
            if path:
                existing = self.findMdiChild(path)
                if existing:
                    self.mdiArea.setActiveSubWindow(existing)
                else:
                    new_workspace = WorkspaceWindow(self)
                    if new_workspace.fileLoad(path):
                        self.statusBar().showMessage("File %s loaded" % path, 5000)
                        new_workspace.setTitle()
                        subwnd = self.createMdiChild(new_workspace)
                        subwnd.show()
                        self.getActiveWorkspace().view.scenePosChanged.connect(self.onScenePosChanged)
                    else:
                        new_workspace.close()

    def createMenus(self):
        menubar = self.menuBar()

        self.fileMenu = menubar.addMenu('&File')
        self.fileMenu.addAction(self.actNew)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.actOpen)
        self.fileMenu.addAction(self.actSave)
        self.fileMenu.addAction(self.actSaveAs)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.actExit)

        self.editMenu = menubar.addMenu('&Edit')
        self.editMenu.addAction(self.actUndo)
        self.editMenu.addAction(self.actRedo)
        self.editMenu.addSeparator()
        self.editMenu.addAction(self.actCut)
        self.editMenu.addAction(self.actCopy)
        self.editMenu.addAction(self.actPaste)
        self.editMenu.addSeparator()
        self.editMenu.addAction(self.actDelete)

        self.windowMenu = self.menuBar().addMenu("&Window")
        self.updateWindowMenu()
        self.windowMenu.aboutToShow.connect(self.updateWindowMenu)

        self.menuBar().addSeparator()

        self.helpMenu = self.menuBar().addMenu("&Help")

        self.editMenu.aboutToShow.connect(self.updateEditMenu)

    def onFileSave(self):
        active_workspace = self.getActiveWorkspace()
        if active_workspace is not None:
            if not active_workspace.isFilenameSet(): return self.onFileSaveAs()

            active_workspace.fileSave()
            self.statusBar().showMessage("Successfully saved %s" % active_workspace.filename, 5000)
            active_workspace.setTitle()

            # support for MDI app
            # if hasattr(active_workspace, "setTitle"):
            # else: self.setTitle()
            return True

    def onFileSaveAs(self):
        current_nodeeditor = self.getActiveWorkspace()
        if current_nodeeditor is not None:
            fname, fformat = QFileDialog.getSaveFileName(self, 'Save visual script',
                                                         filter=self.tr("Visual Python Scripts (*.vpy);;"
                                                                        "All Files (*.*)"))

            if fname == '':
                return False

            extension = fformat.split('.')
            extension = '.' + extension[1].strip(')') if len(extension) == 2 else ''
            if fname.endswith(extension):
                fname = fname[:-len(extension)]

            if extension != '':
                fname += extension

            current_nodeeditor.fileSave(fname)
            self.statusBar().showMessage("Successfully saved as %s" % current_nodeeditor.filename, 5000)
            current_nodeeditor.setTitle()

            # support for MDI app
            # if hasattr(current_nodeeditor, "setTitle"):
            # else: self.setTitle()
            return True

    def onEditUndo(self):
        if self.getActiveWorkspace():
            self.getActiveWorkspace().scene.history.undo()

    def onEditRedo(self):
        if self.getActiveWorkspace():
            self.getActiveWorkspace().scene.history.redo()

    def onEditDelete(self):
        if self.getActiveWorkspace():
            self.getActiveWorkspace().scene.getView().deleteSelected()

    def onEditCut(self):
        if self.getActiveWorkspace():
            data = self.getActiveWorkspace().scene.clipboard.serializeSelected(cut=True)
            str_data = json.dumps(data, indent=4)
            QApplication.instance().clipboard().setText(str_data)

    def onEditCopy(self):
        if self.getActiveWorkspace():
            data = self.getActiveWorkspace().scene.clipboard.serializeSelected(cut=False)
            str_data = json.dumps(data, indent=4)
            QApplication.instance().clipboard().setText(str_data)

    def onEditPaste(self):
        if self.getActiveWorkspace():
            raw_data = QApplication.instance().clipboard().text()

            try:
                data = json.loads(raw_data)
            except ValueError as e:
                print("Pasting of not valid json data!", e)
                return

            # check if the json data are correct
            if 'nodes' not in data:
                print("JSON does not contain any nodes!")
                return

            self.getActiveWorkspace().scene.clipboard.deserializeFromClipboard(data)

    def updateMenus(self):
        # print("update Menus")
        active = self.getActiveWorkspace()
        hasMdiChild = (active is not None)

        self.actSave.setEnabled(hasMdiChild)
        self.actSaveAs.setEnabled(hasMdiChild)
        self.actClose.setEnabled(hasMdiChild)
        self.actCloseAll.setEnabled(hasMdiChild)
        self.actTile.setEnabled(hasMdiChild)
        self.actCascade.setEnabled(hasMdiChild)
        self.actNext.setEnabled(hasMdiChild)
        self.actPrevious.setEnabled(hasMdiChild)
        self.actSeparator.setVisible(hasMdiChild)

        self.updateEditMenu()

    def updateEditMenu(self):
        active = self.getActiveWorkspace()
        hasMdiChild = (active is not None)

        self.actPaste.setEnabled(hasMdiChild)

        hasSelectedItems = hasMdiChild and active.hasSelectedItems()
        self.actCut.setEnabled(hasSelectedItems)
        self.actCopy.setEnabled(hasSelectedItems)
        self.actDelete.setEnabled(hasSelectedItems)

        self.actUndo.setEnabled(hasMdiChild and active.canUndo())
        self.actRedo.setEnabled(hasMdiChild and active.canRedo())

    def updateWindowMenu(self):
        self.windowMenu.clear()

        self.windowMenu.addAction(self.actClose)
        self.windowMenu.addAction(self.actCloseAll)
        self.windowMenu.addSeparator()
        self.windowMenu.addAction(self.actTile)
        self.windowMenu.addAction(self.actCascade)
        self.windowMenu.addSeparator()
        self.windowMenu.addAction(self.actNext)
        self.windowMenu.addAction(self.actPrevious)
        self.windowMenu.addAction(self.actSeparator)

        windows = self.mdiArea.subWindowList()
        self.actSeparator.setVisible(len(windows) != 0)

        for i, window in enumerate(windows):
            child = window.widget()

            text = "%d %s" % (i + 1, child.getUserFriendlyFilename())
            if i < 9:
                text = '&' + text

            action = self.windowMenu.addAction(text)
            action.setCheckable(True)
            action.setChecked(child is self.getActiveWorkspace())
            action.triggered.connect(self.windowMapper.map)
            self.windowMapper.setMapping(action, window)

    def onWindowNodesToolbar(self):
        if self.nodesDock.isVisible():
            self.nodesDock.hide()
        else:
            self.nodesDock.show()

    def createToolBars(self):
        self.toolbar = QToolBar()
        self.toolbar.setWindowTitle("Execution Toolbar")
        self.compileAction = self.toolbar.addAction("Compile")
        self.compileAction.triggered.connect(lambda: self.Compile())
        self.addToolBar(self.toolbar)

    def Compile(self):
        editor_widget = self.getActiveWorkspace()
        self.running = not self.running
        text = "Stop" if self.running else "Compile"
        self.compileAction.setText(text)
        if editor_widget:
            if self.running:
                editor_widget.Compile()
            else:
                editor_widget.Stop()

    def createStatusBar(self):
        self.statusBar().showMessage("Ready")
        self.status_mouse_pos = QLabel("")
        self.statusBar().addPermanentWidget(self.status_mouse_pos)

    def createMdiChild(self, child_widget=None):
        nodeeditor = child_widget if child_widget is not None else WorkspaceWindow(self)
        subwnd = self.mdiArea.addSubWindow(nodeeditor)
        subwnd.setWindowIcon(self.empty_icon)
        nodeeditor.scene.history.addHistoryModifiedListener(self.updateEditMenu)
        nodeeditor.addCloseEventListener(self.onSubWndClose)
        return subwnd

    def onSubWndClose(self, widget, event):
        existing = self.findMdiChild(widget.filename)
        self.mdiArea.setActiveSubWindow(existing)

        if self.maybeSave():
            event.accept()
        else:
            event.ignore()

    def findMdiChild(self, filename):
        for window in self.mdiArea.subWindowList():
            if window.widget().filename == filename:
                return window
        return None

    def setActiveSubWindow(self, window):
        if window:
            self.mdiArea.setActiveSubWindow(window)
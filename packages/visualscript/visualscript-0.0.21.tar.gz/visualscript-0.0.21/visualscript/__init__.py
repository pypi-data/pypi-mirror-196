def open_as_graph(paths=tuple()):
    import sys
    from PyQt5.QtWidgets import QApplication
    from visualscript.editor.editor_window import EditorWindow

    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    wnd = EditorWindow()
    wnd.show()

    wnd.onFileOpen(paths)

    sys.exit(app.exec_())

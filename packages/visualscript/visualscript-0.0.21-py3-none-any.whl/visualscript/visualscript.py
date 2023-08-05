if __name__ == '__main__':
    import argparse
    import sys
    from PyQt5.QtWidgets import QApplication
    from visualscript.editor.editor_window import EditorWindow

    parser = argparse.ArgumentParser(
        prog="VisualScript",
        description="Open scripts in visual scripting visualscript.editor.",
        epilog="contact: adam.wachowicz@vp.pl")
    parser.add_argument("-f", "--paths", metavar="paths", nargs="+", help="paths to scripts you want to open")

    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    wnd = EditorWindow()
    wnd.show()

    args = parser.parse_args()
    wnd.onFileOpen(args.file_paths)

    sys.exit(app.exec_())
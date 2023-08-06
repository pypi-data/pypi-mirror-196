import json
from PyQt5.QtCore import QUrl, Qt, QPointF
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage, QWebEngineSettings
from PyQt5.QtWidgets import QApplication, QShortcut


class Wrap:
    """
    A module that wraps a local web app for desktop use.

    Args:
        html_file (str): Path to the local HTML file to display.
        title (str, optional): Title to display in the window title bar. Defaults to None.
        icon (str, optional): Path to the icon file to display in the window title bar. Defaults to None.
        width (int, optional): Width of the window in pixels. Defaults to 1024.
        height (int, optional): Height of the window in pixels. Defaults to 768.
        expandable (bool, optional): If True, allow the window to be resized. Defaults to True.
        disable_right_click (bool, optional): If True, disable the context menu when right-clicking on the window. Defaults to False.
        hide_top_bar (bool, optional): If True, hide the top bar of the window. Defaults to False.
        hide_status_bar (bool, optional): If True, hide the status bar of the window. Defaults to False.
        clear_cache (bool, optional): If True, clear the browser cache on startup. Defaults to False.
        disable_javascript (bool, optional): If True, disable JavaScript in the browser. Defaults to False.
        disable_keyboard_shortcuts (bool, optional): If True, disable access to remote and file URLs via keyboard shortcuts. Defaults to False.
    """

    def __init__(self, html_file, title=None, icon=None, width=1024, height=768, expandable=True,
                 disable_right_click=False, hide_top_bar=False, hide_status_bar=False, clear_cache=False,
                 disable_javascript=False, disable_keyboard_shortcuts=False):
        self.app = QApplication([])

        if title:
            self.app.setApplicationDisplayName(title)
        if icon:
            self.app.setWindowIcon(QIcon(icon))

        self.view = QWebEngineView()

        if expandable:
            self.view.setMinimumSize(width, height)
        else:
            self.view.setFixedSize(width, height)

        self.view.setUrl(QUrl.fromLocalFile(html_file))

        self.view.page().runJavaScript("window.onload = function() { window.pyapp = new PyApp(); }")
        self.view.page().javaScriptConsoleMessage = self._console_message

        if disable_right_click:
            self.view.setContextMenuPolicy(Qt.NoContextMenu)

        if hide_top_bar:
            self.view.setWindowFlags(Qt.CustomizeWindowHint | Qt.FramelessWindowHint)

        if hide_status_bar:
            self.view.setStatusBarVisible(False)

        if clear_cache:
            self.view.page().profile().clearAllVisitedLinks()
            self.view.page().profile().clearHttpCache()
            self.view.page().profile().clearAllVisitedLinks()

        if disable_javascript:
            settings = self.view.settings()
            settings.setAttribute(QWebEngineSettings.JavascriptEnabled, False)

        if disable_keyboard_shortcuts:
            self.view.page().settings().setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, False)
            self.view.page().settings().setAttribute(QWebEngineSettings.LocalContentCanAccessFileUrls, False)

    def _console_message(self, level, message, line, source_id):
        if level == 0:  # log
            print(message)

    def _inspect_element(self, x, y):
        element = self.view.page().hitTestContent(QPointF(x, y)).element()
        self.view.page().triggerAction(QWebEnginePage.InspectElement)

    def run(self):
        self.view.show()
        self.app.exec_()

    def call_js_function(self, function_name, *args):
        script = "{}({});".format(function_name, ", ".join(str(arg) for arg in args))
        self.view.page().runJavaScript(script)

    def handle_js_event(self, event_name, handler):
        self.view.page().runJavaScript("window.pyapp.register_event('{}');".format(event_name))
        self.view.page().javaScriptMessageReceived.connect(handler)

    def emit_js_event(self, event_name, *args):
        script = "var event = new CustomEvent('{}', {{ detail: {} }}); window.dispatchEvent(event);".format(event_name,
                                                                                                            json.dumps(
                                                                                                                args))
        self.view.page().runJavaScript(script)

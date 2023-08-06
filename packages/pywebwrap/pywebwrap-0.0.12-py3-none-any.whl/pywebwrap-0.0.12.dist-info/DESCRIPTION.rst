PyWebWrap is a package that allows you to run your web app easily on the desktop.

Supported features:
 - Run local web core files within a desktop wrapper.
 - Customize the window's title, icon, width, height, and other parameters easily.
 - Allow the window to be resizable or fixed in size.
 - Disable right-clicking on the window.
 - Hide the top or status bar of the window.
 - Clear the browser cache on startup.
 - Disable JavaScript in the browser.
 - Disable access to remote and file URLs via keyboard shortcuts.

Currently working on:
 - Handle uploads & downloads to and from the web app.
 - Call JavaScript functions from Python.
 - Handle JavaScript events with Python code.
 - Emit JavaScript events from Python.

Please refer to the docstring for a list of available attributes.

To get started, simply import the `Wrap` class from the `pywebwrap.pywebwrap` module and create an instance with the desired attributes. 
Then, call the `run()` method to start the desktop app.

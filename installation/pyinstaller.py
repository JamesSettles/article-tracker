# Having some pathing issues so I can't run pyinstaller from the command line
import PyInstaller.__main__

PyInstaller.__main__.run([
    'app/open_flask.py',
    '--onefile',
    '--windowed',
    '-n ArticleTracker',
    '--debug=all'
])
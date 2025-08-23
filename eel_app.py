import eel
import sys
import os

# Set the web folder
eel.init('web')

@eel.expose
def get_app_size():
    return {'width': 850, 'height': 520}

if __name__ == '__main__':
    try:
        if sys.platform.startswith('win'):
            # Windows - Chrome app mode
            eel.start('index.html',  # Fixed filename
                     mode='chrome-app',
                     size=(850, 520),  # Updated size
                     position=(100, 100),
                     cmdline_args=[
                         '--disable-web-security',
                         '--disable-features=VizDisplayCompositor',
                         '--app-window-size=850,520',
                         '--window-size=850,520',
                         '--disable-extensions',
                         '--disable-default-apps'
                     ])
        else:
            # Mac/Linux  
            eel.start('index.html',  # Fixed filename
                     size=(850, 520),  # Updated size
                     position=(100, 100))
                     
    except (SystemExit, MemoryError, KeyboardInterrupt):
        # On Windows, this prevents the ugly stack trace on exit
        pass

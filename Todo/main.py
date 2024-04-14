from TodoGUI.GUIMainWindow import GUIMainWindow
from backend.Handler import Handler

if __name__ == '__main__':
    worker = Handler()
    gui = GUIMainWindow(worker)

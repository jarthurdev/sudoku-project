import ctypes
ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
import gui

if __name__ == "__main__":
    gui.mostrar_menu()
import tkinter as tk
from gui import SyntaxHighlighterGUI

if __name__ == "__main__":
    # Ana Tkinter penceresini oluşturun
    root = tk.Tk()
    # SyntaxHighlighterGUI sınıfının bir örneğini oluşturun
    app = SyntaxHighlighterGUI(root)
    # GUI'yi etkileşimli hale getirmek için Tkinter olay döngüsünü başlatın
    app.run()

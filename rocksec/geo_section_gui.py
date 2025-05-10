# rocksec/geo_section_gui.py
import matplotlib
matplotlib.use('TkAgg')

import tkinter as tk
from frontend.gui import build_gui

root = tk.Tk()
root.geometry("800x600")

build_gui(root)

root.mainloop()

from gc import callbacks
from tkinter import ttk
import tkinter as tk


class Toplevel(tk.Toplevel):
    def __init__(self, parent, called_from=None, modal=False, *args, **kwargs):
        super().__init__(parent, **kwargs)
        self.called_from = called_from
        self.modal = modal
        # self.wm_attributes("-disabled", True)         Hang up system when use
        # self.transient(self)        Error:  #_tkinter.TclError: can't make ".!toplevel" its own master
        print('this is toplevel class')
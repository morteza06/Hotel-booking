from distutils.cmd import Command
from tkinter import ttk
import tkinter as tk
from . import widgets as w
from tkinter import *


# sample code
   
class Room_View(tk.Frame):
    def __init__(self, parent, data, callbacks, **kwargs):
        super().__init__(parent, **kwargs)
        self.master=parent
        self.callbacks = callbacks
        self.data = data
        self.Header_label = Label(self, text='Room list that is reserve:')
        self.Header_label.grid( column=0, row=0,  sticky="nw")
        self.refresh_btn= Button(self, text='   Refresh   ', command= self.callbacks['on_refresh_reserve_list'])
        self.refresh_btn.grid( column=10, row=0,  sticky="E")
   
class Room_View_Modal(tk.Tk): #This class create top level frame. I needed because for new result or refresh viewtree in worksapce frame skiped and disabled
    def __init__(self, parent, data, callbacks , **kwargs):
        tk.Tk.__init__(self,parent, **kwargs)
        self.callbacks = callbacks
        self.data = data
        
        self.wm_attributes("-disabled", True)
        self.toplevel_dialog = tk.Toplevel(self)
        self.toplevel_dialog.minsize(800, 600)#form 300*100
        self.toplevel_dialog.transient(self)
        self.toplevel_dialog.protocol("WM_DELETE_WINDOW", self.Close_Toplevel)
        self.toplevel_dialog_yes_button = ttk.Button(self.toplevel_dialog, text='Yes', command=self.Close_Toplevel)
        self.toplevel_dialog_yes_button.pack(side='left', fill='x', expand=True)

        
        columns = ('id','ًroomnumber', 'countbedroom', 'price','description', 'personid', 'startdate', 'enddate', 'pricesum')
        self.treeview = ttk.Treeview(self.toplevel_dialog, columns=columns, height=10,show='headings')

        self.treeview.heading(column='#1', text=' ID ')
        self.treeview.column("#1", minwidth=0, width=30, stretch=False)
        
        self.treeview.heading(column='#2', text='Room Number')
        self.treeview.column("#2", minwidth=0, width=100, stretch=False)

        self.treeview.heading(column='#3', text='Count Bedroom',anchor=tk.CENTER)
        self.treeview.column("#3", minwidth=0, width=100, stretch=True)
        
        self.treeview.heading(column='#4', text='Price')
        self.treeview.column("#4", minwidth=0, width=80, stretch=False)
        
        self.treeview.heading(column='#5', text='Description')
        self.treeview.column("#5", minwidth=0, width=200, stretch=True)
        
        self.treeview.heading(column='#6', text='Person Id')
        self.treeview.column("#6", minwidth=0, width=80, stretch=False)
        
        self.treeview.heading(column='#7', text='Start Date')
        self.treeview.column("#7", minwidth=0, width=80, stretch=False)
        
        self.treeview.heading(column='#8', text='End Date')
        self.treeview.column("#8", minwidth=0, width=80, stretch=False)
        
        self.treeview.heading(column='#9', text='Price Summerize')
        self.treeview.column("#9", minwidth=0, width=130, stretch=False)
        
        # Layout
        self.treeview.pack(side='left', fill='x', expand=True)
        self.load_records()

    def Close_Toplevel(self):
        # IMPORTANT!
        self.wm_attributes("-disabled", False) # IMPORTANT!
        self.toplevel_dialog.destroy()
        # Possibly not needed, used to focus parent window again
        self.deiconify() 
    
    def load_records(self):
        print('data.items exists :',self.data.items())
        for key, record in self.data.items():
            self.treeview.insert('', 'end', iid=key, open=False, text='Room ID: {}'.format(key),
                                values =[ record['id'], record['roomnumber'], record['countbedroom'], record['price'],\
                                record['description'], record['personid'],  record['startdate'], record['enddate'], record['pricesum']])
            
            
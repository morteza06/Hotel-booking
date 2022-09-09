from tkinter import ttk
import tkinter as tk
from . import widgets as w

# sample code


class Room_View(tk.Frame):
    def __init__(self, parent, data, callbacks, **kwargs):
        super().__init__(parent, **kwargs)
        self.data = data
        columns = ('id','ًroomnumber', 'countbedroom', 'price','description', 'personid', 'startdate', 'enddate', 'pricesum')
        
        self.treeview = ttk.Treeview(self, columns=columns, height=10,show='headings')
        
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
        self.treeview.grid(row=0, column=0)
        self.load_records()

    def load_records(self):
        print('data.items exists :',self.data.items())
        for key, record in self.data.items():
            self.treeview.insert('', 'end', iid=key, open=False, text='Room ID: {}'.format(key),
                                values =[ record['id'], record['roomnumber'], record['countbedroom'], record['price'],\
                                record['description'], record['personid'],  record['startdate'], record['enddate'], record['pricesum']])   
   

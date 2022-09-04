from tkinter import ttk
import tkinter as tk
from . import widgets as w

# sample code


class Room_View(tk.Frame):
    def __init__(self, parent, data, callbacks, **kwargs):
        super().__init__(parent, **kwargs)
        self.data = data
        self.treeview = ttk.Treeview(self, columns=('id','ًroomnumber', 'countbedroom', 'price','description'))
        self.treeview.heading('id', text='Id')
        self.treeview.heading('roomnumber', text='ًRoomNumber')
        self.treeview.heading('countbedroom', text='CountBedroom')
        self.treeview.heading('price', text='Price')
        self.treeview.heading('description', text='Description')
        self.treeview.heading('personid', text='PersonId')
        self.treeview.heading('startdate', text='StartDate')
        self.treeview.heading('enddate', text='Enddate')
        self.treeview.heading('pricesum', text='PriceSum')
        # Layout
        self.treeview.grid(row=0, column=0)
        self.load_records()

    def load_records(self):
        for key, record in self.data.items():
            self.treeview.insert('', 'end', iid=key, text='Room ID: {}'.format(key),
                                values =[record['id'], record['ًroomnumber'], record['countBedroom'], record['price'],\
                                record['description'], record['personid'], record['enddate'], record['pricesum']])   
from tkinter import ttk
import tkinter as tk
# from . import widgets as w

class RoomAddForm(tk.Frame):
    def __init__(self, parent, fields, callbacks, *args, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.callbacks = callbacks
        self.input = {}

        # input
        self.roomnumber_label = ttk.Label(self, text=fields['roomnumber']['label'])
        self.roomnumber_var = tk.StringVar()
        self.input['roomnumber'] = ttk.Entry(self, textvariable= self.roomnumber_var)
        
        self.countbedroom_label = ttk.Label(self, text=fields['countbedroom']['label'])
        self.countbedroom_var = tk.StringVar()
        self.input['countbedroom'] = ttk.Entry(self, textvariable= self.countbedroom_var)
        
        self.price_label = ttk.Label(self, text=fields['price']['label'])
        self.price_var = tk.StringVar()
        self.input['price'] = ttk.Entry(self, textvariable= self.price_var)
        
        self.description_label = ttk.Label(self, text=fields['description']['label'])
        self.description_var = tk.StringVar()
        self.input['description'] = ttk.Entry(self, textvariable= self.description_var)
        
        self.save_btn = ttk.Button(self, text='Save',
                                   command=self.callbacks['on_save_room_form'])
        # self.close_btn = ttk.Button(self, text='Close',
        #                            command=self.callbacks['on_close_Toplevel'])
                                   
        # Layout
        self.roomnumber_label.grid(column=0, row=0)
        self.input['roomnumber'].grid(column=1, row=0)
        self.countbedroom_label.grid(column=0, row=1)
        self.input['countbedroom'].grid(column=1, row=1)
        self.price_label.grid(column=0, row=2)
        self.input['price'].grid(column=1, row=2)
        self.description_label.grid(column=0, row=3)
        self.input['description'].grid(column=1, row=3)
        self.save_btn.grid(column=1, row=4)
        # self.close_btn.grid(column=1, row=4)
        
    def get(self)-> dict:
        data = {
            # 'id':self.id_var.get(),
            'roomnumber': self.roomnumber_var.get(),
            'countbedroom': self.countbedroom_var.get(),
            'price':self.price_var.get(),
            'description':self.description_var.get()
        }
        return data
    def on_roomadd_saved(self):
        print('somone saved a Room add ')
        
class RoomSelectForm(tk.Frame):
    def __init__(self, parent, fields, callbacks, *args, **kwargs):
        super().__init__(parent, **kwargs)
        self.callbacks = callbacks
        # self.fields = {}
        # Labels
        self.roomnumber_label = ttk.Label(self, text=fields['roomnumber']['label'])\
                                        .grid(column=0, row=1)
        self.selected_room = tk.StringVar(self)
        self.roomnumber_combo = ttk.Combobox(self, values=fields['roomnumber']['label'], 
                                            textvariable=self.selected_room,
                                            state='readonly',
                                            width=80).grid(column=0, row=2)
    
    
   
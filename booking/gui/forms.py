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
        
        # Layout
        self.roomnumber_label.grid(column=0, row=0)
        self.input['roomnumber'].grid(column=1, row=0)
        self.countbedroom_label.grid(column=0, row=1)
        self.input['countbedroom'].grid(column=1, row=2)
        self.price_label .grid(column=0, row=2)
        self.input['price'].grid(column=1, row=1)
        self.description_label.grid(column=0, row=3)
        self.input['description'].grid(column=1, row=3)
        self.save_btn.grid(column=0, row=4)
        
        
    def get(self):
        data = {
            'roomnumber': self.roomnumber_var.get(),
            'countbedroom': self.countbedroom_var.get(),
            'price':self.price_var.get(),
            'description':self.description_var.get()
        }
        return data

    

# class RoomSelectForm(tk.Frame):
#     def __init__(self, parent, fields, callbacks, *args, **kwargs):
#         super().__init__(parent, **kwargs)
#         self.callbacks = callbacks
#         self.fields = {}
#         # Lookups and input
#         self.room_lookups = fields['id']['values']
#         self.fields['roomnumber'] = w.FormField(self, fields['roomnumber'], w.Combobox,
#                                                 input_kwargs={'lookups': self.room_lookups})
        
#         self.name_var = tk.StringVar()
#         self.fields['price'] = w.FormField(self, fields['price'], w.CharEntry,
#                                           input_kwargs={'textvariable':self.name_var})
#         self.save_btn = ttk.Button(self, text='Save', command=self.callbacks['on_save_roommodel_form'])
#         # Layout
#         self.fields['roomnumber'].grid(column=0, row=1)
#         self.fields['price'].grid(column=1, row=1)
#         self.save_btn.grid(column=1, row=2)

#         # Bindings
#         # def 
        
#         # Layout
    
    
#     def get(self):
#         roomnumber = self.fields['roomnumber'].get()
#         roomnumber_id = self.roomnumber_lookups[roomnumber]
#         price = self.fields['price'].get()
#         data = {'room_id':roomnumber_id, 'price':price}
        
        
# class RoomCalcForm(tk.Frame):
#     def __init__(self, parent, fields, callbacks, *args, **kwargs):
#         super().__init__(parent, **kwargs)
#         self.callbacks = callbacks
#         self.fields = {}
        

#         # Bindings
        
        
#         # Layout
    
    
# class RoomModelForm(tk.Frame):
#     def __init__(self, parent, fields, callbacks, *args, **kwargs):
#         super().__init__(parent, **kwargs)
#         self.callbacks = callbacks
#         self.fields = {}
        # Input
        
        
        
        
        # Layout
        
        
        # self.fields['roomnumber'] = w.FormField(self, fields['roomnumber'], widget_cls=w.Combobox,
                                                #   input_kwargs={'lookups': self.roomnumber_lookups})
        #   self.roomnumber_lookups = fields['roomnumber']['values']
        # Bindings
        # self.input['roomnumber'].input.bind('<<ComboboxSelected>>', self.on_roomnumber_selected)
        
        
    # def on_roomnumber_selected(self, event):
    #     roomnum = self.fields['roomnumber'].get()
    #     reserve_lookups = self.callbacks['filter_room_by_reserve'](roomnum)
    #     self.fields['reserve'].lookups = reserve_lookups
    #     self.fields['reserve'].input.configure(values=['', *sorted(reserve_lookups)])
    #     self.fields['reserve'].input.set('')
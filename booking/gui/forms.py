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
        
        self.save_btn = ttk.Button(self, text='     Add Room    ',
                                   command=self.callbacks['on_save_room_form'])
                                 
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
            'roomnumber': self.roomnumber_var,
            'countbedroom': self.countbedroom_var,
            'price':self.price_var,
            'description':self.description_var
        }
        return data
    
    def reset(self):
        self.roomnumber_var = None
        self.countbedroom_var = None
        self.price_var = None
        self.description_var = None
        
    def on_roomadd_saved(self):
        print('somone saved a Room add ')

class ReserveInfoAddForm(tk.Frame):
    def __init__(self, parent, fields, callbacks, *args, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.callbacks = callbacks
        self.input = {}

        # Labels
        self.roomid_label = ttk.Label(self, text=fields['roomid']['label'])
        # Input
        self.roomid_var = tk.StringVar()
        self.input['roomid'] = ttk.Entry(self, textvariable= self.roomid_var)
                                        
        # Labels
        self.personid_label = ttk.Label(self, text=fields['personid']['label'])
        # Input
        self.personid_var = tk.StringVar()
        self.input['personid'] = ttk.Entry(self, textvariable= self.personid_var)
        
        # Labels
        self.startdate_label = ttk.Label(self, text=fields['startdate']['label'])
        # Input
        self.startdate_var = tk.StringVar()
        self.input['startdate'] = ttk.Entry(self, textvariable= self.startdate_var)
        
        # Labels
        self.enddate_label = ttk.Label(self, text=fields['enddate']['label'])
        # Input
        self.enddate_var = tk.StringVar()
        self.input['enddate'] = ttk.Entry(self, textvariable= self.enddate_var)
        # Labels

        self.pricesum_label = ttk.Label(self, text=fields['pricesum']['label'])
        # Input
        self.pricesum_var = tk.StringVar()
        self.input['pricesum'] = ttk.Entry(self, textvariable= self.pricesum_var)
        
        self.save_btn = ttk.Button(self, text='Add Reservation ',
                                   command=self.callbacks['on_save_reserve_form'])
        # self.close_btn = ttk.Button(self, text='c',
        #                            command=self.callbacks['on_close_Toplevel'])

        # Layout
        self.roomid_label.grid(column=0, row=0)
        self.input['roomid'].grid(column=1, row=0)
        self.personid_label.grid(column=0, row=1)
        self.input['personid'].grid(column=1, row=1)
        self.startdate_label.grid(column=0, row=2)
        self.input['startdate'].grid(column=1, row=2)
        self.enddate_label.grid(column=0, row=3)
        self.input['enddate'].grid(column=1, row=3)
        self.pricesum_label.grid(column=0, row=4)
        self.input['pricesum'].grid(column=1, row=4)
        
        self.save_btn.grid(column=1, row=5)
        # self.close_btn.grid(column=1, row=4)
        
    def get(self)-> dict:
        data = {
            # 'id':self.id_var.get(),
            'roomid': self.roomid_var,
            'personid': self.personid_var,
            'startdate':self.startdate_var,
            'enddate':self.enddate_var,
            'pricesum':self.pricesum_var,
        }
        return data
    
    def reset(self):
        self.roomid_var = None
        self.personid_var  = None
        self.startdate_var  = None
        self.enddate_var  = None
        self.pricesum_var = None
        
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
    
class SearchForm(tk.Frame):
    def __init__(self, parent, fields, callbacks, *args, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.callbacks = callbacks
        self.input = {}
        self.Search_By = None
        # Input =>Text for Search 
        self.searchtxt_label = ttk.Label(self, text='Insert Text for search:')
        self.searchtxt_var = tk.StringVar()
        self.input['searchtext'] = ttk.Entry(self, textvariable= self.searchtxt_var)
        # Labels
        self.searchby_label = ttk.Label(self, text='Select this Field for search:')
        self.selected_search_var = tk.StringVar(self)
        self.search_combo = ttk.Combobox(self, values=fields['searchby']['label'], 
                                            textvariable=self.selected_search_var,
                                            state='readonly',width=150)
        self.search_combo.bind('<<ComboboxSelected>>', self.on_searchby_selected)
        self.search_combo['values']= ('Room_Number','Count_Bedroom_exists','Price')
        self.search_combo.current(0) #set the selected item

        # Select => field for search
        self.save_btn = ttk.Button(self, text='      Search     ',
                                   command=self.callbacks['on_search_form'])
        # Layout
        self.searchby_label.grid(column=0, row=0)
        self.search_combo.grid(column=1, row=0)
        self.searchtxt_label.grid(column=0, row=1)
        self.input['searchtext'].grid(column=1, row=1)

        self.save_btn.grid(column=1, row=4)
        
    def on_searchby_selected(self, event):
        return (self.search_combo.get())
        
    def get(self)-> dict:
        data = {
            # 'id':self.id_var.get(),
            'searchby':self.selected_search_var,
            'searchtext':self.searchtxt_var,
        }
        return data
    
    def reset(self):
        self.searchtext_var = None
        
    def on_roomadd_saved(self):
        print('somone saved a Room add ')       
   
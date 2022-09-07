from dataclasses import field
from tkinter import ttk
import tkinter as tk

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
    searchtext_var=''
    searchby_var=''
    def __init__(self, parent, fields, callbacks): 
        global searchtext_var
        global searchby_var
        
        super().__init__(parent)
        self.callbacks = callbacks
        self.fields = fields
        self.fields.clear()
        print('===>',self.fields.items())
        # Input =>Text for Search 
        self.searchtxt_label = ttk.Label(self, text='Insert Text for search:')
        self.searchtxt_var = tk.StringVar()
        self.searchtext = ttk.Entry(self, textvariable= self.searchtxt_var)
        # Labels
        self.selected_search_var = tk.StringVar(self)
        self.searchby_label = ttk.Label(self, text='Select this Field for search:')
        self.searchby = ttk.Combobox(self,textvariable=self.selected_search_var,
                                    state='readonly',width=20)
        self.searchby.bind('<<ComboboxSelected>>', self.on_searchby_selected)
        self.searchby['values']=('','roomnumber','countbedroom','price')
        self.searchby.current(0) #set the selected item
        
        self.save_btn = ttk.Button(self, text='      Search     ',
                                   command=self.callbacks['on_search_form'])
        # Layout
        self.searchtext.grid(column=1, row=0)
        self.searchtxt_label.grid(column=0, row=0)
        self.searchby_label.grid(column=0, row=1)
        self.searchby.grid(column=1, row=1)

        self.save_btn.grid(column=1, row=4)

    def on_searchby_selected(self, event):
        searchtext_var = str(self.searchtext.get())
        searchby_var = str(self.searchby.get())
        
        self.fields.clear()#empty dictionary
        self.fields['searchtext']='label'
        self.fields[searchtext_var]='values'
        self.fields['searchby']='label'#  add to dict
        self.fields[searchby_var]='values'
        
        print('=>>>>>',self.searchtext.get())
        print('=>>>>>',self.searchby.get())
        
        # self.fields[ ]='values'
        
    def get(self)-> dict:
        print('fields1===',self.fields.items())
        data = self.fields.items()
        searchtext_var = str(self.searchtext.get())
        searchby_var = str(self.searchby.get())
        print('get===',searchtext_var)
        print('get===',searchby_var)
        
        # self.fields.clear()#empty dictionary
        # self.fields['searchtext']='label'
        # self.fields[searchtext_var]='values'
        # self.fields['searchby']='label'#  add to dict
        # self.fields[searchby_var]='values'
        print('fields2===',self.fields.items())
        print('fields2===',type(data))
        
        return data
    def reset(self)->None:
        searchtext_var=''
        searchby_var=''
        self.searchtext.delete(0,'end')
        self.searchby.current(0)
        
    def show(self):
        pass
    
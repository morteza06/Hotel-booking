from tkinter import ttk
import tkinter as tk
from tkinter import *
from tkinter.font import BOLD

class RoomForm(tk.Frame):
    def __init__(self, parent, fields, data,callbacks, *args, **kwargs):
        super().__init__(parent, **kwargs)
        self.callbacks = callbacks
        self.data = data
        #require data variables
        self.id_var= int()
        self.roomnumber_var = StringVar()
        self.countbedroom_var = StringVar()
        self.price_var = StringVar()
        self.txt_Description = StringVar()
        
        self.search_by = StringVar()
        self.search_txt = StringVar()
        
        
        self.Header_label = Label(self, text='Insert room information:')
        self.roomnumber_label = Label(self, text='Room Number:')
        self.roomnumber = Entry(self, textvariable= self.roomnumber_var)
        self.countbedroom_label = Label(self, text='Count Bedroom:')
        self.countbedroom = Entry(self, textvariable= self.countbedroom_var)
        self.price_label = Label(self, text='Price:')
        self.price = Entry(self, textvariable= self.price_var)
        self.description_label = Label(self, text='Description:')
        self.txt_Description = Text(self, width=30, height=4)
        # Layout
        self.Header_label.grid( column=0, row=0,  sticky="nw")
        self.roomnumber_label.grid( column=0, row=1, sticky="ne")
        self.countbedroom_label.grid(column=0, row=2, sticky="ne")
        self.price_label.grid(column=0, row=3, sticky="ne")
        self.description_label.grid(column=0, row=4, sticky="ne")
        
        self.roomnumber.grid(column=1, row=1,  sticky="nw")
        self.countbedroom.grid(column=1, row=2,  sticky="nw")
        self.price.grid(column=1, row=3,  sticky="nw")
        self.txt_Description.grid(column=1, row=4,  rowspan=3, sticky="nw")
        # Button 
        self.add_btn = Button(self, text='Add', width=8, command=self.callbacks['on_add_room'])\
            .grid(column=2, row=6,columnspan=2, sticky="W")
        self.update_btn = Button(self, text='Update', width=8, command=self.callbacks['on_update_room'])\
            .grid(column=2, row=6, sticky="N",padx=2)
        self.delete_btn = Button(self, text='Delete', width=8, command=self.callbacks['on_delete_room'],bg='red')\
            .grid(column=2, row=6,columnspan=2,sticky="E")
        self.clear_btn = Button(self, text='Clear', width=8, command=self.callbacks['on_clear_room'])\
            .grid(column=3, row=6, columnspan=2 , sticky="E",padx=2)
        self.show_all_btn = Button(self, text='Show All', width=8, command=self.callbacks['on_showall_room'])\
            .grid(column=5, row=6, sticky="W",padx=2)

        self.page_label = Label(self, text='Room Detail').grid(column=0, row=7, sticky="w")
        # ===== Search box  =====  
        
        lbl_search = Label(self, width=20, text="Search By:") 
        combo_search = ttk.Combobox(self, textvariable=self.search_by, state="readonly" )
        combo_search['values']=('roomnumber','countbedroom','price')
        
        lbl_search.grid(row=8, column=0, padx=4, sticky="w")
        combo_search.grid(row=8, column=1,  sticky="w")
        
        self.txt_search = Entry(self, textvariable=self.search_txt, font=("times new roman", 13), bd=5, relief=GROOVE)\
                            .grid(row=8, column=2,  sticky="w")
        self.searchbtn = Button(self, text="Search", width=8, command=self.callbacks['on_search_room_data'])\
                            .grid(row=8, column=4,  sticky="e")
        
        #=== Tree view Table 
        scroll_x = Scrollbar(self, orient=HORIZONTAL)
        scroll_y = Scrollbar(self, orient=VERTICAL)

        self.Room_Table = ttk.Treeview(self, columns=("id","roomnumber", "countbedroom","price","descrition"), xscrollcommand = scroll_x.set, yscrollcommand = scroll_y.set)
        self.Room_Table.grid(column=0, row=9,columnspan=6,sticky='w') 
                           
        scroll_x.config(command=self.Room_Table.xview)
        scroll_y.config(command=self.Room_Table.yview)
        self.Room_Table.heading(column='#1', text="ID")
        self.Room_Table.heading(column='#2', text="Room Number")
        self.Room_Table.heading(column='#3', text="Count Bedroom")
        self.Room_Table.heading(column='#4', text="Price")
        self.Room_Table.heading(column='#5', text="Description")
        self.Room_Table['show']='headings' # removing extra index col at begining

        #setting up widths of cols
        self.Room_Table.column("#1", width=40)
        self.Room_Table.column("#2", width=100)
        self.Room_Table.column("#3", width=110)
        self.Room_Table.column("#4", width=120)
        self.Room_Table.column("#5", width=350)
        # self.Room_Table.pack(fill=BOTH, expand=1) #fill both is used to fill cols around the frame
        self.Room_Table.bind("<ButtonRelease-1>", self.get_cursor)# this is an event to select row 
         #to display data in grid
        if self.data != {}: 
            self.fetch_data(data)
            
        
    def get_cursor(self, evnt):
        cursor_row = self.Room_Table.focus()
        content = self.Room_Table.item(cursor_row)
        row = content['values']
        self.id_var=row[0]
        self.roomnumber_var.set(row[1])
        self.countbedroom_var.set(row[2])
        self.price_var.set(row[3])
        self.txt_Description.delete('1.0', END)
        self.txt_Description.insert('END', row[3])
    
    def get(self)-> dict:
        data = {
            'id': self.id_var,
            'roomnumber': self.roomnumber_var.get(),
            'countbedroom': self.countbedroom_var.get(),
            'price':self.price_var.get(),
            'description':self.txt_Description.get('1.0','end'),
        }
        return data
    
    def clear(self):
        self.roomnumber_var.set("")
        self.countbedroom_var.set("")
        self.price_var.set("")
        self.txt_Description.set("")
        self.roomnumber.delete('0', 'end')
        self.countbedroom.delete(0, 'end')
        self.price.delete(0, 'end')
        self.txt_Description.delete('1.0', tk.END)
        return None
    
    def fetch_data(self,data):
        res_list = data.values()
        new_value = list(res_list)
        print('data==Dic===to==list== :', new_value)
        for key, record in data.items():
            self.Room_Table.insert('','end', iid=key, open=False, text='Room ID: {}'.format(key),
            values =[ record['id'], record['roomnumber'], record['countbedroom'], record['price'], record['description']])   
   

class ReserveForm(tk.Frame):
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
        
        self.add_btn = ttk.Button(self, text='Add',
                                   command=self.callbacks['on_add_reserve_form'])
        self.update_btn = ttk.Button(self, text='Update',
                                   command=self.callbacks['on_udate_reserve_form'])

        # Layout
        self.roomid_label.grid(column=0, row=0)
        self.input['roomid'].grid(column=0, row=1)
        self.personid_label.grid(column=0, row=2)
        self.input['personid'].grid(column=0, row=3)
        self.startdate_label.grid(column=0, row=4)
        self.input['startdate'].grid(column=0, row=5)
        self.enddate_label.grid(column=0, row=6)
        self.input['enddate'].grid(column=0, row=7)
        self.pricesum_label.grid(column=0, row=8)
        self.input['pricesum'].grid(column=0, row=9)
        
        self.add_btn.grid(column=0, row=10 , sticky='E',padx=2)
        self.update_btn.grid(column=0, row=10, sticky='W', padx=2)
        
    def get(self)-> dict:
        data = {
            # 'id':self.id_var.get(),
            'roomid': self.roomid_var.get(),
            'personid': self.personid_var.get(),
            'startdate':self.startdate_var.get(),
            'enddate':self.enddate_var.get(),
            'pricesum':self.pricesum_var.get(),
        }
        return data
    
    def reset(self):
        self.roomid_var = None
        self.personid_var  = None
        self.startdate_var  = None
        self.enddate_var  = None
        self.pricesum_var = None

class PersonForm(tk.Frame):

    data={}
    def __init__(self, parent, callbacks, *args, **kwargs): 
        pass
    
class UserTypeForm(tk.Frame):
    data={}
    def __init__(self, parent, callbacks, *args, **kwargs): 
        pass
    
class User(tk.Frame):
    data={}
    def __init__(self, parent, callbacks, *args, **kwargs): 
        pass
    



# showall
# def add1():
#     global count

#     get_name = txt_name.get()
#     get_ref = txt_ref.get()
#     get_age = txt_age.get()
#     get_email = txt_email.get()

#     row = (get_name, get_ref, get_age, get_email)
#     data_list.append(row)
#     count += 1
#     tree_table.insert(parent='', index='end', iid=count, text=f'{count}', values=row)

#     txt_name.delete(0, END)
#     txt_ref.delete(0, END)
#     txt_age.delete(0, END)
#     txt_email.delete(0, END)

#     print(data_list)
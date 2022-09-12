from tkinter import messagebox, ttk
import tkinter as tk
from tkinter import *
from tkinter.font import BOLD
from turtle import width

class RoomForm(tk.Frame):   
    def __init__(self, parent, data ,callbacks, *args, **kwargs):
        super().__init__(parent, **kwargs)
        self.callbacks = callbacks
        self.data = {}
        # print('Open page with data init=   ',data.items())
        #require data variables
        # self.id_var= int()
        self.id_var=0
        self.searchby_var=''
        self.roomnumber_var = StringVar()
        self.countbedroom_var = StringVar()
        self.price_var = StringVar()
        self.description_var = StringVar()
        
        self.search_by_var = StringVar()
        self.search_txt_var = StringVar()
        
        
        self.Header_label = Label(self, text='Insert room information:')
        self.roomnumber_label = Label(self, text='Room Number:')
        self.roomnumber = Entry(self, textvariable= self.roomnumber_var)
        self.countbedroom_label = Label(self, text='Count Bedroom:')
        self.countbedroom = Entry(self, textvariable= self.countbedroom_var)
        self.price_label = Label(self, text='Price:')
        self.price = Entry(self, textvariable= self.price_var)
        self.description_label = Label(self, text='Description:')
        self.description = Entry(self,  textvariable= self.description_var)
        # Layout
        self.Header_label.grid( column=0, row=0,  sticky="nw")
        self.roomnumber_label.grid( column=0, row=1, sticky="ne")
        self.countbedroom_label.grid(column=0, row=2, sticky="ne")
        self.price_label.grid(column=0, row=3, sticky="ne")
        self.description_label.grid(column=0, row=4, sticky="ne")
        
        self.roomnumber.grid(column=1, row=1,  sticky="nw")
        self.countbedroom.grid(column=1, row=2,  sticky="nw")
        self.price.grid(column=1, row=3,  sticky="nw")
        self.description.grid(column=1, row=4, columnspan=3, ipadx=90, sticky="nw")
        # Button 
        self.add_btn = Button(self, text='Add',  width=8, command=self.callbacks['on_add_room'])
        self.update_btn = Button(self, text='Update', width=8, command=self.callbacks['on_update_room'])
        self.delete_btn = Button(self, text='Delete', width=8, command=self.callbacks['on_delete_room'],bg='red')
        self.clear_btn = Button(self, text='Clear', width=8, command=self.callbacks['on_clear_room'])
        self.show_all_btn = Button(self, text='Show All', width=8, command=self.callbacks['on_showall_room'])
        
        # layout
        self.add_btn.grid(column=1, row=5,columnspan=2, sticky="W")
        self.update_btn.grid(column=1, row=5, sticky="E",padx=2)
        self.delete_btn.grid(column=2, row=5,columnspan=2,sticky="W")
        self.clear_btn.grid(column=2, row=5, columnspan=2 , sticky="N",padx=2)
        self.show_all_btn.grid(column=3, row=5, sticky="W",padx=2)
        #  ===== show list
        self.page_label = Label(self, text='Room Detail')
        self.page_label.grid(column=0, row=6, sticky="w")
        # ===== Search box  =====  
        
        self.lbl_search = Label(self, width=20, text="Search By:") 
        self.__searchby_list = ttk.Combobox(self,takefocus=1, textvariable=self.search_by_var, state="readonly" )
        self.__searchby_list['values']=('','RoomNumber','CountBedroom','Price[>=]YourEnter','Price[<=]YourEnter')
        self.__searchby_list.bind('<<ComboboxSelected>>', self._on_combo_change)
        
        self.lbl_search.grid(row=8, column=0, padx=4, sticky="w")
        self.__searchby_list.grid(row=8, column=1,  sticky="w")
        
        self.txt_search = Entry(self, textvariable=self.search_txt_var, font=("times new roman", 13),validate='key', bd=5, relief=GROOVE)
        self.txt_search.grid(row=8, column=2,  sticky="w")
        self.searchbtn = Button(self, text="Search", width=8, command=self.callbacks['on_search_room_data'])
        self.searchbtn.grid(row=8, column=3,  sticky="E")
                            
       
        
        

    def _on_combo_change(self,event):
        searchby_var= self.search_by_var.get()
        print('===>', searchby_var)
        print('===>',self.search_txt_var.get())
            
    def get_cursor(self, evnt):  # specific id of table
        try:
            cursor_row = self.Room_Table.focus()
            content = self.Room_Table.item(cursor_row)
            self.row = content['values']
            self.id_var = self.row[0]
            
        except Exception as e:
            messagebox.showerror('warning','Row selection is out ranage.\n{}'.format(e))
            raise
    
    def get(self)-> dict:
        data = {
            'id': self.id_var,
            'roomnumber': self.roomnumber_var.get(),
            'countbedroom': self.countbedroom_var.get(),
            'price':self.price_var.get(),
            'description':self.description_var.get(),
            'searchby': self.searchby_var,
            'searchtext': self.search_txt_var.get()
        }
        return data
    
    def set(self):# show data to entry== for update
        print('======================')
        self.roomnumber_var.set(self.row[1])
        self.countbedroom_var.set(self.row[2])
        self.price_var.set(self.row[3])
        self.description_var.set(self.row[4])
        return
    
    def clear(self):
        self.roomnumber_var.set("")
        self.countbedroom_var.set("")
        self.price_var.set("")
        self.txt_Description=""
        self.roomnumber.delete('0', 'end')
        self.countbedroom.delete(0, 'end')
        self.price.delete(0, 'end')
        
        self.description_var.set("")   
        self.search_txt_var.set("")
        self.search_by_var.set("")
        
    def add_row(self,id):
        print('========add-row',)
        self.Room_Table.insert('','end', values =(id, self.roomnumber_var.get() ,self.countbedroom_var.get() ,\
                                                self.price_var.get() ,self.description_var.get() ))   
            
    def delete_row(self):#okey
        selected_items = self.Room_Table.selection()
        for selected_item in selected_items:
            self.Room_Table.delete(selected_item)
        return self
    
    def delete_all_row_tree(self):
        print('delete all rows========')
        # self.Room_Table.delete(*self.Room_Table.get_children())
        for row in self.Room_Table.get_children():
            self.Room_Table.delete(*row)
        return (self.Room_Table)
    
    def fetch_data1(self,data):
        
         #=== Tree view Table 
        scroll_x = Scrollbar(self, orient=HORIZONTAL)
        scroll_y = Scrollbar(self, orient=VERTICAL)

        self.Room_Table = ttk.Treeview(self, columns=("id","roomnumber", "countbedroom","price","descrition"), xscrollcommand = scroll_x.set, yscrollcommand = scroll_y.set)
        self.Room_Table.grid(column=0, row=7, columnspan=6,sticky='w') 
                           
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
        self.data=data
        #to display data in grid
        try:
            if self.data != {}:
                for key, record in self.data.items():
                    self.Room_Table.insert('', 'end', iid=key, open=False, text='Room ID: {}'.format(key),
                                        values =[ record['id'], record['roomnumber'], record['countbedroom'], record['price'], record['description']])   
        except Exception as e:
            messagebox.showerror(title='Error',message='The Show data not avaiable, Error is about{}',detail=str(e))
        else:
            return
        finally:
            print('finall in fetch layout in init')
    
    def fetch_data2(self,data):
           #=== Tree view Table 
        scroll_x = Scrollbar(self, orient=HORIZONTAL)
        scroll_y = Scrollbar(self, orient=VERTICAL)

        self.Room_Tablex = ttk.Treeview(self, columns=("id","roomnumber", "countbedroom","price","descrition"), xscrollcommand = scroll_x.set, yscrollcommand = scroll_y.set)
        self.Room_Tablex.grid(column=0, row=10, columnspan=6,sticky='w') 
                           
        scroll_x.config(command=self.Room_Tablex.xview)
        scroll_y.config(command=self.Room_Tablex.yview)
        self.Room_Tablex.heading(column='#1', text="ID")
        self.Room_Tablex.heading(column='#2', text="Room Number")
        self.Room_Tablex.heading(column='#3', text="Count Bedroom")
        self.Room_Tablex.heading(column='#4', text="Price")
        self.Room_Tablex.heading(column='#5', text="Description")
        self.Room_Tablex['show']='headings' # removing extra index col at begining

        #setting up widths of cols
        self.Room_Tablex.column("#1", width=40)
        self.Room_Tablex.column("#2", width=100)
        self.Room_Tablex.column("#3", width=110)
        self.Room_Tablex.column("#4", width=120)
        self.Room_Tablex.column("#5", width=350)
        # self.Room_Table.pack(fill=BOTH, expand=1) #fill both is used to fill cols around the frame
        self.Room_Tablex.bind("<ButtonRelease-1>", self.get_cursor)# this is an event to select row
        self.data=data
         #to display data in grid
        try:
            if self.data != {}:
                for key, record in self.data.items():
                    self.Room_Tablex.insert('', 'end', iid=key, open=False, text='Room ID: {}'.format(key),
                                        values =[ record['id'], record['roomnumber'], record['countbedroom'], record['price'], record['description']])   
        except Exception as e:
            messagebox.showerror(title='Error',message='The Show data not avaiable, Error is about{}',detail=str(e))
        else:
            return
        finally:
            print('finall in fetch layout')
        
    def refresh_insert_data_tree(self,data):
        print('I am here')
        self.Room_Table.delete()
        # try:
        #     print('Refresh data to insert tree==Dic===items:', self.data.items())
        #     for key, record in self.data.items():
        #         self.Room_Table.insert('', 'end', iid=key, open=False, text='Room ID: {}'.format(key),
        #                             values =[ record['id'], record['roomnumber'], record['countbedroom'], record['price'], record['description']])   
        # except Exception as e:
        #     messagebox.showerror(title='Error',
        #                          message='in Show data to tree not avaiable, Error is about{}',
        #                          detail=str(e))
        #     raise
        # finally:
        return
    def onValidationNumber(self):
        pass
    
    def switch(self):
        self.add_btn.config(state = 'disabled')
        
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
        self.roomid_var = 0
        self.personid_var  = 0
        self.startdate_var  = ''
        self.enddate_var  = ''
        self.pricesum_var = 0

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
    

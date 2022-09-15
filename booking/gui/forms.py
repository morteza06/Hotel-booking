from tkinter import messagebox, ttk
import tkinter as tk
from tkinter import *
from tkinter.font import BOLD
from tokenize import String
from turtle import width
from tkcalendar import Calendar, DateEntry

class RoomForm(tk.Frame):   
    def __init__(self, parent, data ,callbacks, *args, **kwargs):
        super().__init__(parent, **kwargs)
        self.callbacks = callbacks
        self.data = {}
        # print('Open page with data init=   ',data.items())
        #require data variables
        # self.id_var= int()
        self.id_var=0
        
        self.roomnumber_var = StringVar()
        self.countbedroom_var = StringVar()
        self.price_var = StringVar()
        self.description_var = StringVar()
        
        vcmd = (self.register(self.validate))
        self.Header_label = Label(self, text='Room information:')
        self.roomnumber_label = Label(self, text='Room Number:')
        self.roomnumber = Entry(self, validate = 'all',  validatecommand = (vcmd, '%P'), textvariable= self.roomnumber_var)
        self.countbedroom_label = Label(self, text='Count Bedroom:')
        self.countbedroom = Entry(self, validate = 'all',  validatecommand =(vcmd, '%P'), textvariable= self.countbedroom_var)
        self.price_label = Label(self, text='Price:')
        self.price = Entry(self, validate = 'all',  validatecommand = (vcmd, '%P'), textvariable= self.price_var)
        self.description_label = Label(self, text='Description:')
        self.description = Entry(self,  textvariable= self.description_var)
        # Layout label
        self.Header_label.grid( column=0, row=0,  sticky="nw")
        self.roomnumber_label.grid( column=0, row=1, sticky="ne")
        self.countbedroom_label.grid(column=0, row=2, sticky="ne")
        self.price_label.grid(column=0, row=3, sticky="ne")
        self.description_label.grid(column=0, row=4, sticky="ne")
        # Layout textbox
        self.roomnumber.grid(column=1, row=1,  sticky="nw")
        self.countbedroom.grid(column=1, row=2,  sticky="nw")
        self.price.grid(column=1, row=3,  sticky="nw")
        self.description.grid(column=1, row=4, columnspan=3, ipadx=90, sticky="nw")
        
        # Button 
        self.add_btn = Button(self, text='Add',  width=8, command=self.callbacks['on_add_room'])
        self.update_btn = Button(self, text='Update', width=8, state=DISABLED,command=self.callbacks['on_update_room'])
        self.delete_btn = Button(self, text='Delete', width=8, command=self.callbacks['on_delete_room'],bg='red')
        self.clear_btn = Button(self, text='Clear', width=8, command=self.callbacks['on_clear_room'])
        
        # layout
        self.add_btn.grid(column=1, row=5,columnspan=2, sticky="W")
        self.update_btn.grid(column=1, row=5, sticky="N",padx=2)
        self.delete_btn.grid(column=2, row=5,columnspan=2,sticky="W")
        self.clear_btn.grid(column=2, row=5,  sticky="E",padx=2)
        #  ===== show list
        self.page_label = Label(self, text='Room Detail')
        self.page_label.grid(column=0, row=6, sticky="w")
    
    def validate(self,P):
        if str.isdigit(P) or P == "":
            return True
        else:
            return False
            
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
            
        }
        return data
    
    def set(self):# show data to entry== for update
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
        
    def add_row(self,id):
        self.Room_Table.insert('','end', values =(id, self.roomnumber_var.get() ,self.countbedroom_var.get() ,\
                                                self.price_var.get() ,self.description_var.get() ))   
            
    def delete_row(self):
        selected_items = self.Room_Table.selection()
        for selected_item in selected_items:
            self.Room_Table.delete(selected_item)
        return self
    
    def fetch_data(self,data):
        
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
    
    def delete_all_row_tree(self):
        print('delete all rows========')
        # self.Room_Table.delete(*self.Room_Table.get_children())
        for row in self.Room_Table.get_children():
            self.Room_Table.delete(*row)
        return (self.Room_Table)
    
    def switch(self):
        self.add_btn.config(state = 'disabled')
      
class ReserveForm(tk.Frame):
    def __init__(self, parent, fields, callbacks, *args, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.callbacks = callbacks
        self.data={}
        self.id_var = -1
        self.roomid_var = StringVar()
        self.personid_var = StringVar()
        self.price_var = StringVar()
        self.startdate_var = StringVar()
        self.enddate_var = StringVar()
        self.pricesum_var = StringVar()
        
        
        vcmd = (self.register(self.validate))
        self.Header_label = Label(self, text='Rserve information:')
        self.roomid_label = Label(self, text='Room Id:')
        self.roomid = Entry(self,validate='all', validatecommand= (vcmd, '%P'), textvariable= self.roomid_var)
        self.personid_label = Label(self, text='Persion Id:')
        self.personid = Entry(self,validate='all', validatecommand= (vcmd, '%P'), textvariable= self.personid_var)
        self.startdate_label = Label(self, text='Start date:')
        self.startdate = DateEntry(self, textvariable= self.startdate_var)
        self.enddate_label = Label(self, text='End date:')
        self.enddate = DateEntry(self, textvariable= self.enddate_var)
        self.pricesum_label = Label(self, text='Price Sum:')
        self.pricesum = Entry(self, validate='all', validatecommand= (vcmd, '%P'), textvariable= self.pricesum_var)
        
        # Layout label
        self.Header_label.grid( column=0, row=0,  sticky="nw")
        self.roomid_label.grid( column=0, row=1, sticky="ne")
        self.personid_label.grid(column=0, row=2, sticky="ne")
        self.startdate_label.grid(column=0, row=3, sticky="ne")
        self.enddate_label.grid(column=0, row=4, sticky="ne")
        self.pricesum_label.grid(column=0, row=5, sticky="ne")
        # Layout textbox
        self.roomid.grid(column=1, row=1,  sticky="nw")
        self.personid.grid(column=1, row=2,  sticky="nw")
        self.startdate.grid(column=1, row=3,  sticky="nw")
        self.enddate.grid(column=1, row=4,  sticky="nw")
        self.pricesum.grid(column=1, row=5, sticky="nw")
        
        # Button 
        self.add_btn = Button(self, text='Add',  width=8, command=self.callbacks['on_add_reserve'])
        self.update_btn = Button(self, text='Update', width=8, state=DISABLED,command=self.callbacks['on_update_reserve'])
        self.delete_btn = Button(self, text='Delete', width=8, command=self.callbacks['on_delete_reserve'],bg='red')
        self.clear_btn = Button(self, text='Clear', width=8, command=self.callbacks['on_clear_reserve'])
        
        # layout
        self.add_btn.grid(column=1, row=6,columnspan=2, sticky="W")
        self.update_btn.grid(column=1, row=6, sticky="N",padx=2)
        self.delete_btn.grid(column=2, row=6,sticky="E")
        self.clear_btn.grid(column=2, row=6,columnspan=2,  sticky="E",padx=2)
        #  ===== show list
        self.page_label = Label(self, text='Reserve Detail')
        self.page_label.grid(column=0, row=7, sticky="w")        
   
    def validate(self, P):
        if str.isdigit(P) or P == "":
            return True
        else:
            return False
      
    def clear(self):
        self.roomid_var.set("")
        self.personid_var.set("")
        self.startdate_var.set("")
        self.enddate_var.set("")
        self.pricesum_var.set("")
        return
    
    def get_cursor(self, evnt):  # specific id of table
        try:
            cursor_row = self.Room_Tablex.focus()
            content = self.Room_Tablex.item(cursor_row)
            self.row = content['values']
            self.id_var = self.row[0]
            
        except Exception as e:
            messagebox.showerror('warning','Row selection is out ranage.\n{}'.format(e))
            raise
        
    def get(self)-> dict:
        data = {
            'id':self.id_var,
            'roomid': self.roomid_var.get(),
            'personid': self.personid_var.get(),
            'startdate':self.startdate_var.get(),
            'enddate':self.enddate_var.get(),
            'pricesum':self.pricesum_var.get()
        }
        return data
    
    def add_row(self,id):
        self.Room_Tablex.insert('','end', values =(id, self.roomid_var.get() ,self.personid_var.get() ,\
                                                self.startdate_var.get() ,self.enddate_var.get(),self.pricesum_var.get() )) 
        
    def reset(self):
        self.roomid_var = 0
        self.personid_var  = 0
        self.startdate_var  = ''
        self.enddate_var  = ''
        self.pricesum_var = 0
    
    def delete_row(self):
        selected_items = self.Room_Tablex.selection()
        for selected_item in selected_items:
            self.Room_Tablex.delete(selected_item)
        return self
    
    def fetch_data(self,data):
        #=== Tree view Table 
        scroll_x = Scrollbar(self, orient=HORIZONTAL)
        scroll_y = Scrollbar(self, orient=VERTICAL)
        # person is user
        self.Room_Tablex = ttk.Treeview(self, columns=("id","roomid","roomnumber","personid","title","name","family", "startdate","enddate","pricesum"), xscrollcommand = scroll_x.set, yscrollcommand = scroll_y.set)
        self.Room_Tablex.grid(column=0, row=8, columnspan=7,sticky='w') 
                        
        scroll_x.config(command=self.Room_Tablex.xview)
        scroll_y.config(command=self.Room_Tablex.yview)
        self.Room_Tablex.heading(column='#1', text="Id")
        self.Room_Tablex.heading(column='#2', text="Room Id")
        self.Room_Tablex.heading(column='#3', text="Room Number")
        self.Room_Tablex.heading(column='#4', text="Person Id")
        self.Room_Tablex.heading(column='#5', text="User Type")#title
        self.Room_Tablex.heading(column='#6', text="User Name")#user table
        self.Room_Tablex.heading(column='#7', text="User Family")
        self.Room_Tablex.heading(column='#8', text="Start Date")
        self.Room_Tablex.heading(column='#9', text="Start Date")
        self.Room_Tablex.heading(column='#10', text="Sum Price")
        self.Room_Tablex['show']='headings' # removing extra index col at begining

        #setting up widths of cols
        self.Room_Tablex.column("#1", width=30)
        self.Room_Tablex.column("#2", width=60)
        self.Room_Tablex.column("#3", width=80)
        self.Room_Tablex.column("#4", width=80)
        self.Room_Tablex.column("#5", width=100)
        self.Room_Tablex.column("#6", width=120)
        self.Room_Tablex.column("#7", width=120)
        self.Room_Tablex.column("#8", width=120)
        self.Room_Tablex.column("#9", width=120)
        self.Room_Tablex.column("#10", width=120)
        self.Room_Tablex.bind("<ButtonRelease-1>", self.get_cursor)# this is an event to select row
        self.data=data
        #to display data in grid
        try:
            if self.data != {}:
                for key, record in self.data.items():
                    self.Room_Tablex.insert('', 'end', iid=key, open=False, text='Room ID: {}'.format(key),
                                        values =[ record['id'], record['roomid'], record['roomnumber'], record['personid'],\
                                            record['title'], record['name'], record['family'], record['startdate'],\
                                            record['enddate'], record['pricesum']])   
        except Exception as e:
            messagebox.showerror(title='Error',message='The Show data not avaiable, Error is about{}',detail=str(e))
        else:
            return
        finally:
            print('finall in fetch layout')

class UserForm(tk.Frame):
    
    def __init__(self, parent,data, callbacks, *args, **kwargs): 
        super().__init__(parent, **kwargs)
        self.callbacks = callbacks
        self.data={}
        
        self.id_var = -1
        self.usertype_var = StringVar()
        self.name_var = StringVar()
        self.family_var = StringVar()
        self.email_var = StringVar()
        self.tel_var = StringVar()
        self.address_var = StringVar()
        
        vcmd = (self.register(self.validate))
        self.Header_label = Label(self, text='User information:')
        self.usertype_label = Label(self, text='User Type:')
        self.usertype = Entry(self, validate='all', validatecommand= (vcmd,'%P'), textvariable= self.usertype_var)
        self.name_label = Label(self, text='User Name:')
        self.name = Entry(self, textvariable= self.name_var)
        self.family_label = Label(self, text='User Family:')
        self.family = Entry(self, textvariable= self.family_var)
        self.email_label = Label(self, text='Email:')
        self.email = Entry(self, textvariable= self.email_var)
        self.tel_label = Label(self, text='Telephone:')
        self.tel = Entry(self, textvariable= self.tel_var, validate='all', validatecommand= (vcmd,'%P'))
        self.address_label = Label(self, text='address:')
        self.address = Entry(self, textvariable= self.address_var)
        
        # Layout label
        self.Header_label.grid( column=0, row=0,  sticky="nw")
        
        self.usertype_label.grid( column=0, row=1, sticky="ne")
        self.name_label.grid(column=0, row=2, sticky="ne")
        self.family_label.grid(column=0, row=3, sticky="ne")
        self.email_label.grid(column=0, row=4, sticky="ne")
        self.tel_label.grid(column=0, row=5, sticky="ne")
        self.address_label.grid(column=0, row=6, columnspan=4, sticky="ne")
        
        # Layout textbox
        self.usertype.grid(column=1, row=1,  sticky="nw")
        self.name.grid(column=1, row=2,  sticky="nw")
        self.family.grid(column=1, row=3,  sticky="nw")
        self.email.grid(column=1, row=4,  sticky="nw")
        self.tel.grid(column=1, row=5,  sticky="nw")
        self.address.grid(column=1, row=6, sticky="nw")
        
        # Button 
        self.add_btn = Button(self, text='Add',  width=8, command=self.callbacks['on_add_user'])
        self.update_btn = Button(self, text='Update', width=8, state=DISABLED,command=self.callbacks['on_update_user'])
        self.delete_btn = Button(self, text='Delete', width=8, command=self.callbacks['on_delete_user'],bg='red')
        self.clear_btn = Button(self, text='Clear', width=8, command=self.callbacks['on_clear_user'])
        
        # layout
        self.add_btn.grid(column=1, row=7,columnspan=2, sticky="W")
        self.update_btn.grid(column=1, row=7, sticky="E",padx=2)
        self.delete_btn.grid(column=2, row=7,columnspan=2,sticky="W")
        self.clear_btn.grid(column=2, row=7,  sticky="E",padx=2)
        #  ===== show list
        self.page_label = Label(self, text='Reserve Detail')
        self.page_label.grid(column=0, row=8, sticky="w")        

    def validate(self, P):
        if str.isdigit(P) or P == "":
            return True
        else:
            return False
    
    def clear(self):
        self.usertype_var.set('')
        self.name_var.set('')
        self.family_var.set('')
        self.email_var.set('')
        self.tel_var.set('')
        self.address_var.set('')
        return
 
    def get_cursor(self, event):  # specific id of table
        try:
            cursor_row = self.Room_Tablex.focus()
            content = self.Room_Tablex.item(cursor_row)
            self.row = content['values']
            self.id_var = self.row[0]
            
        except Exception as e:
            messagebox.showerror('warning','Row selection is out  of ranage.\n{}'.format(e))
            raise
        
    def get(self)-> dict:
        data = {
            'id':self.id_var,
            'usertype':self.usertype_var.get(),
            'name':self. name_var.get(),
            'family':self.family_var.get(),
            'email':self.email_var.get(),
            'tel':self.tel_var.get(),
            'address':self.address_var.get(),
        }
        return data
    
    def add_row(self,id):
        self.Room_Tablex.insert('','end', values =(id, self.usertype_var.get() ,self. name_var.get() ,\
                                                self.family_var.get() ,self.email_var.get(),\
                                                    self.tel_var.get(),  self.address_var.get(),  )) 

    def delete_row(self):
        selected_items = self.Room_Tablex.selection()
        for selected_item in selected_items:
            self.Room_Tablex.delete(selected_item)
        return self
    
    def fetch_data(self,data):
        #=== Tree view Table 
        scroll_x = Scrollbar(self, orient=HORIZONTAL)
        scroll_y = Scrollbar(self, orient=VERTICAL)
        # person is user
        self.Room_Tablex = ttk.Treeview(self, columns=("id","title","name","family","email","tel", "address"), xscrollcommand = scroll_x.set, yscrollcommand = scroll_y.set)
        self.Room_Tablex.grid(column=0, row=9, columnspan=7,sticky='w') 
                        
        scroll_x.config(command=self.Room_Tablex.xview)
        scroll_y.config(command=self.Room_Tablex.yview)
        self.Room_Tablex.heading(column='#1', text="Id")
        self.Room_Tablex.heading(column='#2', text="Type")
        self.Room_Tablex.heading(column='#3', text="Name")
        self.Room_Tablex.heading(column='#4', text="Family")
        self.Room_Tablex.heading(column='#5', text="email")
        self.Room_Tablex.heading(column='#6', text="tel")#user table
        self.Room_Tablex.heading(column='#7', text="Address")
        self.Room_Tablex['show']='headings' # removing extra index col at begining

        #setting up widths of cols
        self.Room_Tablex.column("#1", width=30)
        self.Room_Tablex.column("#2", width=80)
        self.Room_Tablex.column("#3", width=100)
        self.Room_Tablex.column("#4", width=100)
        self.Room_Tablex.column("#5", width=100)
        self.Room_Tablex.column("#6", width=100)
        self.Room_Tablex.column("#7", width=200)
        self.Room_Tablex.bind("<ButtonRelease-1>", self.get_cursor)# this is an event to select row
        self.data=data
        #to display data in grid
        try:
            if self.data != {}:
                for key, record in self.data.items():
                    self.Room_Tablex.insert('', 'end', iid=key, open=False, text='Room ID: {}'.format(key),
                                        values =[ record['id'], record['title'], record['name'], record['family'],\
                                            record['email'], record['tel'], record['address']])   
        except Exception as e:
            messagebox.showerror(title='Error',message='The Show data not avaiable, Error is about{}',detail=str(e))
        else:
            return
        finally:
            print('finall in fetch layout')

class UserTypeForm(tk.Frame):
    
    def __init__(self, parent,data, callbacks, *args, **kwargs): 
        super().__init__(parent, **kwargs)
        self.callbacks = callbacks
        self.data={}
        
        self.id_var=-1
        self.title_var = StringVar()
        
        self.Header_label = Label(self, text='User Type information:')
        self.title_label = Label(self, text='Tile:')
        self.title= Entry(self, textvariable= self.title_var)
        
        self.Header_label.grid( column=0, row=0,  sticky="nw")
        
        self.title_label.grid(column=0, row=1, sticky="ne")
        self.title.grid(column=1, row=1, sticky="ne")
        
        self.add_btn = Button(self, text='Add',  width=8, command=self.callbacks['on_add_usertype'])
        self.delete_btn = Button(self, text='Delete', width=8, command=self.callbacks['on_delete_user'],bg='red')
        self.clear_btn = Button(self, text='Clear', width=8, command=self.callbacks['on_clear_usertype'])

        self.add_btn.grid(column=1, row=2,columnspan=2, sticky="W")
        self.delete_btn.grid(column=1, row=2,sticky="E")
        self.clear_btn.grid(column=2, row=2,  sticky="W",padx=2)

    def clear(self):
        self.title_var.set('')
        return
    
    def get_cursor(self, evnt):
        try:
            cursor_row =self.Room_Table.focus()
            content = self.Room_Table.item(cursor_row)
            self.row = content['values']
            self.id_var = self.row[0]
        except Exception as e:
            messagebox.showerror('Warning', 'Row selection in out of range .\n {}'.format(e))
            raise
        
    def get(self)-> dict:
        data = {
            'id': self.id_var,
            'title': self.title.get()
        }
        return data
    
    def set(self):
        self.title_var.set(self.row[0])
        return
    
    def add_row(self, id):
        self.Room_Table.insert('', 'end', values=(id,self.title_var.get()))
        return
    
    def delete_row(self):
        selected_items = self.Room_Table.selection()
        for selected_item in selected_items:
            self.Room_Table.delete(selected_item)
        return self
    
    def fetch_data(self,data):
         #=== Tree view Table 
        scroll_x = Scrollbar(self, orient=HORIZONTAL)
        scroll_y = Scrollbar(self, orient=VERTICAL)

        self.Room_Table = ttk.Treeview(self, columns=("id","tite"), xscrollcommand = scroll_x.set, yscrollcommand = scroll_y.set)
        self.Room_Table.grid(column=0, row=7, columnspan=4,sticky='w') 
                           
        scroll_x.config(command=self.Room_Table.xview)
        scroll_y.config(command=self.Room_Table.yview)
        self.Room_Table.heading(column='#1', text="ID")
        self.Room_Table.heading(column='#2', text="Title")
        
        #setting up widths of cols
        self.Room_Table.column("#1", width=40)
        self.Room_Table.column("#2", width=100)
        
        self.Room_Table.bind("<ButtonRelease-1>", self.get_cursor)# this is an event to select row
        self.data=data
        #to display data in grid
        try:
            if self.data != {}:
                for key, record in self.data.items():
                    self.Room_Table.insert('', 'end', iid=key, open=False, text='Room ID: {}'.format(key),
                                        values =[ record['id'], record['title']])   
        except Exception as e:
            messagebox.showerror(title='Error',message='The Show data not avaiable, Error is about{}',detail=str(e))
        else:
            return
        finally:
            print('finall in fetch layout in init')
        
class SearchRoomForm(tk.Frame):
   
    def __init__(self, parent ,data,callbacks, *args, **kwargs):
        super().__init__(parent, **kwargs)
        self.callbacks = callbacks
        self.data = {}
        self.searchby_var=''
        
        self.search_by_var = StringVar()
        self.search_txt_var = StringVar()
        vcmd = (self.register(self.validate))
        
        # ===== Search box  =====  
        self.lbl_search = Label(self, width=20, text="Search By:") 
        self.__searchby_list = ttk.Combobox(self,takefocus=1, textvariable=self.search_by_var, state="readonly" )
        self.__searchby_list['values']=('','RoomNumber','CountBedroom','Price[>=]YourEnter','Price[<=]YourEnter')
        # self.__searchby_list.bind('<<ComboboxSelected>>', self._on_combo_change)
        
        self.lbl_search.grid(row=8, column=0, padx=4, sticky="w")
        self.__searchby_list.grid(row=8, column=1,  sticky="w")
        
        self.txt_search = Entry(self, validate = 'all',  validatecommand = (vcmd, '%P'), textvariable=self.search_txt_var, font=("times new roman", 13), bd=5, relief=GROOVE)
        self.txt_search.grid(row=8, column=2,  sticky="w")
        self.searchbtn = Button(self, text="Search", width=8, command=self.callbacks['on_search_room_data'])
        self.searchbtn.grid(row=8, column=3,  sticky="E")
    
    def validate(self, P):
        if str.isdigit(P) or P == "":
            return True
        else:
            return False
        
    def get(self)-> dict:
        data = {
            'searchby': self.search_by_var.get(),
            'searchtext': self.search_txt_var.get()
        }
        return data
        
    def fetch_data(self,data):
        self.data=data
        #=== Tree view Table 
        print('==show to treeview==',self.data.items())
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
 
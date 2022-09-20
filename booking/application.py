from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import tkinter as tk
from tkinter import  *
from tkinter import ttk, messagebox
from datetime import datetime
import traceback
from .db.forms import RoomForm

from . import db 
from . import gui
from . import menus
from .config import AppConfig

from sqlalchemy.ext.declarative import declarative_base 

class Application(tk.Tk):
    def __init__(self, *args ,**kwargs) :
        tk.Tk.__init__(self, *args, **kwargs)
        
        
        self._appconfig = AppConfig()
        self.settings = {}
        self.title('Hotel Booking ')
        #   pattern= postgresql+psycopg2://user:password@host:port/dbname[?key=value&key=value...]
        global engine 
        engine = create_engine("postgresql://postgres:admin@localhost:5432/Booking", client_encoding="utf8",echo=True)
        self.Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

        self.callbacks = {
            # Menu option
            'file--quit': self.quit,
            'settings--preferences': self.open_preferences,
            'settings--preferences--update': self.update_preferences,
            'settings--preferences': self.open_preferences,
            'settings--createschema': self.open_createschema,
            'help--help':self.open_help,
            'help--about':self.open_about,
            
            # Menu calls
            'open_room_form':self.open_room_form,
            'open_reserve_form':self.open_reserve_form,
            'open_user_form':self.open_user_form,
            'open_usertype_form': self.open_usertype_form,
            'open_reserve_form':self.open_reserve_form,
            'open_report_view': self.open_report_view,
            'open_search_room_form':self.open_search_room_form,
            
            # Room page functionality
            'on_add_room': self.on_add_room,
            'on_update_room': self.on_update_room,
            'on_delete_room': self.on_delete_room,
            'on_clear_room': self.on_clear_room,
            
            # Reserve page functionality
            'on_add_reserve': self.on_add_reserve,
            'on_update_reserve': self.on_update_reserve,
            'on_delete_reserve': self.on_delete_reserve,
            'on_clear_reserve': self.on_clear_reserve,
            'on_calc_reserve': self.on_calc_reserve,
            'on_refresh_usertype': self.on_refresh_usertype,
            
            'on_refresh_reserve_list': self.on_refresh_reserve_list,
            'on_refresh_roomnumber_personid': self.on_refresh_roomnumber_personid,
            
            
            # User page functionality
            'on_add_user': self.on_add_user,
            'on_update_user': self.on_update_user,
            'on_delete_user': self.on_delete_user,
            'on_clear_user': self.on_clear_user,
            
            # User Type page functionality
            'on_add_usertype': self.on_add_usertype,
            'on_update_usertype': self.on_update_user,
            'on_clear_usertype': self.on_clear_usertype,
            'on_delete_usertype': self.on_delete_usertype,
            
            'on_search_room_data': self.on_search_room_data,
            
        }

        # Root configuration for minsize, resize support
        self.minsize(640, 480)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        # Menu
        menu = menus.MainMenu(self, self.callbacks)
        self.configure(menu=menu)
        # First "layer" of elements
        self.main_frame = tk.Frame(self)
        self.main_frame.configure(bg='lightblue')
        self.main_frame.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)
        self.status_bar = tk.Frame(self)
        self.status_bar.configure(relief='ridge', bd=1)
        self.status_bar_label = ttk.Label(self.status_bar, text='STATUS BAR!')
        self.status_bar_label.grid(row=0)
        self.main_frame.grid(row=0, sticky='NSEW')
        self.status_bar.grid(row=1, sticky='EW')
        # sub-main_frame
        self.left_nav_frame = tk.Frame(self.main_frame)
        self.workspace_frame = tk.Frame(self.main_frame)
        self.left_nav_frame.configure(bg='#85929E')
        self.workspace_frame.configure(bg='#5D6D7E')
        self.left_nav_frame.grid(row=0, column=0, sticky='NSEW')
        self.workspace_frame.grid(row=0, column=1, sticky='NSEW')
        
        self.room_btn = ttk.Button(self.left_nav_frame,    text='        Room       ',
                                          command=self.callbacks['open_room_form'])
        self.reserve_btn = ttk.Button(self.left_nav_frame, text='     Reservation   ',
                                          command=self.callbacks['open_reserve_form'])
        self.user_btn = ttk.Button(self.left_nav_frame,  text='         User       ',
                                          command=self.callbacks['open_user_form'])
        self.usertype_btn = ttk.Button(self.left_nav_frame,text='       User type   ',
                                          command=self.callbacks['open_usertype_form'])
        self.report_view_btn = ttk.Button(self.left_nav_frame,text='        Report     ',
                                          command=self.callbacks['open_report_view'])
        self.search_room_btn = ttk.Button(self.left_nav_frame,text='  Search Room ',
                                          command=self.callbacks['open_search_room_form'],
                                          default='disabled')
        
        self.room_btn.grid(row=0, column=0, pady=2)
        self.reserve_btn.grid(row=1, column=0, pady=2)
        self.user_btn.grid(row=2, column=0, pady=2)
        self.usertype_btn.grid(row=3, column=0, pady=2)
        self.report_view_btn.grid(row=4, column=0, pady=2)
        self.search_room_btn.grid(row=5, column=0, pady=2)

        # Instance of Object- (View)
        self.app_form_window = None
        
        self.room_form = None
        self.search_room_form = None
        self.reserve_form = None
        self.user_form = None
        self.usertype_form = None
        self.report_form = None

        self.room_view = None # 
        self.room_view_modal = None
        
        self.preferences_form_window = None
        self.preferences_form = None
        
        self.search_form_window = None
        
        
    @contextmanager
    def session_scope(self):
        session = self.Session()
        try:
            yield session
            session.commit()
        except Exception as e:
            print('@contextmanager caught an error! {}'.format(e))
            session.rollback()
            raise
        finally:
            session.close()
 
    def init_db(self):
        self.Base=db.models.Base
        Base=declarative_base(self.Base)
        self.Base.metadata.create_all(engine)
        return
    
    def open_room_form(self):
        data={}
        if self.room_form is None:
            with self.session_scope() as session:
                data=db.queries.qry_room_showall(session)
                self.room_form = gui.forms.RoomForm(
                    self.workspace_frame,
                    data,
                    self.callbacks
                )
            self.room_form.fetch_data(data)
            self.room_form.grid(row=0, column=0, sticky='NSEW')
        else: 
            self.room_form.lift()
        
    # == Room callback Contorls { 
    def on_add_room(self):
        data = self.room_form.get()
        if data['roomnumber'] and data['countbedroom'] and data['price'] and data['description']:
            try:
                    with self.session_scope() as session:
                        idd=db.forms.RoomForm(session).add_room(data)
                        messagebox.showinfo('Information','            Record saved             ')
                        self.room_form.add_row(idd)
                    self.room_form.clear()
            except NameError:
                self.room_form.clear()
        else: 
            messagebox.showinfo('Information','          Please Insert all fields  ')
            return   
   
    def on_delete_room(self):
        answer = messagebox.askyesno(title='Warning',
                                     message='Are you sure delete this room information?\n Because by delete room information any reservation information for this room become [lost!!!]') 
        if answer: 
            data=self.room_form.get()
            id = data['id']
            try:
                with self.session_scope() as session:
                    db.forms.RoomForm(session).delete_room(id)
                    self.room_form.delete_row()
            except Exception as e:
                messagebox.showinfo(title='Information',message='Not deleted selected row.')   
             
    def on_update_room(self):
        # switch state
        self.room_form.switch()
        # data=self.room_form.get()
        # idd= data['id']
        # print('idd=====',idd  )
        # data2={}
        # try:
        #     if flag==False:
        #         # step 1 fill the fields
        #         self.room_form.set()   #show data to entry widget
        #         if self.room_form.roomnumber_var.get()=="" or self.room_form.countbedroom.get()=="" or self.room_form.price.get() =="":
        #             messagebox.showinfo("Information","Please fill all the fields!!!")
        #             flag=True
        #     else:
        #         self.room_form.delete_row()
        #         iid=data['id'].get()
        #         with self.session_scope() as session:
        #             # show content to text entry 
        #             data=self.room_form.get()
        #             self.room_db_form=db.forms.RoomForm(session,data)
        #             self.room_db_form.updata_room(data)
        #             self.on_showall_room()
        #         if idd == '':
        #             messagebox.showinfo(title='Information',message='Please select row of list for edit this')
        # except Exception as e:
        #     messagebox.showerror()
        return
    
    def on_clear_room(self):
        self.room_form.clear()
    # } == Room callback Contorls 
    global room_list
    room_list={}
    # handling  Reserve view,model    
    def open_reserve_form(self):
        if self.reserve_form is None:
            with self.session_scope() as session:
                data = db.queries.qry_reserve_showall(session)
                self.reserve_form = gui.forms.ReserveForm(
                    self.workspace_frame,
                    data,
                    self.callbacks
                )
            self.reserve_form.fetch_data(data)
            room_list = db.queries.qry_roomnumber_showall(session)
            self.reserve_form.list_room_number(room_list)
            price_id_list = db.queries.qry_priceid_list(session)
            self.reserve_form.list_price_id(price_id_list)
            
            self.reserve_form.grid(row=0, column=0, sticky='NSEW')
        else: 
            self.reserve_form.lift()
            
    # == Reserve callback Contorls {     
    def on_add_reserve(self):
        self.reserve_form.start_time()#set variable spinbox time 
        self.reserve_form.end_time()#set variable spinbox time   
        self.start_datetime = self.reserve_form.datetime_start()# Gather date and time from widget => str(datetime)
        self.end_datetime = self.reserve_form.datetime_end()# Gather date and time from widget => str(datetime)
        
        data = self.reserve_form.get()
        if data['roomnumber'] and data['personid'] and data['startdatetime'] and data['enddatetime'] and data['pricesum']:
            # convert str(datetime) to obj(datetime)
            data['startdatetime']=  datetime.strptime(self.start_datetime,'%m/%d/%y %H:%M:%S')
            data['enddatetime']=  datetime.strptime(self.end_datetime,'%m/%d/%y %H:%M:%S')
            try:
                with self.session_scope() as session:
                    room_id = db.queries.qry_find_roomid_from_listroom(data['roomnumber'],session )#Show Form with combobox roomnumber and insert by id room
                    idd = db.forms.ReserveForm(session).add_reserve(room_id, data)
                    self.reserve_form.set(room_id)
                    # self.reserve_form.add_row(idd,data)
                    self.on_refresh_reserve()
                messagebox.showinfo('Information','     Record saved      ')
            except NameError:
                messagebox.showinfo('Warning','Something went wrong')
        else: 
                messagebox.showinfo('Warning','Please Insert all fields')
                return    
    
    def on_delete_reserve(self):
        answer = messagebox.askyesno(title='Warning',
                                     message='Are you sure delete this reserveation information?\n Because if delete this reservation information for that room state is => [Free!!!]') 
        if answer: 
            data=self.reserve_form.get()
            id= data['id']# need it check data[id] by  if id:
            try:
                with self.session_scope() as session:
                    db.forms.ReserveForm(session).delete_reserve(id)
                    self.reserve_form.delete_row()
            except Exception as e:
                messagebox.showinfo(title='Information',message='Not deleted selected row.')  
            
    def on_update_reserve(self):
        pass
    
    def on_clear_reserve(self):
        self.reserve_form.clear()
    
    def on_calc_reserve(self):
        try:
            data= self.reserve_form.get()
            with self.session_scope() as session:
                dicts = db.queries.qry_find_roomid_price_from_listroom(data['roomnumber'],session )#Show Form with combobox roomnumber and insert by id room
                # find_id_price find id and price from room number and return by dict data keys=id and values=price
                price=int(dicts['price'])
                room_id=dicts['id']
                print(price, room_id)
                self.reserve_form.sets(price,room_id)
            if room_id and data['startdatetime'] and data['enddatetime']:
                with self.session_scope() as session:
                    self.reserve_form.show_sumprice(price)
                    # self.reserve_form.check_reserve_valid(room_id)
            else: 
                messagebox.showinfo('Information','please Insert a Room Id,then start and end Date you have for Reservation.')
        except Exception as e:
            messagebox.showinfo('Information','Not found information record for this room Id.\n{}'.format(e))
        else: 
            return
    # == Reserve callback Contorls }
    # handling  User view,model 
    global usertype_dict
    usertype_dict={}   
    def open_user_form(self):
        data={}
        if self.user_form is None:
            with self.session_scope() as session:
                data = db.queries.qry_user_showall(session)
                self.user_form = gui.forms.UserForm(
                    self.workspace_frame,
                    data,
                    self.callbacks
                )
            self.user_form.fetch_data(data)
            self.usertype_dict = db.queries.qry_usertype_list(session)
            self.user_form.list_usertype(self.usertype_dict)
            
            self.user_form.grid(row=0, column=0, sticky='NSEW')
        else: 
            self.user_form.lift()
    
    # { == User callback Contorls  User is Person table
    def on_add_user(self):
        
        data = self.user_form.get()
        if data['usertype'] and data['name'] and data['family'] and data['email'] and data['tel'] and data['address']:
            try:
                with self.session_scope() as session:
                    self.usertype_id=self.find_key(self.usertype_dict,data['usertype'])
                    
                    idd = db.forms.UserForm(session).add_user(data,  self.usertype_id)
                    self.user_form.add_row(idd)
                messagebox.showinfo('Information','     Record saved      ')
            except NameError:
                messagebox.showinfo('Warning','Something went wrong')
        else: 
                messagebox.showinfo('Warning','Please Insert all fields. ')
                return
            
    def find_key(self,input_dict, value):
        return next((k for k, v in input_dict.items() if v == value), None)
    
    def on_delete_user(self):
        answer = messagebox.askyesno(title='Warning',
                                     message='Are you sure delete this user information?\n Because if delete this user information any reserve for this user state is => [Lost!!!]') 
        if answer: 
            data = self.user_form.get()
            id= data['id']
            try:
                with self.session_scope() as session:
                    db.forms.UserForm(session).delete_user(id)
                    self.user_form.delete_row()
            except Exception as e:
                messagebox.showinfo(title='Information',message='Not deleted selected row.') 
             
    def on_update_user(self):
        pass
   
    def on_clear_user(self):
        self.user_form.clear()
        return
    # == User callback Contorls } 
    
    # handling  UserType view,model    
    def open_usertype_form(self,):
        data={}
        if self.usertype_form is None:
            with self.session_scope() as session:
                data = db.queries.qry_usertype_showall(session)
                self.usertype_form = gui.forms.UserTypeForm(
                    self.workspace_frame,
                    data,
                    self.callbacks
                )
            self.usertype_form.fetch_data(data)
            self.usertype_form.grid(row=0, column=0, sticky='NSEW')
        else: 
            self.usertype_form.lift()
            return
            
    # { == Usertype callback Contorls
    def on_add_usertype(self):
        data = self.usertype_form.get()
        if data['title']:
            try:
                with self.session_scope() as session:
                    iid=db.forms.UserTypeForm(session).add_usertype(data)
                    self.usertype_form.add_row(iid)
                messagebox.showinfo('Information','     Record saved      ')
            except NameError:
                messagebox.showinfo('Warning','Something went wrong')
        else: 
                messagebox.showinfo('Warning','Please Insert all fields. ')
                return
    
    def on_delete_usertype(self):
        data = self.usertype_form.get()
        id= data['id']
        try:
            with self.session_scope() as session:
                db.forms.UserTypeForm(session).delete_usertype(id)
                self.usertype_form.delete_row()
        except Exception as e:
            messagebox.showinfo(title='Information',message='Not deleted selected row.') 
  
    def on_clear_usertype(self):
        self.usertype_form.clear()
        return
    # == Usertype callback Contorls }        
   
    def open_report_view(self):
        if self.room_view is None:
            with self.session_scope() as session:
                self.room_view = gui.views.Room_View(
                    self.workspace_frame,
                    db.queries.qry_room_view(session),
                    self.callbacks
                )
            self.room_view.grid(row=0, column=0, sticky='NSEW')
        else:
            self.room_view.lift()
    
    def on_refresh_reserve_list(self):# use Modal
        if self.room_view_modal is None:
            with self.session_scope() as session:
                data = db.queries.qry_room_view(session)
                self.room_view_modal = gui.views.Room_View_Modal( 
                            self.app_form_window,
                            data,
                            self.callbacks
                    )
                self.room_view_modal.load_records()
        return 
    
    def on_refresh_roomnumber_personid(self):
        
        with self.session_scope() as session:
            room_list = db.queries.qry_roomnumber_showall(session)
            self.reserve_form.list_room_number(room_list)
            price_id_list = db.queries.qry_priceid_list(session)
            self.reserve_form.list_price_id(price_id_list)
        return
            
     #  == Search callback Contorls 
    def open_search_room_form(self):
       
        data={}
        if self.search_room_form is None:
            with self.session_scope() as session:
                self.search_room_form = gui.forms.SearchRoomForm(self.workspace_frame,data,self.callbacks)
            self.search_room_form.grid(row=0, column=0, sticky='NSEW')
        else:
            self.search_room_form.lift()
            
    def on_search_room_data(self):
        try:
            data = self.search_room_form.get()
            print( data['searchby'],data['searchtext'])
            if data['searchby'] and data['searchtext']:
                with self.session_scope() as session:
                    self.search_room_form = gui.forms.SearchRoomModal(self.workspace_frame, data, self.callbacks)
                    dict = db.forms.SearchRoomForm().search( data, session)
                    print('Dict==search===',dict)
                    self.search_room_form.fetch_data(dict)
                    dict={}
                    data={}
            else: 
                messagebox.showinfo(title='search',message='Please Select search by and insert text for search.')
        except Exception as e:
            traceback.print_exc()
            messagebox.showerror('Error','You have an error in main search. \n')
            return
        finally:
            print('finally all search function comlete.')
    
    def on_refresh_usertype(self):
        with self.session_scope() as session:
            self.usertype_dict = db.queries.qry_usertype_list(session)
            self.user_form.list_usertype(self.usertype_dict)
        return
            
    def on_refresh_reserve(self):
        with self.session_scope() as session:
            data = db.queries.qry_reserve_showall(session)
            self.reserve_form.fetch_data(data)
        return
    
    def open_preferences(self):
        if self.preferences_form_window is None or not self.preferences_form_window.winfo_exists():
            self.preferences_form_window = tk.Toplevel(self)
            self.preferences_form_window.minsize(480, 320)
            self.preferences_form_window.rowconfigure(0, weight=1)
            self.preferences_form_window.columnconfigure(0, weight=1)
            self.preferences_form = menus.Preferences(self.preferences_form_window, self.callbacks, self.settings)
            self.preferences_form.grid(row=0, column=0, sticky='NSEW')
        else:
            self.preferences_form_window.lift(self)
        self.preferences_form_window.focus()

    def update_preferences(self):
        data = self.preferences_form.appearance_frame.get()
        self._appconfig.update_settings(data)
    
    def open_createschema(self):
        try:
            self.init_db()
        except Exception as e:
            messagebox.showwarning('Error ','Fail to Generate schema for database (Booking). ')
        else:
            messagebox.showinfo('Info','Successfully to generate database schema.')
        return
    
    def open_help(self):
        messagebox.showinfo('Info','For first Run This application, please create Booking database in postgresql server and \n from Settings menu click [Create Database Schema] ')
        return
    
    def open_about(self):
         messagebox.showinfo('About','Thank you for use this application. \n Email:m_gehangir2006@gmail.com')
    # --------end
 
            
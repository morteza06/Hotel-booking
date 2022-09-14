from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import tkinter as tk
from tkinter import  *
from tkinter import ttk, messagebox

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
        #   pattern=    postgresql+psycopg2://user:password@host:port/dbname[?key=value&key=value...]
        global engine 
        engine = create_engine("postgresql://postgres:admin@localhost:5432/Booking", client_encoding="utf8",echo=True)
        self.Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

        # At first run please create database Booking in to pgadmin4 then create database Schema by run this under command for create model 
        # Base.metadata.create_all(engine)  
        
        self.callbacks = {
            # Menu option
            'file--quit': self.quit,
            'settings--preferences': self.open_preferences,
            'settings--preferences--update': self.update_preferences,
            'settings--preferences': self.open_preferences,
            
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
            
            # User page functionality
            'on_add_user': self.on_add_user,
            'on_update_user': self.on_update_user,
            'on_delete_user': self.on_delete_user,
            'on_clear_user': self.on_clear_user,
            
            # User Type page functionality
            'on_add_usertype': self.on_add_usertype,
            'on_update_usertype': self.on_update_user,
            'on_clear_usertype': self.on_clear_usertype,
            
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
                                          command=self.callbacks['open_search_room_form'])
        
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
        
        self.preferences_form_window = None
        self.preferences_form = None
        
        
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
    
    # handling ROOM view,model
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
            
    def on_delete_room(self):
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
            self.reserve_form.grid(row=0, column=0, sticky='NSEW')
        else: 
            self.reserve_form.lift()
            
    # == Reserve callback Contorls {     
    def on_add_reserve(self):
        data = self.reserve_form.get()
        if data['roomid'] and data['personid'] and data['startdate'] and data['enddate'] and data['pricesum']:
            try:
                with self.session_scope() as session:
                    iid=db.forms.ReserveForm(session).add_reserve(data)
                    self.reserve_form.add_row(idd)
                messagebox.showinfo('Information','     Record saved      ')
            except NameError:
                messagebox.showinfo('Warning','Something went wrong')
        else: 
                messagebox.showinfo('Warning','Please Insert all fields')
            
    def on_delete_reserve(self):
        data=self.reserve_form.get()
        id= data['id']
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
    # == Reserve callback Contorls }
    
    # handling  User view,model    
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
            self.user_form.grid(row=0, column=0, sticky='NSEW')
        else: 
            self.user_form.lift()
    
    # { == User callback Contorls  User is Person table
    def on_add_user(self):
        data = self.user_form.get()
        if data['id'] and data['usertype'] and data['name'] and data['family'] and data['email'] and data['telephone'] and data['address']:
            try:
                with self.session_scope() as session:
                    iid=db.forms.UserForm(session).add_user(data)
                    self.user_form.add_row(idd)
                messagebox.showinfo('Information','     Record saved      ')
            except NameError:
                messagebox.showinfo('Warning','Something went wrong')
        else: 
                messagebox.showinfo('Warning','Please Insert all fields. ')

    def on_delete_user(self):
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
            
    # { == User callback Contorls
    def on_add_usertype(self):
        data = self.usertype_form.get()
        if data['title']:
            try:
                with self.session_scope() as session:
                    iid=db.forms.UserTypeForm(session).add_usertype(data)
                    self.usertype_form.add_row(idd)
                messagebox.showinfo('Information','     Record saved      ')
            except NameError:
                messagebox.showinfo('Warning','Something went wrong')
        else: 
                messagebox.showinfo('Warning','Please Insert all fields. ')

    def on_delete_usertype(self):
        data = self.usertype_form.get()
        id= data['id']
        try:
            with self.session_scope() as session:
                db.forms.UserTypeForm(session).delete_user(id)
                self.usertype_form.delete_row()
        except Exception as e:
            messagebox.showinfo(title='Information',message='Not deleted selected row.') 
  
    def on_clear_usertype(self):
        self.usertype_form.clear()
        return
    # == User callback Contorls }        
   
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
            
     #  == Search callback Contorls 
    def open_search_room_form(self):
        data={}
        if self.search_room_form is None:
            with self.session_scope() as session:
                self.search_room_form = gui.forms.SearchRoomForm(self.workspace_frame,data,self.callbacks)
            data={}
            self.search_room_form.fetch_data(data)
            self.search_room_form.grid(row=0, column=0, sticky='NSEW')
        else:
            self.search_room_form.lift()
            
    def on_search_room_data(self):
        try:
            data= self.search_room_form.get()
            # data['searchby']=self.room_form.search_by_var.get()
            # data['searchtext']=self.room_form.search_txt_var.get()
            print('@@@',data['searchby'])
            print('$$$',data['searchtext'])
            with self.session_scope() as session:
                self.search_room_form = gui.forms.SearchRoomForm(self.workspace_frame, data, self.callbacks)
                data2 = db.forms.SearchRoomForm(self).search( data, session)
                self.search_room_form.fetch_data(data2)
        except Exception as e:
            messagebox.showerror('Error','You have an error in main search. \n{e}'.format(e))
        else:
            messagebox.showinfo(title='search',message='search data done.')
            return
        finally:
            print('finally all search function comlete.')
            
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
    # --------end
 
            
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import tkinter as tk
from tkinter import  *
from tkinter import ttk, messagebox

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
            'file--quit': self.quit,
            'settings--preferences': self.open_preferences,
            'settings--preferences--update': self.update_preferences,
            'settings--preferences': self.open_preferences,
            
            
            'open_room_form':self.open_room_form,
            'open_reserve_form':self.open_reserve_form,
            'open_user_form':self.open_user_form,
            'open_usertype_form': self.open_usertype_form,
            'open_reserve_form':self.open_reserve_form,
            'open_report_view': self.open_report_view,
            
            'on_add_room': self.on_add_room,
            'on_update_room': self.on_update_room,
            'on_delete_room': self.on_delete_room,
            'on_clear_room': self.on_clear_room,
            'on_showall_room': self.on_showall_room,
            'on_search_room_data': self.on_search_room_data,
            'on_fetch_room_data': self.on_fetch_room_data,
            
            
            'on_add_reserve_form': self.on_add_reserve_form,
            'on_udate_reserve_form': self.on_udate_reserve_form,
            
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
        
        self.room_btn.grid(row=0, column=0, pady=2)
        self.reserve_btn.grid(row=1, column=0, pady=2)
        self.user_btn.grid(row=2, column=0, pady=2)
        self.usertype_btn.grid(row=3, column=0, pady=2)
        self.report_view_btn.grid(row=4, column=0, pady=2)

        self.app_form_window = None
        
        self.room_form = None
        self.reserveadd_form = None
        self.user_form = None
        self.usertype_form = None
        self.report_form = None

        self.room_view = None
        
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
    
  
    # handling view,model
    def open_room_form(self):
        data={}
        if self.room_form is None:
            with self.session_scope() as session:
                self.room_form = gui.forms.RoomForm(
                    self.workspace_frame,
                    db.forms.RoomForm(session).fields,
                    data,
                    self.callbacks
                )
            self.room_form.grid(row=0, column=0, sticky='NSEW')
        else: 
            self.room_form.lift()
    # == Room callback Contorls { 
    def on_add_room(self):
        try:
            data = self.room_form.get()
            with self.session_scope() as session:
                db.forms.RoomForm(self).save(session, data)
            messagebox.showinfo('Information','Record saved')
            self.room_form.clear(self)
        except NameError:
            messagebox.showinfo('Warning','Something went wrong')
    
    def on_update_room(self):
        
        pass
    
    def on_delete_room(self):
        pass
    
    def on_clear_room(self):
        pass
            
    def on_showall_room(self):
        print('== in showall C')
        with self.session_scope() as session:
            data =  db.queries.qry_room_showall_view(session)
            # print("quer is run==",data.items())
            self.room_form =  gui.forms.RoomForm(
                self.workspace_frame,
                db.forms.RoomForm(session).fields,
                data,
                self.callbacks
            )
        self.room_form.fetch_data(data)

    def on_search_room_data(self):
        pass
    
    def on_fetch_room_data(self):
        pass
    # } == Room callback Contorls 
    
    # handling view,model    
    def open_reserve_form(self):
        if self.reserveadd_form is None:
            with self.session_scope() as session:
                self.reserveadd_form = gui.forms.ReserveForm(
                    self.workspace_frame,
                    db.forms.ReserveForm().fields,
                    self.callbacks,
                )
            self.reserveadd_form.grid(row=0, column=0, sticky='NSEW')
        else: 
            self.reserveadd_form.lift()
    # == Reserve callback Contorls {     
    def on_add_reserve_form(self):
        try:
            data = self.reserveadd_form.get()
            with self.session_scope() as session:
                new_record = db.forms.ReserveForm().save(session, data)
            messagebox.showinfo('Information','Record saved')
        except NameError:
            messagebox.showinfo('Warning','Something went wrong')
            
    def on_udate_reserve_form(self):
        pass
            
    def open_user_form(self, called_from=None, modal=False):
        self.app_form_window = gui.widgets.Toplevel(self,called_from, modal)
        if modal is True:
            self.app_form_window.grab_set()
        with self.session_scope() as session:
            self.user_form = gui.forms.PersonForm(
                self.app_form_window,
                db.forms.PersonForm(session=session, data=None).fields,
                self.callbacks,
        )
        self.app_form_window.focus()

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
    # } == Reserve callback Contorls 
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

    def open_usertype_form(self):
        pass
    # --------end
    def open_search_form(self):
        if self.search_form is None:
            with self.session_scope() as session:
                self.search_form = gui.forms.SearchForm(
                    self.workspace_frame,
                    db.forms.SearchForm(self),
                    self.callbacks,
                )
            self.search_form.grid(row=0, column=0, sticky='NSEW')
        else: 
            self.search_form.lift()
            
    def on_search_form(self):
        try:
            data = self.search_form.get()
            self.search_form.reset()
            with self.session_scope() as session:
                list_search = db.forms.SearchForm().search(session, data)
                print(list_search)    
                # self.search_form = gui.forms.SearchForm().show(session)
            
            messagebox.showinfo('Information','Search complete')
        except NameError:
            messagebox.showinfo('Warning','Input type have a fault.')
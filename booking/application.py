from contextlib import contextmanager
from dataclasses import field, fields
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import tkinter as tk
from tkinter import ttk, messagebox

from .gui.widgets import Toplevel

from .db.models import Base
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
        # postgresql+psycopg2://user:password@host:port/dbname[?key=value&key=value...]
        global engine 
        engine = create_engine("postgresql://postgres:admin@localhost:5432/Booking", client_encoding="utf8",echo=True)
        self.Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        
        # At first run please create database Booking Schema and run this code for create model 
        # Base.metadata.create_all(engine)  
        
        self.callbacks = {
            'file--quit': self.quit,
            'settings--preferences': self.open_preferences,
            'settings--preferences--update': self.update_preferences,
            'settings--preferences': self.open_preferences,
            # 'filter_clemake_by_vehicleyear': self.filter_room_by_reserve,
            
            
            'open_roomadd_form':self.open_roomadd_form,
            'open_roomselect_form':self.open_roomselect_form,
            # 'open_roompayment_form':self.open_roompayment_form,
            'open_room_view': self.open_room_view,
            'on_save_room_form': self.on_save_room_form,
            
            # 'open_vehicleasset_form': self.open_vehicleasset_form,
            # 'qry_vehiclemake': self.qry_vehiclemake
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
        
        self.roomadd_btn = ttk.Button(self.left_nav_frame, text='Add new a Room',
                                          command=self.callbacks['open_roomadd_form'])
        self.roomselect_btn = ttk.Button(self.left_nav_frame, text='Select the Room',
                                          command=self.callbacks['open_roomselect_form'])
        # self.roompayment_btn = ttk.Button(self.left_nav_frame, text='payment Room',
        #                                   command=self.callbacks['open_roompayment_form'])
        self.room_view_btn = ttk.Button(self.left_nav_frame, text='View Rooms Records',
                                          command=self.callbacks['open_room_view'])
        
        
        self.roomadd_btn.grid(row=0, column=0)
        self.roomselect_btn.grid(row=1, column=0)
        # self.roompayment_btn.grid(row=2, column=0)
        self.room_view_btn.grid(row=3, column=0)

        self.app_form_window = None
        self.roomadd_form_window = None
        self.roomselect_form = None
        # self.roompayment_form = None

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
            
    def open_roomadd_form(self, called_from=None, modal=False):
        self.app_form_window = gui.widgets.Toplevel(self, called_from, modal)
        if modal is True:
            # print('is modal')
            self.app_form_window.grab_set()
        self.roomadd_form = gui.forms.RoomAddForm(
            self.app_form_window,
            db.forms.RoomAddForm().fields,
            self.callbacks,
            # print('Obj.roomadd_form init')
        )
        self.roomadd_form.pack(fill='x', expand=True)
        # print(self.roomadd_form)
        # self.app_form_window.focus()
        
    def on_save_room_form(self):
        try:
            data = self.roomadd_form.get()
            self.app_form_window = gui.widgets.Toplevel(self)
            self.app_form_window.grab_set()
            with self.session_scope() as session:
                new_record = db.forms.RoomAddForm().save(session, data)
                        
            messagebox.showinfo('Information','Record saved')
        except NameError:
            messagebox.showinfo('Warning','Something went wrong')
        
    def open_roomselect_form(self, called_from=None, modal=False):
        self.app_form_window = gui.widgets.Toplevel(self,called_from, modal)
        if modal is True:
            self.app_form_window.grab_set()
        with self.session_scope() as session:
            self.roomselect_form = gui.forms.RoomSelectForm(
                self.app_form_window,
                db.forms.RoomSelectForm(session=session, data=None).fields,
                self.callbacks,
        )
        self.roomselect_form.pack(fill='x', expand=True)
        self.app_form_window.focus()

    def open_room_view(self):
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
        
            
    # def on_save_room_form(self):
    #     data = self.room_form.get()
    #     print('save-room_form= data=>',data)
    #     with self.session_scope() as session:
    #         db.forms.RoomAddForm(session, data),save()
    #     self.room_form.reset()
    
    # def filter_room_by_reserve(self, reserve_id, roomnumber ):
    #     with self.session_scope() as session:
    #         return db.filters.room_by_reserve(session, reserve_id, roomnumber)
    
    
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

from contextlib import contextmanager
from dataclasses import field, fields
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import tkinter as tk
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
            
            
            'open_roomadd_form':self.open_roomadd_form,
            'open_reserveinfoadd_form':self.open_reserveinfoadd_form,
            'open_roomselect_form':self.open_roomselect_form,
            'open_search_form':self.open_search_form,
            
            'open_room_view': self.open_room_view,
            'on_save_room_form': self.on_save_room_form,
            'on_save_reserve_form': self.on_save_reserve_form,
            'on_search_form': self.on_search_form,
            'open_reserveinfoadd_form': self.open_reserveinfoadd_form,
            
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
        
        self.roomadd_btn = ttk.Button(self.left_nav_frame, text='      Add New Room     ',
                                          command=self.callbacks['open_roomadd_form'])
        self.reserveadd_btn = ttk.Button(self.left_nav_frame, text='     Add Reserve info   ',
                                          command=self.callbacks['open_reserveinfoadd_form'])
        self.search_btn = ttk.Button(self.left_nav_frame, text='             Search          ',
                                          command=self.callbacks['open_search_form'])
        # self.roomselect_btn = ttk.Button(self.left_nav_frame, text='Select the Room',
        #                                   command=self.callbacks['open_roomselect_form'])
        # self.roompayment_btn = ttk.Button(self.left_nav_frame, text='payment Room',
        #                                   command=self.callbacks['open_roompayment_form'])
        self.room_view_btn = ttk.Button(self.left_nav_frame, text='    View Rooms Records  ',
                                          command=self.callbacks['open_room_view'])
        
        
        self.roomadd_btn.grid(row=0, column=0)
        self.reserveadd_btn.grid(row=1, column=0)
        # self.roomselect_btn.grid(row=2, column=0)
        self.search_btn.grid(row=3, column=0)
        # self.roompayment_btn.grid(row=2, column=0)
        self.room_view_btn.grid(row=4, column=0)

        self.app_form_window = None
        self.roomadd_form = None
        self.search_form = None
        self.reservinfoadd_form = None
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
    
    def open_search_form(self):
        if self.search_form is None:
            with self.session_scope() as session:
                self.search_form = gui.forms.SearchForm(
                    self.workspace_frame,
                    db.forms.SearchForm(self).fields,
                    self.callbacks,
                )
            self.search_form.grid(row=0, column=0, sticky='NSEW')
        else: 
            self.search_form.lift()
            
    def on_search_form(self):
        try:
            data = self.search_form.get()
            print(type(data))
            self.search_form.reset()
            with self.session_scope() as session:
                list_search = db.forms.SearchForm().search(session, data)
                
                # self.search_form = gui.forms.SearchForm().show(session)
            messagebox.showinfo('Information','Search complete')
        except NameError:
            messagebox.showinfo('Warning','Input type have a fault.')
            
    def open_roomadd_form(self):
        if self.roomadd_form is None:
            with self.session_scope() as session:
                self.roomadd_form = gui.forms.RoomAddForm(
                    self.workspace_frame,
                    db.forms.RoomAddForm(session).fields,
                    self.callbacks,
                )
            self.roomadd_form.grid(row=0, column=0, sticky='NSEW')
        else: 
            self.roomadd_form.lift()
        
    def on_save_room_form(self):
        try:
            data = self.roomadd_form.get()
            print(data)
            with self.session_scope() as session:
                new_record = db.forms.RoomAddForm().save(session, data)
            messagebox.showinfo('Information','Record saved')
        except NameError:
            messagebox.showinfo('Warning','Something went wrong')
            
    def open_reserveinfoadd_form(self):
        if self.reservinfoadd_form is None:
            with self.session_scope() as session:
                self.reservinfoadd_form = gui.forms.ReserveInfoAddForm(
                    self.workspace_frame,
                    db.forms.ReserveInfoAddForm().fields,
                    self.callbacks,
                )
            self.reservinfoadd_form.grid(row=0, column=0, sticky='NSEW')
        else: 
            self.reservinfoadd_form.lift()
        
    def on_save_reserve_form(self):
        try:
            data = self.reservinfoadd_form.get()
            with self.session_scope() as session:
                new_record = db.forms.ReserveInfoAddForm().save(session, data)
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

    # def filter_search(self):
    #     with self.session_scope() as session:
    #         return db.filters.filter_search(session)
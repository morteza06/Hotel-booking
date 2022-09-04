from tkinter import font as tkfont
from tkinter import ttk
from .constants import DEFAULT_CONFIG
from .ext.themes import THEMES
# from .db import models as MD
# from sqlalchemy import create_engine
# import sqlalchemy
# from sqlalchemy.orm import sessionmaker
import configparser


class AppConfig:
    def __init__(self):
        self.cp = configparser.ConfigParser()
        self._load_themes()
        self.load()
        # self.database_exists()
    
    # def database_exists(self):
    #     # create database manually in database Software
        
    #     engine = create_engine("postgresql://postgres:admin@localhost:5432/Booking", client_encoding="utf8")
    #     self.Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    #     if  sqlalchemy.inspect(engine).has_table('Room'):
    #         print('Table room exitst')
    #     else:
    #         print('database Table not exisit')
        
    #     if not engine.dialect.has_table(engine, Variable_tableName):  # If table don't exist, Create.
    #         metadata = MetaData(engine)
    #         # Create a table with the appropriate Columns

    #     # Implement the creation
    #     metadata.create_all()
        
        
    def _load_themes(self):
        style = ttk.Style()
        for k, v in THEMES.items():
            style.theme_create(k, v['parent'], v['settings'])
        # style.theme_use('Dark')
        print(style.theme_names())

    def _update_font(self):
        for font in ('TkHeadingFont', 'TkTextFont', 'TkDefaultFont'):
            f = tkfont.nametofont(font)
            f.configure(size=self.cp['Appearance']['fontsize'])
        return

    def save(self):
        with open('settings.ini', 'w') as configfile:
            self.cp.write(configfile)
        return

    def load(self):
        self.cp.read_dict(DEFAULT_CONFIG)
        self.cp.read('settings.ini')
        self._update_font()
        return

    def update_settings(self, data):
        if 'fontsize' in data:
            self.cp.set('Appearance', 'fontsize', data['fontsize'])
            self._update_font()
        self.save()
        return

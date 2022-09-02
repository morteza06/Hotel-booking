from tkinter import StringVar, font as tkfont
import tkinter as tk
from  tkinter import ttk
from tkinter.constants import  BOTH, E, EW, LEFT, NS, NW, S, SINGLE, VERTICAL, X, END
from constants import *
from tkinter.messagebox import askyesno, showerror, showwarning, showinfo
from db import models 



class Application(tk.Tk):
    def __init__(self,**kwargs) :
        super().__init__(**kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.text_font = tkfont.Font(family='Helvetica', size=16, weight="bold", slant="roman")
        self.geometry(WINDOW_SIZE)
        self.title(WINDOW_TITLE)
        self.resizable(False, False)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}

        # for frame in (MainMenu):
        frameObject = MainMenu(container, self) # container Frame is a parent, tkinter.Tk is a controller
        self.frames[MainMenu.__name__] = frameObject
        
        # self.frameObject = {}
        for F in (MainPage, StartPage, PageOne, PageTwo):
            page_name = F.__name__
            frameObject = F(parent=container, controller=self)
            self.frames[page_name] = frameObject

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frameObject.grid(row=0, column=0, sticky="nsew")
     
    
    def showFrame(self, frameName):
        '''Show a frame for the given page name'''
        frame = self.frames[frameName]
        frame.tkraise()
    
    def __del__(self):
        print('Destructor Called')
#================================================================================    
class MainPage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.controller = controller
        
        self.backFrame = tk.Frame(self)
        self.backFrame.place(x=0, y=0, anchor="nw", height=DEFAULT_FRAME_BACK_HEIGHT, width = WINDOW_WIDTH )

        self.dataFrame = tk.Frame(self) #, bg ='blue' )
        self.dataFrame.place(x=0, y=DEFAULT_FRAME_BACK_HEIGHT , anchor="nw", height=DEFAULT_FRAME_DATA_HEIGHT, width = WINDOW_WIDTH  )
        
        label = tk.Label(self, text="This is the Main page", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        
        label = tk.Label(self, text="Room lists:", font=controller.text_font)
        label.pack(side="left", fill="x", pady=10)

        self.room_number = StringVar
        self.room_number = ""
        # lbl_search = tk.Label(self, width=8, text="Search By",  bg="crimson", fg="white", font=("times new roman", 15, "bold"))
        # lbl_search.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        # combo_search = ttk.Combobox(self, textvariable=self.room_number, font=("times new roman", 13), state="readonly" )
        # combo_search['values'] = self.lists()
        # combo_search.pack(side="left", fill="x", pady=10)
        # combo_search.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # txt_search = tk.Entry(self, textvariable=self.search_txt, font=("times new roman", 13), bd=5)
        # txt_search.grid(row=0, column=2, padx=5, pady=5, sticky="w")

        # searchbtn = tk.Button(self, text="Search", width=8, command=self.search_data).grid(row=0, column=3, padx=5, pady=5)
        # showallbtn = tk.Button(self, text="Show All", width=8,  command=self.fetch_data).grid(row=0, column=4, padx=5, pady=5)


        button1 = tk.Button(self, text="Go to StartPage",
                            command=lambda: controller.showFrame("StartPage"))
        button2 = tk.Button(self, text="Go to Page one",
                            command=lambda: controller.showFrame("PageOne"))
        button3 = tk.Button(self, text="Go to Page Two",
                            command=lambda: controller.showFrame("PageTwo"))
        button1.pack()
        button2.pack()
        button3.pack()
            
#============================================                   
class MainMenu(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        print('run maminmenu')
        self.buttonsDataDict = MM_BUTTONS_DICT # this only copies from constants and its values are strings
        self.buttonsObjectDict = {} # values are button objects
        self.continueState = "disabled" # when you first start the program, continue and save buttons are disabled
        self.saveState = "disabled"

        # so that main menu buttons are centered
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure( len(self.buttonsDataDict) + 1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.createButtons()
        
        # print('createbuttons runned')
        # self.deployButtons(controller)
        # print('deploy Buttons runned')


    def createButtons(self):
        for k, v in self.buttonsDataDict.items():
            self.buttonsObjectDict[k] = tk.Button(self, text=v, width= MM_BUTTON_WIDTH, pady = MM_BUTTON_Y_PADDING) # container is self - that is, MainMenu instance

            
    def deployButtons(self, app):
        for k, v in self.buttonsObjectDict.items():
            v.grid(row = k, column = 0, pady = MM_BUTTON_Y_PADDING)
        self._bindButtons(app)
        
    # def _bindExit(self, app):
    #     self.buttonsObjectDict[6].config(command = app.destroy )
        
    # def _bindLogin(self, app):
    #     app1 = Derived()
    #     app1.master.title("Mybooking app")
    #     app1.mainloop()
        
    def _bindButtons(self, app):
        pass
        # self._bindLogin(app)
        # self._bindTicketBooking(app)
        # self._bindLogoutn(app)
        # self._bindExit(app)
#====================================  
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is the start page", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        button1 = tk.Button(self, text="Go to Page One",
                            command=lambda: controller.showFrame("PageOne"))
        button2 = tk.Button(self, text="Go to Page Two",
                            command=lambda: controller.showFrame("PageTwo"))
        button3 = tk.Button(self, text="Go to MainPage",
                            command=lambda: controller.showFrame("MainPage"))
        button1.pack()
        button2.pack()
        button3.pack()

#====================================
class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 1", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button1 = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.showFrame("StartPage"))
        button2 = tk.Button(self, text="Go to Page Two",
                            command=lambda: controller.showFrame("PageTwo"))
        button3 = tk.Button(self, text="Go to MainPage",
                            command=lambda: controller.showFrame("MainPage"))
        button1.pack()
        button2.pack()
        button3.pack()

#===============================
class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 2", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button1 = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.showFrame("StartPage"))
        button2 = tk.Button(self, text="Go to Page One",
                            command=lambda: controller.showFrame("PageOne"))
        button3 = tk.Button(self, text="Go to MainPage",
                            command=lambda: controller.showFrame("MainPage"))
        button1.pack()
        button2.pack()
        button3.pack()


#============================================
def main():
    
    models.init_db()    
    app = Application()
    app.mainloop()



if __name__ == "__main__":
    
    main()
    
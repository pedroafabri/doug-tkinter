import tkinter as tk
from tkinter import ttk
from PIL import ImageTk,Image
from tkinter.messagebox import showinfo
import pathlib

# Scrollable frame class
class ScrollableFrame(tk.Frame):
    def __init__(self, container, bg_color, fg_color, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = tk.Canvas(self, bg=bg_color)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview, bg=fg_color)
        self.scrollable_frame = tk.Frame(canvas, bg=bg_color)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)
        
        

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        

# AppUI class - Singleton
class AppUI(tk.Frame):
    
    __instance = None

    @staticmethod
    def get_instance():
        if AppUI.__instance == None:
            raise Exception("Class not instanciated yet.")
        return AppUI.__instance

    # Constructor
    def __init__(self, title, features, logo=str(pathlib.Path(__file__).parent.absolute())+"/logo.png", logo_width=300, logo_height=181):

        if AppUI.__instance != None:
            raise Exception("This class is a singleton and has already been instanciated. Use method 'get_instance()' instead.")
        
        AppUI.__instance = self # Creates the singleton
        self.master = tk.Tk()
        self.primary_color="white"
        self.secondary_color="orange red"
        self.terciary_color="royalblue1"
        self.files = []
        self.checkboxes = []
        self.pages = len(features)
        self.current_page = 0
        self.features = features
        self.configure_master(title)
        self.create_logo(logo, logo_width, logo_height)
        self.create_file_label()
        self.create_page_navigation()
        self.create_scrollable_frame()
        self.create_buttons()
        self.update_pages()
        self.create_progress_bar()
        self.center_window()

    # starts mainloop
    def show(self):
        self.master.mainloop()

    # Configures the main window
    def configure_master(self, title):
        self.master.config(bg=self.primary_color)
        self.master.attributes("-topmost", 1)
        self.master.overrideredirect(True) # turns off title bar, geometry
        self.master.resizable(False, False)

        title_bar = tk.Frame(self.master, bg=self.secondary_color, relief='raised', bd=2,highlightthickness=0)
        
        # put a close button on the title bar
        self.cross_button = tk.Button(title_bar, text='X', command=self.master.destroy, bg=self.secondary_color,padx=2,pady=2,activebackground='red',bd=0,font="bold",fg='white',highlightthickness=0)

        # minimize button
        self.minimize_button = tk.Button(title_bar, text='—', command=self.minimize, bg=self.secondary_color,padx=2,pady=2,activebackground='red',bd=0,font="bold",fg='white',highlightthickness=0)

        # Title Label
        title_label = tk.Label(title_bar, text=title, bg=self.secondary_color, fg=self.primary_color)

        # pack the widgets
        title_bar.pack(expand=1, fill=tk.X)
        self.cross_button.pack(side=tk.RIGHT)
        self.minimize_button.pack(side=tk.RIGHT)
        title_label.pack(side=tk.LEFT)
        self.xwin=0
        self.ywin=0 

        # Binds
        title_bar.bind('<B1-Motion>', self.move_window)
        title_bar.bind('<Button-1>', self.get_pos)
        self.cross_button.bind('<Enter>', lambda x:self.change_on_hovering(self.cross_button))
        self.cross_button.bind('<Leave>', lambda x:self.return_to_normalstate(self.cross_button))
        self.minimize_button.bind('<Enter>', lambda x:self.change_on_hovering(self.minimize_button))
        self.minimize_button.bind('<Leave>', lambda x:self.return_to_normalstate(self.minimize_button))
        self.master.bind('<Map>', self.window_activated)

    # get mouse position
    def get_pos(self, event):
        self.xwin = self.master.winfo_x()
        self.ywin = self.master.winfo_y()
        startx = event.x_root
        starty = event.y_root

        self.ywin = self.ywin - starty
        self.xwin = self.xwin - startx

    # Minimize window
    def minimize(self, event = None):
        self.master.overrideredirect(False)
        self.master.iconify()

    # Maximize window
    def maximize(self):
        self.master.deiconify()
        self.window_activated(None)

    # Reactivates de window
    def window_activated(self, event):
        if(self.master.state() == "normal"):
           self.master.overrideredirect(True)

    # move window on drag
    def move_window(self, event):
        self.master.geometry('+{0}+{1}'.format(event.x_root + self.xwin, event.y_root + self.ywin))

    # change close on hover
    def change_on_hovering(self, button):
        button['bg']='red'

    # change close on blur
    def return_to_normalstate(self, button):
        button['bg']=self.secondary_color

    # Import the logo.png
    def create_logo(self, logo, logo_width, logo_height):
        canvas = tk.Canvas(self.master, width=logo_width, height=logo_height, bg=self.primary_color, highlightthickness=0)
        canvas.pack()
        self.logo_image = ImageTk.PhotoImage(Image.open(logo)) 
        canvas.create_image(0,0,anchor=tk.NW, image=self.logo_image)
        
    def create_file_label(self):
        file_container = tk.Frame(self.master, bg=self.primary_color)
        self.file_label = tk.Label(file_container, bg=self.primary_color)

        self.file_label.pack(side=tk.LEFT)
        file_container.pack(fill=tk.X)

    # Creates the page navigation
    def create_page_navigation(self):
        buttons_container = tk.Frame(self.master, bg=self.primary_color)
        self.check_all_button = tk.Button(buttons_container, text="Marcar Todos", bg=self.secondary_color, fg=self.primary_color) 
        self.uncheck_all_button = tk.Button(buttons_container, text="Desmarcar Todos", bg=self.secondary_color, fg=self.primary_color) 
        self.back_button = tk.Button(buttons_container, text="<", bg=self.secondary_color, fg=self.primary_color)
        self.pages_label = tk.Label(buttons_container, bg=self.primary_color)
        self.next_button = tk.Button(buttons_container, text=">", bg=self.secondary_color, fg=self.primary_color) 
        fixed_label = tk.Label(buttons_container, bg=self.primary_color, text="Cenários Disponíveis")

        self.back_button["command"] = self.previous_page
        self.next_button["command"] = self.next_page
        self.check_all_button["command"] = self.check_all
        self.uncheck_all_button["command"] = self.uncheck_all

        fixed_label.pack(side=tk.LEFT, padx=5, pady=5 )    
        self.next_button.pack(side=tk.RIGHT, padx=5, pady=5)
        self.pages_label.pack(side=tk.RIGHT, padx=5, pady=5)
        self.back_button.pack(side=tk.RIGHT, padx=5, pady=5)
        self.check_all_button.pack(side=tk.RIGHT, padx=5, pady=5)
        self.uncheck_all_button.pack(side=tk.RIGHT, padx=5, pady=5)
        buttons_container.pack(fill=tk.X)

    def check_all(self):
        for page in self.checkboxes:
            for checkbox in page:
                checkbox.set(1)

    def uncheck_all(self):
        for page in self.checkboxes:
            for checkbox in page:
                checkbox.set(0)

    # Instantiates the Scrollable Frame
    def create_scrollable_frame(self):
        self.scroll_container = tk.Frame(self.master, bg=self.primary_color)
        self.scrollable_frame = ScrollableFrame(self.scroll_container, borderwidth=1, bg_color=self.primary_color, fg_color=self.secondary_color, relief=tk.RIDGE, highlightbackground="orange red")
        self.create_checkboxes_list()
        self.add_checkboxes()
        self.scrollable_frame.pack()
        self.scroll_container.pack(side=tk.TOP, fill=tk.X)

    # Creates a list of checkboxes variables
    def create_checkboxes_list(self):
        for page in self.features:
            self.files.append(page)
            new_page = []
            for feature in self.features[page]:
                new_page.append(tk.IntVar())
            self.checkboxes.append(new_page)

    # Creates the buttons
    def create_buttons(self):
        buttons_container = tk.Frame(self.master, bg=self.primary_color)
        self.confirm_button = tk.Button(buttons_container, text="Confirmar", bg=self.secondary_color, fg=self.primary_color)
        self.results_button = tk.Button(buttons_container, text="Resultados", bg=self.secondary_color, fg=self.primary_color) 

        self.confirm_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.results_button.pack(side=tk.LEFT, padx=5, pady=5)
        buttons_container.pack(side=tk.BOTTOM)

    # Adds the checkboxes based on "features" list
    def add_checkboxes(self):
        for widget in self.scrollable_frame.scrollable_frame.winfo_children():
            widget.destroy()

        for idx, feature in enumerate(self.features[self.files[self.current_page]]):
            cb = tk.Checkbutton(self.scrollable_frame.scrollable_frame, text=feature, variable=self.checkboxes[self.current_page][idx], wraplength=380, justify=tk.LEFT, bg=self.primary_color)
            cb.grid(sticky=tk.W)
    
    def update_pages(self):
        self.pages_label["text"] = "{0} de {1}".format(self.current_page + 1, self.pages)
        self.file_label["text"] = self.files[self.current_page]

    def previous_page(self):
        if(self.current_page == 0):
            return
        self.current_page = self.current_page - 1
        self.update_pages()
        self.add_checkboxes()

    def next_page(self):
        if(self.current_page == self.pages - 1):
            return
        self.current_page = self.current_page + 1
        self.update_pages()
        self.add_checkboxes()
    
    # Returns the selected values as a list
    def get_selected(self):
        returnList = []

        for page_idx, page in enumerate(self.checkboxes):
            for item_idx, item in enumerate(page):
                if item.get() > 0:
                    returnList.append(self.features[self.files[page_idx]][item_idx]) 
        return returnList
        
    # Set the confirm button command
    def set_confirm_command(self, command):
        self.confirm_button["command"] = command

    # Set the results button command
    def set_results_command(self, command):
        self.results_button["command"] = command

    # Default close command destroys the application
    def default_close_command(self):
        self.master.destroy()

    def center_window(self):
        # Gets the requested values of the height and widht.
        windowWidth = self.master.winfo_reqwidth()
        windowHeight = self.master.winfo_reqheight()
        print("Width",windowWidth,"Height",windowHeight)
        
        # Gets both half the screen width/height and window width/height
        positionRight = int(self.master.winfo_screenwidth()/2 - windowWidth/2)
        positionDown = int(self.master.winfo_screenheight()/2 - windowHeight/2)
        
        # Positions the window in the center of the page.
        self.master.geometry("+{}+{}".format(positionRight, positionDown))

    # Creates a progress bar with progress label
    def create_progress_bar(self):
        
        # Create style for progress label
        self.style = ttk.Style(self.master)
        # add the label to the progressbar style
        self.style.layout("LabeledProgressbar",
                [('LabeledProgressbar.trough',
                {'children': [('LabeledProgressbar.pbar',
                                {'side': 'left', 'sticky': 'ns'}),
                                ("LabeledProgressbar.label",
                                {'side': 'left', "sticky": ""})],
                'sticky': 'nswe'})])
        self.style.configure("LabeledProgressbar", foreground="black", background=self.secondary_color)
        progress_container = tk.Frame(self.master, bg=self.primary_color)
        self.progress = tk.DoubleVar()
        progress_bar = ttk.Progressbar(progress_container, variable=self.progress, maximum=100, style="LabeledProgressbar")
        
        progress_bar.pack(fill=tk.X)
        progress_container.pack(fill=tk.X)
        self.style.configure("LabeledProgressbar", text="")

    # Updates progress bar
    def update_progress(self, value):
        self.progress.set(value)
        self.master.update()

    # Update the process name
    def update_process(self, process):
        self.style.configure("LabeledProgressbar", text=process)

    # Check if any test is selcted
    def is_test_selected(self):
        for page in self.checkboxes:
            for checkbox in page:
                if(checkbox.get() > 0):
                    return True
        return False

    def show_popup(self, title, text):
        showinfo(title, text)

    def disable_screen(self):
        self.disable_enable('disabled')

    def enable_screen(self):
        self.disable_enable('normal')

    def reset_progress(self):
        self.update_process("")
        self.update_progress(0)

    def disable_enable(self, status):
        self.back_button.configure(state=status)
        self.next_button.configure(state=status)
        self.confirm_button.configure(state=status)
        self.results_button.configure(state=status)
        self.check_all_button.configure(state=status)
        self.uncheck_all_button.configure(state=status)
        for widget in self.scrollable_frame.scrollable_frame.winfo_children():
            widget.configure(state=status)

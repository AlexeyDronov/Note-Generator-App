#######################################################################
# Modules imports
import tkinter as tk
import numpy as np
from PIL import ImageTk, Image
import musical_scales as ms
import customtkinter as ctk
import pygame
import CTkSpinbox
import time
import os, sys

#######################################################################

class MainWindow(tk.Frame): # Create the Main Window and create two frames in it
    def __init__(self, master=None, *args, **kwargs):
        super().__init__(master)
        self.master = master
        self.pack()
        self.configure(bg='#c1bed6')
        self.create_widgets()

    def create_widgets(self):
        # Create a Top Frame
        self.top_frame = TopFrame(self)
        self.top_frame.pack(side="top")

        # Create a Bottom Frame
        self.bottom_frame = BottomFrame(self)
        self.bottom_frame.pack(side="bottom")

        

#######################################################################

class TopFrame(tk.Frame):
    def __init__(self, master=None):
        global looping
        super().__init__(master)
        self.master = master
        self.pack()
        self.configure(bg='#c1bed6')
        self.note_displayed()
        # Create a Button that starts the Randomiser
        self.randomise_button = ctk.CTkButton(self, text = "Randomise!", command=self.intermediate_step)
        self.randomise_button.grid(row = 1, column=0)

        # Create a Button that turns off the volume
        self.volume_icon = ctk.CTkButton(self, image=img_volume,fg_color='transparent',text='', width=5, 
                                            command=self.turn_volume_off, bg_color='transparent', hover_color='#c1bed6')
        self.volume_icon.grid(row=1, column=0, sticky='w')
        looping = True
        

    def note_displayed(self):
        global next_notes

        # Label that will be updated when a new note is selected
        next_notes = ['C']
        self.notes = tk.Label(self, text=next_notes[0], font=("Arial Rounded MT Bold", 180), padx=200, pady=40,width=1, bg='#c1bed6')
        self.notes.grid(row=0, column=0)

        

    def intermediate_step(self):
        global looping
        # Replace the old button with a new one to stop the randomiser
        looping = True

        # Replace the Randomise button with a Stop button
        self.randomise_button.destroy()
        self.stop_button = ctk.CTkButton(self, text = "Stop", command=self.stop_randomiser)
        self.stop_button.grid(row = 1, column=0)

        self.randomise_notes()

    def randomise_notes(self): # Note randomiser algorithm
        global looping
        global entry_box_value, selected_num_notes, selected_notes_from_scale, next_notes
        # Get the selected time interval 
        self.interval = int(entry_box_value)

        # Loop that randomises the notes displayed on the screen
        if looping:
            self.notes.destroy() # Destroy the previous label with notes
            next_notes = []
            # Catch cases when no notes are selected 
            if len(selected_notes_from_scale)>0: 
                self.next_note = np.random.choice(selected_notes_from_scale, size=selected_num_notes, replace=False)
            else:
                self.next_note = ''

            # Create a list with the notes to be displayed
            for i in range(len(self.next_note)):
                next_notes.append(self.next_note[i])
            
            # Place the notes on the frame depending on how many notes are selected
            if selected_num_notes == 1:
                self.notes = tk.Label(self, text=next_notes[0], font=("Arial Rounded MT Bold", 180), padx=200,width=1, pady=40, bg='#c1bed6')
                self.notes.grid(row=0, column=0) 
            elif selected_num_notes == 2:
                self.notes = tk.Label(self, text=next_notes[0] + next_notes[1], font=("Arial Rounded MT Bold", 159), padx=206.4,width=1, pady=51.5, bg='#c1bed6')
                self.notes.grid(row=0, column=0)
            elif selected_num_notes == 3:
                self.notes = tk.Label(self, text=next_notes[0]+ next_notes[1] + next_notes[2], font=("Arial Rounded MT Bold", 140), padx=211, pady=63, width=1, bg='#c1bed6')
                self.notes.grid(row=0, column=0)

            self.play_sounds() # Start the sound playback
            self.master.after(self.interval*1000, self.randomise_notes) # Repeat the loop 
    


    def stop_randomiser(self):
        global looping
        # Assign the looping variable 0 and replase the stop button with randomise button
        looping = False
        self.stop_button.destroy()
        self.randomise_button = ctk.CTkButton(self, text = "Randomise!", command=self.intermediate_step)
        self.randomise_button.grid(row = 1, column=0)

    def play_sounds(self):
        global next_notes, selected_num_notes
        # Start the playback of sounds based on how many notes were selected
        if selected_num_notes ==2:
            pygame.mixer.set_num_channels(2)
            pygame.mixer.Channel(0).play(pygame.mixer.Sound(music_files[next_notes[0]]))
            pygame.mixer.Channel(1).play(pygame.mixer.Sound(music_files[next_notes[1]]))
        if selected_num_notes==3:
            pygame.mixer.set_num_channels(3)
            pygame.mixer.Channel(0).play(pygame.mixer.Sound(music_files[next_notes[0]]))
            pygame.mixer.Channel(1).play(pygame.mixer.Sound(music_files[next_notes[1]]))
            pygame.mixer.Channel(2).play(pygame.mixer.Sound(music_files[next_notes[2]]))
        elif selected_num_notes ==1:
            pygame.mixer.set_num_channels(1)
            pygame.mixer.Channel(0).play(pygame.mixer.Sound(music_files[next_notes[0]]))
            
    def turn_volume_off(self):
        global selected_num_notes
        # Turn the volume off
        self.volume_icon_value = 0
        time.sleep(0.2)
        if selected_num_notes == 1:
            pygame.mixer.Channel(0).set_volume(0)
        elif selected_num_notes == 2:
            pygame.mixer.Channel(0).set_volume(0)
            pygame.mixer.Channel(1).set_volume(0)
        elif selected_num_notes==3:
            pygame.mixer.Channel(0).set_volume(0)
            pygame.mixer.Channel(1).set_volume(0)
            pygame.mixer.Channel(2).set_volume(0)

        # Replace the volume icon on with the volume icon off
        self.volume_icon.destroy()
        self.volume_icon_off = ctk.CTkButton(self, image=img_volume_off,fg_color='transparent',text='', 
                                         command=self.turn_volume_on, bg_color='transparent', width=5, hover_color='#c1bed6')
        self.volume_icon_off.grid(row=1, column=0, sticky='w')

    def turn_volume_on(self):
        global selected_num_notes
        time.sleep(0.2)
        # Turn volume on
        self.volume_icon_value=1
        if selected_num_notes == 1:
            pygame.mixer.Channel(0).set_volume(1)
        elif selected_num_notes == 2:
            pygame.mixer.Channel(0).set_volume(1)
            pygame.mixer.Channel(1).set_volume(1)
        elif selected_num_notes ==3:
            pygame.mixer.Channel(0).set_volume(1)
            pygame.mixer.Channel(1).set_volume(1)
            pygame.mixer.Channel(2).set_volume(1)

        # Replace the volume icon off with volume icon on
        self.volume_icon_off.destroy()
        self.volume_icon = ctk.CTkButton(self, image=img_volume,fg_color='transparent',text='', 
                                         command=self.turn_volume_off, bg_color='transparent', width=5, hover_color='#c1bed6')
        self.volume_icon.grid(row=1, column=0, sticky='w')



#######################################################################

class BottomFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.configure(bg='#c1bed6')
        self.create_canvas()
        self.put_options_label()
        self.put_time_interval()
        self.put_note_selection()
        self.multiple_notes_selection()
        self.select_scale_to_show()
        self.open_fretboard_view()
        

    def put_options_label(self):
        # Create a canvas with the separating line and place the Options label underneath
        self.line_canv = tk.Canvas(self, width=500, height=45, bg='#c1bed6', highlightthickness=0)
        self.line_canv.grid(row=0, column=0, columnspan=15, pady=20, rowspan=1)
        self.line_canv.create_line(0,3,1000,3, fill='black', width=2)
        self.line_canv.grid_propagate(0) 

        self.options_label = tk.Label(self.line_canv, text = "Options", font=("American Typewriter", 30), bg='#c1bed6')
        self.options_label.place(x=196, y=5)

    def put_time_interval(self):
        # Place the time interval label and a spinbox to select the time interval
        self.time_interval_label = tk.Label(self, text = "Time interval:",font=('American Typewriter', 15), bg='#c1bed6', pady=15)
        self.time_interval_label.grid(row=1, column=0)

        self.entry_box = CTkSpinbox.CTkSpinbox(self, min_value=1, max_value=30, fg_color='#c1bed6', start_value=1,
                                               button_color='#3B8ED0', button_hover_color='#1F6AA5', border_color='#c1bed6', 
                                               text_color='black',button_border_color='#c1bed6')
        self.entry_box.grid(row=1, column=1, sticky='W')
        
        self.get_input_value()
    
    def get_input_value(self):
        global entry_box_value
        # Loop to update the global variable associated with a spinbox 
        self.test = True
        if self.test:
            entry_box_value = self.entry_box.get()
            self.after(10, self.get_input_value)

    def create_canvas(self):
        # Draw the keyboard displaying which notes are selected
        white_key_width = 60
        white_key_height = 150
        black_key_width = 45
        black_key_height = 100
        note_selection_canvas = tk.Canvas(self, bg='#c1bed6', width=white_key_width*7, height=white_key_height, highlightthickness=0.5)
        note_selection_canvas.grid(row=3, column=1, columnspan=14)

        # Draw white keys
        for i in range(7):
            x0 = i * white_key_width
            y0 = 0
            x1 = x0 + white_key_width
            y1 = white_key_height
            note_selection_canvas.create_rectangle(x0, y0, x1, y1, fill="white", outline="black")

        # Draw black keys
        black_keys_pos = [1, 2, 4, 5, 6]  # Indices of black keys
        for i in black_keys_pos:
            x0 = (i * white_key_width) - (black_key_width / 2)
            y0 = 0
            x1 = x0 + black_key_width
            y1 = black_key_height
            note_selection_canvas.create_rectangle(x0, y0, x1, y1, fill="black", outline="black")

    def put_note_selection(self):
        # Long ass dumb code to put all the buttons in their positions on the fretboard

        note_selection_label = tk.Label(self, text = 'Notes displayed:',font=('American Typewriter', 15), padx=10,pady=5, bg='#c1bed6')
        note_selection_label.grid(row=2, column=0, rowspan=2)

        self.checkbox_vars = [tk.IntVar() for i in range(12)]
        c = tk.Checkbutton(self, text="C", variable=self.checkbox_vars[0], command=self.deactivate_loop, bg='white')
        cs = tk.Checkbutton(self, text="C#", variable=self.checkbox_vars[1], command=self.deactivate_loop, bg='black', fg='white')
        d = tk.Checkbutton(self, text="D", variable=self.checkbox_vars[2], bg='white', command=self.deactivate_loop)
        ds = tk.Checkbutton(self, text="D#", variable=self.checkbox_vars[3], command=self.deactivate_loop, bg='black', fg='white')
        e = tk.Checkbutton(self, text="E", variable=self.checkbox_vars[4], bg='white', command=self.deactivate_loop)
        f = tk.Checkbutton(self, text="F", variable=self.checkbox_vars[5], bg='white', command=self.deactivate_loop)
        fs = tk.Checkbutton(self, text="F#", variable=self.checkbox_vars[6], command=self.deactivate_loop, bg='black', fg='white')
        g = tk.Checkbutton(self, text="G", variable=self.checkbox_vars[7], bg='white', command=self.deactivate_loop)
        gs = tk.Checkbutton(self, text="G#", variable=self.checkbox_vars[8], command=self.deactivate_loop, bg='black', fg='white')
        a = tk.Checkbutton(self, text="A", variable=self.checkbox_vars[9], bg='white', command=self.deactivate_loop)
        aS = tk.Checkbutton(self, text="A#", variable=self.checkbox_vars[10], command=self.deactivate_loop, bg='black', fg='white')
        b = tk.Checkbutton(self, text="B", variable=self.checkbox_vars[11], bg='white', command=self.deactivate_loop)
        c.place(x=155, y=245) 
        cs.place(x=183, y=150)
        d.place(x= 215, y=245)
        ds.place(x=243, y=150) 
        e.place(x= 275, y=245)
        f.place(x= 335, y=245)
        fs.place(x=364, y=150) 
        g.place(x= 395, y=245)
        gs.place(x=423, y=150) 
        a.place(x= 455, y=245)
        aS.place(x=484, y=150) 
        b.place(x= 515, y=245)
        c.select()
        cs.deselect()
        d.select()
        ds.deselect()
        e.select()
        f.select()
        fs.deselect()
        g.select()
        gs.deselect()
        a.select()
        aS.deselect()
        b.select()

        self.test_scale = False
        self.get_notes_from_scale()

    

    
    def multiple_notes_selection(self):
        # Radiobuttons to select how many notes are displayed at once
        select_num_notes = tk.Label(self, text="Number of \nnotes displayed:",font=('American Typewriter', 15), bg='#c1bed6', pady=10)
        select_num_notes.grid(row = 4, column=0, rowspan=2, sticky='nsew')

        self.num_notes_var = tk.StringVar()
        self.num_notes_var.set("1")
        self.num_notes_options = ["1", "2", "3"]
        for idx, option in enumerate(self.num_notes_options):
            tk.Radiobutton(self, text = option, variable=self.num_notes_var, value=option, bg='#c1bed6').grid(row=4, column=idx+1, rowspan=2)
    
        self.get_num_notes_selected()
    
    def get_num_notes_selected(self):
        # Loop to update the global variable associated with the number of notes selected 
        global selected_num_notes
        if self.test:
            selected_num_notes = int(self.num_notes_var.get())
            self.after(1, self.get_num_notes_selected)
    
    def select_scale_to_show(self):
        # Option to select from the scale instead of manual input
        select_scale_label = tk.Label(self, text="Select scale:",font=('American Typewriter',15), bg='#c1bed6', pady=10)
        select_scale_label.grid(row=6, column=0)

        # Option menu for the note of the scale
        self.scale_note_var = tk.StringVar()
        self.scale_note_var.set(value="C")
        self.scale_note = tk.OptionMenu(self, self.scale_note_var, *notes, command=self.activate_loop)
        self.scale_note.configure(bg='#c1bed6')
        self.scale_note.grid(row=6, column=1, columnspan=2)

        # Option menu for the mode of the scale (only ionian and aeolian)
        self.maj_min_var = tk.StringVar()
        self.maj_min_var.set(value="Major")
        self.maj_min = tk.OptionMenu(self, self.maj_min_var, *maj_min, command=self.activate_loop)
        self.maj_min.grid(row=6, column=3, columnspan=1)
        self.maj_min.configure(bg='#c1bed6')
        self.test_scale = False

    # Two commands for the app to know if it's drawing notes from scale or from the fretboard checkboxes
    def deactivate_loop(self):
        self.test_scale = False
    def activate_loop(self,x):
        self.test_scale = True


    def get_notes_from_scale(self):
        # Get notes from scale (either checboxes or fretboard)
        global selected_notes_from_scale
        if self.test_scale:
            selected_notes_from_scale_dict = {}
            if self.maj_min_var.get() == "Major":
                selected_notes_from_scale = ms.scale(starting_note=self.scale_note_var.get(), mode="ionian")[:-1]
            else:
                selected_notes_from_scale = ms.scale(starting_note=self.scale_note_var.get(), mode="aeolian")[:-1]

            for i in range(len(selected_notes_from_scale)):
                selected_notes_from_scale[i] = str(selected_notes_from_scale[i])[:-1]

            for value in notes:
                    if value in selected_notes_from_scale:
                        selected_notes_from_scale_dict[value] = 1
                    else:
                        selected_notes_from_scale_dict[value] = 0

            for idx, value in enumerate(selected_notes_from_scale_dict.values()):
                if value == 1:
                    self.checkbox_vars[idx].set(1)
                if value == 0:
                    self.checkbox_vars[idx].set(0)
            self.after(1, self.get_notes_from_scale)

        else:
            self.notes_dictionary = {notes[idx]:self.checkbox_vars[idx].get() for idx in range(12)}
            selected_notes_from_scale = [k for k in self.notes_dictionary if self.notes_dictionary[k] == 1]
            self.after(1, self.get_notes_from_scale)

    def open_fretboard_view(self):
        # Open up a new window that displays the fretboard
        open_fretboard = tk.Label(self, text="Fretboard view:", bg='#c1bed6',font=('American Typewriter',15), pady=10)
        open_fretboard.grid(row=7, column=0)

        open_button = ctk.CTkButton(self, text="Open", command = FretboardWindow, width=100)
        open_button.grid(row=7, column=1, columnspan=5)


class FretboardWindow(tk.Tk):
    # Class that creates a window with a fretboard image and displays the selected notes
    def __init__(self):
        self.fretboard_win = tk.Toplevel()
        self.fretboard_win.geometry("790x225+550+200")
        self.fretboard_win.title('Fretboard view')
        self.fretboard_canv()
        self.fretboard_win.resizable(False, False)
        self.loop = True

    def fretboard_canv(self):
        # Create a canvas and put the diagram of a fretboard on it 
        self.canvas = tk.Canvas(self.fretboard_win, width=770, height=210, bg='red')
        self.canvas.pack(side='top', expand='yes', fill='both')
        self.canvas.create_image(0, 0, image=fretboard_img, anchor='nw')
        self.draw_on_canv()
    

    def draw_on_canv(self): 
        # Iteratively draw the selected notes on the canvas
        global entry_box_value, next_notes, looping
        if looping:  
            self.canvas.delete('Notes')
            if len(next_notes) == 1:
                for i in range(6):
                    self.canvas.create_oval(coordinate_dictionary[next_notes[0]][i][0]-10, coordinate_dictionary[next_notes[0]][i][1]-10,
                                        coordinate_dictionary[next_notes[0]][i][0]+10,coordinate_dictionary[next_notes[0]][i][1]+10,
                                        fill='red', tags='Notes')
            elif len(next_notes) ==2:
                for i in range(6):
                    self.canvas.create_oval(coordinate_dictionary[next_notes[0]][i][0]-10, coordinate_dictionary[next_notes[0]][i][1]-10,
                                        coordinate_dictionary[next_notes[0]][i][0]+10,coordinate_dictionary[next_notes[0]][i][1]+10,
                                        fill='red', tags='Notes')
                    self.canvas.create_oval(coordinate_dictionary[next_notes[1]][i][0]-10, coordinate_dictionary[next_notes[1]][i][1]-10,
                                        coordinate_dictionary[next_notes[1]][i][0]+10,coordinate_dictionary[next_notes[1]][i][1]+10,
                                        fill='green', tags='Notes')
            elif len(next_notes) ==3:
                for i in range(6):
                    self.canvas.create_oval(coordinate_dictionary[next_notes[0]][i][0]-10, coordinate_dictionary[next_notes[0]][i][1]-10,
                                        coordinate_dictionary[next_notes[0]][i][0]+10,coordinate_dictionary[next_notes[0]][i][1]+10,
                                        fill='red', tags='Notes')
                    self.canvas.create_oval(coordinate_dictionary[next_notes[1]][i][0]-10, coordinate_dictionary[next_notes[1]][i][1]-10,
                                        coordinate_dictionary[next_notes[1]][i][0]+10,coordinate_dictionary[next_notes[1]][i][1]+10,
                                        fill='green', tags='Notes')
                    self.canvas.create_oval(coordinate_dictionary[next_notes[2]][i][0]-10, coordinate_dictionary[next_notes[2]][i][1]-10,
                                        coordinate_dictionary[next_notes[2]][i][0]+10,coordinate_dictionary[next_notes[2]][i][1]+10,
                                        fill='yellow', tags='Notes')
            self.fretboard_win.after(2, self.draw_on_canv)
        else:
            self.fretboard_win.after(1, self.draw_on_canv)
        

#######################################################################
# Data used throughout the code
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    print(base_path)
    return os.path.join(base_path, relative_path)

rng = np.random.default_rng() # Rng generator 
notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"] # All the notes of the scale to be drawn from 
maj_min = ["Major", "Minor"] # Major or minor scale for the option menu
# Dictionary with coordinates for the fretboard canvas 
coordinate_dictionary = { 
        'C': [(483, 200),(173, 165),(607, 129),(297, 93), (49, 57),(483, 22)],   
        'C#': [(545, 200),(235, 165),(669, 129),(359, 93),(111, 57),(545, 22)],
        'D': [(607, 200),(297, 165),(19, 129),(421, 93),(173, 57),(607, 22)],
        'D#': [(669, 200),(359, 165),(49, 129),(483, 93),(235, 57),(669, 22)],
        'E': [(19, 200),(421, 165),(111, 129),(545, 93),(297, 57),(19, 22)],
        'F': [(49, 200),(483, 165),(173, 129),(607, 93),(359, 57),(49, 22)],
        'F#': [(111, 200),(545, 165),(235, 129),(669, 93),(421, 57),(111, 22)],
        'G': [(173, 200),(607, 165),(297, 129),(19, 93),(483, 57),(173, 22)],
        'G#': [(235, 200),(669, 165),(359, 129),(49, 93),(545, 57),(235, 22)],
        'A': [(297, 200),(19, 165),(421, 129),(111, 93),(607, 57),(297, 22)],
        'A#': [(359, 200),(49, 165),(483, 129),(173, 93),(669, 57),(359, 22)],
        'B': [(421, 200),(111, 165),(545, 129),(235, 93),(19, 57),(421, 22)], 
}
# Files containing the music note sounds
music_files = {
    'C':resource_path('Sounds/C.wav'),
    'C#':resource_path('Sounds/C#.wav'),
    'D':resource_path('Sounds/D.wav'),
    'D#':resource_path('Sounds/D#.wav'),
    'E':resource_path('Sounds/E.wav'),
    'F':resource_path('Sounds/F.wav'),
    'F#':resource_path('Sounds/F#.wav'),
    'G':resource_path('Sounds/G.wav'),
    'G#':resource_path('Sounds/G#.wav'),
    'A':resource_path('Sounds/A.wav'),
    'A#':resource_path('Sounds/A#.wav'),
    'B':resource_path('Sounds/B.wav'),
}
#######################################################################

if __name__ == "__main__":
    root = tk.Tk() # Create the main Tk instance

    fretboard_img = Image.open(resource_path('Images/fretboard.png'))
    fretboard_img = ImageTk.PhotoImage(fretboard_img)

    img_volume = Image.open(resource_path('Images/volume.png')).convert('RGBA').resize(size=(30,30))
    img_volume = ImageTk.PhotoImage(img_volume, 'rgba')
    root.title('Note Generator')

    img_volume_off = Image.open(resource_path('Images/volume_off.png')).convert('RGBA').resize(size=(30,30))
    img_volume_off = ImageTk.PhotoImage(img_volume_off, 'rgba')
    root.title('Note Generator')
    pygame.mixer.init()

    app = MainWindow(master=root)
    root.resizable(False, False)
    app.mainloop()
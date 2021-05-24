import tkinter as GUI


class App():
    chord_names = ["A", "A#/Bb", "B", "C", "C#/Db", "D", "D#/Eb", "E", "F",
                   "F#/Gb", "G"]
    chord_types = ["Dom", "Maj", "Min"]
    tension_levels = ["7", "9", "11/13"]

    selected_chord_type = 'Dom'
    tension_level = '7'
    chord = ''
    chordbox = None
    chord_sequence = []

    def __init__(self):
        # create window
        self.main_window = GUI.Tk()
        self.main_window.resizable(False, False)
        self.main_window.title("LaTeef")
        self.main_window.geometry("850x700")
        self.main_window['bg'] = "#2B292B"

        # welcome message
        welcome = "Welcome to LaTeef! Select some Chords and let's get writing!"
        message = GUI.Message(self.main_window, text=welcome)
        message.config(bg="#4F5260", fg="#F5F7F9",
                       width=200, font=("Helvetica", 16, "italic"))
        message.place(relx=0.37)

        # create chord buttons
        for name in self.chord_names:
            b = self.add_button(name)
            b.grid(row=1, column=self.chord_names.index(name), padx=3, pady=100)

        # chord type message
        type_message = "Select the type of chord"
        message1 = GUI.Message(self.main_window, text=type_message)
        message1.config(bg="#427446", fg="#F5F7F9",
                       width=200, font=("Helvetica", 16, "italic"))
        message1.place(rely=0.28)

        # chord type radio button
        chord_color = GUI.StringVar()
        for c_type in self.chord_types:
            r = GUI.Radiobutton(self.main_window, text=c_type,
                                variable=chord_color, bg="#2B292B", fg="#F5F7F9",
                                font=("Helvetica", 12, "italic"), height=5,
                                value=str(self.chord_types.index(c_type)+1),
                                selectcolor='navy',
                                command=(lambda name=c_type: self.chord_type_radio(name)))
            r.grid(row=2, column=self.chord_types.index(c_type))

        # tension level message
        tension_message = "Select the tension level of the chord"
        message2 = GUI.Message(self.main_window, text=tension_message)
        message2.config(bg="#8A3427", fg="#F5F7F9",
                        width=200, font=("Helvetica", 16, "italic"))
        message2.place(relx=.475,rely=0.28)

        # tension level radio button
        tension_level = GUI.StringVar()
        for tension in self.tension_levels:
            t = GUI.Radiobutton(self.main_window, text=tension,
                                    variable=tension_level, bg="#2B292B",
                                    fg="#F5F7F9",
                                    font=("Helvetica", 12, "italic"), height=5,
                                    value=str(self.tension_levels.index(tension) +1),
                                    selectcolor='navy',
                                    command=(lambda name=tension: self.tension_level_radio(name)))
            t.grid(row=2, column=5 + self.tension_levels.index(tension))

        self.main_window.config(width=850, heigh=700)

        # written chord text
        GUI.Label(self.main_window, text='Chords: ').grid(row=4)
        t1 = GUI.Text(self.main_window, height=20, state=GUI.DISABLED)
        t1.place(relx=.1, rely=.5)
        self.chordbox = t1

        # backspace button
        back = GUI.Button(self.main_window, text="Delete", width=6, height=2,
                          command=lambda: self.remove_chord(),
                          bg="#AE5C4F",
                          fg="#F5F7F9", font=("Helvetica", 16, "bold"),
                          bd=0)
        back.grid(row=2, column=9)

        # launch gui window
        self.main_window.mainloop()

    def button_function(self, name):
        self.chord = name
        self.chordbox.config(state=GUI.NORMAL)
        chord_unit = name + ' '+ self.selected_chord_type + self.tension_level
        self.chordbox.insert(GUI.END,  chord_unit + ",")
        self.chordbox.config(state=GUI.DISABLED)
        self.chord_sequence.append(chord_unit)
        print(name)

    def remove_chord(self):
        text = self.chordbox.get(1.0, GUI.END+"-1c")
        if len(text) > 0:
            for i in range(len(text)-2, -1, -1):
                if text[i] == ',':
                    break
        self.chordbox.config(state=GUI.NORMAL)
        i = i-1 if i<3 else i
        self.chordbox.delete('1.0', GUI.END)
        self.chordbox.insert('1.0', text[:i+1])
        self.chordbox.config(state=GUI.DISABLED)
        self.chord_sequence.remove(self.chord_sequence[-1])

    def chord_type_radio(self, c_type):
        self.selected_chord_type = c_type

    def tension_level_radio(self, level):
        self.tension_level = level

    # add a button with [name] as the text
    def add_button(self, name):
        return GUI.Button(self.main_window, text=name, width=5, height=2,
                              command=(lambda n=name: self.button_function(n)), bg="#426796",
                              fg="#F5F7F9", font=("Helvetica", 16, "bold"),
                              bd=0)

    def fun(self):
        pass

e = App()

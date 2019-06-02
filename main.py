import utils
import stream
from tkinter import *
import tkinter.ttk
import icon


class Main:
    """
    Main UI class.
    """
    REFRESH_RATE = 120 * 1000

    def __init__(self):
        self.__stream_list = {}

        self.stream_available = False

        self.window = Tk()
        self.window.title("HFR-RG 1.0.1")

        self.load_icon()
        menu_bar = Menu(self.window)

        menu_bar.add_command(label="Rafraîchir la liste", command=self.refresh_stream_list)
        menu_bar.add_command(label="Quitter", command=self.window.quit)

        self.window.config(menu=menu_bar)

        stream_label = Label(self.window, text="Stream")
        stream_label.grid(row=0, column=0, padx=10, pady=5)

        self.chosen_stream = tkinter.StringVar()
        self.chosen_stream.trace('w', self.on_link_selection)

        self.stream_selection = tkinter.ttk.Combobox(self.window, textvar=self.chosen_stream)
        self.stream_selection.grid(row=0, column=1, padx=10, pady=5)
        self.stream_selection.config(width=80)

        link_label = Label(self.window, text="Lien")
        link_label.grid(row=1, column=0, padx=10, pady=5)

        self.link = tkinter.Entry(self.window, state="readonly")
        self.link.grid(row=1, column=1, padx=10, pady=10)
        self.link.config(width=100, readonlybackground="White")
        self.link.bind("<FocusIn>", self.select_link)

        play_button = tkinter.ttk.Button(self.window, text="Jouer avec VLC")
        play_button.grid(row=2, column=0, columnspan=2, pady=5)
        play_button.bind("<Button-1>", self.start_vlc)

        self.window.update()
        self.window.minsize(self.window.winfo_width(), self.window.winfo_height())

        self.refresh_stream_list()
        self.window.mainloop()

    def load_icon(self):
        icon_data = icon.decode_icon()
        self.window.wm_iconbitmap(icon_data)

    def refresh_stream_list(self):
        self.__stream_list = {}
        for stream_info in stream.get_streams_list():
            self.__stream_list[stream_info.title + " (" + stream_info.channel + ")"] = stream_info.video_uuid
        self.stream_selection['values'] = list(self.__stream_list.keys())
        # Refresh link selection, in order to avoid having an outdated link in the box
        self.update_link_value()
        self.window.after(self.REFRESH_RATE, self.refresh_stream_list)

    def select_link(self, event):
        event.widget.selection_range(0, END)

    def update_link_value(self):
        self.link.config(state="normal")
        self.link.delete(0, END)
        chosen_stream = self.chosen_stream.get()
        link_value = ""
        # No link was selected yet
        if chosen_stream not in self.__stream_list:
            self.stream_available = False
            if chosen_stream != "":
                link_value = "Live non disponible"
        else:
            link_value = stream.get_authenticated_stream_url(self.__stream_list[chosen_stream])
            self.stream_available = True
        self.link.insert(0, link_value)
        self.link.config(state="readonly")

    def on_link_selection(self, index, value, op):
        self.update_link_value()

    def start_vlc(self, event):
        if self.stream_available:
            link_url = self.link.get()
            utils.start_vlc(link_url)


Main()

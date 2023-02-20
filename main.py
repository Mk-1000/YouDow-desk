import threading
import tkinter
import tkinter.messagebox
import webbrowser
import cProfile
import customtkinter
import psutil as psutil
from mode_section import select_mode
import time
import os
from PIL import Image


# remove the call to set appearance mode and color theme, as it doesn't seem to be defined in the code
# customtkinter.set_appearance_mode("Dark")
# customtkinter.set_default_color_theme("blue")

class App(customtkinter.CTk):
    WIDTH = 880
    HEIGHT = 460

    def __init__(self):
        super().__init__()

        labelText = "YouDow\n\n you simply need to copy and paste a YouTube video URL \n\n choose a mode and file type, and start the download process."
        font = customtkinter.CTkFont(family='Courier New', size=13)
        YouDow_color = "#1f6aa5"

        image = Image.open("C:/Users/Administrator/Desktop/pfe/YouDow-desk/logoSmall.png")
        resized_image = image.resize((500, 35))
        self.logo = customtkinter.CTkImage(resized_image)

        self.title("YouDow")
        # self.iconbitmap("logo.ico")
        self.channelPath = None
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # call .on_closing() when app gets closed

        # ============ create frames ============

        # configure grid layout (2x1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame = customtkinter.CTkFrame(master=self)
        self.frame.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        # ============ frame ============

        # configure grid layout (3x7)

        self.frame.columnconfigure((0, 1), weight=1)
        self.frame.columnconfigure(2, weight=0)

        self.frame_info = customtkinter.CTkFrame(master=self.frame)
        self.frame_info.grid(row=0, column=0, columnspan=2, rowspan=7, pady=20, padx=20, sticky="nsew")

        # ============ frame_info ============

        # configure grid layout (1x1)
        self.frame_info.rowconfigure(0, weight=1)
        self.frame_info.columnconfigure(0, weight=1)

        self.label_info_1 = customtkinter.CTkLabel(master=self.frame_info,
                                                   text=labelText,
                                                   text_color="white",
                                                   font=font,
                                                   height=100,
                                                   corner_radius=6,  # <- custom corner radius
                                                   fg_color=None,  # <- no fg_color
                                                   justify=tkinter.CENTER)
        self.label_info_1.grid(column=0, row=0, sticky="nwe", padx=15, pady=15)

        self.progressbar = customtkinter.CTkProgressBar(master=self.frame_info)
        self.progressbar.grid(row=1, column=0, padx=15, sticky="swe", pady=15)
        self.progressbar.grid_remove()  # hide the progress bar initially

        self.button_open = customtkinter.CTkButton(master=self.frame_info, text="Open folder", command=self.open_file)
        self.button_open.grid(row=1, column=0, padx=15, pady=15)
        self.button_open.grid_remove()  # hide the progress bar initially

        # ============ frame_right ============

        self.radio_var = tkinter.IntVar(value=0)

        self.label_radio_group = customtkinter.CTkLabel(master=self.frame,
                                                        font=font,
                                                        text_color=YouDow_color,
                                                        text="Download Options :")
        self.label_radio_group.grid(row=0, column=2, columnspan=1, pady=20, padx=10, sticky="we")

        self.radio_button_1 = customtkinter.CTkRadioButton(master=self.frame,
                                                           variable=self.radio_var,
                                                           text="Single Link",
                                                           font=font,
                                                           command=self.changeText,
                                                           value=1)
        self.radio_button_1.grid(row=1, column=2, pady=10, padx=20, sticky="we")

        self.radio_button_2 = customtkinter.CTkRadioButton(master=self.frame,
                                                           variable=self.radio_var,
                                                           text="One Playlist",
                                                           font=font,
                                                           command=self.changeText,
                                                           value=2)
        self.radio_button_2.grid(row=2, column=2, pady=10, padx=20, sticky="we")

        self.radio_button_3 = customtkinter.CTkRadioButton(master=self.frame,
                                                           variable=self.radio_var,
                                                           text="All Channel",
                                                           font=font,
                                                           command=self.changeText,
                                                           value=3)
        self.radio_button_3.grid(row=3, column=2, pady=10, padx=20, sticky="we")

        self.radio_button_4 = customtkinter.CTkRadioButton(master=self.frame,
                                                           variable=self.radio_var,
                                                           text="All Playlists",
                                                           font=font,
                                                           command=self.changeText,
                                                           value=4)
        self.radio_button_4.grid(row=4, column=2, pady=10, padx=20, sticky="we")

        self.combobox = customtkinter.CTkComboBox(master=self.frame,
                                                  font=font,
                                                  state="readonly",
                                                  values=["mp4_hd", "mp4", "mp3"])
        self.combobox.grid(row=6, column=2, columnspan=1, pady=10, padx=20, sticky="we")

        self.entry = customtkinter.CTkEntry(master=self.frame,
                                            width=120,
                                            font=font,
                                            placeholder_text="Paste the youtube link here")
        self.entry.grid(row=7, column=0, columnspan=2, pady=20, padx=20, sticky="we")

        self.button_download = customtkinter.CTkButton(master=self.frame,
                                                       text="Download",
                                                       command=self.button_event,
                                                       border_width=2,  # <- custom border_width
                                                       fg_color=None,
                                                       )
        self.button_download.grid(row=7, column=2, columnspan=1, pady=20, padx=20, sticky="we")

        self.button_stop = customtkinter.CTkButton(master=self.frame,
                                                   text="Stop",
                                                   command=self.pause_event,
                                                   border_width=2,  # <- custom border_width
                                                   fg_color=None,
                                                   )
        self.button_stop.grid(row=7, column=2, columnspan=1, pady=20, padx=20, sticky="we")
        self.button_stop.grid_remove()  # hide the progress bar initially

        label_options = {
            'font': font,
            'text_color': YouDow_color,
            'height': 50,
            'corner_radius': 6,
        }
        # Create the first label
        self.label_author = customtkinter.CTkLabel(master=self.frame,
                                                   # text="© 2023, made with \u2764 by Hamdi Mokni",
                                                   text="© 2023, made by Hamdi Mokni",
                                                   justify=tkinter.CENTER,
                                                   **label_options)
        self.label_author.grid(column=0, row=8, columnspan=3, sticky="w", padx=15, pady=(0, 15))

        # Create the second label
        self.label_logo = customtkinter.CTkLabel(master=self.frame,
                                                 text="",
                                                 image=self.logo,
                                                 **label_options)
        self.label_logo.grid(column=1, row=8, columnspan=3, sticky="w", padx=15, pady=(0, 15))

        # Create the third label
        self.label_how = customtkinter.CTkLabel(master=self.frame,
                                                text="How to use",
                                                **label_options)
        self.label_how.grid(column=2, row=8, columnspan=3, sticky="we", padx=15, pady=(0, 15))

        # set default values
        self.radio_button_1.select()
        self.combobox.set("mp3")
        self.progressbar.configure(mode="indeterminnate")
        self.progressbar.start()
        self.label_author.configure(cursor="heart")
        self.label_author.bind("<Button-1>",
                               lambda event: webbrowser.open_new("https://www.linkedin.com/in/mokni-hamdi-mk712/"))
        self.label_how.configure(cursor="hand2")
        self.label_how.bind("<Button-1>",
                            lambda event: webbrowser.open_new("https://mk-1000.github.io/YouDow//"))

    def changeText(self):
        if self.radio_var.get() == 1:
            self.label_info_1.configure(text="Copy and paste the URL of a YouTube video")
            # self.entry.configure(placeholder_text="https://www.youtube.com/watch?v=abcd...")
        elif self.radio_var.get() == 2:
            self.label_info_1.configure(
                text="Copy and paste the URL of a YouTube video\n\nmake sure that it is part of any YouTube playlis")
            # self.entry.configure(placeholder_text="https://www.youtube.com/watch?v=abcd...")
        elif self.radio_var.get() == 3:
            self.label_info_1.configure(text="Copy and paste the URL of a YouTube video")
            # self.entry.configure(placeholder_text="https://www.youtube.com/watch?v=abcd...")
        elif self.radio_var.get() == 4:
            self.label_info_1.configure(text="Copy and paste the URL of a YouTube video")
            # self.entry.configure(placeholder_text="https://www.youtube.com/watch?v=abcd...")
        else:
            pass

    def button_event(self):
        # Hide the progress bar initially
        self.button_open.grid_remove()  # hide the progress bar initially
        self.radio_button_1.configure(state="disabled")
        self.radio_button_2.configure(state="disabled")
        self.radio_button_3.configure(state="disabled")
        self.radio_button_4.configure(state="disabled")
        self.combobox.configure(state="disabled")
        self.entry.configure(state="disabled")

        # change label
        self.label_info_1.configure(text="Searching... ")
        self.progressbar.grid()
        self.label_info_1.update()

        # Get the URL from the entry field
        url = self.entry.get()
        # Create a new thread to run the long-running code

        thread = threading.Thread(target=self.run_long_running_code, args=(url,))
        thread.start()

        self.button_stop.grid()

    def run_long_running_code(self, url):
        text = ""
        test: str | tuple[str, Exception] = select_mode.testUrl(url)
        self.progressbar.grid_remove()
        if test == "Link is valid and exists.":

            # creat Youdow Path
            exe = select_mode
            youDowPath = exe.youDowPath()
            text += "\n• Step 1: YouDow path has been created.\n\n--> " + youDowPath
            self.label_info_1.configure(text=text)
            self.label_info_1.update()
            time.sleep(1)  # wait 2 seconds

            # creat channel path
            channelPath = exe.channel_path(youDowPath, url)
            self.channelPath = channelPath
            lists = channelPath.split("\\")
            if lists[-1] == "Error Invalid URL":
                self.label_info_1.configure(text="Invalid URL")
                raise Exception("Invalid URL")

            text += "\n\n\n• Step 2: The channel path has been created. \n\n--> " + "YouDow\\" + lists[-1]
            self.label_info_1.configure(text=text)
            self.label_info_1.update()
            time.sleep(1)  # wait 2 seconds

            # download option
            step3 = "\n\n\n• Step 3: Downloading..."
            self.progressbar.grid()
            self.label_info_1.configure(text=text + step3)
            self.label_info_1.update()
            # time.sleep(1)  # wait 2 seconds
            try:
                exe.youDow(channelPath, url, self.radio_var.get(), self.combobox.get())

            except:
                self.label_info_1.configure(text="Invalid URL\n\n take any url from a playlist")
                raise Exception("Invalid URL")
            # All Done
            step3 = "\n\n\n• Step 3: All Done."
            text += step3
            self.label_info_1.configure(text=text)
            self.progressbar.grid_remove()  # hide the progress bar initially
            self.button_open.grid()  # hide the progress bar initially
            self.label_info_1.update()

        else:
            self.label_info_1.configure(text=test)

        self.button_stop.grid_remove()
        # self.button_1.configure(state="disabled")
        self.radio_button_1.configure(state="normal")
        self.radio_button_2.configure(state="normal")
        self.radio_button_3.configure(state="normal")
        self.radio_button_4.configure(state="normal")
        self.combobox.configure(state="readonly")
        self.entry.configure(state="normal")

    def open_file(self):
        try:
            os.startfile(self.channelPath)
        except OSError as e:
            print(f"Error opening file: {e}")

    def pause_event(self):
        self.open_file()
        time.sleep(0.1)
        self.reload_page()

    def reload_page(self):
        self.destroy()
        cProfile.run('app = App(); app.mainloop()')

    def kill_processes(self):
        # Get the current process ID
        current_process = psutil.Process()

        # Get the list of all child processes and their children, and kill them
        children = current_process.children(recursive=True)
        for child in children:
            child.kill()

        # Kill the current process
        current_process.kill()

    def on_closing(self, event=None):
        self.kill_processes()
        self.destroy()


if __name__ == "__main__":
    cProfile.run('app = App(); app.mainloop()')

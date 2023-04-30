import tkinter
import customtkinter  # <- import the CustomTkinter module
from tkinter import filedialog
import threading
import helpers
from PIL import Image, ImageTk

primaryColor="#0A0A0A"
secondaryColor="#1DC5E1"
secondaryHoverColor="#146876"
textColor="#0A0A0A"

root_tk = tkinter.Tk()  # create the Tk window like you normally do
root_tk.geometry("600x400")
root_tk.title("Metadata Maker")
root_tk.configure(background=primaryColor) 
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

# Load the image
image=Image.open('./folder.png')

# Resize the image in the given (width, height)
img=image.resize((20, 20))

# Conver the image in TkImage
folderImage=ImageTk.PhotoImage(img)

# Display the image with label
def workerThread():
    progressbar.start()
    goButton.configure(state="disabled", text="Creating Metadata...", fg_color="#146876")
    chooseDirectoryButton.configure(state="disabled", fg_color="#146876")
    entryAPIKey.configure(state="disabled")
    labelFinished.configure(text="Note: Each song will take 20 seconds to complete due to OpenAI API limits", text_color=textColor)
    userAPIKey=entryAPIKey.get()
    try:
        helpers.main(filepath, userAPIKey)
        progressbar.stop()
        goButton.configure(state="normal", text="Create Metadata", fg_color="#1DC5E1")
        chooseDirectoryButton.configure(state="normal", fg_color="#1DC5E1")
        entryAPIKey.configure(state="normal")
        labelFinished.configure(text="Finished Successfully!", text_color="green")
    except:
        progressbar.stop()
        goButton.configure(state="normal", text="Create Metadata", fg_color="#1DC5E1")
        chooseDirectoryButton.configure(state="normal", fg_color="#1DC5E1")
        entryAPIKey.configure(state="normal")
        labelFinished.configure(text="Failed, check API key and folder path", text_color="red")
        
def startButton():
    threading.Thread(target=workerThread).start()

def openFile():
    global filepath
    filepath = filedialog.askdirectory()
    labelFolder.configure(text=filepath)


labelFolder = customtkinter.CTkLabel(master=root_tk, fg_color="transparent", text="Choose Folder")
labelFolder.place(relx=0.5, rely=0.2, anchor=tkinter.CENTER)

chooseDirectoryButton = customtkinter.CTkButton(master=root_tk, corner_radius=10, command=openFile, text="",  fg_color=secondaryColor, text_color=textColor, hover_color=secondaryHoverColor, image=folderImage)
chooseDirectoryButton.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)

labelAPIKey = customtkinter.CTkLabel(master=root_tk, fg_color="transparent", text="OpenAI API key")
labelAPIKey.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)

entryAPIKey = customtkinter.CTkEntry(master=root_tk, placeholder_text="Paste here")
entryAPIKey.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

goButton = customtkinter.CTkButton(master=root_tk, corner_radius=10, command=startButton, text="Create Metadata", fg_color=secondaryColor, text_color=textColor, hover_color=secondaryHoverColor, text_color_disabled=textColor)
goButton.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)

labelFinished = customtkinter.CTkLabel(master=root_tk, fg_color="transparent", text="")
labelFinished.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)

progressbar = customtkinter.CTkProgressBar(master=root_tk, orientation="horizontal")
progressbar.configure(mode="indeterminate", progress_color=secondaryColor)
progressbar.place(relx=0.5, rely=0.8, anchor=tkinter.CENTER)

root_tk.mainloop()
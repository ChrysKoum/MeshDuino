from pathlib import Path
from tkinter import *
from gui.Primary_Window.sub_gui.about_GUI.gui import About
from gui.Primary_Window.sub_gui.home_GUI.gui import Home
from gui.Primary_Window.sub_gui.leaderboard_GUI.gui import Leaderboard
from gui.Primary_Window.sub_gui.challenge_GUI.gui import Challenge


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./gui/Primary_Window/assets")
def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def handle_button_press(btn_name):
    global current_window
    if btn_name == "home":
        home_button_clicked()
        current_window = Home(window)
    elif btn_name == "leaderboard":
        leaderboard_button_clicked()
        current_window = Leaderboard(window)
    elif btn_name=="challenge":
        challenge_button_clicked()
        current_window = Challenge(window)
    elif btn_name == "about":
        about_button_clicked()
        current_window=About(window)
        


# ~ FUNCTIONS FOR BUTTONS FOR CHANGING TABS ~

def home_button_clicked(): # (coordinates : x= 0 , y= 133)
    print("Home button clicked")
    canvas.itemconfig(page_navigator, text="Home")
    sidebar_navigator.place(x=0, y=133)    

def challenge_button_clicked():
    print("challenge button clicked")
    canvas.itemconfig(page_navigator, text="Challenge")
    sidebar_navigator.place(x=0, y=184)

def leaderboard_button_clicked(): # (coordinates : x= 0 , y= 184)
    print("leaderboard button clicked")
    canvas.itemconfig(page_navigator, text="Leaderboard")
    sidebar_navigator.place(x=0, y=232)

def about_button_clicked(): # (coordinates : x= 0 , y= 232)
    print("About button clicked")
    canvas.itemconfig(page_navigator, text="About")
    sidebar_navigator.place(x=0, y=280)

window = Tk()
window.title("MeshDuino")
window.geometry("930x506")
window.configure(bg = "#171435")

'''for custom cursor'''
# cursor_path=relative_to_assets("chrome.cur")
# window['cursor']=cursor=cursor_path

'''For Custom title bar'''
# window.overrideredirect(1)
# window.wm_attributes("-transparentcolor","#35F331")


'''For Icon'''
window.iconbitmap(relative_to_assets("minilogo.ico"))


canvas = Canvas(
    window,
    bg = '#171435',
    height = 506,
    width = 930,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)
canvas.place(x = 0, y = 0)
background_image = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    566.0,
    253.0,
    image=background_image
)

current_window=Home(window)

####### HOME BUTTON #############
home_button_image = PhotoImage(
    file=relative_to_assets("button_1.png"))
home_button = Button(
    image=home_button_image,
    bg="#171435",
    borderwidth=0,
    highlightthickness=0,
    command=lambda: handle_button_press("home"),
    relief="sunken",
    activebackground="#171435",
    activeforeground="#171435"
)
home_button.place(
    x=7.35,
    y=133.0,
    width=191.0,
    height=47.0
)
#################################

####### Challenge BUTTON #############
challenge_button_image = PhotoImage(
    file=relative_to_assets("button_2.png"))
challenge_button = Button(
    image=challenge_button_image,
    borderwidth=0,
    bg="#171435",
    highlightthickness=0,
    command=lambda: handle_button_press("challenge"),
    relief="sunken",
    activebackground="#171435",
    activeforeground="#171435"
)
challenge_button.place(
    x=11.35,
    y=184.0,
    width=191,
    height=47.0
)
#####################################

####### leaderboard BUTTON #############
leaderboard_button_image = PhotoImage(
    file=relative_to_assets("button_8.png"))
leaderboard_button = Button(
    image=leaderboard_button_image,
    borderwidth=0,
    bg="#171435",
    highlightthickness=0,
    command=lambda: handle_button_press("leaderboard"),
    relief="sunken",
    activebackground="#171435",
    activeforeground="#171435"
)
leaderboard_button.place(
    x=8.0,
    y=232.0,
    width=191.146240234375,
    height=47.0
)





####### ABOUT BUTTON ################
About_button_image = PhotoImage(
    file=relative_to_assets("button_7.png"))
About_button = Button(
    image=About_button_image,
    borderwidth=0,
    bg="#171435",
    highlightthickness=0,
    command=lambda: handle_button_press("about"),
    relief="sunken",
    activebackground="#171435",
    activeforeground="#171435"
)

About_button.place(
    x=7.351776123046875,
    y=280.0,
    width=191.146240234375,
    height=47.0
)
#####################################





##################### Navigators ###############################

####### (i)  SIDEBAR NAVIGATOR #########
sidebar_navigator = Frame(background="#FFFFFF")
sidebar_navigator.place(x=0, y=133, height=47, width=7)
########################################

####### (ii)  PAGE NAVIGATOR ###########
page_navigator = canvas.create_text(
    251.0,
    37.0,
    anchor="nw",
    text="Home",
    fill="#171435",
    font=("Montserrat Bold", 26 * -1))
########################################

#################################################################


#App name
canvas.create_text(             
    21.0,
    21.0,
    anchor="nw",
    text="MeshDuino",
    fill="#FFFFFF",
    font=("Montserrat Bold", 32 * -1)
)


############## Greetings/Hello ################################ 
from gui.Primary_Window.scripts.greetings import greet
canvas.create_text(
    800.0,
    46.0,
    anchor="nw",
    text=greet(),
    fill="#808080",
    font=("Montserrat SemiBold", 16 * -1)
)
#################################################################


#Text-to-delete
canvas.create_text( #Background
    283.39056396484375,
    216.0,
    anchor="nw",
    text="(Starting the Magic",
    fill="#171435",
    font=("Montserrat Bold", 48 * -1)
)
canvas.create_text(
    311.3304748535156,
    275.0,
    anchor="nw",
    text="Loading Screens...)",
    fill="#171435",
    font=("Montserrat Bold", 48 * -1)
)


#################################################################

#window.after(1000, lambda: continous_playing_thread())

#################################################################
window.resizable(False, False)
window.mainloop()
###################################################################


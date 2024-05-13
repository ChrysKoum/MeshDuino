
from pathlib import Path
from tkinter import *
from math import sin, cos

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)




def About(parent_window):
    canvas = Canvas(
    parent_window,
    bg = "#FFFFFF",
    height = 405,
    width = 675,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
    )
    canvas.place(x = 230, y = 72)
    canvas.create_text(
    36.0,
    43.0,
    anchor="nw",
    text="MeshDuino was created by",
    fill="#C67FFC",
    font=("Montserrat Bold", 26 * -1)
    )
 
    
    global about_image_1
    about_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
    canvas.create_image(190.0,30.0,image=about_image_1)

    global about_image_2 #or this can be used : round_rectangle(180,108,510,300,fill="#171435")
    about_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
    canvas.create_image(345.0,211.0,image=about_image_2)
    
    global about_image_3
    about_image_3 = PhotoImage(file=relative_to_assets("MeshDuino.png"))
    canvas.create_image(
    410.0,
    168.0,
    image=about_image_3
    )

    

    canvas.create_text(
    200.0,
    120,
    anchor="nw",
    text="Computer & Electrical\n Engineering Students",
    fill="#EFEFEF",
    font=("Montserrat SemiBold", 15 * -1)
    )

    canvas.create_text(
    200.0,
    162.0,
    anchor="nw",
    text="MeshDuino",
    fill="#C67FFC",
    font=("Montserrat Bold", 26 * -1)
    )

    canvas.create_text(
    197.0,
    190.0,
    anchor="nw",
    text="@meshduino",
    fill="#C67FFC",
    font=("Montserrat Bold", 18 * -1)
    )

    canvas.create_rectangle(
    199.0,
    219.0,
    337.0,
    221.0,
    fill="#EFEFEF",
    outline="")

    canvas.create_text(
    190.0,
    360.0,
    anchor="nw",
    text=" © 2024 MeshDuino, All rights reserved",
    fill="#3b5e74",
    font=("Montserrat Bold", 16 * -1)
    )

    canvas.create_text(
    180.0,
    380.0,
    anchor="nw",
    text="  Open sourced under the MIT license",
    fill="#3b5e74",
    font=("Montserrat Bold", 16 * -1)
    )

    canvas.create_text(
    194.0,
    234.75,
    anchor="nw",
    text="Enthusiastic engineers that created MeshDuino for",
    fill="#EFEFEF",
    font=("Montserrat SemiBold", 13 * -1)
    )

    canvas.create_text(
    193.0,
    252.5625,
    anchor="nw",
    text="Applications of Telecommunication Devices Project",
    fill="#EFEFEF",
    font=("Montserrat SemiBold", 13 * -1)
    )

    canvas.create_text(
    194.0,
    270.1875,
    anchor="nw",
    text="hyped of IoT and Embedded Systems",
    fill="#EFEFEF",
    font=("Montserrat SemiBold", 13 * -1)
    )



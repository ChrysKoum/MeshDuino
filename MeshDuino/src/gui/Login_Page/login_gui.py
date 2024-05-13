

from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, messagebox, Checkbutton, IntVar


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def access_details():
    try:
        with open(relative_to_assets("details.txt"), "r") as f:
            details = f.read().splitlines()
        if len(details) >= 2:
            return details[0], details[1]  # name, email
        else:
            return None, None
    except FileNotFoundError:
        return None, None


def LOGIN():
    global login_success  # Declare a global variable to track login status
    login_success = False  # Initially set to False
    def round_rectangle(x1, y1, x2, y2, radius=25, **kwargs):  
        points = [x1+radius, y1,
                x1+radius, y1,
                x2-radius, y1,
                x2-radius, y1,
                x2, y1,
                x2, y1+radius,
                x2, y1+radius,
                x2, y2-radius,
                x2, y2-radius,
                x2, y2,
                x2-radius, y2,
                x2-radius, y2,
                x1+radius, y2,
                x1+radius, y2,
                x1, y2,
                x1, y2-radius,
                x1, y2-radius,
                x1, y1+radius,
                x1, y1+radius,
                x1, y1]

        return canvas.create_polygon(points, **kwargs, smooth=True)


    def continue_button_clicked():
        f=open(relative_to_assets("details.txt"), "w")
        name=entry_3.get()
        email=entry_4.get()
        if name=="" or email=="":
            messagebox.showerror("Error", "Please fill all the details")
        else:
            #add these into f :
            f.write(name+"\n")
            f.write(email+"\n")
            f.close()
            a=open(relative_to_assets("auth.txt"), "w")
            a.write("TRUE")  
            a.close()
            global login_success
            login_success = True  # Set to True if login details are successfully written
            window.destroy()

    window = Tk()
    window.title("MeshDuino")


    '''For Icon'''
    window.iconbitmap(relative_to_assets("minilogo.ico"))
    window.geometry("930x506")
    window.configure(bg = "#FFFFFF")


    remember_var = IntVar()  # Variable to keep track of the "Remember Me" checkbox

    # Load saved details if available
    saved_name, saved_email = access_details()
    
    canvas = Canvas(
        window,
        bg = "#FFFFFF",
        height = 506,
        width = 930,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )

    canvas.place(x = 0, y = 0)
    canvas.create_rectangle(
        469.0,
        0.0,
        1012.0,
        506.0,
        fill="#FFFFFF",
        outline="")

    entry_image_1 = PhotoImage(
        file=relative_to_assets("entry_1.png"))
    entry_bg_1 = canvas.create_image(
        676.3636474609375,
        331.00000000000006,
        image=entry_image_1
    )


    entry_image_2 = PhotoImage(
        file=relative_to_assets("entry_2.png"))
    entry_bg_2 = canvas.create_image(
        676.3636474609375,
        224.00000000000006,
        image=entry_image_2
    )

    canvas.create_text(
        527.0,
        306.00000000000006,
        anchor="nw",
        text="Email",
        fill="#171435",
        font=("Montserrat Bold", 14 * -1)
    )

    canvas.create_text(
        527.0,
        204.00000000000006,
        anchor="nw",
        text="Name",
        fill="#171435",
        font=("Montserrat Bold", 14 * -1)
    )

    canvas.create_text(
        517.0,
        66.00000000000006,
        anchor="nw",
        text="Enter your details",
        fill="#171435",
        font=("Montserrat Bold", 26 * -1)
    )

    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: continue_button_clicked(),
        relief="flat"
    )
    button_1.place(
        x=641.0,
        y=412.00000000000006,
        width=190.0,
        height=48.0
    )



    rounded_background = round_rectangle(20.0, 17.00, 469, 491, radius=50, fill="#171435")

    canvas.create_text(
        85.0,
        77.00000000000006,
        anchor="nw",
        text="MeshDuino",
        fill="#FFFFFF",
        font=("RenogareSoft Regular", 50 * -1)
    )

    canvas.create_text(
        518.0,
        109.00000000000006,
        anchor="nw",
        text="before starting, please enter some of",
        fill="#808080",
        font=("Montserrat SemiBold", 16 * -1)
    )

    canvas.create_text(
        520.0,
        130.00000000000006,
        anchor="nw",
        text="the information required below",
        fill="#808080",
        font=("Montserrat SemiBold", 16 * -1)
    )

    entry_image_3 = PhotoImage(
        file=relative_to_assets("entry_3.png"))
    entry_bg_3 = canvas.create_image(
        675.0,
        241.00000000000006,
        image=entry_image_3
    )
    entry_3 = Entry(
        bd=0,
        bg="#EFEFEF",
        highlightthickness=0,
        font=("Montserrat SemiBold", 16 * -1),
        foreground="#171435"
    )
    entry_3.place(
        x=525.0,
        y=225.0,
        width=290.0,
        height=30.0
    )

    entry_image_4 = PhotoImage(
        file=relative_to_assets("entry_4.png"))
    entry_bg_4 = canvas.create_image(
        676.0,
        342.00000000000006,
        image=entry_image_4
    )
    entry_4 = Entry(
        bd=0,
        bg="#EFEFEF",
        highlightthickness=0,
        font=("Montserrat SemiBold", 16 * -1),
        foreground="#171435"
    )
    entry_4.place(
        x=525.0,
        y=325.00000000000006,
        width=290.0,
        height=30.0
    )

    canvas.create_text(
        90.0,
        162.00000000000006,
        anchor="nw",
        text="MeshDuino is an educational platform\nusing Arduinos in a mesh network for\ninteractive STEM challenges. Dive into\nour experiments to learn coding,\nengineering principles, and network\ncommunication without barriers.",
        fill="#FFFFFF",
        font=("Montserrat Regular", 18 * -1)
    )

    canvas.create_text(
        90.0,
        431.00000000000006,
        anchor="nw",
        text= ("©") + " MeshDuino, 2024",
        fill="#FFFFFF",
        font=("Montserrat Bold", 18 * -1)
    )


    if saved_name and saved_email:
        entry_3.insert(0, saved_name)
        entry_4.insert(0, saved_email)

    # Checkbox for "Remember Me"
    Checkbutton(window, text="Remember Me", variable=remember_var).place(x=525, y=380)

    window.resizable(False, False)
    window.mainloop()

    return login_success  # Return the status of the login


if __name__ == "__main__":
    success = LOGIN()
    if success:
        print("Login successful, launching next part of the application.")
        # Place the code here to open the next window or part of your application
    else:
        print("Login failed or was cancelled.")
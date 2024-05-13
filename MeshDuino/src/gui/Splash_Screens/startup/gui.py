from pathlib import Path
import time
import threading
from tkinter import *
import os


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / "assets"

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / path

def startup():
    print("\n\nStartup Initialization...")
    latest_version = "1.0.0"  # Example version
    version = "1.0.0"  # Local version

    def handle_process():
        global handling_label
        auth_path = OUTPUT_PATH / "src/gui/Login_Page/assets/auth.txt"
        try:
            with open(auth_path, "r") as auth:
                has_logedin = auth.read().strip()
        except FileNotFoundError:
            print("Authentication file not found.")
            has_logedin = "FALSE"

        if has_logedin == "TRUE":
            if latest_version == version:
                print("No Update Available")
                time.sleep(1)
                canvas.itemconfig(display_text, text=" Starting CodTubify...")
                time.sleep(2)
                print("Current Working Directory:", os.getcwd())
                window.withdraw()
                handling_label = "Success"
            else:
                canvas.itemconfig(display_text, text=" Updating CodTubify...")
                time.sleep(1)
                window.withdraw()
                handling_label = "Update"
        else:
            canvas.itemconfig(display_text, text=" Please login to continue...", font=("Montserrat Bold", 20))
            time.sleep(3)
            window.withdraw()
            handling_label = "Login"
        
        window.quit()

    def handle_process_thread():
        threading.Thread(target=handle_process, daemon=True).start()

    window = Tk()
    window.geometry("350x350")
    window.configure(bg="#09052D")
    window.resizable(False, False)
    window.overrideredirect(1)

    window.withdraw()
    window.update_idletasks()
    x = (window.winfo_screenwidth() - window.winfo_reqwidth()) / 2
    y = (window.winfo_screenheight() - window.winfo_reqheight()) / 2
    window.geometry("+%d+%d" % (x, y))
    window.deiconify()

    canvas = Canvas(window, bg="#09052D", height=350, width=350, bd=0, highlightthickness=0, relief="ridge")
    canvas.place(x=0, y=0)

    global logo_img
    logo_img = PhotoImage(file=relative_to_assets("Arduino_logo_transperant_v3_smaller.png"))
    canvas.create_image(170, 150, image=logo_img)

    display_text = canvas.create_text(18.0, 283.0, anchor="nw", text="Checking For Updates...", fill="#FFFFFF", font=("Montserrat Bold", 26 * -1))

    window.after(500, handle_process_thread)
    window.mainloop()
    print("Final Handling Label:", handling_label)
    return handling_label

if __name__ == "__main__":
    print(startup())

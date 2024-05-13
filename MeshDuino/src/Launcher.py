import subprocess
import sys
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def startup():
    """Start the GUI and wait for it to complete."""
    print("Start The Startup")
    try:
        result = subprocess.run(
            [sys.executable, "src/gui/Splash_Screens/startup/gui.py"],
            capture_output=True,
            text=True,
            check=True
        )
        output = result.stdout.strip()
        print("Full output:", output)  # Print full output for debugging
        handling_label = output.split('\n')[-1]  # Assume the last line is the handling label
        print("Extracted Handling Label:", handling_label)
        return handling_label
    except subprocess.CalledProcessError as e:
        print("Error", e)
        logging.error("Failed to run startup GUI: %s", e)
        return None

try:
    handling_label = startup()
    if handling_label:
        logging.info("Handling Label: %s", handling_label)

        if handling_label == "Success":
            logging.info("Launching application")
            subprocess.Popen([sys.executable, "src/app.py"])
        
        elif handling_label == "Login":
            logging.info("Login is required")
            # Start the login GUI and wait for it to finish
            login_result = subprocess.run(
                [sys.executable, "src/gui/Login_Page/login_gui.py"],
                text=True,
                capture_output=True  # Capture the output for analysis
            )
            print("Login Result:", login_result.stdout.lower())

            # Check if the login was successful
            if "success" in login_result.stdout.lower():
                print("Login successful, starting the application...")
                # Start the main application
                subprocess.run([sys.executable, "src/app.py"])
            else:
                print("Login failed or was canceled, not starting the application.")
        
        elif handling_label == "Update":
            logging.info("Update is available")
            subprocess.Popen([sys.executable, "src/gui/Splash_Screens/update/gui.py"])
    else:
        logging.error("Startup did not complete properly. No valid handling label received.")

except Exception as e:
    logging.error("An error occurred while starting up: %s", e)
    try:
        subprocess.Popen([sys.executable, "src/app.py"])
    except Exception as ex:
        logging.error("Couldn't even start the app: %s", ex)

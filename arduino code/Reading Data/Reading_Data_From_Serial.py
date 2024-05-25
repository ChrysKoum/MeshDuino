import serial
import time
import random
import tkinter as tk
from tkinter import ttk, messagebox

# Function to send command and wait for response from Arduino
def send_command_and_wait_for_response(command, expected_response, arduino_serial):
    print(f"Sending command: {command}")
    arduino_serial.write(command.encode())
    
    response = ""
    while True:
        if arduino_serial.inWaiting() > 0:
            time.sleep(0.5)  # Wait for the data to be available
            response = arduino_serial.readline().decode('utf-8').strip()
            print(f"Received response: {response}")
            if response == expected_response:
                break
    return response

# Function to run the selected experiments
def run_experiments(selected_option):
    # Set up the serial connection
    arduino_serial = serial.Serial('COM11', 9600)
    time.sleep(2)  # Wait for the connection to establish

    # Start timing the whole process
    start_time = time.time()

    # Gates list and selection of 4 random gates
    gates = ['NotGate', 'OrGate', 'AndGate', 'NorGate', 'NandGate', 'XorGate', 'XnorGate']
    selected_gates = random.sample(gates, 1)

    if selected_option in ['1', 'All']:
        # Experiment 1: Send '1' to start, then send each selected gate command sequentially
        send_command_and_wait_for_response('1', "Experiment 1 Start", arduino_serial)
        send_command_and_wait_for_response(selected_gates, "Experiment 1 Finish", arduino_serial)
        print("Experiment 1 finished.")

    print("Experiment 2 Starting...")
    time.sleep(5)  # Wait for the connection to establish
    if selected_option in ['2', 'All']:
        # Experiment 2: Send '2' to start and wait for finish
        send_command_and_wait_for_response('2', "Experiment 2 Finish", arduino_serial)
        print("Experiment 2 finished.")

    print("Experiment 3 Start.")
    if selected_option in ['3', 'All']:
        # Experiment 3: Send '3' to start, send a random 5-letter word, and wait for finish
        send_command_and_wait_for_response('3', "Experiment 3 Start", arduino_serial)
        
        time.sleep(5)  # Wait for the connection to establish
        
        # Pick a random 5-letter word
        words = ['APPLE', 'GRAPE', 'PEACH', 'LEMON', 'BERRY']
        selected_word = random.choice(words)
        print(f"Selected word for decoding: {selected_word}")
        
        # Wait for "Experiment 3 Finish" message
        send_command_and_wait_for_response(selected_word, "Experiment 3 Finish", arduino_serial)
        print("Experiment 3 finished.")
    
    # End timing the whole process
    end_time = time.time()
    total_time = end_time - start_time

    print("All selected experiments finished.")
    print(f"Total time taken for the whole process: {total_time:.2f} seconds")

    # If you need to continue reading data after the experiments
    while True:
        if arduino_serial.inWaiting() > 0:
            my_data = arduino_serial.readline().decode('utf-8').strip()
            print(my_data)
            # Parse your data here as needed

# Function to handle the selection from the dropdown menu
def on_select(event):
    selected_option = combo.get()
    if selected_option in ['1', '2', '3', 'All']:
        root.destroy()  # Close the selection window
        run_experiments(selected_option)
    else:
        messagebox.showerror("Selection Error", "Please select a valid option.")

# Setup Tkinter window
root = tk.Tk()
root.title("Select Experiment")
root.geometry("300x200")

label = tk.Label(root, text="Select an Experiment to Run:", font=("Arial", 12))
label.pack(pady=10)

options = ['1', '2', '3', 'All']
combo = ttk.Combobox(root, values=options)
combo.pack(pady=10)
combo.bind("<<ComboboxSelected>>", on_select)

root.mainloop()

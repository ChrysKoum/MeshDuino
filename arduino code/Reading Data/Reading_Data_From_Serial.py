import serial
import time
import random

def send_command_and_wait_for_response(command, expected_response, arduino_serial):
    print(f"Sending command: {command}")
    arduino_serial.write(command.encode())

    response = ""
    while True:
        if arduino_serial.inWaiting() > 0:
            response = arduino_serial.readline().decode('utf-8').strip()
            print(f"Received response: {response}")
            if response == expected_response:
                break
    return response

# Set up the serial connection
arduino_serial = serial.Serial('COM10', 9600)
time.sleep(2)  # Wait for the connection to establish

# Start timing the whole process
start_time = time.time()


# Gates list and selection of 4 random gates
gates = ['NotGate', 'OrGate', 'AndGate', 'NorGate', 'NandGate', 'XorGate', 'XnorGate']
selected_gates = random.sample(gates, 4)


selected_gates = ['NotGate', 'OrGate', 'AndGate'  , 'NorGate']  # For testing purposes  

   # Experiment 1: Send '1' to start, then send each selected gate command sequentially
send_command_and_wait_for_response('1', "Experiment 1 Start", arduino_serial)
for i, gate in enumerate(selected_gates, 1):
      send_command_and_wait_for_response(gate, f"Gate {i} Completed", arduino_serial)
print("Experiment 1 finished.")





# Experiment 2: Send '2' to start and wait for finish
send_command_and_wait_for_response('2', "Experiment 2 Finish", arduino_serial)
print("Experiment 2 finished.")




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

print("All experiments finished.")
print(f"Total time taken for the whole process: {total_time:.2f} seconds")

# If you need to continue reading data after the experiments
while True:
    if arduino_serial.inWaiting() > 0:
        my_data = arduino_serial.readline().decode('utf-8').strip()
        print(my_data)
        # Parse your data here as needed

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
arduino_serial = serial.Serial('COM9', 9600)
time.sleep(2)  # Wait for the connection to establish

# Start timing the whole process
start_time = time.time()

# Gates list and selection of 4 random gates
gates = ['NotGate', 'OrGate', 'AndGate', 'NorGate', 'NandGate', 'XorGate', 'XnorGate']
selected_gates = random.sample(gates, 4)

# Experiment 1: Send '1' to start, then send each selected gate command sequentially
send_command_and_wait_for_response('1', "Experiment 1 Start", arduino_serial)
for i, gate in enumerate(selected_gates, 1):
    send_command_and_wait_for_response(gate, f"Gate {i} Completed", arduino_serial)
send_command_and_wait_for_response('Finish', "Experiment 1 Finish", arduino_serial)

# Experiment 2 and 3 commands as needed
responses = [
    send_command_and_wait_for_response('2', "Experiment 2 Finish", arduino_serial),
    send_command_and_wait_for_response('3', "Experiment 3 Finish", arduino_serial),
]

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

import subprocess
import pdb

input_file_count = 2
for i in range(770,5000):

    if input_file_count == 97:
        input_file_count = 2

    top_file = "top (" + str(input_file_count) + ").csv"
    top_location_file = "top_location (" + str(input_file_count) + ").csv"
    bottom_file = "bottom (" + str(input_file_count) + ").csv"
    bottom_location_file = "bottom_location (" + str(input_file_count) + ").csv"
    steps_file = "steps (" + str(input_file_count) + ").csv"
    # pdb.set_trace()
    subprocess.check_call(["python", "collect_data.py", top_file, top_location_file, bottom_file, bottom_location_file, steps_file, str(i)])

    input_file_count = input_file_count + 1

import subprocess
import pdb

input_file_count = 2
for i in range(1,11):
    # pdb.set_trace()
    # print i
    top_file = "testing_frontier/top (" + str(i) + ").csv"
    top_location_file = "testing_frontier/top_location (" + str(i) + ").csv"
    bottom_file = "testing_frontier/bottom (" + str(i) + ").csv"
    bottom_location_file = "testing_frontier/bottom_location (" + str(i) + ").csv"
    steps_file = "testing_frontier/steps (" + str(i) + ").csv"
    # pdb.set_trace()
    subprocess.check_call(["python", "collect_data.py", top_file, top_location_file, bottom_file, bottom_location_file, steps_file, str(i)])

    input_file_count = input_file_count + 1

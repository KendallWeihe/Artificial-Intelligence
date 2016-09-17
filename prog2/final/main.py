import subprocess

files_1 = ["test/top.csv", "test/top_location.csv", "test/bottom.csv", "test/bottom_location.csv", "test/steps.csv"]
files_2 = ["test/top (1).csv", "test/top_location (1).csv", "test/bottom (1).csv", "test/bottom_location (1).csv", "test/steps (1).csv"]
files_3 = ["test/top (2).csv", "test/top_location (2).csv", "test/bottom (2).csv", "test/bottom_location (2).csv", "test/steps (2).csv"]
files_4 = ["test/top (3).csv", "test/top_location (3).csv", "test/bottom (3).csv", "test/bottom_location (3).csv", "test/steps (3).csv"]
files_5 = ["test/top (4).csv", "test/top_location (4).csv", "test/bottom (4).csv", "test/bottom_location (4).csv", "test/steps (4).csv"]

print "Running search where k = 5"
subprocess.check_call(["python", "ida_search.py", files_1[0], files_1[1], files_1[2], files_1[3], files_1[4]])

print "\n\n"
print "Running search where k = 6"
subprocess.check_call(["python", "ida_search.py", files_2[0], files_2[1], files_2[2], files_2[3], files_2[4]])

print "\n\n"
print "Running search where k = 7"
subprocess.check_call(["python", "ida_search.py", files_3[0], files_3[1], files_3[2], files_3[3], files_3[4]])

print "\n\n"
print "Running search where k = 8"
subprocess.check_call(["python", "ida_search.py", files_4[0], files_4[1], files_4[2], files_4[3], files_4[4]])

print "\n\n"
print "Running search where k = 9"
subprocess.check_call(["python", "ida_search.py", files_5[0], files_5[1], files_5[2], files_5[3], files_5[4]])

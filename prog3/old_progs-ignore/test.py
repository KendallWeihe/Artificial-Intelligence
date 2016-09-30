# import multiprocessing
# import subprocess
# import time
#
# def exe():
# 	subprocess.call(["python", "test1.py"])
# 	return
#
# # p = multiprocessing.Process(target=exe)
# # p.start()
# # time.sleep(3)
# # p.terminate()
# # p.join()
#
# import signal
#
# signal.signal(signal.SIGALRM, exe())
# signal.alarm(3)


import subprocess as sub
import threading

class RunCmd(threading.Thread):
    def __init__(self, cmd, timeout):
        threading.Thread.__init__(self)
        self.cmd = cmd
        self.timeout = timeout

    def run(self):
        self.p = subprocess.Popen(self.cmd)
        self.p.wait()

    def Run(self):
        self.start()
        self.join(self.timeout)

        if self.is_alive():
            self.p.terminate()      #use self.p.kill() if process needs a kill -9
            self.join()

RunCmd(["python", "test1.py"], 3).Run()

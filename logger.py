from time import strftime
class Logger(object):
    def __init__(self, logger_msg):
        self.logger_msg = logger_msg
    def log(self, st):
        print(self.logger_msg+st)
        with open("logs/{}.log".format(strftime("%Y-%m-%d")), "a") as logfile:
            logfile.write(self.logger_msg+st+'\n')
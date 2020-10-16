


from threading import Thread


class Threading_support:

    def __init__(self, label_logs):
        print("Initialized Threading_support")
        self.lblLogDetails = label_logs


    def logDetail(self, text):
        current_text = self.lblLogDetails.get()
        self.lblLogDetails.set(current_text + text)
        print("Details")


    @staticmethod
    def runThread():
        print("RUN THREAD")
        thread = Thread(target = runAutomatedMiner)
        thread.start()


'''
    THREADING FUNCTIONS
'''

def runAutomatedMiner():
    print("Running Automated Miner")



# for i in range(5):
#     t = Threading_support()
#     t.start()



# class DestinationThread(threading.Thread):
#     def run(self, name, config):
#         print 'In thread'

# destination_name = "dest name"
# destination_config = "dest config"

# thread = DestinationThread(args = (destination_name, destination_config))
# thread.start()



# def myfunc(arg1, arg2):
#     print 'In thread'
#     print 'args are', arg1, arg2

# thread = Threading_support(target = myfunc, args = (destination_name, destination_config))
# thread.start()



















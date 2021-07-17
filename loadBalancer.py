import threading
import sys
import time

requestsQueue = []
def parse(request):
    global requestsQueue
    tuple =request[1:len(request)-1].split('>')
    tuple = tuple[0:len(tuple)-1]
    tmp = []
    for t in tuple:
        tmp.append(t.split('<')[1])
    tuple = tmp
    outputDirectory = tuple.pop()
    tmp = []
    for t in tuple:
        tmp.append(t.split(','))

    tmp.append(outputDirectory)
    requestsQueue.append(tmp)
    return tmp

def balancer():
    #write your code from here
    # tasks in requestsQueue
    # format of each task: [req1, req2, ..., reqn, outputdirectory]
    # format of each request: [method, inputFile]
       pass

def main():
    loadbalancerThread = threading.Thread(target=balancer)
    loadbalancerThread.daemon = True
    loadbalancerThread.start()

    while True:
        request = input()
        if request == 'end':
            sys.exit()
        else:
            parse(request)

if __name__ == '__main__':
    main()
import docker
import threading
import sys
import time
import os

requestsQueue = []
last_id = 0

def parse(request):
    global requestsQueue
    global last_id
    tuple =request[1:len(request)-1].split('>')
    tuple = tuple[0:len(tuple)-1]
    tmp = []
    for t in tuple:
        tmp.append(t.split('<')[1])
    tuple = tmp
    outputDirectory = tuple.pop()
    tmp = []
    tmp.append(last_id)
    last_id+=1
    for t in tuple:
        tmp.append(t.split(','))

    tmp.append(outputDirectory)
    requestsQueue.append(tmp)
    return tmp

def balancer():
    #write your code from here
    # tasks in requestsQueue
    # format of each task: [id,req1, req2, ..., reqn, outputdirectory]
    # format of each request: [method, inputFile]
    
    
    client = docker.from_env()
    #container = client.containers.run('loadbalancer/test:v1', detach=True, )
    #print(container.id)
    print(client.images.list())
    id= "729287d05935"
    container = client.containers.get(id)

    while True:
        if len(requestsQueue) > 0:

            curr_request = requestsQueue.pop(0)
            curr_reqid = curr_request.pop(0)
            output_dir = curr_request.pop(-1)
            
            print(curr_reqid, output_dir)
            for command in curr_request:
                cmd_name ,inputfile_path = command
                print("###############")
                copy_file(inputfile_path, id)
                print("iiiiiiiiii###############")
                file_name = os.path.basename(inputfile_path)
                exec_command(container, cmd_name, file_name)

            

            #print(client)
    
def copy_file(inputfile_path, container_id):
    copy_file_command = "docker cp " + inputfile_path + " " + container_id + ":/home/loadBalancer/in"
    print("copy command:", copy_file_command)
    a = os.system(copy_file_command)
    print(a)

def exec_command(container, cmd_name, file_name):
    exec_command_str = "python fileProcessor.py " + cmd_name + " " + "./in/" + file_name
    print("exec string:", exec_command_str)
    ou = container.exec_run(exec_command_str, stdout=True)
    print(ou)


def main():
    
    loadbalancerThread = threading.Thread(target=balancer)
    loadbalancerThread.daemon = True
    loadbalancerThread.start()

    while True:
        request = input()
        if request == 'end':
            print(requestsQueue)
            sys.exit()

        else:
            parse(request)

if __name__ == '__main__':
    main()

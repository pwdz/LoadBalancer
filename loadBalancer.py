import docker
import threading
import sys
import time
import os

requestsQueue = []
last_id = int(time.time()) % 100000
containerDic = {}
command_names = ['max', 'min', 'average', 'sort', 'wordcount']

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


def makeContainers(client):

    for i in range(3):
        container = client.containers.run("loadbalancer/fileprocessor:v1.0", detach=True, tty=True)
        containerDic[container.id] = True

    return containerDic


def balancer():
    client = docker.from_env()
    makeContainers(client)

    while True:
        if len(requestsQueue) > 0:
            idle = None

            curr_request = requestsQueue.pop(0)
            curr_reqid = curr_request.pop(0)
            output_dir = curr_request.pop(-1)

            print(curr_reqid, output_dir)
            for command in curr_request:
                while not idle:
                    for container in containerDic.keys():
                        if containerDic[container] == True:
                            idle = container
                            break
                cmd_name ,inputfile_path = command

                copy_file(inputfile_path, str(idle))
                file_name = os.path.basename(inputfile_path)

                container = client.containers.get(idle)

                if cmd_name in command_names:
                    containerThread = threading.Thread(target=exec_command, args=(container,curr_reqid,cmd_name, file_name,output_dir,))
                    containerThread.daemon = True
                    containerThread.start()


                else:
                    containerThread = threading.Thread(target=exec_program, args=(container, cmd_name, file_name,output_dir,))
                    containerThread.daemon = True
                    containerThread.start()


def copy_file(inputfile_path, container_id):
    copy_file_command = "docker cp " + inputfile_path + " " + container_id + ":/home/loadBalancer/in"
    print("copy command:", copy_file_command)
    status_code = os.system(copy_file_command)
    print("copy status code:", status_code)

def exec_command(container, reqid, cmd_name, inputfile_name, output_dir):
    exec_command_str = "python fileProcessor.py " + cmd_name + " " + "./in/" + inputfile_name
    print("exec string:", exec_command_str)
    containerDic[container.id] =False
    print("heyyyy",container.id)
    status_code, output_bytes = container.exec_run(exec_command_str, stdout=True)
    print(status_code, output_bytes)

    if status_code == 0:
        outputfile_name = cmd_name + str(reqid) + ".txt"
        outputfile = open(output_dir + "/" + outputfile_name, "w")

        outputfile.write(output_bytes.decode("utf-8"))
        outputfile.close()

    containerDic[container.id] = True

def exec_program(container, program_name, filename, output_dir):

    containerDic[container.id] =False

    exec_commands = [
        'mkdir ./in/temp',
        'g++ ./in/' + filename + ' -o ./in/temp/prog.o',
        './in/temp/prog.o',
        'rm -r -f ./in/temp'
    ]

    for cmd in exec_commands:
        if cmd.startswith("."): 
            status_code, output_bytes = container.exec_run(cmd, stdout=True)
            if status_code == 0:
                outputfile_name = program_name + ".out"
                outputfile = open(output_dir + "/" + outputfile_name, "w")

                outputfile.write(output_bytes.decode("utf-8"))  
                outputfile.close()
           
        else:
            container.exec_run(cmd)

    containerDic[container.id] = True


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

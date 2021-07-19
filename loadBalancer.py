import docker
import threading
import sys
import time
import os

requestsQueue = []
last_id = int(time.time()) % 100000
containers = []
pool = []
command_names = ['max', 'min', 'average', 'sort', 'wordcount']
client = docker.from_env()
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
    print("AVAILABLE CONTAINERS:")
    for i in range(3):
        container = client.containers.run("loadbalancer/losers:version1.0", detach=True, tty=True)
        containers.append(container.id)
        pool.append(container.id)
        print(container.name)

    return pool


def balancer():

    makeContainers(client)

    while True:
        if len(requestsQueue) > 0:


            curr_request = requestsQueue.pop(0)
            curr_reqid = curr_request.pop(0)
            output_dir = curr_request.pop(-1)

            # print(curr_reqid, output_dir)
            for command in curr_request:
                idle = None
                while not idle:
                    if len(pool)!= 0:
                        idle =pool.pop()
                    #
                    # for container in pool.keys():
                    #     if pool[container] == True:
                    #         idle = container
                    #         break
                cmd_name ,inputfile_path = command

                copy_file(inputfile_path, str(idle))
                file_name = os.path.basename(inputfile_path)

                container = client.containers.get(idle)

                if cmd_name in command_names:
                    containerThread = threading.Thread(target=exec_command, args=(container,curr_reqid,cmd_name, file_name,output_dir,))
                else:
                    containerThread = threading.Thread(target=exec_program, args=(container, cmd_name, file_name,output_dir,))

                containerThread.daemon = True
                containerThread.start()


def copy_file(inputfile_path, container_id):
    copy_file_command = "docker cp " + inputfile_path + " " + container_id + ":/home/loadBalancer/in"
    status_code = os.system(copy_file_command)


def exec_command(container, reqid, cmd_name, inputfile_name, output_dir):
    exec_command_str = "python fileProcessor.py " + cmd_name + " " + "./in/" + inputfile_name
    print("container name: "+container.name+" exec string: "+ exec_command_str)
    status_code, output_bytes = container.exec_run(exec_command_str, stdout=True)

    if status_code == 0:
        outputfile_name = cmd_name + str(reqid) + ".txt"
        outputfile = open(output_dir + "/" + outputfile_name, "w")
        outputfile.write(output_bytes.decode("utf-8"))
        outputfile.close()
        print(cmd_name+" from request "+str(reqid)+" ready in "+ output_dir+"/"+outputfile_name)

    pool.append(container.id)

def exec_program(container, program_name, filename, output_dir):
    # container.commit(repository=, tag=None)
    container.exec_run('mkdir ./in/temp')
    container.exec_run('mv ./in/'+filename+' ./in/temp')
    file, extension = os.path.splitext('./in/' + filename)
    cmd = ''
    if extension == '.cpp':
        container.exec_run('g++ ./in/temp/' + filename + ' -o ./in/temp/prog.o', stdout=True)
        cmd = './in/temp/prog.o'
    elif extension =='.py':
        cmd = 'python3 ./in/temp/'+filename

    print("container name: " + container.name + " executing file: " + program_name)

    status_code, output_bytes = container.exec_run(cmd, stdout=True)
    if status_code == 0:
            outputfile_name = program_name + ".out"
            outputfile = open(output_dir + "/" + outputfile_name, "w")
            outputfile.write(output_bytes.decode("utf-8"))
            outputfile.close()
            print("results of "+program_name+" ready in " + output_dir + "/" + outputfile_name)

    container.exec_run('rm -r -f ./in/temp')

    pool.append(container.id)

def cleanup():
    for container in containers:
        con = client.containers.get(container)
        con.remove(force=True)

def main():
    print(">> WELCOME TO THE ULTIMATE LOADBALANCER PROGRAM")
    loadbalancerThread = threading.Thread(target=balancer)
    loadbalancerThread.daemon = True
    loadbalancerThread.start()

    while True:
        request = input()
        if request == 'end':
            cleanup()
            sys.exit()

        else:
            parse(request)

if __name__ == '__main__':
    main()

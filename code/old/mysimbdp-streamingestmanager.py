import os
import logging
import sys
import subprocess
import signal


log_format = '%(asctime)s : [%(levelname)s] - %(message)s'

logs_directory = "../logs/mysimbdp-streamingingestmanager.log"
logs_dir_full_path = os.path.abspath(logs_directory)

logging.basicConfig(filename= logs_dir_full_path , filemode="a", level= logging.INFO, format=log_format)


scripts_directory = './clientstreamingestapps/'
configs_directory = './config_files/'

configs_dir_full_path = os.path.abspath(configs_directory)
scripts_dir_full_path = os.path.abspath(scripts_directory)

arguments = sys.argv[1:]
client = arguments[0]
action = arguments[1]



def launch_client(client):
    args = []
    args.append('python3')
    script = "clientstreamingestapp_" + client + ".py"
    args.append(scripts_dir_full_path + "/" + script)
    config = client+"_config.json"
    args.append(configs_dir_full_path + "/" + config)
    process = subprocess.Popen(args)
    logging.info(client+" running with PID: "+str(process.pid))
    return process.pid

def stop_client(client, pid):
    p_id = int(pid)
    #subprocess.call(["kill", "-9", "%d" % p_id])
    #os.kill(p_id, signal.SIGKILL)   # like -9
    os.kill(p_id, signal.SIGTERM)
    logging.info(client+" process with PID: "+str(pid)+" stopped")


def main():
    if action == 'start':
        new_pid = launch_client(client)
        print("clientstreamingestapp_" + client + " started, process ID: " + str(new_pid))
        f = open(client+'_PID.txt', 'a')
        f.write(str(new_pid))
        f.write('\n')
        f.close()
    elif action == 'stop':
        f = open(client+'_PID.txt', 'r+')
        pid = f.read().splitlines()
        f.truncate(0)
        f.seek(0)
        if (len(pid) > 1):
            stop_client(client, pid[0])
            print("clientstreamingestapp_" + client + " stopped, process ID: " + str(pid[0]))
            pid.remove(pid[0])
        else:
            logging.error("No more process to remove")
            print("No more process of " + client + " to remove")
        for element in pid:
            f.write(str(element))
            f.write('\n')
        f.close()
    elif action == 'stop_all':
        f = open(client + '_PID.txt', 'r+')
        pid = f.read().splitlines()
        f.truncate(0)
        f.close()
        for p in pid:
            stop_client(client, p)
            print("clientstreamingestapp_" + client + " stopped, process ID: " + str(p))
    else:
        logging.error("action argument not correct")


# Entry point of the script
if __name__ == "__main__":
     main()

import os
import multiprocessing
import time
import logging


log_format = '%(asctime)s : [%(levelname)s] - %(message)s'

logs_directory = "../logs/mysimbdp-batchingestmanager.log"
logs_dir_full_path = os.path.abspath(logs_directory)

logging.basicConfig(filename= logs_dir_full_path , filemode="a", level= logging.INFO, format=log_format)

scripts_directory = './clientbatchingestapps/'
configs_directory = './config_files/'
stage_directory = '/Users/ddp/dev/bdp/stage/'

configs_dir_full_path = os.path.abspath(configs_directory)


def ingest(command):
    os.system(command[0])
    return command[1]


def client_callback(results):
    for result in results:
        if result == -1:
            logging.error('Uploading error')
            print('Uploading error')
        else:
            os.remove(result)
            print('File ' + result + ' removed')
            logging.info('File ' + result + ' removed')


def main():
    print('mysimbdp-batchingestmanager running...')
    pool = multiprocessing.Pool(4)
    while True:
        client_scripts = []
        for dir in os.walk(scripts_directory):
            for file in dir[2]:
                if not file == '.DS_Store':
                    client_scripts.append(file)

        config_files = []
        for dir in os.walk(configs_directory):
            for file in dir[2]:
                if not file == '.DS_Store':
                    config_files.append(file)

        commands = []
        for dir in os.walk(stage_directory):
            if not stage_directory == dir[0]:
                client_app = "clientbatchingestapp_" + os.path.basename(os.path.normpath(dir[0])) + ".py"
                client_config = os.path.basename(os.path.normpath(dir[0])) +"_config.json"
                if client_app in client_scripts and client_config in config_files:
                    for file in dir[2]:
                        if not file == '.DS_Store':
                            file_path = dir[0] + "/" + file
                            command = "python3 " + scripts_directory + client_app + " '" + dir[0] + "/" + file + "'"+" '" + configs_dir_full_path + "/" + client_config + "'"
                            commands.append((command, file_path))

        res = pool.map_async(ingest, commands, callback = client_callback)
        res.get()
        time.sleep(5)


# Entry point of the script
if __name__ == "__main__":
    main()


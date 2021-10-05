import json, os, sys, subprocess, logging, time


with open(os.path.join(sys.path[0],'servers.json'), encoding='utf-8') as json_data:
    server_data = json.load(json_data)


def write_json(new_data, filename='servers.json'):
    with open(os.path.join(sys.path[0], filename),'r+') as file:
          # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        file_data["hosts"][clusters].update(new_data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent = 4)    



command_git = "echo `git rev-parse --abbrev-ref HEAD` `git rev-parse --short HEAD`"
command_subversion = "echo `svn info | grep '^URL:' | egrep -o '(tags|branches)/[^/]+|trunk' | egrep -o '[^/]+$'` `svn info | grep Revision: | awk '{print $2}'`"
command_dir = "cd ~/bw/"

def loc_start(self, cmd_line, cwd=None):
    output = ""
    process = subprocess.Popen(cmd_line, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, cwd=cwd, shell=True)
    for line in process.stdout:
        logging.info(line.rstrip())
        output += "{}".format(line)
    for line in process.stderr:
        logging.info(line.rstrip())
        output += "{}".format(line)
    time.sleep(1)
    process_exit_code = process.wait()
    return process_exit_code, output


for clusters in server_data["hosts"]:
    # print(clusters)
    remote_uname = server_data["hosts"][clusters]["user"]
    remote_host = server_data["hosts"][clusters]["host"]
    out_git = loc_start("ssh", "{}@{} {} && {}".format(remote_uname, remote_host, command_dir, command_git))
    out_svn = loc_start("ssh", "{}@{} {} && {}".format(remote_uname, remote_host, command_dir, command_subversion))
    # print(out)
    # print("ssh", "{}@{} {} && {}".format(remote_uname, remote_host, command_dir, command_git))
    rev_info_git = {"rev_git": out_git[1]}

    if "error" or " not found" in rev_info_git["rev_git"]:
        rev_info_git = {"rev_git": "no git repo in directory"}
        write_json(rev_info_git)

    rev_info_svn = {"rev_svn": out_svn[1]}
    if "error" in rev_info_svn["rev_svn"]:
        rev_info_svn = {"rev_svn": "no svn repo in directory"}    
        write_json(rev_info_svn )


    
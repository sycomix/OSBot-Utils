import os
import signal
import subprocess


#def run_process(executable, params = None, cwd='.'):
#    return Process.run(executable, params, cwd)

def chmod_x(executable_path):
    return run_process("chmod", ['+x', executable_path])

class Process:

    @staticmethod
    def run(executable, params = None, cwd='.'):
        params = params or []
        if type(params) is str:
            params = [params]
        run_params  = [executable] + params
        try:
            result      = subprocess.run(run_params, cwd = cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            return {
                "runParams" : run_params            ,
                "cwd"       : cwd                   ,
                "stdout"    : result.stdout.decode(),
                "stderr"    : result.stderr.decode(),
            }
        except Exception as error:
            return {
                "runParams" : run_params            ,
                "cwd"       : cwd                   ,
                "stdout"    : None                  ,
                "stderr"    : error                 ,
            }

    @staticmethod
    def stop(pid):
        #print('killing process {0} with {1}'.format(pid, signal.SIGKILL))
        return os.kill(pid, signal.SIGKILL)

    # exec helpers
    @staticmethod
    def exec_open(file_path, cwd='.'): return Process.run("open", [file_path], cwd)


kill_process  = Process.stop
run_process   = Process.run
exec_open     = Process.exec_open
exec_process  = Process.run
start_process = Process.run
stop_process  = Process.stop




#def run_process(executable, params = None, cwd='.'):
#    return Process.run(executable, params, cwd)
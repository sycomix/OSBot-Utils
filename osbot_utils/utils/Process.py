import os
import signal
import subprocess

class Process:

    @staticmethod
    def run(executable, params = None, cwd='.'):
        params = params or []
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
        print('killing process {0} with {1}'.format(pid, signal.SIGKILL))
        print(os.kill(pid, signal.SIGKILL))

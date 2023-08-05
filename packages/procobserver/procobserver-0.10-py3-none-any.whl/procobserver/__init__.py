import os
from time import time
import pandas as pd
import psutil
from deepcopyall import deepcopy
from a_pandas_ex_dillpickle import pd_add_dillpickle
from kthread_sleep import sleep
import sys

pd_add_dillpickle()


def observe_procs(
    executables=(), pids=(), pickle_output_path=None, sleeptime=0.1, timeout=None
):
    if not timeout:
        timeout = sys.maxsize // 2
    finaltimeout = timeout + time()
    alldafs = []
    stopnow = False
    try:
        while not stopnow and finaltimeout > time():
            for ini, p in enumerate(psutil.process_iter()):
                if finaltimeout < time():
                    print("Timeout ...")

                    stopnow = True
                    break

                try:

                    if p.name() in executables or p.pid in pids:
                        df = pd.DataFrame(p.as_dict().items()).set_index(0).T
                        df["aa_process_no"] = ini
                        df["aa_localtime"] = time()
                        alldafs.append(deepcopy(df))
                except Exception as fe:
                    print(fe)
                    continue
                except KeyboardInterrupt as ke:
                    print("Stopping observation ...")
                    stopnow = True
                    break
            sleep(sleeptime)
    except KeyboardInterrupt as ke:
        print("Stopping observation ...")
    df = pd.concat(alldafs, ignore_index=True)
    if pickle_output_path:
        pickle_output_path = os.path.normpath(pickle_output_path)
        df.to_dillpickle(pickle_output_path)
    return df

"""Enforce the registered UTC wall deadline across macOS system sleep."""
import datetime
import json
import os
from pathlib import Path
import signal
import subprocess
import time

root=Path('/Users/andrej/workspace/antikythera')
launch=json.loads((root/'reports/curveball_extension1_launch.json').read_text())
parent=launch['pid']
deadline=datetime.datetime.fromisoformat(launch['started_utc']).timestamp()+launch['global_sampling_wall_seconds']
path=root/'reports/curveball_extension1_wall_guard.json'
record=dict(started_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),parent_pid=parent,
            deadline_utc=datetime.datetime.fromtimestamp(deadline,datetime.timezone.utc).isoformat(),
            reason='macOS maintenance sleep pauses the internal monotonic clock; enforce the unchanged original six-hour UTC wall limit externally.',status='WATCHING')
def save():
    temp=path.with_suffix('.tmp');temp.write_text(json.dumps(record,indent=2)+'\n');temp.replace(path)
def processes():
    result={}
    for line in subprocess.check_output(['ps','-axo','pid=,ppid=,command='],text=True).splitlines():
        parts=line.strip().split(None,2)
        if len(parts)==3:result[int(parts[0])]=(int(parts[1]),parts[2])
    return result
save()
while True:
    rows=processes()
    if parent not in rows or 'python eval/run_curveball_extension.py' not in rows[parent][1]:
        record['status']='QUEUE_EXITED';break
    if time.time()>=deadline:
        workers=[pid for pid,(ppid,cmd) in rows.items() if ppid==parent and 'multiprocessing.spawn' in cmd]
        record.update(status='UTC_WALL_BUDGET_STOP',worker_pids=workers)
        save()
        for pid in workers+[parent]:
            try:os.kill(pid,signal.SIGTERM)
            except ProcessLookupError:pass
        break
    time.sleep(min(5,max(.1,deadline-time.time())))
record['finished_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();save()

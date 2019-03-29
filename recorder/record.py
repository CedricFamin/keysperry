#!/usr/bin/python3

import os, signal, time, pytz, sys
from datetime import datetime
from subprocess import check_output, Popen

recpath = '/home/pi/midi'
tz = pytz.timezone('Europe/Helsinki')
arec = '/usr/bin/arecordmidi'

def get_ports():
        str = check_output([arec, '-l'], universal_newlines=True)
        res = [line.split()[0] for line in str.split('n') if 'MIDI' in line]
        return res

def get_pids(proc):
        try:
                str = check_output(['pgrep', proc], universal_newlines=True)
                return [int(pid) for pid in str.split()]
        except: return []

print('recmidi.sh started')

while True:
        pids = get_pids('arecordmidi')
        ports = get_ports()
        timestr = datetime.now(tz).strftime('%Y-%m-%d_%H.%M.%S')

        if ports and pids: print(timestr, 'Recording...')
        elif ports:
                cmd = [arec, '-p', ports[0], '%s/rec%s.mid' % (recpath, timestr)]
                pid = Popen(cmd).pid
                print(timestr, 'Started [%d] %s' % (pid, ' '.join(cmd)))
        elif pids:
                os.kill(pids[0], signal.SIGINT)
                print(timestr, 'Killed (SIGINT) [%d]' % pids[0])

        sys.stdout.flush()
        time.sleep(10) # Sleep until retry
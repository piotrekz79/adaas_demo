import sys
import select
import subprocess
import time
import os
cmds=['/home/adaas/adaas_demo/selector_consumer1_topic.py','/home/adaas/adaas_demo/selector_consumer2_topic.py']

i=0
old_proc=subprocess.Popen(['python', cmds[i]])
new_proc=[]



# files monitored for input
read_list = [sys.stdin]
# select() should wait for this many seconds for input.
# A smaller number means more cpu usage, but a greater one
# means a more noticeable delay between input becoming
# available and the program starting to work on it.
timeout = 0.1 # seconds
last_work_time = time.time()

def treat_input(linein):
  global last_work_time
  global i
  global old_proc
  global new_proc
  i=(i+1)%2
  print("switching to consumer %d" ,i+1)
  new_proc=subprocess.Popen(['python', cmds[i]])
  old_proc.kill()
  old_proc=new_proc
  last_work_time = time.time()

def idle_work():
  global last_work_time
  now = time.time()
  # do some other stuff every 2 seconds of idleness
  if now - last_work_time > 2:
    print('waiting for switchover action')
    last_work_time = now

def main_loop():
  global read_list
  # while still waiting for input on at least one file
  while read_list:
    ready = select.select(read_list, [], [], timeout)[0]
    if not ready:
      idle_work()
    else:
      for file in ready:
        line = file.readline()
        if not line: # EOF, remove file from input list
          read_list.remove(file)
        elif line.rstrip(): # optional: skipping empty lines
          treat_input(line)

try:
    main_loop()
except KeyboardInterrupt:
  pass





#while sys.stdin in select.select([sys.stdin],[],[],0)[0]:
#    line = sys.stdin.readline()
#    if line:
#        print(i)
#        i=(i+1)%2
#curr_proc.kill()
import multiprocessing as mp
import time
import vision
import os
import color

def a():
    i = 1
    initidx = 0
    lsof = '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'
    while i<101:
        print(color.colors.fg.lightgray+ str(i) + '%', color.colors.fg.lightgreen + lsof[0:initidx])
        print(color.colors.reset)

        i+=1
        initidx += 1
        time.sleep(0.025)
        os.system('clear')

def b():
    vision.run('yolov8n')


proc2 = mp.Process(target=a())
proc1 = mp.Process(target=b())
proc2.start()
proc1.start()
proc2.join()
proc1.join()
print("Both Processes Completed!")
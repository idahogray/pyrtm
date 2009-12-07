#!/usr/bin/env python
# simple app

from rtm import createRTM

from Tkinter import *

def createApp(rtm):
    rspTasks = rtm.tasks.getList(filter='dueWithin:"1 week of today"')
    tasks = [t.name for t in rspTasks.tasks.list.taskseries]

    root = Tk()
    root.wm_attributes('-topmost', 1)
    root.wm_attributes('-alpha', 0.5)
    l = Label(text='\n'.join(tasks))
    l.pack()
    l.mainloop()

def test(apiKey, secret, token=None):
    rtm = createRTM(apiKey, secret, token)
    createApp(rtm)

if __name__ == '__main__':
    import sys
    try:
        prog, api_key, secret = sys.argv
    except ValueError:
        print >>sys.stderr, 'Usage: ./app.py APIKEY SECRET'
    else:
        test(api_key, secret)
    
    
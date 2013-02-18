#! /usr/bin/env python
# coding:utf-8

import terminal
import threading
import time

term = terminal.TerminalController()
#print term.render('hello, ${GREEN}world${NORMAL}')

class ProgressLine(threading.Thread):
    def __init__(self, interval_time, title=''):
        threading.Thread.__init__(self)
        self.interval_time = interval_time
        self.title=title
        self._stop_flag = False
        self._count = 0
        self.setDaemon(True)

    def run(self):
        while not self._stop_flag:
            if self._count in [0, 2, 6]:
                print term.render('%s -${UP}' % self.title)
            elif self._count in [1, 5, 9]:
                print term.render('%s /${UP}' % self.title)
            elif self._count in [3, 7]:
                print term.render('%s \${UP}' % self.title)
            elif self._count in [4, 8]:
                print term.render('%s |${UP}' % self.title)

            if self._count == 9:
                self._count = 0
            else:
                self._count += 1
            time.sleep(self.interval_time)

    def stop(self):
        self._stop_flag = True
        print term.render('%s done' % self.title)


if __name__=='__main__':
    print 'start get application'
    p = ProgressLine(0.12, title='now loading...')
    p.start()
    time.sleep(3)
    p.stop()
    print ' download ok'
    p = ProgressLine(0.12, title='now loading...')
    p.start()
    time.sleep(3)
    p.stop()
    print 'finish'

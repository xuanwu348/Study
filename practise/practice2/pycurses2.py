#https://stackoverflow.com/questions/26152942/python-curses-user-input-while-updating-screen

import curses, curses.panel
import random
import time
import sys
import select

gui = None

class ui:
    def __init__(self):
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        self.stdscr.keypad(1)

        self.win1 = curses.newwin(10,50,0,0)
        self.win1.border(0)
        self.pan1 = curses.panel.new_panel(self.win1)
        self.win2 = curses.newwin(10,50,0,0)
        self.win2.border(0)
        self.pan2 = curses.panel.new_panel(self.win2)
        self.win3 = curses.newwin(10, 50, 12, 0)
        self.win3.border(0)
        self.pan3 = curses.panel.new_panel(self.win3)

        self.win1.addstr(1, 1, "Windows 1")
        self.win2.addstr(1, 1, "Windows 2")
        self.win3.addstr(1, 1, "Press 's' to switch windows or 'q' to quit.")

        self.pan1.hide()
    
    def refresh(self):
        curses.panel.update_panels()
        self.win2.refresh()
        self.win1.refresh()

    def switch_pan(self):
        if self.pan1.hidden():
            self.pan2.bottom()
            self.pan2.hide()
            self.pan1.top()
            self.pan1.show()
        else:
            self.pan1.bottom()
            self.pan1.hide()
            self.pan2.top()
            self.pan2.show()

        self.refresh()

    def quit_ui(self):
        curses.nocbreak()
        self.stdscr.keypad(0)
        curses.curs_set(1)
        curses.echo()
        curses.endwin()
        print("UI quitted")
        exit(0)

class feeder:
    #Fake U.I feeder
    def __init__(self):
        self.running = False
        self.ui = ui()
        self.count = 0

    def stop(self):
        self.running = False

    def run(self):
        self.running = True
        self.feed()

    def feed(self):
        while self.running:
            while sys.stdin in select.select([sys.stdin],[],[],0)[0]:
                line = sys.stdin.read(1)
                if line.strip() == "q":
                    self.stop
                    self.ui.quit_ui()
                    break
                elif line.strip() == "s":
                    self.ui.switch_pan()

            self.ui.win1.addstr(3, 1, str(self.count) + ": " + str(int(round(random.random() * 999))))
            self.ui.win1.addstr(4, 1, str(self.running))
            self.ui.win2.addstr(3, 1, str(self.count) + ": " + str(int(round(random.random() * 999))))
            self.ui.win2.addstr(4, 1, str(self.running))
            self.ui.refresh()
            time.sleep(0.1)
            self.count += 1

if __name__ == "__main__":
    f = feeder()
    f.run()



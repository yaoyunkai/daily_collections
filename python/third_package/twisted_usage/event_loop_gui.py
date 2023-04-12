"""
file: event_loop_gui.py
Created by Libyao at 2023/4/12


"""

from six.moves import tkinter
from six.moves.tkinter import scrolledtext


class Application(tkinter.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.pack()

        self.helloButton = tkinter.Button(self, text='Say Hello', command=self.sayHello)
        self.worldButton = tkinter.Button(self, text='Say World', command=self.sayWorld)

        self.output = scrolledtext.ScrolledText(master=self)
        self.helloButton.pack(side='top')
        self.worldButton.pack(side='top')
        self.output.pack(side='top')

    def outputLine(self, text):
        self.output.insert(tkinter.INSERT, text + '\n')

    def sayHello(self):
        self.outputLine('Hello')

    def sayWorld(self):
        self.outputLine('World')


if __name__ == '__main__':
    Application(tkinter.Tk()).mainloop()

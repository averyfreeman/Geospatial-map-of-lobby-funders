#!/usr/bin/env python3
print('################################################################')
print('### if this script fails, you are probably missing a library ###')
print('################################################################')

import sys
import matplotlib
import tkinter

path_formatted = str(sys.path).replace('[','\n').replace(',','\n').replace(']','')
tkinter_path = str(tkinter.__path__).replace('[','').replace(',','').replace(']','')
tkinter_spec = str(tkinter.__spec__).replace('(','\n').replace(')','').replace(',','\n').replace('[','').replace(',','').replace(']','')
matplotlib_path = str(matplotlib.__path__).replace('[','').replace(',','').replace(']','')

docstring = """ 
    this is a very simple script meant only to test your system 
    for the libraries required to run matplotlib with tkinter
    """
print(docstring)
print('Python version:', sys.version)
print('Python path(s):', path_formatted)
print('tkinter version info type:', tkinter._VersionInfoType)
print('tkinter name:', tkinter.__name__)
print('tkinter package:', tkinter.__package__)
print('tkinter path:', tkinter_path)
print('tkinter spec:', tkinter_spec)
print('Matplotlib path:', matplotlib_path)
print('Matplotlib version:', matplotlib.__version__)
# print('Matplotlib available backends:', matplotlib_dir)
backend_str = 'Backend: ' + str(matplotlib.get_backend())


class Application(tkinter.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()

        self.entry = tkinter.Entry(self)
        self.entry.pack()

        self.button = tkinter.Button(self, text="Validate", command=self.validate)
        self.button.pack()

    def validate(self):
        # Get the input from the entry widget
        self.entry.insert(0, backend_str)
        print(backend_str)
        print('visit https://matplotlib.org/stable/users/explain/figure/backends.html for more information about configuring your matplotlib backend')

if __name__ == "__main__":
    root = tkinter.Tk()
    app = Application(root)
    app.mainloop()
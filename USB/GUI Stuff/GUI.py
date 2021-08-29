from tkinter import *
import os
from PrinterFileServer import *

GREEN = "#4FFC1B"


class baseGUI:
    def __init__(self, server=True):
        self.isServer = server
        self.top = Tk()
        self.top.geometry("325x450")
        self.top.configure(bg="Black")
        self.AddrWrapper = Frame(self.top, bg="Black")
        self.IPLabel = Label(self.AddrWrapper, text="IP Address", bg="Black", fg=GREEN)
        self.IPAddr = Entry(self.AddrWrapper, bd=5, bg="Black", fg=GREEN)
        if self.isServer:
            self.IPAddr.insert(0, "0.0.0.0")
        self.AddrWrapper.grid(row=1, sticky="W")

        self.PortWrapper = Frame(self.top, bg="Black")
        self.PortLabel = Label(self.PortWrapper, text="Port Number", bg="Black", fg=GREEN)
        self.PortNum = Entry(self.PortWrapper, bd=2, bg="Black", fg=GREEN)
        self.PortWrapper.grid(row=2, sticky="W")

        self.FileWrapper = Frame(self.top, bg="Black")
        self.FileWrapper.grid(row=3)
        self.FileLabel = Label(self.FileWrapper, text="File / Folder Path", bg="Black", fg=GREEN)
        self.FilePath = Entry(self.FileWrapper, bd=2, bg="Black", fg=GREEN)
        self.FilePath.insert(0, os.path.abspath(os.getcwd()))

        self.selection = StringVar()
        self.FileRadioWrapper = Frame(self.top, bg="Black")
        self.FileRadioWrapper.grid(row=4, sticky="W")
        self.FileRadio = Radiobutton(self.FileRadioWrapper, text="File", variable=self.selection,
                                     value="File", bg="Black", fg=GREEN)
        self.FolderRadio = Radiobutton(self.FileRadioWrapper, text="Folder", variable=self.selection,
                                       value="Folder", bg="Black", fg=GREEN)
        self.FileWrapper.grid(row=3, sticky="W")

        self.OutputWrapper = Frame(self.top, bg="Black")
        self.OutputWrapper.grid(row=5, sticky="W")
        self.Output = Text(self.OutputWrapper, bg="Black", fg=GREEN, width="39")

        self.RunWrapper = Frame(self.top, bg="Black")
        self.RunButton = Button(self.RunWrapper, text="Run", bg="Black", fg="Red", command=self.__FTPStart)
        self.RunWrapper.grid(row=1, sticky="E")

        self.__pack()
        if self.isServer:
            self.FileRadio.configure(state=DISABLED)
            self.FolderRadio.configure(state=DISABLED)
        self.__run(server) if self.isServer else self.__run(False)

    def __FTPStart(self):
        if self.selection.get() == '' and not self.isServer:
            self.__displayMessage("Need to select radio button", False)
            return
        elif self.IPAddr.get() == '':
            self.__displayMessage("Missing IP Address", False)
            return
        elif self.PortNum.get() == '':
            self.__displayMessage("Missing Port Number", False)
            return
        elif self.FilePath.get() == '':
            self.__displayMessage("Missing File Path", False)
            return
        CommonFilePath = self.FilePath.get()
        if CommonFilePath[-1] != '\\' or CommonFilePath[-1] != '/' and self.selection.get() != 'File':
            if '\\' in CommonFilePath:
                CommonFilePath += '\\'
            else:
                CommonFilePath += '/'

        if self.isServer:
            self.PFS = PrinterFileServerWithGUI(str(self.IPAddr.get()), str(self.PortNum.get()), self.Output, str(CommonFilePath))
            while True:
                try:
                    self.PFS.run_server()
                except Exception as e:
                    self.__displayMessage(e, False)
        else:
            self.PFS = PrinterFileServerWithGUI(str(self.IPAddr.get()), str(self.PortNum.get()), self.Output)
            if self.selection.get() == 'File':
                if os.path.isfile(CommonFilePath):
                    self.PFS.run_client(CommonFilePath.strip())
                else:
                    self.__displayMessage("File was not found at given path", False)
            else:
                if os.path.isdir(CommonFilePath):
                    files = os.listdir(CommonFilePath)
                    for f in files:
                        if not os.path.isdir(CommonFilePath + f):
                            self.__displayMessage("Sending {}...".format(CommonFilePath + f))
                            try:
                                self.PFS.run_client(CommonFilePath + f)
                            except:
                                self.__displayMessage("Was unable to send {}".format(CommonFilePath + f))
                else:
                    self.__displayMessage("Given path is not a directory", False)

    def __displayMessage(self, message, append=True):
        if append:
            self.Output.insert(INSERT, '\n' + message)
        else:
            self.Output.delete("1.0", END)
            self.Output.insert(INSERT, message)

    def __pack(self):
        for frame in self.top.children:
            for child in self.top.children[frame].children:
                self.top.children[frame].children[child].pack()
                if self.top.children[frame].children[child].children:
                    for infant in self.top.children[frame].children[child].children:
                        self.top.children[frame].children[child].children[infant].pack()

    def __run(self, server):
        self.__pack()
        if server:
            self.__server_GUI()
        else:
            self.__client_GUI()
        self.__show()

    def __show(self):
        self.top.mainloop()

    def __server_GUI(self):
        self.top.title("Server")

    def __client_GUI(self):
        self.top.title("Client")


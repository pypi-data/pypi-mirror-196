import os

from tkinter import *

from autoappanalysis.model.Vm import Vm
from autoappanalysis.cmd.HostCommand import HostCommand

class Gui():
    def __init__(self, vm, user, pw, input, output, outputHost, snapshotDir, snapshotName="snapshot", snapshotNumber=1) -> None:

        # Tk window
        self.root = Tk()
        self.root.title('AutoAppAnalysis')
        self.root.resizable(False, False)

        # Layouts
        frameLeft = Frame(self.root)
        frameLeft.grid(row=0, column=0, padx=10, pady=10)
        frameRight = Frame(self.root)
        frameRight.grid(row=0, column=1, padx=10, pady=10)

        # Button
        self.rootBtn = Button(frameRight, text="Root", command=self._rootAVD)
        self.rootBtn.grid(row=0, column=0, pady=2, sticky="w")
        self.extractBtn = Button(frameRight, text="Extract File", command=self.extractFile)
        self.extractBtn.grid(row=1, column=0, pady=2, sticky="w")
        self.createBtn = Button(frameRight, text="Create Snapshot", command=self._createSnapshot)
        self.createBtn.grid(row=2, column=0, pady=2, sticky="w")
        self.decryptBtn = Button(frameRight, text="Decrypt Snapshots", command=self._decryptSnapshots)
        self.decryptBtn.grid(row=4, column=0, pady=2, sticky="w")
        self.analyseBtn = Button(frameRight, text="Analyse Snapshots", command=self._analyseSnapshots)
        self.analyseBtn.grid(row=5, column=0, pady=2, sticky="w")

        # Text
        self.labelVm = Label(frameLeft, text='VM Name:')
        self.labelVm.grid(row=0, column=0, sticky="w")
        self.vmTxt = Text(frameLeft, height = 1, width = 20)
        self.vmTxt.insert('1.0', vm)
        self.vmTxt.grid(row=1, column=0)
        
        self.labelUser = Label(frameLeft, text='VM User Name:')
        self.labelUser.grid(row=0, column=1, sticky="w")
        self.userTxt = Text(frameLeft, height = 1, width = 20)
        self.userTxt.insert('1.0', user)
        self.userTxt.grid(row=1, column=1)
        
        self.labelPw = Label(frameLeft, text='VM Password:')
        self.labelPw.grid(row=0, column=2, sticky="w")
        self.pwTxt = Text(frameLeft, height = 1, width = 20)
        self.pwTxt.insert('1.0', pw)
        self.pwTxt.grid(row=1, column=2)

        self.labelInputDir = Label(frameLeft, text='VM Input Directory:')
        self.labelInputDir.grid(row=2, column=0, sticky="w")
        self.inputTxt = Text(frameLeft, height = 1, width = 20)
        self.inputTxt.insert('1.0', input)
        self.inputTxt.grid(row=3, column=0)

        self.labelOutputDir = Label(frameLeft, text='VM Output Directory:')
        self.labelOutputDir.grid(row=2, column=1, sticky="w")
        self.outputTxt = Text(frameLeft, height = 1, width = 20)
        self.outputTxt.insert('1.0', output)
        self.outputTxt.grid(row=3, column=1)

        self.labelhOutputDir = Label(frameLeft, text='Host Output Directory:')
        self.labelhOutputDir.grid(row=2, column=2, sticky="w")
        self.hOutputTxt = Text(frameLeft, height = 1, width = 20)
        self.hOutputTxt.insert('1.0', outputHost)
        self.hOutputTxt.grid(row=3, column=2)

        self.labelAvdPath = Label(frameLeft, text='AVD Path:')
        self.labelAvdPath.grid(row=4, column=0, sticky="w")
        self.avdPathTxt = Text(frameLeft, height = 1, width = 20)
        self.avdPathTxt.insert('1.0', snapshotDir)
        self.avdPathTxt.grid(row=5, column=0)

        self.labelFilePath = Label(frameLeft, text='AVD File Path:')
        self.labelFilePath.grid(row=4, column=1, sticky="w")
        self.avdFileTxt = Text(frameLeft, height = 1, width = 20)
        self.avdFileTxt.insert('1.0', "/data/data/")
        self.avdFileTxt.grid(row=5, column=1)

        self.labelSName = Label(frameLeft, text='Snapshot Name:')
        self.labelSName.grid(row=6, column=0, sticky="w")
        self.sNameTxt = Text(frameLeft, height = 1, width = 20)
        self.sNameTxt.insert('1.0', snapshotName)
        self.sNameTxt.grid(row=7, column=0)

        self.labelSNumber = Label(frameLeft, text='Snapshot Number:')
        self.labelSNumber.grid(row=6, column=1, sticky="w")
        self.sNumberTxt = Text(frameLeft, height = 1, width = 20)
        self.sNumberTxt.insert('1.0', snapshotNumber)
        self.sNumberTxt.grid(row=7, column=1)

    def _rootAVD(self):
        cmd = HostCommand.ADB_ROOT
        print(cmd)

    def extractFile(self):
        path = self.avdFileTxt.get("1.0", "end-1c")
        cmd = HostCommand.ADB_PULL.substitute(path=path)
        print(cmd)

    def _createSnapshot(self):
        name_ = self.sNameTxt.get("1.0", "end-1c")
        number = self.sNumberTxt.get("1.0", "end-1c")
        cmd = HostCommand.ADB_SNAPSHOT_SAVE.substitute(name=name_ + "." + number)
        print(cmd)
        cmdResult = os.popen(cmd).read()
        print(cmdResult)

    def _getSnapshotList(self):
        snapshots = []
        avdDir = self.avdPathTxt.get("1.0", "end-1c")
        for path, dirs, files in os.walk(os.path.join(avdDir, "snapshots"), topdown=False):
            for name in dirs:
                if("default_boot" not in name):
                    snapshots.append(name)
        return snapshots
    
    def _decryptSnapshots(self):
        vm = self.vmTxt.get("1.0", "end-1c")
        user = self.userTxt.get("1.0", "end-1c")
        pw = self.pwTxt.get("1.0", "end-1c")
        avdPath = self.inputTxt.get("1.0", "end-1c")
        outputDir = self.outputTxt.get("1.0", "end-1c") + "/decrypted"
        snapshots = self._getSnapshotList()

        for snapshot in snapshots:
            py = "/usr/bin/python3"
            avdecrypt = "/home/" + user + "/scripts/avdecrypt/avdecrypt.py"
            params = "-a " + avdPath + " -s " + snapshot + " -o " + outputDir
            cmd = py + " " + avdecrypt + " " + params
            analysisVm = Vm(vm, user, pw)
            analysisVm.executeWithParams(py, cmd)

        print("Decryption finished")

    def _analyseSnapshots(self):
        vm = self.vmTxt.get("1.0", "end-1c")
        user = self.userTxt.get("1.0", "end-1c")
        pw = self.pwTxt.get("1.0", "end-1c")
        outputDir = self.outputTxt.get("1.0", "end-1c")
        decryptedDir = outputDir + "/decrypted"
        snapshots = self._getSnapshotList()
        outputHost = self.hOutputTxt.get("1.0", "end-1c")

        init = ""
        py = "/usr/bin/python3"
        dfxml = "/home/" + user + "/scripts/dfxml_python/dfxml/bin/idifference2.py"
        
        for snapshot in snapshots:
            if("init" in snapshot):
                init = snapshot

        for snapshot in snapshots:
            if("init" not in snapshot):
                before = decryptedDir + "/" + init + ".raw"
                after = decryptedDir + "/" + snapshot + ".raw"
                target = outputHost + "\\ge\\" + snapshot + ".idiff"
                cmd = py + " " + dfxml + " " + before + " " + after + " > " + target
                analysisVm = Vm(vm, user, pw)
                result = analysisVm.executeWithParams(py, cmd)

        print("Analysis finished")


    def _processSnapshots(self):
      pass

    def start(self):
        self.root.mainloop()
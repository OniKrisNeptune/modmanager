import os
import shutil
import sys
import PySimpleGUI as sg
sg.theme("dark grey 3")

def guiButton(key):
    return sg.Button(key, size=15)
def guiColumn(col, size):
    return sg.Column(col, size=size, scrollable=True, vertical_scroll_only=True)
def kfv(dick, value):
    return list(dick.keys())[list(dick.values()).index(value)]

def main(f):
    f.seek(0)
    file = f.read().split("\n")
    namefile = {}
    filepath = {}
    mods = []
    def start():
        f.seek(0)
        file = f.read().split("\n")
        if file[0] == "":
            layout = [[sg.Text("Enter location of minecraft mods folder")],
                      [sg.Input(), sg.FolderBrowse()],
                      [guiButton("OK")]]
            window = sg.Window("First time setup", layout)
            event, values = window.read()
            window.close()
            f.write(values[0])
            f.seek(0)
        namefile.clear()
        filepath.clear()
        for i in file[1:]:
            if i == "":
                break
            i = i.split(",")
            fn = i[1].split("/")[-1]
            namefile[i[0]] = fn
            filepath[fn] = i[1]
        mods.clear()
        for i in os.listdir(file[0]):
            if i in filepath:
                i = kfv(namefile, i)
            else:
                i = "? " + i
            mods.append([True, i])
        for i in namefile:
            if not namefile[i] in os.listdir(file[0]):
                mods.append([False, i])

        guiMods = []
        for i in mods:
            guiMods.append([sg.CBox(i[1], default=i[0])])
        layout = [[sg.Text("Mods")],
                  [guiColumn(guiMods, (300,300))],
                  [guiButton("Apply"), guiButton("Add mod")],
                  [guiButton("Refresh"), guiButton("Quit")]]
        window = sg.Window("Mod manager", layout)
        event, values = window.read()
        window.close()

        match event:
            case "Apply":
                apply(values)
            case "Add mod":
                addmod()
            case "Refresh":
                pass
            case "Quit":
                sys.exit()
        start()

    def apply(status):
        for i in range(len(mods)):
            ouchy = False
            if mods[i][1][0] == "?":
                mods[i][1] = mods[i][1][2:]
                ouchy = True
            else:
                mods[i][1] = namefile[mods[i][1]]
            if status[i] & (not mods[i][0]):
                shutil.copy(filepath[mods[i][1]], file[0])
            elif (not status[i]) & mods[i][0]:
                if ouchy:

                    layout = [[sg.Text("File " + mods[i][1])],
                              [sg.Text("not known by the program.")],
                              [sg.Text("Removing it may be irrevirsible")],
                              [sg.Text("Confirm removal?")],
                              [sg.Button("Confirm"), sg.Button("Skip it")]]
                    window = sg.Window("Confirm removal", layout)
                    event, values = window.read()
                    window.close()

                    match event:
                        case "Confirm":
                            pass
                        case "Skip it":
                            continue
                os.remove(file[0] + "/" + mods[i][1])

    def addmod():
        
        layout = [[sg.Text("mod location")],
                  [sg.Input(size=25), sg.FileBrowse(file_types=(("JAR Files", "*.jar"),))],
                  [sg.Input("Name", size=17)],
                  [guiButton("OK"), guiButton("Cancel")]]
        window = sg.Window("Add mod", layout)
        event, values = window.read()
        window.close()

        match event:
            case "OK":
                f.write("\n" + values[1] + "," + values[0])
            case "Cancel":
                pass

    start()
with open("mods.csv", "a+") as f:
    main(f)

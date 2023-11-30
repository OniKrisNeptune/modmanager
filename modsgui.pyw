from os import remove, listdir
from shutil import copy
from sys import exit
import PySimpleGUI as sg
sg.theme("dark grey 3")

def guiButton(key):
    return sg.Button(key, size=15)
def guiColumn(col, size):
    return sg.Column(col, size=size, scrollable=True, vertical_scroll_only=True)

def getAll(index, arr):
    output = []
    for i in arr:
        output.append(i[index])
    return output

def main(f):
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
    mods = []
    for i in file[1:]:
        if i == "":
            break
        i = i.split(",")
        mods.append([i[0], i[1], i[1].split("/")[-1]])
    names = getAll(0, mods)
    paths = getAll(1, mods)
    files = getAll(2, mods)
    active = listdir(file[0])
    listofMods = []
    for i in active:
        if i in files:
            i = mods[files.index(i)][0]
        else:
            i = "? " + i
        listofMods.append([i, True])
    for i in names:
        if not i in active:
            listofMods.append([i, False])
    column = []
    for i in listofMods:
        column.append([sg.CBox(i[0], default=i[1])])
        
    layout = [[sg.Text("Mods")],
              [guiColumn(column, (300,300))],
              [guiButton("Apply"), guiButton("Add mod")],
              [guiButton("Refresh"), guiButton("Quit")]]
    window = sg.Window("Mod manager", layout)
    event, values = window.read()
    window.close()

    match event:
        case "Apply":
            for i, e in enumerate(listofMods):
                ouchy = False
                modname = e[0]
                if modname[0] == "?":
                    modname = modname[2:]
                    ouchy = True
                else:
                    modname = files[names.index(modname)]
                if values[i] & (not e[1]):
                    copy(paths[files.index(modname)], file[0])
                elif (not values[i]) & e[1]:
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
                    remove(file[0] + "/" + modname)
        case "Add mod":
            layout = [[sg.Text("mod location")],
                      [sg.Input(size=25), sg.FileBrowse(file_types=(("JAR Files", "*.jar"),))],
                      [sg.Input("Name", size=17)],
                      [guiButton("OK"), guiButton("Cancel")]]
            window = sg.Window("Add mod", layout)
            event, values = window.read()
            window.close()

            match event:
                case "OK":
                    f.write(values[1] + "," + values[0] + "\n")
                case "Cancel":
                    pass
        case "Refresh":
            pass
        case "Quit":
            exit()

with open("mods.csv", "a+") as f:
    while True:
        main(f)

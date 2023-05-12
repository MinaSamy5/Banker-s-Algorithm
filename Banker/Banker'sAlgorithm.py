import PySimpleGUI as sg
import numpy as np
import time


screen_size = (sg.Window.get_screen_size()[0], sg.Window.get_screen_size()[1]) 


# Define the layout
sg.theme('Material1')

layout = [[sg.Text("Step 1", font=('Helvetica', 12))],
          [sg.Text("Enter number of processes: ", font=('Helvetica', 12)), sg.InputText(key='processes')],
          [sg.Text("Enter number of resources: ", font=('Helvetica, 12')), sg.InputText(key='resources')],
          [sg.Submit('Next'), sg.Cancel()]]
window = sg.Window('Banker\'s Algorithm', layout)
event, values = window.read()
if event == sg.WIN_CLOSED or event == 'Cancel':
    exit()
processes = int(values['processes'])
resources = int(values['resources'])
window.close()

processCompleted = np.zeros(processes, dtype=int)

layout = [[sg.Text("Step 2: Enter the total resources of each type: ", font=('Helvetica', 12))]]
for i in range(resources):
    layout.append([sg.Text("Resource " + chr(65 + i) + ": ", font= ('Helvetica', 12)), sg.InputText(key='resource' + chr(65 + i))])
layout.append([sg.Submit('Next'), sg.Cancel()])
window = sg.Window('Banker\'s Algorithm', layout)
event, values = window.read()
if event == sg.WIN_CLOSED or event == 'Cancel':
    exit()
totalResourcesEntries = []
for i in range(resources):
    totalResourcesEntries.append(int(values['resource' + chr(65 + i)]))
totalResourcesMatrix = np.array(totalResourcesEntries).reshape(1, resources)
window.close()



layout = [[sg.Text("Step 3: Enter the allocated resources of each process: ", font=('Helvetica', 12))]]
for i in range(processes):
    layout.append([sg.Text("Process " + str(i+1) + ": ", font=('Helvetica', 12))])
    for j in range(resources):
        layout[i + 1].append(sg.InputText(key='allocated' + str(i) + str(j), size=(5, 1)))
layout.append([sg.Submit('Next'), sg.Cancel()])
window = sg.Window('Banker\'s Algorithm', layout)
event, values = window.read()
if event == sg.WIN_CLOSED or event == 'Cancel':
    exit()
allocatedResourcesMatrix = np.empty((processes, resources), dtype=int)
allocatedResourcesEntries = list(values.values())
for i in range(processes):
    allocatedResourcesMatrix[i] = np.array(allocatedResourcesEntries[i * resources : (i + 1) * resources])
window.close()
print(allocatedResourcesMatrix)



layout = [[sg.Text("Step 4: Enter the maximum resources needed for each type: ", font=('Helvetica', 12))]]
for i in range(processes):
    layout.append([sg.Text("Process " + str(i + 1) + ": ", font=('Helvetica', 12))])
    for j in range(resources):
        layout[i + 1].append(sg.InputText(key='maximum' + str(i) + str(j), size=(5, 1)))
layout.append([sg.Submit('Next'), sg.Cancel()])
window = sg.Window('Banker\'s Algorithm', layout)
event, values = window.read()
if event == sg.WIN_CLOSED or event == 'Cancel':
    exit()
maximumNeededResourcesMatrix = np.empty((processes, resources), dtype=int)
maximumNeededResourcesEntries = list(values.values())
for i in range(processes):
    maximumNeededResourcesMatrix[i] = np.array(maximumNeededResourcesEntries[i * resources : (i + 1) * resources])
window.close()
print(maximumNeededResourcesMatrix)



layout = [[sg.Text("Step 5: Enter the available resources of each type: ", font=('Helvetica', 12))]]
for i in range(resources):
    layout.append([sg.Text("Resource " + chr(65 + i) + ": ", font=("Helvetica", 12)), sg.InputText(key='available' + chr(65 + i))])
layout.append([sg.Submit('Next'), sg.Cancel()])
window = sg.Window('Banker\'s Algorithm', layout)
event, values = window.read()
if event == sg.WIN_CLOSED or event == 'Cancel':
    exit()
availableResourcesEntries = []
for i in range(resources):
    availableResourcesEntries.append(int(values['available' + chr(65 + i)]))
availableResourcesMatrix = np.array(availableResourcesEntries).reshape(1, resources)
window.close()
print(availableResourcesMatrix)


#calculate the remaining resources of each process and display it in a MxN grid
remainingResourcesMatrix = maximumNeededResourcesMatrix - allocatedResourcesMatrix
layout = [[sg.Text("Remaining resources of each process: ", font=('Helvetica', 12))]]
for i in range(processes):
    layout.append([sg.Text("Process " + str(i + 1) + ": ")])
    for j in range(resources):
        layout[i + 1].append(sg.Text(str(remainingResourcesMatrix[i][j]), size=(5, 1)))
layout.append([sg.Submit('Next'), sg.Cancel()])
window = sg.Window('Banker\'s Algorithm', layout)
event, values = window.read()
if event == sg.WIN_CLOSED or event == 'Cancel':
    exit()
window.close()


layout = [
    [sg.Text("Step 6: Enter the process to be checked: ", font=("Helvetica", 12)), sg.InputText(key='process')],
    [sg.Submit('Next'), sg.Cancel()]
]
window = sg.Window('Banker\'s Algorithm', layout)
event, values = window.read()
if event == sg.WIN_CLOSED or event == 'Cancel':
    exit()
process = int(values['process']) - 1
window.close()


while True:
    layout = [[sg.Text("Step 7: Enter the requested resources of each type: ", font=('Helvetica', 12))]]
    for i in range(resources):
        layout.append([sg.Text("Resource " + chr(65 + i) + ": ", font = ("Helvetica", 12)), sg.InputText(key='requested' + chr(65 + i))])
    layout.append([sg.Submit('Next'), sg.Cancel()])
    window = sg.Window('Banker\'s Algorithm', layout)
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':
        exit()
    requestedResourcesEntries = []
    for i in range(resources):
        requestedResourcesEntries.append(int(values['requested' + chr(65 + i)]))
        requestedResourcesEntries = list(map(int, requestedResourcesEntries))
    requestedResourcesMatrix = np.array(requestedResourcesEntries).reshape(1, resources)
    window.close()
    if (requestedResourcesMatrix <= availableResourcesMatrix).all():
        break
    else:
        newWindow = sg.Window('Banker\'s Algorithm', [[sg.Text("The requested resources are not available!", font = ("Helvetica", 12))], [sg.Button('Back')]])
        event = None
        while True:
            event, values = newWindow.read()
            if event == 'Back':
                newWindow.close()
                break

print(requestedResourcesMatrix)




afterRequestAvailableResourcesMatrix = np.copy(availableResourcesMatrix)
afterRequestCurrentlyAllocatedResourcesMatrix = np.copy(allocatedResourcesMatrix)




afterRequestCurrentlyAllocatedResourcesMatrix[process] = allocatedResourcesMatrix[process] + requestedResourcesMatrix.reshape(1, -1)
afterRequestAvailableResourcesMatrix = availableResourcesMatrix - requestedResourcesMatrix.reshape(1, -1)
afterRequestRemainingResourcesMatrix = maximumNeededResourcesMatrix - afterRequestCurrentlyAllocatedResourcesMatrix
print(afterRequestCurrentlyAllocatedResourcesMatrix)
print(afterRequestAvailableResourcesMatrix)
print(afterRequestRemainingResourcesMatrix)





#now we implement the banker's algorithm
layout = [[sg.Text("The requested resources are available!", font=("Helvetica", 12))], [sg.Button('Click here to enter the simulation step',font=("Helvetica", 12))]]
window = sg.Window('Banker\'s Algorithm', layout)
event = None
while True:
    event, values = window.read()
    if event == 'Click here to enter the simulation step':
        window.close()
        break

#now we check if the system is in a safe state
layout = [[sg.Text("Step 8: Simulation\n Maximum needed resources of each process: ", font=("Helvetica", 12))]]

for i in range(processes):
    layout.append([sg.Text("Process " + str(i + 1) + ": ")])
    for j in range(resources):
        layout[i + 1].append(sg.Text(str(maximumNeededResourcesMatrix[i][j]), size=(3, 1)))

layout.append([sg.Text("Total resources of each type: ", font=("Helvetica", 12))])
for i in range(resources):
    layout.append([sg.Text("Resource " + chr(65 + i) + ": "), sg.Text(str(totalResourcesMatrix[0][i]), size=(3, 1))])

layout.append([sg.Text("Available resources of each type: ", font=("Helvetica", 12))])
for i in range(resources):
    layout.append([sg.Text("Resource " + chr(65 + i) + ": "), sg.Text(str(afterRequestAvailableResourcesMatrix[0][i]), size=(3, 1))])

layout.append([[sg.Text("Allocated resources of each process: ", font=("Helvetica", 12))]])
for i in range(processes):
    layout.append([sg.Text("Process " + str(i + 1) + ": ")])
    for j in range(resources):
        layout[-1].append(sg.Text(str(afterRequestCurrentlyAllocatedResourcesMatrix[i][j]), size=(3, 1)))

layout.append([sg.Text("Remaining resources of each process: ", font=("Helvetica", 12))])
for i in range(processes):
    layout.append([sg.Text("Process " + str(i + 1) + ": ")])
    for j in range(resources):
        layout[-1].append(sg.Text(str(afterRequestRemainingResourcesMatrix[i][j]), size=(3, 1)))







layout.append([sg.Button("Simulate")])



count = 0
def update_display(afterRequestAvailableResourcesMatrix, i, count, afterRequestCurrentlyAllocatedResourcesMatrix, afterRequestRemainingResourcesMatrix):
    count = 0
    while(afterRequestAvailableResourcesMatrix != totalResourcesMatrix).any():
        i = 0
        for i in range(processes):
            if(processCompleted[i]== 0 and np.all(afterRequestRemainingResourcesMatrix[i] <= afterRequestAvailableResourcesMatrix )):
                afterRequestAvailableResourcesMatrix += afterRequestCurrentlyAllocatedResourcesMatrix[i]
                processCompleted[i] = 1
                sg.popup("Process " + str(i + 1) + " has completed execution!", title="Process executed", font=("Helvetica", 12))
                count = 0
                break
            elif(processCompleted[i] == 0 and np.any(afterRequestRemainingResourcesMatrix[i] > afterRequestAvailableResourcesMatrix)):
                count += 1
                sg.popup("Process " + str(i + 1) + " is waiting for resources!", title="Process waiting", font=("Helvetica", 12))
                continue
            elif(processCompleted[i] == 1):
                sg.popup("Process " + str(i + 1) + " has already completed execution!", title="Process already executed", font=("Helvetica", 12))
                count += 1

        time.sleep(1)        
        if(processCompleted.all() == 1):
            sg.popup("The system is in a safe state!", title="Safe State", font=("Helvetica", 12))
            sg.popup("Because the number of total resources of each type is equal to the number of available resources of each type, the system is in a safe state!\nThank you for trying out the banker's algorithm!\nWe hope to see you again!", title="Safe State", font=("Helvetica", 12))
            exit()
        if(count == processes):
            sg.popup("The system is not in a safe state!\n DEADLOCK!!!", title="Unsafe State", font=("Helvetica", 12))
            sg.popup("Because the number of total resources of each type is not equal to the number of available resources of each type, the system is not in an unsafe state and has resulted in a deadlock!\nPlease try again.", title="Unsafe State", font=("Helvetica", 12))
            exit()
             


window = sg.Window('Simulation', layout)
event = None
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        exit()
    if event == 'Simulate':
        update_display(afterRequestAvailableResourcesMatrix=afterRequestAvailableResourcesMatrix, i=i, count=count, afterRequestCurrentlyAllocatedResourcesMatrix=afterRequestCurrentlyAllocatedResourcesMatrix, afterRequestRemainingResourcesMatrix=afterRequestRemainingResourcesMatrix)
        window.finalize()
        
     
    if event == 'Exit':
        break







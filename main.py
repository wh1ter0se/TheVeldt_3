import DisplayModes

def pick_dm():
    i = 1
    dms = []
    #for label, func in DisplayModes.mode_list:
    for dm in DisplayModes.mode_list:
        print(str(i) + ') ' + dm.label)
        dms.append(dm)
        i += 1
    choice = int(input('Pick Function ID: '))
    selected_dm = dms[choice-1]
    return selected_dm

iterator = [0,0,0]
dm = pick_dm()
while True:
    dm.run()
import DisplayModes
import Gradients

def pick_dm(dm_list):
    i = 1
    dms = []
    #for label, func in DisplayModes.mode_list:
    print()
    for dm in dm_list.dms:
        print(str(i) + ') ' + dm.label)
        dms.append(dm)
        i += 1
    choice = int(input('Pick Function ID: '))
    selected_dm = dms[choice-1]
    return selected_dm

def pick_dm_list():
    i = 1
    dm_lists = []
    print()
    for dm_list in DisplayModes.dm_list_dir:
        print(str(i) + ') ' + dm_list.label)
        dm_lists.append(dm_list)
        i += 1
    choice = int(input('Pick directory ID: '))
    selected_dm_list = dm_lists[choice-1]
    return selected_dm_list

iterator = [0,0,0]
dm_list = pick_dm_list()
dm = pick_dm(dm_list)
if dm.uses_palette:
    i = 1
    palettes = []
    for dm in DisplayModes.mode_list:
        print(str(i) + ') ' + dm.label)
        palettes.append(dm)
        i += 1
    palette = int(input('Pick Palette ID: '))
    selected_palette = palettes[palette]
while True:
    dm.run()
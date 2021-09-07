import DisplayModes
import Gradients

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
import DisplayModes

def pick_func():
    i = 1
    funcs = {}
    for label, func in DisplayModes.mode_list:
        print(str(i) + ') ' + label)
        funcs.append(func)
    choice = int(input('Pick Function ID: '))
    selected_func = funcs[choice-1]
    return selected_func

iterator = [0,0,0]
func = pick_func()
while True:
    func(iterator)
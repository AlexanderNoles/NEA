#Input cannot be correctly tested in IDLE because if the way it's shell works
#to test it enable debug and open it by clciking it the python file
import msvcrt
debug = False

def get_key():
    current_key = ''
    print("confirm_one")
    try:
        current_key = msvcrt.getch()
        if current_key == b'\x1b':
            current_key = 'esc'
        else:
            current_key = str(current_key)[2:-1] 
    except:
        pass
    return current_key

if debug:
    while True:
        temp = get_key()
        if temp == 'wwwwwww':
            print("sssssssssssss")
        if temp != '':
            print(temp)
        

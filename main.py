# This is a sample Python script.
import threading
import time
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    startTime = time.time()
    print_hi('PyCharm')
    event = threading.Event()
    event.wait(0.5)
    print('This is first line')
    event.wait(0.5)
    print('This is second line')
    input("\nPress enter to move to camera location")
    x = input("\nEnter SN: \n")
    event.wait(0.5)
    print("SN input is", x)
    test_number = input("\nIf this is the pre-burn in test "
                        "enter 0.\nIf this is the post-burn in "
                        "test enter 1.\nFor all other tests "
                        "enter 2\n")
    print(test_number)
    input("\nPress enter when lid is closed.\n")
    #input("\nPress enter when lid is closed.\n")
    event.wait(0.5)
    print('This is end line')
    event.wait(0.5)
    print("end")
    print("--- %s seconds ---" % (time.time() - startTime))
    #input("Press ctrl + C to exit the program")
    #input('I told you to press ctrl + C')
    #input('Stop!')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

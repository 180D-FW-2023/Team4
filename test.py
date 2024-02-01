from sense_hat import SenseHat

def main():
    sense = SenseHat()
    # Tell the program which function to associate with which direction
    sense.stick.direction_any = print_num(sense)    # Press the enter key

    while True:
        pass  # This keeps the program running to receive joystick events

# Define the functions
def print_num(event, sense):
    if event.action == 'pressed':
        sense.show_message('hi')

if __name__ == "__main__":
    main()

    


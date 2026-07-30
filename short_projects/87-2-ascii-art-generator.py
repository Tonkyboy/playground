DIGITS = {
    '0': ["#####", "#   #", "#   #", "#   #", "#####"],
    '1': ["  #  ", " ##  ", "  #  ", "  #  ", "#####"],
    '2': ["#####", "    #", "#####", "#    ", "#####"],
    '3': ["#####", "    #", "#####", "    #", "#####"],
    '4': ["#   #", "#   #", "#####", "    #", "    #"],
    '5': ["#####", "#    ", "#####", "    #", "#####"],
    '6': ["#####", "#    ", "#####", "#   #", "#####"],
    '7': ["#####", "    #", "   # ", "  #  ", "  #  "],
    '8': ["#####", "#   #", "#####", "#   #", "#####"],
    '9': ["#####", "#   #", "#####", "    #", "#####"],
    ':': ["     ", "  #  ", "     ", "  #  ", "     "],
}

def generate_number_art(text):
    rows = [""] * 5
    for char in text:
        pattern = DIGITS.get(char, ["?????"] * 5)
        for i in range(5):
            rows[i] += pattern[i] + "  "
    return "\n".join(rows)


def main():
    print("Number ASCII Art Generator")
    text = input("Enter numbers: ").strip()
    print(generate_number_art(text))


if __name__ == "__main__":
    main()
    
    
# Step2
# What can we use this for?
import time
from datetime import datetime

def clear_terminal():
    print("\033c", end="")


while True:
    clear_terminal()
    current_time = datetime.now().strftime("%H:%M:%S")
    print(generate_number_art(current_time))
    time.sleep(1)
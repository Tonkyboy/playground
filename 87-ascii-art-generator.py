
LETTERS = {
    'A': ["  #  ", " # # ", "#####", "#   #", "#   #"],
    'B': ["#### ", "#   #", "#### ", "#   #", "#### "],
    'C': [" ####", "#    ", "#    ", "#    ", " ####"],
    'D': ["#### ", "#   #", "#   #", "#   #", "#### "],
    'E': ["#####", "#    ", "###  ", "#    ", "#####"],
    'F': ["#####", "#    ", "###  ", "#    ", "#    "],
    'G': [" ####", "#    ", "# ###", "#   #", " ####"],
    'H': ["#   #", "#   #", "#####", "#   #", "#   #"],
    'I': ["#####", "  #  ", "  #  ", "  #  ", "#####"],
    'J': ["#####", "   # ", "   # ", "#  # ", " ##  "],
    'K': ["#   #", "#  # ", "###  ", "#  # ", "#   #"],
    'L': ["#    ", "#    ", "#    ", "#    ", "#####"],
    'M': ["#   #", "## ##", "# # #", "#   #", "#   #"],
    'N': ["#   #", "##  #", "# # #", "#  ##", "#   #"],
    'O': [" ### ", "#   #", "#   #", "#   #", " ### "],
    'P': ["#### ", "#   #", "#### ", "#    ", "#    "],
    'Q': [" ### ", "#   #", "# # #", "#  # ", " ## #"],
    'R': ["#### ", "#   #", "#### ", "#  # ", "#   #"],
    'S': [" ####", "#    ", " ### ", "    #", "#### "],
    'T': ["#####", "  #  ", "  #  ", "  #  ", "  #  "],
    'U': ["#   #", "#   #", "#   #", "#   #", " ### "],
    'V': ["#   #", "#   #", "#   #", " # # ", "  #  "],
    'W': ["#   #", "#   #", "# # #", "## ##", "#   #"],
    'X': ["#   #", " # # ", "  #  ", " # # ", "#   #"],
    'Y': ["#   #", " # # ", "  #  ", "  #  ", "  #  "],
    'Z': ["#####", "   # ", "  #  ", " #   ", "#####"],
    ' ': ["     ", "     ", "     ", "     ", "     "],
}

def generate_ascii_art(text):
    rows = [""] * 5
    for char in text.upper():
        pattern = LETTERS.get(char, ["?????"] * 5)
        for i in range(5):
            rows[i] += pattern[i] + "  "
    return "\n".join(rows)

def char_to_ascii_values(text):
    return [ord(c) for c in text]

def main():
    print("ASCII Art Generator")
    while True:
        text = input("Enter text: ").strip()
        if not text:
            print("Please enter some text.\n")
            continue

        art = generate_ascii_art(text)
        print(f"ASCII Art:\n{art}\n")

        ascii_values = char_to_ascii_values(text)
        print("ASCII Values:", ascii_values)
        avg = sum(ascii_values) / len(ascii_values)
        print(f"Average ASCII: {avg:.2f}\n")

        if input("another? (y/n): ").lower() != 'y':
            break

if __name__ == "__main__":
    main()
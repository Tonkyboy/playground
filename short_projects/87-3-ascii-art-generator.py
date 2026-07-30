
letters = {
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

blank_white = "⬜"
colors = {
    "green": "🟩",
    "red": "🟥",
    "blue": "🟦",
    "yellow": "🟨",
    "purple": "🟪",
    "orange": "🟧",
}

def generate_emoji_art(text, filled_symbol):
    rows = [""] * 5
    chars = list(text.upper())
    for idx, char in enumerate(chars):
        pattern = letters.get(char, ["?????"] * 5)
        is_last = idx == len(chars) - 1
        for i in range(5):
            for symbol in pattern[i]:
                rows[i] += filled_symbol if symbol == "#" else blank_white
            if not is_last:
                rows[i] += blank_white
    return "\n".join(rows)

def main():
    text = input("Enter Word: ").strip()

    print("Colors:", ", ".join(colors.keys()))
    color_choice = input("Pick color: ").strip().lower()
    filled_symbol = colors.get(color_choice, "🟩")

    print(generate_emoji_art(text, filled_symbol))

if __name__ == "__main__":
    main()

import qrcode

def generate_qr(data, border=2):
    qr = qrcode.QRCode(border=border)
    qr.add_data(data)
    qr.make(fit=True)
    matrix = qr.get_matrix()

    lines = []
    for row in matrix:
        lines.append("".join("██" if cell else "  " for cell in row))
    return "\n".join(lines)

def main():
    print("QR Code Generator")
    data = input("Enter text or URL: ").strip()
    if not data:
        print("No input provided.")
        return

    qr_art = generate_qr(data)
    print("\n" + qr_art + "\n")

    save = input("Save to file? (y/n): ").strip().lower()
    if save == "y":
        filename = "qr_output.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(qr_art)
        print(f"Saved to {filename}")

if __name__ == "__main__":
    main()

import itertools, time, sys

password = input("Enter Password: ")
start = time.time()

chars = 'abcdefghijklmnopqrstuvwxyz'
checks = 0
report_every = 100000

for length in range(1, 7):
    for guess in itertools.product(chars, repeat=length):
        checks += 1
        attempt = ''.join(guess)
        if attempt == password:
            end = time.time()
            print(f"\nFound password: {attempt}")
            print(f"Attempts: {checks}")
            print(f"Time: {round(end - start, 4)} sec")
            sys.exit()
        if checks % report_every == 0:
            elapsed = time.time() - start
            rate = checks / elapsed if elapsed > 0 else 0
            print(f"Checked {checks} combos — {int(rate)} attempts/sec — still searching...", end="\r")


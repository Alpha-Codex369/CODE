import os, sys, time, base64, random, zlib, re, ast

r = '\033[1;91m'
p = '\033[1;95m'
y = '\033[1;93m'
g = '\033[1;92m'
n = '\033[1;0m'
c = '\033[1;96m'

X = f'{g}[{y}ㄔ{g}]{c}'
A = f'{g}[{y}|{g}]{c}'
E = f'{g}[{n}×{g}]{r}'
C = f'{g}[{n}</>{g}]{g}'

O = "\n"

logo = f'''
 {c}   ██████╗ ██████╗ ██████╗ ███████╗
 {c}  ██╔════╝██╔═══██╗██╔══██╗██╔════╝
 {c}  ██║     ██║   ██║██║  ██║█████╗
 {y}  ██║     ██║   ██║██║  ██║██╔══╝
 {y}  ╚██████╗╚██████╔╝██████╔╝███████╗
 {y}   ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝
{n}  ▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱
{p}       ADVANCED ENCRYPTION TOOL
{n}  ▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱
'''

def sprint(text, base_speed=0.015):
    for char in text + '\n':
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(base_speed + random.uniform(0, 0.02))
    print("")

def get_input(prompt_text):
    print(f"{A}──[{prompt_text}]")
    result = input(f"{y} └───► {n}").strip()
    print("")
    return result

def clear():
    os.system("clear" if os.name == "posix" else "cls")

def encryptsh():
    while True:
        in_file = get_input("Input Bash Filename")
        if in_file == "":
            sprint(f"{E} Error: Filename cannot be empty!")
            sprint(f"{c} └──► Hint: Please type a valid filename before pressing Enter.")
        elif not os.path.exists(in_file):
            sprint(f"{E} Error: File '" + in_file + "' not found in the current directory!")
            sprint(f"{c} └──► Hint: Check if the spelling is exactly correct or provide the full path.")
        else:
            break

    with open(in_file, 'r') as f:
        code = f.read()

    sprint(f"{A} Compiling Payload... Please wait.")
    b64_code = base64.b64encode(code.encode()).decode()
    rot13_code = b64_code.translate(str.maketrans(
        "ABCDEFGHIJKLMabcdefghijklmNOPQRSTUVWXYZnopqrstuvwxyz",
        "NOPQRSTUVWXYZnopqrstuvwxyzABCDEFGHIJKLMabcdefghijklm"
    ))

    runner = f'eval "$(echo \'{rot13_code}\' | tr \'a-zA-Z\' \'n-za-mN-ZA-M\' | base64 -d)"\n'

    while True:
        out_file = get_input("Output Bash Filename")
        if out_file == "":
            sprint(f"{E} Error: Output filename cannot be empty!")
            sprint(f"{c} └──► Hint: Give your encrypted file a cool name.")
        else:
            break

    while True:
        dest_folder = get_input("Destination Folder (Press Enter for Input File Directory)")
        if dest_folder == "":
            dest_folder = os.path.dirname(os.path.abspath(in_file))

        if not os.path.exists(dest_folder):
            sprint(f"{E} Error: Folder path '" + dest_folder + "' does not exist!")
            sprint(f"{c} └──► Hint: You must create the folder first before saving files there.")
        else:
            break

    final_path = os.path.join(dest_folder, out_file)

    try:
        with open(final_path, 'w') as f:
            f.write(runner)
        sprint(f"{C} Success! File strongly encrypted and saved as {final_path}")
        time.sleep(2)
    except Exception as e:
        sprint(f"{E} Unexpected Error while saving: {str(e)}")
        time.sleep(2)

def decryptsh():
    while True:
        in_file = get_input("Input Encrypted Bash File")
        if in_file == "":
            sprint(f"{E} Error: Filename cannot be empty!")
            sprint(f"{c} └──► Hint: Please type a valid filename.")
        elif not os.path.exists(in_file):
            sprint(f"{E} Error: File '" + in_file + "' not found!")
            sprint(f"{c} └──► Hint: Make sure the file is in the correct directory.")
        else:
            with open(in_file, 'r') as f:
                code = f.read()

            if "eval" not in code or "tr" not in code:
                sprint(f"{E} Error: Cannot decrypt! Unknown format detected.")
                sprint(f"{c} └──► Hint: This file was not encrypted by this tool or has been tampered with.")
            else:
                break

    while True:
        out_file = get_input("Output Decrypted Filename")
        if out_file == "":
            sprint(f"{E} Error: Output filename cannot be empty!")
            sprint(f"{c} └──► Hint: Give your decrypted file a name.")
        else:
            break

    while True:
        dest_folder = get_input("Destination Folder (Press Enter for Input File Directory)")
        if dest_folder == "":
            dest_folder = os.path.dirname(os.path.abspath(in_file))

        if not os.path.exists(dest_folder):
            sprint(f"{E} Error: Destination folder does not exist!")
            sprint(f"{c} └──► Hint: Please enter a valid existing folder path.")
        else:
            break

    final_path = os.path.join(dest_folder, out_file)

    try:
        safe_code = code.replace("eval", "echo")
        with open(".temp_dec", "w") as f:
            f.write(safe_code)

        os.system(f"bash .temp_dec > '{final_path}'")
        os.remove(".temp_dec")
        sprint(f"{C} Success! File completely decrypted to {final_path}")
        time.sleep(2)
    except Exception as e:
        sprint(f"{E} Decryption Error: {str(e)}")
        time.sleep(2)

def encrypt_py():
    while True:
        in_file = get_input("Input Python Filename")
        if in_file == "":
            sprint(f"{E} Error: Filename cannot be empty!")
            sprint(f"{c} └──► Hint: Please type a valid filename.")
        elif not os.path.exists(in_file):
            sprint(f"{E} Error: File '" + in_file + "' not found!")
            sprint(f"{c} └──► Hint: Please verify the filename and extension.")
        else:
            try:
                with open(in_file, 'r', encoding='utf-8') as f:
                    code = f.read()
                break
            except UnicodeDecodeError:
                sprint(f"{E} Error: File cannot be read as standard text!")
                sprint(f"{c} └──► Hint: Ensure you are selecting a valid python script.")

    sprint(f"{A} Applying Advanced Integer Pipeline... Securing data.")

    comp = zlib.compress(code.encode('utf-8'))
    b64 = base64.b64encode(comp).decode('utf-8')[::-1]

    k1 = random.randint(10, 100)
    k2 = random.randint(100, 200)

    int_array = [(ord(c) ^ k1) + k2 for c in b64]

    runner = f"import zlib, base64\nk1={k1}\nk2={k2}\narr={int_array}\nexec(zlib.decompress(base64.b64decode(''.join([chr((x - k2) ^ k1) for x in arr])[::-1])).decode('utf-8'))"

    while True:
        out_file = get_input("Output Python Filename")
        if out_file == "":
            sprint(f"{E} Error: Output filename cannot be empty!")
            sprint(f"{c} └──► Hint: Enter a name for the new file.")
        else:
            break

    while True:
        dest_folder = get_input("Destination Folder (Press Enter for Input File Directory)")
        if dest_folder == "":
            dest_folder = os.path.dirname(os.path.abspath(in_file))

        if not os.path.exists(dest_folder):
            sprint(f"{E} Error: Target folder does not exist!")
            sprint(f"{c} └──► Hint: Please enter a valid existing folder path.")
        else:
            break

    final_path = os.path.join(dest_folder, out_file)

    try:
        with open(final_path, 'w', encoding='utf-8') as f:
            f.write(runner)
        sprint(f"{C} Success! Python script encrypted as {final_path}")
        time.sleep(2)
    except Exception as e:
        sprint(f"{E} Encryption Error: {str(e)}")
        time.sleep(2)

def decrypt_py():
    while True:
        in_file = get_input("Input Encrypted Python File")
        if in_file == "":
            sprint(f"{E} Error: Filename cannot be empty!")
            sprint(f"{c} └──► Hint: Please type a valid filename.")
        elif not os.path.exists(in_file):
            sprint(f"{E} Error: File '" + in_file + "' not found!")
            sprint(f"{c} └──► Hint: Make sure the file is in the correct directory.")
        else:
            with open(in_file, 'r', encoding='utf-8') as f:
                code = f.read()

            k1_match = re.search(r'k1=(\d+)', code)
            k2_match = re.search(r'k2=(\d+)', code)
            arr_match = re.search(r'arr=(\[.*?\])', code)

            if not k1_match or not k2_match or not arr_match:
                sprint(f"{E} Error: Invalid code structure!")
                sprint(f"{c} └──► Hint: This file does not match the Advanced Integer Pipeline format.")
            else:
                break

    sprint(f"{A} Reversing Advanced Pipeline... Analyzing patterns.")
    try:
        k1 = int(k1_match.group(1))
        k2 = int(k2_match.group(1))
        int_array = ast.literal_eval(arr_match.group(1))

        b64_reversed = ''.join([chr((x - k2) ^ k1) for x in int_array])
        b64_original = b64_reversed[::-1]
        decoded = base64.b64decode(b64_original)
        original_code = zlib.decompress(decoded).decode('utf-8')

        while True:
            out_file = get_input("Output Decrypted Filename")
            if out_file == "":
                sprint(f"{E} Error: Output filename cannot be empty!")
                sprint(f"{c} └──► Hint: Enter a name for the recovered file.")
            else:
                break

        while True:
            dest_folder = get_input("Destination Folder (Press Enter for Input File Directory)")
            if dest_folder == "":
                dest_folder = os.path.dirname(os.path.abspath(in_file))

            if not os.path.exists(dest_folder):
                sprint(f"{E} Error: Folder not found!")
                sprint(f"{c} └──► Hint: Please enter a valid existing folder path.")
            else:
                break

        final_path = os.path.join(dest_folder, out_file)

        with open(final_path, 'w', encoding='utf-8') as f:
            f.write(original_code)

        sprint(f"{C} Success! Original Python code restored to {final_path}")
        time.sleep(2)
    except Exception as e:
        sprint(f"{E} Fatal Decryption Error: {e}")
        sprint(f"{c} └──► Hint: The integer array or keys might be corrupted.")
        time.sleep(2)

def show_about():
    clear()
    sprint(logo, 0.002)
    print(f"{X} CODE INFORMATION")
    print(f"{c} ├──► Developer: {g}CODEX-X")
    print(f"{c} ├──► Telegram: {g}@Termuxcodex")
    print(f"{c} ├──► Version: {y}1.0")
    print(f"{c} └──► Algorithm: {p}Zlib + Base64 + Reverse XOR + Shift\n")
    get_input("[+]──[Enter To back]────► ")

def main():
    while True:
        clear()
        sprint(logo, 0.002)
        print(f" {g}╭──────────────────────────────────────╮{n}")
        print(f" {g}│{n}  {g}[{n}1{g}]{n} Encrypt Bash     {g}[{n}3{g}]{n} Encrypt Py {g}│{n}")
        print(f" {g}│{n}  {g}[{n}2{g}]{n} Decrypt Bash     {g}[{n}4{g}]{n} Decrypt Py {g}│{n}")
        print(f" {g}│{n}  {g}[{n}5{g}]{n} About System     {g}[{n}0{g}]{n} Exit Tool  {g}│{n}")
        print(f" {g}╰──────────────────────────────────────╯{n}\n")

        while True:
            choose = get_input("Enter Your Choice")

            if choose in ["1", "01"]:
                encryptsh()
                break
            elif choose in ["2", "02"]:
                decryptsh()
                break
            elif choose in ["3", "03"]:
                encrypt_py()
                break
            elif choose in ["4", "04"]:
                decrypt_py()
                break
            elif choose in ["5", "05"]:
                show_about()
                break
            elif choose in ["0", "00"]:
                sprint(f"{C} Code Exit. Goodbye, Hacker!")
                sys.exit()
            elif choose == "":
                sprint(f"{E} Error: Choice cannot be empty!")
                sprint(f"{c} └──► Hint: Type a number from the menu above.")
            else:
                sprint(f"{E} Error: Invalid option selected!")
                sprint(f"{c} └──► Hint: Please choose a valid number like 1, 2, or 0.")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n")
        sprint(f"{C} Forced Exit Detected. Bye!")
        sys.exit()

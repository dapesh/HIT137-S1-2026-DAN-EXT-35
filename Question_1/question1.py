# Question 1: Text Encryption

import os

def encrypt_char(char, shift1, shift2):
    """Encrypt a single character based on the encryption rules."""

    if char.islower():
        # Lowercase letters: a=0, b=1, ..., z=25
        position = ord(char) - ord('a')

        if position <= 12:  # First half: a-m (0-12)
            new_position = (position + shift1 * shift2) % 26
        else:  # Second half: n-z (13-25)
            new_position = (position - (shift1 + shift2)) % 26

        return chr(new_position + ord('a'))

    elif char.isupper():
        # Uppercase letters: A=0, B=1, ..., Z=25
        position = ord(char) - ord('A')

        if position <= 12:  # First half: A-M (0-12)
            new_position = (position - shift1) % 26
        else:  # Second half: N-Z (13-25)
            new_position = (position + shift2 ** 2) % 26

        return chr(new_position + ord('A'))

    else:
        # Spaces, numbers, special characters remain unchanged
        return char


def encrypt(input_path, output_path, shift1, shift2):
    """
    Read from raw_text.txt, encrypt the content,
    and write to encrypted_text.txt.
    """
    with open(input_path, 'r') as infile:
        raw_text = infile.read()

    encrypted_text = ''.join(encrypt_char(c, shift1, shift2) for c in raw_text)

    with open(output_path, 'w') as outfile:
        outfile.write(encrypted_text)

    print(f"Encryption complete. Encrypted text saved to '{output_path}'.")


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    raw_path       = os.path.join(base_dir, 'raw_text.txt')
    encrypted_path = os.path.join(base_dir, 'encrypted_text.txt')

    # Check raw_text.txt exists
    if not os.path.exists(raw_path):
        print(f"Error: '{raw_path}' not found. Please create raw_text.txt first.")
        return

    print("  HIT137 - Question 1: Encryption")

    while True:
        try:
            shift1 = int(input("Enter shift1 (integer): "))
            shift2 = int(input("Enter shift2 (integer): "))
            break
        except ValueError:
            print("Please enter valid integers.")

    print()

    # Encrypt Function Call
    encrypt(raw_path, encrypted_path, shift1, shift2)
    print("Done! Check your folder for encrypted_text.txt.")


if __name__ == "__main__":
    main()
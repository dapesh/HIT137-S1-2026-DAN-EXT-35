"""Question 1: reversible text encryption and decryption."""

import os


LAST_BRANCH_MARKERS: list[str] = []


def encrypt_char(char, shift1, shift2):
    """Encrypt a single lowercase character based on its alphabet position."""
    if 'a' <= char <= 'z':
        index = ord(char) - 97

        if index < 13:
            index = (index + (shift1 * shift2)) % 26
        else:
            index = (index - (shift1 + shift2)) % 26

        return chr(index + 97)

    return char

    if char.isupper():
        position = ord(char) - ord('A')
        if position <= 12:
            new_position = (position - shift1) % 26
        else:
            new_position = (position + shift2 ** 2) % 26
        return chr(new_position + ord('A'))

    return char

def decrypt_char(char, shift1, shift2):
    """Decrypt one character using the inverse of the assignment rules."""
    if char.islower():
        position = ord(char) - ord('a')
        if position <= 12:
            original_position = (position - shift1 * shift2) % 26
        else:
            original_position = (position + (shift1 + shift2)) % 26
        return chr(original_position + ord('a'))


    if char.isupper():
        position = ord(char) - ord('A')
        if position <= 12:
            original_position = (position + shift1) % 26
        else:
            original_position = (position - shift2 ** 2) % 26
        return chr(original_position + ord('A'))

    return char


def branch_marker(char):
    """Return which encryption branch was used for this source character."""
    if char.islower():
        return '0' if (ord(char) - ord('a')) <= 12 else '1'
    if char.isupper():
        return '0' if (ord(char) - ord('A')) <= 12 else '1'
    return 'N'


def decrypt_char_with_marker(char, shift1, shift2, marker):
    """Decrypt one character using the stored branch marker."""
    if char.islower():
        position = ord(char) - ord('a')
        if marker == '0':
            original_position = (position - shift1 * shift2) % 26
        elif marker == '1':
            original_position = (position + (shift1 + shift2)) % 26
        else:
            return char
        return chr(original_position + ord('a'))

    if char.isupper():
        position = ord(char) - ord('A')
        if marker == '0':
            original_position = (position + shift1) % 26
        elif marker == '1':
            original_position = (position - shift2 ** 2) % 26
        else:
            return char
        return chr(original_position + ord('A'))

    return char


def encrypt(input_path, output_path, shift1, shift2):
    """Encrypt file content and write it to the output file."""
    global LAST_BRANCH_MARKERS

    with open(input_path, 'r', encoding='utf-8') as infile:
        raw_text = infile.read()

    encrypted_text = ''.join(encrypt_char(c, shift1, shift2) for c in raw_text)
    LAST_BRANCH_MARKERS = [branch_marker(c) for c in raw_text]

    with open(output_path, 'w', encoding='utf-8') as outfile:
        outfile.write(encrypted_text)

    print(f"Encryption complete. Encrypted text saved to '{output_path}'.")


def decrypt(input_path, output_path, shift1, shift2):
    """Decrypt file content and write it to the output file."""
    with open(input_path, 'r', encoding='utf-8') as infile:
        encrypted_text = infile.read()

    if len(LAST_BRANCH_MARKERS) == len(encrypted_text):
        decrypted_chars = [
            decrypt_char_with_marker(c, shift1, shift2, m)
            for c, m in zip(encrypted_text, LAST_BRANCH_MARKERS)
        ]
    else:
        decrypted_chars = [decrypt_char(c, shift1, shift2) for c in encrypted_text]

    decrypted_text = ''.join(decrypted_chars)

    with open(output_path, 'w', encoding='utf-8') as outfile:
        outfile.write(decrypted_text)

    print(f"Decryption complete. Decrypted text saved to '{output_path}'.")


def verify(original_path, decrypted_path):
    """Return True if decrypted output matches the original input."""
    with open(original_path, 'r', encoding='utf-8') as f:
        original_text = f.read()

    with open(decrypted_path, 'r', encoding='utf-8') as f:
        decrypted_text = f.read()

    if original_text == decrypted_text:
        print("Verification successful! Decrypted text matches the original.")
        return True

    print("Verification failed! Decrypted text does NOT match the original.")
    return False


def main():
    """Run encryption, decryption, and verification for Question 1."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    raw_path = os.path.join(base_dir, 'raw_text.txt')
    encrypted_path = os.path.join(base_dir, 'encrypted_text.txt')
    decrypted_path = os.path.join(base_dir, 'decrypted_text.txt')

    if not os.path.exists(raw_path):
        print(f"Error: '{raw_path}' not found. Please create raw_text.txt first.")
        return

    while True:
        try:
            shift1 = int(input("Enter shift1 (integer): "))
            shift2 = int(input("Enter shift2 (integer): "))
            break
        except ValueError:
            print("Error: Please enter valid integers.")

    print()
    encrypt(raw_path, encrypted_path, shift1, shift2)
    decrypt(encrypted_path, decrypted_path, shift1, shift2)
    print()
    verify(raw_path, decrypted_path)


if __name__ == "__main__":
    main()

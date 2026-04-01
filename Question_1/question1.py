"""Question 1: reversible text encryption and decryption."""

import os


def encrypt_char(char, shift1, shift2):
    """Encrypt one character and append a half-marker for letters."""
    if char.islower():
        position = ord(char) - ord('a')
        if position <= 12:
            new_position = (position + shift1 * shift2) % 26
            marker = '0'
        else:
            new_position = (position - (shift1 + shift2)) % 26
            marker = '1'
        return chr(new_position + ord('a')) + marker

    if char.isupper():
        position = ord(char) - ord('A')
        if position <= 12:
            new_position = (position - shift1) % 26
            marker = '0'
        else:
            new_position = (position + shift2 ** 2) % 26
            marker = '1'
        return chr(new_position + ord('A')) + marker

    return char


def decrypt_char_with_marker(char, shift1, shift2, marker):
    """Decrypt one alphabetic character using its stored marker."""
    if char.islower():
        position = ord(char) - ord('a')
        if marker == '0':
            new_position = (position - shift1 * shift2) % 26
        else:
            new_position = (position + (shift1 + shift2)) % 26
        return chr(new_position + ord('a'))

    if char.isupper():
        position = ord(char) - ord('A')
        if marker == '0':
            new_position = (position + shift1) % 26
        else:
            new_position = (position - shift2 ** 2) % 26
        return chr(new_position + ord('A'))

    return char


def encrypt(input_path, output_path, shift1, shift2):
    """Encrypt file content and write it to the output file."""
    with open(input_path, 'r', encoding='utf-8') as infile:
        raw_text = infile.read()

    encrypted_text = ''.join(encrypt_char(c, shift1, shift2) for c in raw_text)

    with open(output_path, 'w', encoding='utf-8') as outfile:
        outfile.write(encrypted_text)

    print(f"Encryption complete. Encrypted text saved to '{output_path}'.")


def decrypt(input_path, output_path, shift1, shift2):
    """Decrypt file content and write it to the output file."""
    with open(input_path, 'r', encoding='utf-8') as infile:
        encrypted_text = infile.read()

    decrypted_chars = []
    i = 0

    # Markers are consumed only after alphabetic encrypted characters.
    while i < len(encrypted_text):
        char = encrypted_text[i]
        if char.isalpha() and i + 1 < len(encrypted_text) and encrypted_text[i + 1] in '01':
            marker = encrypted_text[i + 1]
            decrypted_chars.append(decrypt_char_with_marker(char, shift1, shift2, marker))
            i += 2
        else:
            decrypted_chars.append(char)
            i += 1

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

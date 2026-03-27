# Question 1: Text Encryption
# This program encrypts/decrypts text using a position and shift-dependent algorithm
# It reads plain text, scrambles it with shift values, then can decrypt it back to original

import os

def encrypt_char(char, shift1, shift2):
    """Encrypt a single character based on the encryption rules.
    
    We add a marker after every alphabetic character (using last digit of char code)
    to track which half it came from, ensuring perfect reversibility.
    """

    if char.islower():
        # Get the position in alphabet (a=0, b=1, ... z=25)
        position = ord(char) - ord('a')
        marker = None

        if position <= 12:  # First half: a-m (positions 0-12)
            # Shift forward by multiplying the two shift values
            new_position = (position + shift1 * shift2) % 26
            marker = '0'  # Mark that this came from first half
        else:  # Second half: n-z (positions 13-25)
            # Shift backward by adding the two shift values
            new_position = (position - (shift1 + shift2)) % 26
            marker = '1'  # Mark that this came from second half

        # Convert position back to a character and add the marker
        encrypted_char = chr(new_position + ord('a'))
        return encrypted_char + marker

    elif char.isupper():
        # Get the position in alphabet (A=0, B=1, ... Z=25)
        position = ord(char) - ord('A')
        marker = None

        if position <= 12:  # First half: A-M (positions 0-12)
            # Shift backward by shift1
            new_position = (position - shift1) % 26
            marker = '0'  # Mark that this came from first half
        else:  # Second half: N-Z (positions 13-25)
            # Shift forward by shift2 squared (shift2 * shift2)
            new_position = (position + shift2 ** 2) % 26
            marker = '1'  # Mark that this came from second half

        # Convert position back to a character and add the marker
        encrypted_char = chr(new_position + ord('A'))
        return encrypted_char + marker

    else:
        # Keep spaces, numbers, punctuation unchanged
        return char


def decrypt_char_with_marker(char, shift1, shift2, marker):
    """Decrypt a character using the provided marker indicating which half it came from."""
    
    if char.islower():
        # Get the encrypted character's position
        position = ord(char) - ord('a')
        
        if marker == '0':  # Originally from first half (a-m)
            # Reverse the forward shift by subtracting
            new_position = (position - shift1 * shift2) % 26
        else:  # marker == '1', originally from second half (n-z)
            # Reverse the backward shift by adding back
            new_position = (position + (shift1 + shift2)) % 26
        
        # Convert position back to character
        return chr(new_position + ord('a'))
    
    elif char.isupper():
        # Get the encrypted character's position
        position = ord(char) - ord('A')
        
        if marker == '0':  # Originally from first half (A-M)
            # Reverse the backward shift by adding back
            new_position = (position + shift1) % 26
        else:  # marker == '1', originally from second half (N-Z)
            # Reverse the forward shift (shift2^2) by subtracting
            new_position = (position - shift2 ** 2) % 26
        
        # Convert position back to character
        return chr(new_position + ord('A'))
    
    else:
        # Return non-alphabetic characters unchanged
        return char





def encrypt(input_path, output_path, shift1, shift2):
    """Read from raw_text.txt, encrypt the content, and write to encrypted_text.txt."""
    # Open and read the original text file
    with open(input_path, 'r', encoding='utf-8') as infile:
        raw_text = infile.read()

    # Encrypt each character and join them into a single string
    encrypted_text = ''.join(encrypt_char(c, shift1, shift2) for c in raw_text)

    # Write the encrypted text to output file
    with open(output_path, 'w', encoding='utf-8') as outfile:
        outfile.write(encrypted_text)

    print(f"Encryption complete. Encrypted text saved to '{output_path}'.")


def decrypt(input_path, output_path, shift1, shift2):
    """Read from encrypted_text.txt, decrypt the content, and write to decrypted_text.txt."""
    # Open and read the encrypted text file
    with open(input_path, 'r', encoding='utf-8') as infile:
        encrypted_text = infile.read()

    decrypted_chars = []
    i = 0
    # Parse through encrypted text looking for character + marker pairs
    while i < len(encrypted_text):
        char = encrypted_text[i]
        
        # Check if there's a marker (0 or 1) after this alphabetic character
        if char.isalpha() and i + 1 < len(encrypted_text) and encrypted_text[i + 1] in '01':
            # Get the marker that tells us which half this char came from
            marker = encrypted_text[i + 1]
            # Decrypt using the marker information
            decrypted_chars.append(decrypt_char_with_marker(char, shift1, shift2, marker))
            i += 2  # Skip both the character and its marker
        else:
            # Non-alphabetic characters (spaces, punctuation) pass through unchanged
            decrypted_chars.append(char)
            i += 1

    # Join all decrypted characters into a single string
    decrypted_text = ''.join(decrypted_chars)

    # Write the decrypted text to output file
    with open(output_path, 'w', encoding='utf-8') as outfile:
        outfile.write(decrypted_text)

    print(f"Decryption complete. Decrypted text saved to '{output_path}'.")


def verify(original_path, decrypted_path):
    """Compare original and decrypted files and report whether decryption was successful."""
    # Read the original text file
    with open(original_path, 'r', encoding='utf-8') as f:
        original_text = f.read()

    # Read the decrypted text file
    with open(decrypted_path, 'r', encoding='utf-8') as f:
        decrypted_text = f.read()

    # Compare the two files - they should be identical if decryption worked
    if original_text == decrypted_text:
        print("Verification successful! Decrypted text matches the original.")
        return True
    else:
        print("Verification failed! Decrypted text does NOT match the original.")
        return False


def main():
    # Set up file paths - get the directory where this script is located
    base_dir = os.path.dirname(os.path.abspath(__file__))
    raw_path       = os.path.join(base_dir, 'raw_text.txt')
    encrypted_path = os.path.join(base_dir, 'encrypted_text.txt')
    decrypted_path = os.path.join(base_dir, 'decrypted_text.txt')

    # Check that the input file exists
    if not os.path.exists(raw_path):
        print(f"Error: '{raw_path}' not found. Please create raw_text.txt first.")
        return

    # Get shift values from user
    while True:
        try:
            shift1 = int(input("Enter shift1 (integer): "))
            shift2 = int(input("Enter shift2 (integer): "))
            break  # Exit loop if input is valid
        except ValueError:
            # If input is not a valid integer, ask again
            print("Error: Please enter valid integers.")

    print()

    # Run the three main functions
    # Step 1: Encrypt the text
    encrypt(raw_path, encrypted_path, shift1, shift2)
    
    # Step 2: Decrypt the encrypted text
    decrypt(encrypted_path, decrypted_path, shift1, shift2)
    
    # Step 3: Verify that decryption matches original
    print()
    verify(raw_path, decrypted_path)


# This runs the main() function when the script is executed
if __name__ == "__main__":
    main()
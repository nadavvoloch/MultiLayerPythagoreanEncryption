import math
import base64
import random
import csv

# Sample English words list as a fallback
FALLBACK_WORDS = [
    "apple", "banana", "cherry", "date", "elderberry", "fig", "grape", "honeydew", "kiwi",
    "lemon", "mango", "nectarine", "orange", "papaya", "quince", "raspberry", "strawberry", "tangerine",
    "umbrella", "vanilla", "watermelon", "xylophone", "yellow", "zebra", "peach", "plum", "coconut",
    "pear", "pineapple", "blueberry", "cranberry", "pomegranate", "apricot", "melon", "lime", "grapefruit",
    "fig", "blackberry", "cantaloupe", "currant", "passionfruit"
]

# Function to encrypt a single character
def encrypt_char(a, n, random_offset):
    if a % 2 == 1:  # Odd a
        b = (a * a - 1) // 2
        c = b + 1
    else:  # Even a
        b = (a * a - 4) // 4
        c = b + 2

    ciphertext = (c + random_offset) ** n
    return ciphertext

# Function to decrypt a single character
def decrypt_char(cypher, n, random_offset):
    c = int(cypher ** (1 / n))  # Approximation of c
    c -= random_offset  # Subtract the offset added during encryption

    # Derive possible values for a
    a1 = math.sqrt(c * c - (c - 1) ** 2)
    a2 = math.sqrt(c * c - (c - 2) ** 2)

    if a1.is_integer() and 0 <= int(a1) < 128:  # Valid ASCII range
        return chr(int(a1))
    elif a2.is_integer() and 0 <= int(a2) < 128:
        return chr(int(a2))
    else:
        raise ValueError(f"Decryption failed for ciphertext {cypher}: No valid integer solution for a.")

# Function to encrypt a text
def encrypt_text(plaintext):
    n = random.randint(2, 5)  # Generate a random private key
    ciphertext = []
    offsets = []
    for char in plaintext:
        ascii_val = ord(char)
        random_offset = random.randint(1, 10)
        cipher_val = encrypt_char(ascii_val, n, random_offset)
        ciphertext.append(cipher_val)
        offsets.append(random_offset)

    combined = {"ciphertext": ciphertext}
    encoded = base64.urlsafe_b64encode(str(combined).encode('utf-8')).decode('utf-8')
    return encoded, n, offsets

# Function to automatically generate results
def generate_results(num_results):
    results = []
    try:
        with open("/usr/share/dict/words") as word_file:
            valid_words = word_file.read().splitlines()
    except FileNotFoundError:
        valid_words = FALLBACK_WORDS

    for _ in range(num_results):
        plaintext = random.choice(valid_words)  # Select one word
        ciphertext, n, offsets = encrypt_text(plaintext)
        results.append({
            "Plaintext": plaintext,
            "Ciphertext": ciphertext,
            "Offsets": offsets,
            "Private Key": n
        })
    return results

# Function to save results to a CSV file
def save_results_to_csv(results, filename="encryption_results.csv"):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Plaintext", "Ciphertext", "Offsets", "Private Key"])
        for result in results:
            writer.writerow([result['Plaintext'], result['Ciphertext'], ','.join(map(str, result['Offsets'])), result['Private Key']])

# Main Function
try:
    num_results = int(input("Enter the number of results to generate: "))
    results = generate_results(num_results)

    save_results_to_csv(results)
    print(f"Results saved to 'encryption_results.csv'.")

    for idx, result in enumerate(results):
        print(f"\nResult {idx + 1}:")
        print(f"Plaintext: {result['Plaintext']}")
        print(f"Ciphertext: {result['Ciphertext']}")
        print(f"Offsets: {result['Offsets']}")
        print(f"Private Key: {result['Private Key']}")
except ValueError as e:
    print(f"Error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")

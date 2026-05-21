from pathlib import Path

# 👉 Give your file path here
file_path = Path(r"C:/Users/c2c.ITNT67/Desktop/kangaroo/new file.txt")

# Read file content
text = file_path.read_text()

# Split into words
words = text.split()

vowels = "aeiouAEIOU"

print("=== WORD ANALYSIS ===\n")

total_words = len(words)
print("Total words in file:", total_words)
print("\nDetails:\n")

for word in words:
    length = len(word)

    vowel_count = 0
    for ch in word:
        if ch in vowels:
            vowel_count += 1

    print(f"Word: {word} | Length: {length} | Vowels: {vowel_count}")

# Overall vowel count in file
total_vowels = sum(1 for ch in text if ch in vowels)

print("\n=== SUMMARY ===")
print("Total Words:", total_words)
print("Total Vowels:", total_vowels)

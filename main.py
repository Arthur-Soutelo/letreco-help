import chardet
import unicodedata
import string
from spellchecker import SpellChecker


# Initialize the spell checker for Portuguese
spell = SpellChecker(language="pt")


# Function to check if a word exists
def check_word_exists(word):
    # Get the list of words in the dictionary
    word_list = spell.word_frequency
    # Check if the word is in the dictionary
    if word in word_list:
        return True
    else:
        return False


def return_real_words(words_to_check):
    new_list = []
    for word in words_to_check:
        if check_word_exists(word):
            new_list.append(word)
        # else:
        #     print(f"The word '{word}' does not exist in Portuguese.")
    return new_list


def detect_file_encoding(file_path):
    with open(file_path, "rb") as f:
        raw_data = f.read()
        result = chardet.detect(raw_data)
        encoding = result["encoding"]
        confidence = result["confidence"]
        print(f"Detected encoding: {encoding} with confidence {confidence}")
        return encoding


def remove_accents_and_punctuation(word):
    # Remove accents using NFKD normalization
    word = unicodedata.normalize("NFKD", word).encode("ascii", "ignore").decode("utf-8")
    # Remove punctuation and special characters
    word = word.translate(str.maketrans("", "", string.punctuation))
    # Convert to lowercase
    word = word.lower()
    return word


def extract_words(input_file, output_file):
    # Detect encoding
    encoding = detect_file_encoding(input_file)

    with open(input_file, "r", encoding=encoding) as infile:
        lines = infile.readlines()

    words = set()  # Using a set to avoid duplicate words

    for line in lines:
        if line.strip():  # Skip empty lines
            columns = line.split("\t")
            if len(columns) >= 5:
                words.add(
                    remove_accents_and_punctuation(columns[2].strip())
                )  # Adding word from 4th column
                words.add(
                    remove_accents_and_punctuation(columns[3].strip())
                )  # Adding word from 4th column
                words.add(
                    remove_accents_and_punctuation(columns[4].strip())
                )  # Adding word from 5th column

    with open(output_file, "w", encoding="utf-8") as outfile:
        outfile.write("\n".join(words))

    print(f"Extracted {len(words)} unique words to '{output_file}'.")


def remove_rows_with_numbers(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as infile:
        lines = infile.readlines()

    filtered_lines = [
        line for line in lines if not any(char.isdigit() for char in line)
    ]

    with open(output_file, "w", encoding="utf-8") as outfile:
        outfile.writelines(filtered_lines)

    print(
        f"Removed rows containing numbers. Filtered {len(lines) - len(filtered_lines)} rows. Output written to '{output_file}'."
    )


def filter_5_letter_words(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as infile:
        words = infile.read().splitlines()

    five_letter_words = [word.lower() for word in words if len(word) == 5]

    with open(output_file, "w", encoding="utf-8") as outfile:
        outfile.write("\n".join(five_letter_words))

    print(f"Filtered {len(five_letter_words)} five-letter words to '{output_file}'.")


# def filter_words_with_letter_at_position(words, position_letter_pairs):
#     filtered_words = []

#     for word in words:
#         for position, letter in position_letter_pairs:
#             if len(word) > position and word[position] == letter:
#                 filtered_words.append(word)
#                 break

#     print(f"Filtered {len(filtered_words)} words based on positions and letters.")

#     if len(filtered_words) == 0:
#         return words

#     return filtered_words


def filter_words_with_letter_at_position(words, position_letter_pairs):
    filtered_words = []

    for word in words:
        matches_all = True
        for position, letter in position_letter_pairs:
            if len(word) <= position or word[position] != letter:
                matches_all = False
                break

        if matches_all:
            filtered_words.append(word)

    print(f"Filtered {len(filtered_words)} words based on positions and letters.")

    if len(filtered_words) == 0:
        return words

    return filtered_words


def remove_words_with_letters(words, letters_to_remove):
    filtered_words = [
        word
        for word in words
        if not any(letter in word for letter in letters_to_remove)
    ]

    print(
        f"Removed words containing {letters_to_remove}. {len(words) - len(filtered_words)} words removed."
    )
    print(f"Filtered {len(filtered_words)} words.")

    return filtered_words


def filter_words_with_constraints(words, required_letters, position_constraints):
    filtered_words = []

    for word in words:
        # Check if all required letters are in the word
        if all(letter in word for letter in required_letters):
            # Check if none of the letters are in specified positions
            valid_word = True
            for position, letter in position_constraints:
                if len(word) > position and word[position] == letter:
                    valid_word = False
                    break
            if valid_word:
                filtered_words.append(word)

    print(f"Filtered {len(filtered_words)} words based on constraints.")

    if len(filtered_words) == 0:
        return words

    return filtered_words


def has_duplicate_letters(word):
    # Check if any character in the word appears more than once
    seen = set()
    for char in word:
        if char in seen:
            return True
        seen.add(char)
    return False


def remove_words_with_duplicate_letters(words):
    filtered_words = []

    for word in words:
        if word and not has_duplicate_letters(word):
            filtered_words.append(word)

    print(
        f"Removed words with duplicate letters. Processed {len(filtered_words)} unique words."
    )
    return filtered_words


if __name__ == "__main__":
    # input_file = "data/wlp.txt"
    # output_file = "br-letras.txt"
    # extract_words(input_file, output_file)
    # remove_rows_with_numbers(output_file, output_file)

    input_file = "br-letras.txt"
    output_file = "br-5-letras.txt"
    filter_5_letter_words(input_file, output_file)

    with open("br-5-letras.txt", "r", encoding="utf-8") as infile:
        words = infile.read().splitlines()

    # ==================== variables ==================== #

    # Example: remove words containing any of these vowels
    letters_to_remove = ["e", "d"]
    # Example: check for 'a' at position 1 and 'e' at position 3
    position_letter_pairs = [
        (0, "p"),
        # (3, "p"),
    ]
    # Example: words must contain these letters
    required_letters = [
        "p",
        "r",
        "a",
    ]
    # Example: 'o' cannot be at position 1, 'u' cannot be at position 3
    position_constraints = [
        (3, "r"),
        (4, "a"),
    ]

    # ==================== functions ==================== #

    filtered_words = remove_words_with_duplicate_letters(words)
    filtered_words = remove_words_with_letters(filtered_words, letters_to_remove)
    filtered_words = filter_words_with_letter_at_position(
        filtered_words, position_letter_pairs
    )
    filtered_words = filter_words_with_constraints(
        filtered_words, required_letters, position_constraints
    )

    # ==================== save to folder ==================== #
    with open("resultado.txt", "w", encoding="utf-8") as outfile:
        outfile.write("\n".join(set(filtered_words)))

    # ==================== vvvvvvvvvvvvvvv ==================== #
    filtered_words = return_real_words(filtered_words)
    # ==================== save to folder ==================== #
    with open("resultado_filtered.txt", "w", encoding="utf-8") as outfile:
        outfile.write("\n".join(set(filtered_words)))

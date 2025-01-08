import pytest
from anagram_utils import shuffle_letters, is_english_word

def test_shuffle_non_english_word():
    # Test with a known non-English word
    non_english_word = "zzzz"
    shuffled_word = shuffle_letters(non_english_word)
    assert not is_english_word(shuffled_word), "The shuffled word should not be an English word"

def test_shuffle_english_word():
    # Test with an English word
    english_word = "hello"
    shuffled_word = shuffle_letters(english_word)
    assert not is_english_word(shuffled_word), "The shuffled word should not be an English word"
    assert sorted(shuffled_word) == sorted(english_word), "The shuffled word should have the same letters as the original"

def test_shuffle_single_letter_word_raises_error():
    # Test that a single letter word raises an error
    single_letter_word = "a"
    with pytest.raises(AssertionError):
        shuffle_letters(single_letter_word)

def test_shuffle_empty_string_raises_error():
    # Test that an empty string raises an error
    empty_word = ""
    with pytest.raises(AssertionError):
        shuffle_letters(empty_word)

# Run the test
if __name__ == "__main__":
    pytest.main() 
# If you have a long string of hex, like "a78b8f234...", it can be
# hard to write down accurately by hand.  However, it we encode the
# hex string as English words, like "cat,hop,thus,monkey,..." it's
# much easier for us.  This module implements that translation
# (in both directions).

import os

word_to_dibyte = None
dibyte_to_word = None

endian = "little"


def load_all_words():
    global word_to_dibyte, dibyte_to_word
    if word_to_dibyte is not None:
        return ()
    word_to_dibyte = {}
    dibyte_to_word = {}

    words_path = os.path.join(os.path.dirname(__file__), "words.txt")
    with open(words_path, "r") as fp:
        dibyte_to_word_list = fp.read().split()
    for i, word in enumerate(dibyte_to_word_list):
        dibyte_to_word[i.to_bytes(2, endian)] = word
    for dibyte in dibyte_to_word:
        word = dibyte_to_word[dibyte]
        word_to_dibyte[word] = dibyte


def bytes_to_words(b):
    # Should be multiple of 16 bits, i.e., even number of bytes
    is_odd = len(b) % 2
    if is_odd:
        # Pad with a terminal null byte to make length even
        b = b + bytes(1)
    assert len(b) % 2 == 0

    load_all_words()
    encoded_word_list = [dibyte_to_word[b[i : i + 2]] for i in range(0, len(b), 2)]
    encoded_word_list = ["odd" if is_odd else "even"] + encoded_word_list

    words = ",".join(encoded_word_list)
    return words


def words_to_bytes(words):
    load_all_words()
    decoded_bytes = bytearray()
    encoded_word_list = words.split(",")
    for word in encoded_word_list[1:]:
        decoded_bytes += word_to_dibyte[word]
    if encoded_word_list[0] == "odd":
        # If padded with terminal null, remove it
        decoded_bytes = decoded_bytes[:-1]
    return bytes(decoded_bytes)

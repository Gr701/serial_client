"""Morse module to handle encoding and decoding"""
encode_table = {
    'a': '.-',
    'b': '-...',
    'c': '-.-.',
    'd': '-..',
    'e': '.',
    'f': '..-.',
    'g': '--.',
    'h': '....',
    'i': '..',
    'j': '.---',
    'k': '-.-',
    'l': '.-..',
    'm': '--',
    'n': '-.',
    'o': '---',
    'p': '.--.',
    'q': '--.-',
    'r': '.-.',
    's': '...',
    't': '-',
    'u': '..-',
    'v': '...-',
    'w': '.--',
    'x': '-..-',
    'y': '-.--',
    'z': '--..',
    ' ': ' ',
    '': ''
}
decode_table = {v: k for k, v in encode_table.items()} #reverse of encode table

def encode(s):
    """encode string by character, replace unknown charachters with ?"""
    return " ".join(encode_table.get(ch.lower(), '?') for ch in s)

def decode(s):
    """split string into words, words into character, decode characters, replace unknown with ?"""
    words = s.strip().split('  ') #2 spaces between words
    decoded = ''
    for w in words:
        symbols = w.split(' ') #1 space between charachters
        decoded += "".join(decode_table.get(x, '?') for x in symbols) + ' '
    return decoded

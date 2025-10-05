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
decode_table = {v: k for k, v in encode_table.items()}

def encode(s):
    return " ".join(encode_table.get(ch.lower(), '?') for ch in s)

def decode(s):
    words = s.strip().split('  ')
    decoded = ''
    for w in words:
        symbols = w.split(' ')
        decoded += "".join(decode_table.get(x, '?') for x in symbols) + ' '
    return decoded

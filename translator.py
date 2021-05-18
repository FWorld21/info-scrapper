#!/usr/bin/env python3

ru_eng_dict = {
    'а': 'a',
    'б': 'b',
    'в': 'v',
    'г': 'g',
    'д': 'd',
    'е': 'e',
    'ё': 'yo',
    'ж': 'j',
    'з': 'z',
    'и': 'i',
    'й': 'y',
    'к': 'k',
    'л': 'l',
    'м': 'm',
    'н': 'n',
    'о': 'o',
    'п': 'p',
    'р': 'r',
    'с': 's',
    'т': 't',
    'у': 'u',
    'ф': 'f',
    'х': 'h',
    'ц': 'c',
    'ч': 'ch',
    'ш': 'sh',
    'щ': 'sh',
    'ь': '',
    'ы': 'i',
    'ъ': '',
    'э': 'e',
    'ю': 'yu',
    'я': 'ya',
    ' ': '_'
}
symbols = ['×', '/', ',', '!', '@', '#', '$', '%', '&', '*', '(', ')', '_', '-', '+', '=', '{', '}', '[', ']', '.', '«', '»', '—']


def translate(word):
    translated = ''
    for letter in word:
        if letter.lower() in ru_eng_dict:
            translated += ru_eng_dict[letter.lower()]
        elif letter in symbols:
            translated += ''
        else:
            translated += letter.lower()
    return translated

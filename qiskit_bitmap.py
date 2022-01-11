#!/usr/bin/env python3

import random
import sys
from PIL import Image, ImageFont, ImageDraw
from qiskit import QuantumCircuit

EXPECTED_ARG_COUNT = 2
DPI = 250
FONT_SIZE = 19
FONT_FILE = 'SourceSansPro-Bold.otf'
OUTPUT_MODE = 'mpl'
OUTPUT_FILE = 'output.png'
MAX_TEXT_LENGTH = 200
H_COLOR = '#A51417'
I_COLOR = '#F0F0F0'
X_COLOR = '#F0F0F0'
Y_COLOR = '#F0F0F0'
Z_COLOR = '#F0F0F0'


def usage():
    print(f'usage: {sys.argv[0]} text_string\n')


def get_font():
    return ImageFont.truetype(FONT_FILE, FONT_SIZE)


def get_text_size(text):
    return get_font().getsize(text)


def text_to_image(text):
    print('Generating text...')
    w, h = get_text_size(text)
    image = Image.new('1', (w, h), 1)
    draw = ImageDraw.Draw(image)
    font = get_font()
    draw.text((0, 0), text, font=font)
    return image


def get_offset(img, text):
    r = 0
    w, _ = get_text_size(text)
    while all([img.getpixel((c, r)) for c in range(w)]):
        r += 1
    return r


def append_random(qc, qubit):
    n = random.uniform(0, 1)
    if n < 0.25:
        qc.i(qubit)
    elif n < 0.5:
        qc.x(qubit)
    elif n < 0.75:
        qc.y(qubit)
    else:
        qc.z(qubit)
    return qc


def bit_to_gate(qc, img, r, c, offset):
    if img.getpixel((c, r)):
        append_random(qc, r-offset)
    else:
        qc.h(r-offset)
    return qc


def image_to_circuit(img, text):
    print('Generating circuit...')
    w, h = get_text_size(text)
    offset = get_offset(img, text)
    qc = QuantumCircuit(h-offset)
    for r in range(offset, h):
        for c in range(w):
            qc = bit_to_gate(qc, img, r, c, offset)
    return qc


def main():
    if len(sys.argv) != EXPECTED_ARG_COUNT:
        usage()
        return
    text = sys.argv[1]
    if len(text) > MAX_TEXT_LENGTH:
        print(f'Length of input ({len(text)}) exceeded max ({MAX_TEXT_LENGTH})')
        return
    try:
        image = text_to_image(text)
    except OSError:
        print(f'Unable to locate {FONT_FILE}')
        return
    qc = image_to_circuit(image, text)
    print('Drawing circuit...')
    qc.draw(output=OUTPUT_MODE,
        filename=OUTPUT_FILE,
        fold=MAX_TEXT_LENGTH,
        style={
            'displaycolor': {
                'h': H_COLOR,
                'id': I_COLOR,
                'x': X_COLOR,
                'y': Y_COLOR,
                'z': Z_COLOR
            },
            'dpi': DPI
        }
    )    
    print(f'Finished. Output at {OUTPUT_FILE}')


if __name__ == '__main__':
    main()

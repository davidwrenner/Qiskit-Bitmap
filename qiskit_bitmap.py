
import random
import sys
from PIL import Image, ImageFont, ImageDraw
from qiskit import QuantumCircuit

DPI = 250
FONT_SIZE = 19
FONT_FILE = 'Times.ttc'
OUTPUT_MODE = 'mpl'
OUTPUT_FILE = './qiskit_text.png'
MAX_TEXT_LENGTH = 200
H_COLOR = '#33B1FF'
I_COLOR = '#F0F0F0'
X_COLOR = '#F0F0F0'
Y_COLOR = '#F0F0F0'
Z_COLOR = '#F0F0F0'


def usage():
    print(f'Usage: python {sys.argv[0]} <textstring>\n')

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


def bit_to_gate(qc, img, c, r):
    if img.getpixel((c,r)):
        append_random(qc, r-2)
    else:
        qc.h(r-2)
    return qc


def get_font():
    return ImageFont.truetype(FONT_FILE, FONT_SIZE)


def get_text_size(text):
    return get_font().getsize(text)


def text_to_image(text):
    w, h = get_text_size(text)
    image = Image.new('1', (w, h), 1)
    draw = ImageDraw.Draw(image)
    font = get_font()
    draw.text((0, 0), text, font=font)
    return image


def image_to_circuit(img, text):
    w, h = get_text_size(text)
    qc = QuantumCircuit(h-2,1)
    for r in range(2,h):
        for c in range(w):
            qc = bit_to_gate(qc, img, c, r)
    return qc


if __name__ == '__main__':
    if len(sys.argv) < 2:
        usage()
        sys.exit(0)
    text = sys.argv[1]
    if len(text) > MAX_TEXT_LENGTH:
        print(f'Exceeded maximum text length of {MAX_TEXT_LENGTH}.')
        sys.exit(0)
    image = text_to_image(text)
    print('Building circuit...')
    qc = image_to_circuit(image, text)
    fold = MAX_TEXT_LENGTH
    print('Generating image...')
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
    print(f'Image generated, view output at {OUTPUT_FILE}')

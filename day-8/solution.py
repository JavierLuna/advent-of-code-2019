from collections import Counter
from pprint import pprint
from typing import List

INPUT_FILE = 'input'

WIDTH, LENGHT = 25, 6

with open(INPUT_FILE) as input_file:
    pixels = list(input_file.read().strip())

layers = []

while pixels:
    layer = pixels[:WIDTH * LENGHT]
    pixels = pixels[WIDTH * LENGHT:]
    layers.append(layer)

# Part 1
least_zero_layer = sorted([Counter(l) for l in layers], key=lambda c: c['0'])[0]
print(least_zero_layer['1'] * least_zero_layer['2'])


# Part 2

class Colors:
    BLACK = '0'
    WHITE = '1'
    TRANSPARENT = '2'


def flatten_layers(layers: List[List[str]]) -> List[str]:
    flattered_layer = [Colors.TRANSPARENT] * (WIDTH * LENGHT)
    for layer in layers:
        for pixel_index, pixel in enumerate(layer):
            if flattered_layer[pixel_index] == Colors.TRANSPARENT:
                flattered_layer[pixel_index] = pixel
    return flattered_layer


def decode_picture(layer: List[str]) -> List[List[str]]:
    layer = layer[:]
    final_picture = []
    while layer:
        final_picture.append(layer[:WIDTH])
        layer = layer[WIDTH:]
    return final_picture


def prettify_layer(layer: List[str]) -> List[str]:
    prettify = {
        Colors.TRANSPARENT: '',
        Colors.BLACK: '  ',
        Colors.WHITE: '█ '
    }
    return [prettify[pixel] for pixel in layer]


flattened_layer = flatten_layers(layers)
pretty_layer = prettify_layer(flattened_layer)
decoded_picture = decode_picture(pretty_layer)
print('\n'.join([''.join(a) for a in decoded_picture]))

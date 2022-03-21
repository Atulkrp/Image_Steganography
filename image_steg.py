
"""This code is for image steganography  written by Atul Kumar Pandit"""

from typing import Iterable
import numpy as np
from PIL import Image
import cv2


# This function is for providing ascii values of the text we typed
def bits_provider(message) -> Iterable[int]:
    for char in message:
        ascii_value = ord(char)
        for bit_position in range(8):
            power = 7 - bit_position
            yield 1 if ascii_value & (1 << power) else 0


def chars_provider(pixel_red_values) -> Iterable[str]:
    ascii_value = 0
    for i, pixel_red_value in enumerate(pixel_red_values):
        ascii_value_bit_position = 7 - i % 8
        if pixel_red_value & 1:
            ascii_value |= 1 << ascii_value_bit_position
        if ascii_value_bit_position == 0:
            char: str = chr(ascii_value)
            if not char.isprintable() and char != '\n':
                return

            yield char

            ascii_value = 0

#This function is for encoding image
def encode_image(message: str, input_filename, output_filename: str) -> None:
    img = Image.open(input_filename)
    pixels = np.array(img)
    img.close()
    clear_low_order_bits(pixels)
    for i, bit in enumerate(bits_provider(message)):
        row = i // pixels.shape[1]
        col = i % pixels.shape[1]
        pixels[row, col, 0] |= bit
    out_img = Image.fromarray(pixels)
    out_img.save(output_filename)
    out_img.close()


def clear_low_order_bits(pixels) -> None:
    for row in range(pixels.shape[0]):
        for col in range(pixels.shape[1]):
            pixels[row, col, 0] &= ~1


def decode_image(filename: str) -> str:
    img = Image.open(filename)
    result = ''.join(chars_provider(img.getdata(band=0)))
    img.close()
    return result

def showoriginalpic():
    print("This is original image")
    img=cv2.imread('original-image.png')

    cv2.imshow('original-image',img)

    cv2.waitKey(2000) & 0xff
    cv2.destroyAllWindows()

def showencodedpic():
    print("This is encoded image")
    img=cv2.imread('secret-image.png')

    cv2.imshow('secret-image',img)

    cv2.waitKey(2000) & 0xff
    cv2.destroyAllWindows()

def Main():
    print("Image Stegonaraphy")
    inpt = int(input("1. Encode Image \n2. Decode Image \n Please Select Option\n"))
    if inpt == 1:
        msg = str(input("Enter the text u want to encode: "))
        encode_image(msg, 'original-image.png', 'secret-image.png')
        print("your text is Encoded successfully !")
        showoriginalpic()
    elif inpt == 2:
        print("The Decoded text is: ")
        decoded = decode_image('secret-image.png')
        print(decoded)
        showencodedpic()
    else:
        print("Incorrect input")
    exit(0)


if __name__ == '__main__':
    Main()

import board
import neopixel

def pixels(brightness = 0.1):
    if brightness == 0:
        pixels = neopixel.NeoPixel(board.D18, 24)
        pixels.show()
    else:
        pixels = neopixel.NeoPixel(board.D18, 24, brightness)
        pixels.fill((255, 0, 0))
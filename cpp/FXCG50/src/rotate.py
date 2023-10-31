import sys
from PIL import Image, ImageDraw

# Char dimensions
CHAR_W = 7
CHAR_H = 9

# Source file organisation
HORZ_COUNT = 16
VERT_COUNT = 6

C_WHITE = (255, 255, 255)

# Source image
try:
    src = Image.open("/home/jhb/Nextcloud/personnel/JHB/dev/tetris/cpp/FXCG50/assets-cg/font_default.png")
except FileNotFoundError:
    print("Le fichier source est introuvable")
    sys.exit(1)

# Dimensions
width, height = src.size

if width != (CHAR_W * HORZ_COUNT) or height != (CHAR_H * VERT_COUNT):
    print("Les dimensions de l'image ne sont pas correctes")

# Create dest image
dest = Image.new('RGB', (HORZ_COUNT * CHAR_H, VERT_COUNT * CHAR_W), C_WHITE)

for row in range(VERT_COUNT):
    for y in range(CHAR_H):
        for col in range(HORZ_COUNT):
            for x in range(CHAR_W):
                # put the same pixel in the dest file
                dest.putpixel((col * CHAR_H + y, (row + 1) * CHAR_W - x -1), src.getpixel((col * CHAR_W + x, row * CHAR_H + y)))

# Save dest
dest.save("/home/jhb/Nextcloud/personnel/JHB/dev/tetris/cpp/FXCG50/assets-cg/font_vert.png", 'png')
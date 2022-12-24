# This script is meant to be run from the root level
# of your font's git repository. For example, from a Unix terminal:
# $ git clone my-font
# $ cd my-font
# $ python3 documentation/image1.py --output documentation/image1.png

# Import moduels from external python packages: https://pypi.org/
from drawbot_skia.drawbot import *
from fontTools.ttLib import TTFont
from fontTools.misc.fixedTools import floatToFixedToStr

# Import moduels from the Python Standard Library: https://docs.python.org/3/library/
import subprocess
import sys
import argparse

# Constants, these are the main "settings" for the image
WIDTH, HEIGHT, MARGIN, FRAMES = 1380, 520, 30, 1
FONT_PATH = "fonts/otf/MatrixSans-Regular.otf"
FONT_LICENSE = "OFL v1.1"
AUXILIARY_FONT = "Open Sans"
AUXILIARY_FONT_SIZE = 22
BIG_TEXT = "Aa"
BIG_TEXT_FONT_SIZE = 100
BIG_TEXT_SIDE_MARGIN = WIDTH // 2
BIG_TEXT_BOTTOM_MARGIN = 30
BIG_TEXT_INTERLINE = BIG_TEXT_FONT_SIZE * 1.3
GRID_VIEW = False # Change this to "True" for a grid overlay

# Handel the "--output" flag
# For example: $ python3 documentation/image1.py --output documentation/image1.png
parser = argparse.ArgumentParser()
parser.add_argument("--output", metavar="PNG", help="where to write the PNG file")
args = parser.parse_args()



# Constants that are worked out dynamically
MY_URL = subprocess.check_output("git remote get-url origin", shell=True).decode()
MY_HASH = subprocess.check_output("git rev-parse --short HEAD", shell=True).decode()



# Draws a grid
def grid():
	stroke(1, 0, 0, 0.75)
	strokeWidth(2)
	STEP_X, STEP_Y = 0, 0
	INCREMENT_X, INCREMENT_Y = MARGIN / 2, MARGIN / 2
	rect(MARGIN, MARGIN, WIDTH - (MARGIN * 2), HEIGHT - (MARGIN * 2))
	for x in range(29):
		polygon((MARGIN + STEP_X, MARGIN), (MARGIN + STEP_X, HEIGHT - MARGIN))
		STEP_X += INCREMENT_X
	for y in range(29):
		polygon((MARGIN, MARGIN + STEP_Y), (WIDTH - MARGIN, MARGIN + STEP_Y))
		STEP_Y += INCREMENT_Y
	polygon((WIDTH / 2, 0), (WIDTH / 2, HEIGHT))
	polygon((0, HEIGHT / 2), (WIDTH, HEIGHT / 2))


# Remap input range to VF axis range
# This is useful for animation
# (E.g. sinewave(-1,1) to wght(100,900))
def remap(value, inputMin, inputMax, outputMin, outputMax):
	inputSpan = inputMax - inputMin  # FIND INPUT RANGE SPAN
	outputSpan = outputMax - outputMin  # FIND OUTPUT RANGE SPAN
	valueScaled = float(value - inputMin) / float(inputSpan)
	return outputMin + (valueScaled * outputSpan)


# Draw the page/frame and a grid if "GRID_VIEW" is set to "True"
def draw_background(colour, height):
	newPage(WIDTH, height)
	fill(colour[0], colour[1], colour[2])
	rect(-2, -2, WIDTH + 2, height + 2)
	if GRID_VIEW:
		grid()
	else:
		pass


# Draw main text
def draw_main_text(text_list, colour):
	fill(colour[0], colour[1], colour[2])
	stroke(None)
	# font(FONT_PATH)
	fontSize(BIG_TEXT_FONT_SIZE)

	# Adjust this line to center main text manually.
	# TODO: This should be done automatically when drawbot-skia
	# has support for textBox() and FormattedString
	#text(BIG_TEXT, ((WIDTH / 2) - MARGIN * 4.75, (HEIGHT / 2) - MARGIN * 2.5))
	openTypeFeatures(smcp=True)
	font("fonts/otf/MatrixSans-Regular.otf")
	# text(text_list[0], (BIG_TEXT_SIDE_MARGIN, BIG_TEXT_BOTTOM_MARGIN + BIG_TEXT_INTERLINE*4), "center")

	# font("fonts/otf/MatrixSansPrint-Regular.otf")
	text(text_list[0], (BIG_TEXT_SIDE_MARGIN, BIG_TEXT_BOTTOM_MARGIN + BIG_TEXT_INTERLINE*3), "center")
	# font("fonts/otf/MatrixSansRaster-Regular.otf")
	text(text_list[1], (BIG_TEXT_SIDE_MARGIN, BIG_TEXT_BOTTOM_MARGIN + BIG_TEXT_INTERLINE*2), "center")
	# font("fonts/otf/MatrixSansScreen-Regular.otf")
	text(text_list[2], (BIG_TEXT_SIDE_MARGIN, BIG_TEXT_BOTTOM_MARGIN + BIG_TEXT_INTERLINE*1), "center")
	openTypeFeatures(c2sc=True)
	# font("fonts/of/MatrixSansVideo-Regular.otf")
	text(text_list[3], (BIG_TEXT_SIDE_MARGIN, BIG_TEXT_BOTTOM_MARGIN + BIG_TEXT_INTERLINE*0), "center")


# Divider lines
def draw_divider_lines():
	stroke(0.5)
	strokeWidth(2)
	lineCap("round")
	line((MARGIN, HEIGHT - MARGIN), (WIDTH - MARGIN, HEIGHT - MARGIN))
	line((MARGIN, MARGIN + (MARGIN / 2)), (WIDTH - MARGIN, MARGIN + (MARGIN / 2)))
	stroke(None)


# Draw text describing the font and it's git status & repo URL
def draw_auxiliary_text():
	# Load the font with the parts of fonttools that are imported with the line:
	# from fontTools.ttLib import TTFont
	# Docs Link: https://fonttools.readthedocs.io/en/latest/ttLib/ttFont.html
	ttFont = TTFont(FONT_PATH)
	# FONT_NAME = ttFont["name"].getDebugName(4)
	# FONT_NAME = ttFont["name"].getBestFamilyName()
	FONT_NAME = ttFont["name"].getBestFullName()
	if str(FONT_NAME) == "Matrix Sans":
		FONT_NAME = "Matrix Sans Regular"
	# FONT_VERSION = "v%s" % floatToFixedToStr(ttFont["head"].fontRevision, 16)
	FONT_VERSION = str(ttFont["name"].getName(5, 3, 1))
	# Setup
	fill(0.5)
	font(AUXILIARY_FONT)
	fontSize(AUXILIARY_FONT_SIZE)
	POS_TOP_LEFT = (MARGIN, HEIGHT - MARGIN * 1.5)
	POS_TOP_RIGHT = (WIDTH - MARGIN, HEIGHT - MARGIN * 1.5)
	POS_BOTTOM_LEFT = (MARGIN, MARGIN)
	POS_BOTTOM_RIGHT = (WIDTH - MARGIN * 0.95, MARGIN)
	# URL_AND_HASH = MY_URL + "at commit " + MY_HASH
	URL_AND_HASH = MY_URL
	URL_AND_HASH = URL_AND_HASH.replace("\n", " ")
	# Draw Text
	text(FONT_NAME, POS_TOP_LEFT, align="left")
	text(FONT_VERSION, POS_TOP_RIGHT, align="right")
	text(URL_AND_HASH, POS_BOTTOM_LEFT, align="left")
	text(FONT_LICENSE, POS_BOTTOM_RIGHT, align="right")


def make_image(text_list, text_colour, bg_colour):
	height = BIG_TEXT_INTERLINE * len(text_list)
	draw_background(bg_colour, height)
	draw_main_text(text_list, text_colour)
	# draw_divider_lines()
	# draw_auxiliary_text()

# Build and save the image
if __name__ == "__main__":
	FONT_PATH = "fonts/otf/MatrixSans-Regular.otf"
	make_image(["Now with Small Capitals!","Grumpy wizards make","toxic brew for the evil","queen and jack 12345678"], [0, 0, 0], [1, 1, 1])
	# Save output, using the "--output" flag location
	saveImage(args.output)
	# Print done in the terminal
	print("DrawBot: Done")
	
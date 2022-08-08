"""Run a matrix-like screensaver."""

# Core libs
import random
import string
from pathlib import Path
from typing import Tuple, Set, List
from dataclasses import dataclass

# Third party libs
import pygame, pygame.font


@dataclass
class Color(tuple):
    """Representation of a color."""

    red: int
    green: int
    blue: int

    def __post_init__(self):
        if any(x > 255 or x < 0 for x in self):
            raise ValueError("Color values must be between 0 and 255.")

    def to_tuple(self) -> Tuple[int, int, int]:
        return (self.red, self.green, self.blue)

    def __getitem__(self, index):
        return self.to_tuple()[index]

    def __iter__(self):
        return self.to_tuple().__iter__()

    def dim(self, factor: float) -> 'Color':
        """Dim the color."""
        # TODO: Carson ---------------------------------------------------------
        # Return another color that's been dimmed by the given `factor`.
        # Difficulty: Medium
        # ----------------------------------------------------------------------


# TODO: Carson -----------------------------------------------------------------
# Difficulty: Hard
# Change the variable `COLOR` to instead be an instance of the `Color` class.
COLOR = (0, 200, 200)  # The Color of the Matrix
# ------------------------------------------------------------------------------


ZERO_ONE: bool = False  # Makes a rain of zeros and ones instead of random ASCII character
SET_CHARACTERS: Set[str] = set(string.ascii_lowercase + string.ascii_uppercase + string.digits)




def is_written() -> bool:
    for x in range(
        (lettersOnScreen[0] / 2) - (len(str_characters) / 2),
        (lettersOnScreen[0] / 2) + (len(str_characters) / 2) + 1,
    ):
        if xHeads[x] == -1:
            return False
    return True


def get_color(xHeads, fx, fy) -> Color:
    defTemp = xHeads[fx] - fy

    if maxCol > defTemp > 0:
        return defTemp
    else:
        return maxCol - 1

def get_list_color(length: int) -> List[Color]:
    return [get_color(x, y) for x in range(length) for y in range(length)]


try:
    with Path("words.txt").open() as f:
        words = f.read().splitlines()
except:
    str_characters = ""
str_characters = str_characters.upper()  # for better placement


# Pygame init
pygame.init()

_info = pygame.display.Info()
display_width, display_height = display_dimentions = (_info.current_w, _info.current_h)
surface = pygame.display.set_mode(display_dimentions, pygame.FULLSCREEN)

# Font init
pygame.font.init()
fontObj = pygame.font.Font(pygame.font.get_default_font(), 14)
sampleLetter = fontObj.render("_", False, (0, 111, 0))
width_letter, height_letter = dimention_letter = (sampleLetter.get_width(), sampleLetter.get_height())

# TODO: Carson -----------------------------------------------------------------
# Difficulty: Hard
# Make the value of `lettersOnScreen` be obtained through a function
# Help: the signature of the functions should be
#       `get_letters_on_screen(width_display, height_display, width_letter, height_letter)`
lettersOnScreen = (
    int(display_dimentions[0] / dimention_letter[0]),
    int(display_dimentions[1] / dimention_letter[1]),
)
# ------------------------------------------------------------------------------

print(f"Running with dimentions: {display_dimentions}")
print(f"Running with letter dimentions: {dimention_letter}")
print(f"Running with {lettersOnScreen[0]} letters on the x axis and {lettersOnScreen[1]} letters on the y axis")


# color init
# list_color = get_list_color(lettersOnScreen[0])
list_color = [(255, 255, 255)]
primeColors = len(list_color) + 1
R, G, B = COLOR
list_color += [(R + 10, G + 10, B + 10)] * ((lettersOnScreen[1] - 10))
endColors = len(list_color)
list_color += [
    (R - 50 if R else 0, B - 50 if B else 0, G - 50 if G else 0),
    (R - 100 if R else 0, B - 100 if B else 0, G - 100 if G else 0),
    (0, 0, 0),
]
endColors = len(list_color) - endColors + 1

maxCol = len(list_color)


# char generator
letters = [
    [0 for _ in range(lettersOnScreen[1] + 1)] for _ in range(lettersOnScreen[0])
]
if ZERO_ONE:
    char = chr(random.randint(48, 49))
else:
    char = chr(random.randint(32, 126))

for y in range(lettersOnScreen[1] + 1):
    for x in range(lettersOnScreen[0]):
        letters[x][y] = [
            fontObj.render(char, False, list_color[col]) for col in range(maxCol)
        ]
        if ZERO_ONE:
            char = chr(random.randint(48, 49))
        else:
            char = chr(random.randint(32, 126))


# word write
wordMode = False
if len(str_characters) > 0:
    wordMode = True
    for x in range(
        (lettersOnScreen[0] / 2) - (len(str_characters) / 2),
        (lettersOnScreen[0] / 2) + (len(str_characters) / 2),
    ):
        letters[x][lettersOnScreen[1] / 2] = [
            fontObj.render(
                str_characters[x - ((lettersOnScreen[0] / 2) - (len(str_characters) / 2))],
                False,
                (255, 255, 255),
            )
            for col in range(maxCol)
        ]

    for y in range(lettersOnScreen[1] / 2 + 1, lettersOnScreen[1] + 1):
        for x in range(
            (lettersOnScreen[0] / 2) - (len(str_characters) / 2),
            (lettersOnScreen[0] / 2) + (len(str_characters) / 2),
        ):
            letters[x][y] = [
                fontObj.render(char, False, (0, 0, 0)) for col in range(maxCol)
            ]
            char = chr(random.randint(32, 126))

    if len(str_characters) % 2 == 1:

        letters[(lettersOnScreen[0] / 2) + (len(str_characters) / 2)][lettersOnScreen[1] / 2] = [
            fontObj.render(str_characters[len(str_characters) - 1], False, (255, 255, 255))
            for col in range(maxCol)
        ]

        for y in range(lettersOnScreen[1] / 2 + 1, lettersOnScreen[1] + 1):
            letters[(lettersOnScreen[0] / 2) + (len(str_characters) / 2)][y] = [
                fontObj.render(char, False, (0, 0, 0)) for col in range(maxCol)
            ]
            char = chr(random.randint(32, 126))

if wordMode:
    xHeads = [-1 for _ in range(lettersOnScreen[0] + 1)]
else:
    xHeads = [0 for _ in range(lettersOnScreen[0] + 1)]


# 1st loop - word write, no char switch
notDone = True
ticksLeft = lettersOnScreen[1] + maxCol
while ticksLeft > 0 and (notDone) and (wordMode):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            notDone = False
        if event.type == pygame.KEYDOWN:
            notDone = False
    if is_written():
        ticksLeft -= 1
    if random.randint(1, 2) == 1:
        randomInt = random.randint(0, lettersOnScreen[0])
        if wordMode:
            if xHeads[randomInt] == -1:
                xHeads[randomInt] = 1
            if random.randint(1, 6):
                randomInt = random.randint(
                    (lettersOnScreen[0] / 2) - len(str_characters),
                    (lettersOnScreen[0] / 2) + len(str_characters) + 1,
                )
                if xHeads[randomInt] == -1:
                    xHeads[randomInt] = 1
        else:
            if xHeads[randomInt] == 0:
                xHeads[randomInt] = 1
    for x in range(lettersOnScreen[0]):
        col = 0
        counter = xHeads[x]
        while (counter > 0) and (col < maxCol):
            if (counter < lettersOnScreen[1] + 2) and (
                col < primeColors or col > (maxCol - endColors)
            ):
                surface.blit(
                    letters[x][counter - 1][col],
                    (x * dimention_letter[0], (counter - 1) * dimention_letter[1]),
                )
            col += 1
            counter -= 1
        if xHeads[x] > 0:
            xHeads[x] += 1
        if xHeads[x] - maxCol > lettersOnScreen[1]:
            xHeads[x] = 0

    pygame.display.update()
    clock = pygame.time.Clock()
    clock.tick(20)

# word delete
if len(str_characters) % 2 == 1:
    strLen = int((lettersOnScreen[0] / 2) + (len(str_characters) / 2) + 1)
else:
    strLen = int((lettersOnScreen[0] / 2) + (len(str_characters) / 2))

for x in range(int((lettersOnScreen[0] / 2) - (len(str_characters) / 2)), strLen):
    letters[x][lettersOnScreen[1] / 2] = [
        fontObj.render(
            str_characters[x - ((lettersOnScreen[0] / 2) - (len(str_characters) / 2))], False, list_color[col]
        )
        for col in range(maxCol)
    ]

char = chr(random.randint(32, 126))
for y in range(int(lettersOnScreen[1] / 2 + 1), int(lettersOnScreen[1] + 1)):
    for x in range(
        int((lettersOnScreen[0] / 2) - (len(str_characters) / 2)),
        int((lettersOnScreen[0] / 2) + (len(str_characters) / 2) + 1),
    ):
        letters[x][y] = [
            fontObj.render(char, False, list_color[col]) for col in range(maxCol)
        ]
        char = chr(random.randint(32, 126))


# main matrix, has char switch
is_done = False
while not is_done:
    for event in pygame.event.get():
        # TODO: Carson -----------------------------------------------------
        # Change the following code to use an `in` operator.
        # Difficulty: medium
        if event.type == pygame.QUIT:
            is_done = True
        if event.type == pygame.KEYDOWN:
            is_done = True
        # ------------------------------------------------------------------


    if random.randint(1, 2) == 1:
        randomInt = random.randint(0, lettersOnScreen[0])
        if xHeads[randomInt] <= 0:
            xHeads[randomInt] = 1
    for x in range(lettersOnScreen[0]):
        col = 0
        counter = xHeads[x]
        # main loop for redraw
        while (counter > 0) and (col < maxCol):
            if (counter < lettersOnScreen[1] + 2) and (
                col < primeColors or col > (maxCol - endColors)
            ):
                surface.blit(
                    letters[x][counter - 1][col],
                    (x * dimention_letter[0], (counter - 1) * dimention_letter[1]),
                )
            col += 1
            counter -= 1

        # charswirch
        randomInt = random.randint(1, maxCol - 1)
        charPosY = xHeads[x] - randomInt
        if lettersOnScreen[1] - 1 > charPosY > 0:
            temp = letters[x][charPosY]
            randomX = random.randint(1, lettersOnScreen[0] - 1)
            randomY = random.randint(1, lettersOnScreen[1] - 1)

            surface.blit(
                letters[x][charPosY][maxCol - 1],
                (x * dimention_letter[0], charPosY * dimention_letter[1]),
            )
            surface.blit(
                letters[randomX][randomY][maxCol - 1],
                (randomX * dimention_letter[0], randomY * dimention_letter[1]),
            )
            # char swap
            letters[x][charPosY] = letters[randomX][randomY]
            letters[randomX][randomY] = temp

            surface.blit(
                letters[x][charPosY][randomInt],
                (x * dimention_letter[0], charPosY * dimention_letter[1]),
            )
            surface.blit(
                letters[randomX][randomY][get_color(xHeads,randomX, randomY)],
                (randomX * dimention_letter[0], randomY * dimention_letter[1]),
            )
        # check if is out of screen
        if xHeads[x] > 0:
            xHeads[x] += 1
        if xHeads[x] - maxCol > lettersOnScreen[1]:
            xHeads[x] = 0

    pygame.display.update()
    clock = pygame.time.Clock()
    clock.tick(20)

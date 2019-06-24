import audioio
import board
import digitalio
import time
from adafruit_circuitplayground.express import cpx
from random import randint

cpx.pixels.brightness = 0.01

def getLedColorByLevel(level):
  return (0, 255, 0) if level <= 2 else (255, 255, 0) if level <= 4 else (255, 127, 80) if level <= 7 else (255, 0, 0)

def chooseLevel():
  level = 0
  cpx.play_file("level.wav")
  while True:
    cpx.pixels[level] = getLedColorByLevel(level)
    if cpx.button_a:
      cpx.pixels.fill((0,0,0))
      return level
    if cpx.button_b:
      if level < 9 :
        level += 1
      else:
        level = 0
        cpx.pixels.fill((0,0,0))
    time.sleep(0.2)

def printLB():
  cpx.pixels[7] = (255, 0, 255)
  cpx.pixels[8] = (255, 0, 255)
  cpx.pixels[9] = (255, 0, 255)
  cpx.play_file("do.wav")
  time.sleep(0.6)
  cpx.pixels.fill((0,0,0))
  time.sleep(0.6)

def printRB():
  cpx.pixels[0] = (0, 255, 255)
  cpx.pixels[1] = (0, 255, 255)
  cpx.pixels[2] = (0, 255, 255)
  cpx.play_file("fa.wav")
  time.sleep(0.6)
  cpx.pixels.fill((0,0,0))
  time.sleep(0.6)

def printLT():
  cpx.pixels[5] = (255, 255, 0)
  cpx.pixels[6] = (255, 255, 0)
  cpx.pixels[7] = (255, 255, 0)
  cpx.play_file("re.wav")
  time.sleep(0.6)
  cpx.pixels.fill((0,0,0))
  time.sleep(0.6)

def printRT():
  cpx.pixels[2] = (0, 255, 0)
  cpx.pixels[3] = (0, 255, 0)
  cpx.pixels[4] = (0, 255, 0)
  cpx.play_file("mi.wav")
  time.sleep(0.6)
  cpx.pixels.fill((0,0,0))
  time.sleep(0.6)

def printError(error):
  fn = printFunctions[error]
  cpx.pixels.fill((255,0,0))
  time.sleep(0.2)
  cpx.pixels.fill((0,0,0))
  time.sleep(0.2)
  cpx.pixels.fill((255,0,0))
  time.sleep(0.2)
  cpx.pixels.fill((0,0,0))

  fn()
  cpx.play_file("lose.wav")

def printGameColours(level):
  sequence = []
  for i in range(0, level):
    j = randint(0, 3)
    sequence.append(j)
    fn = printFunctions[j]
    fn()

  return sequence

def play(level):
  for i in range(2, level + 1):
    sequence = printGameColours(i)
    error = False
    hits = 0
    while (not error) and hits < i:
      if cpx.touch_A4 or cpx.touch_A5:
        printRB()
        if sequence[hits] == 0: hits += 1
        else: error = True
      elif cpx.touch_A6 or cpx.touch_A7:
        printRT()
        if sequence[hits] == 1: hits += 1
        else: error = True
      elif cpx.touch_A1:
        printLT()
        if sequence[hits] == 2: hits += 1
        else: error = True
      elif cpx.touch_A2 or cpx.touch_A3:
        printLB()
        if sequence[hits] == 3: hits += 1
        else: error = True

    if error:
      printError(sequence[hits])
      return

  cpx.play_file("win.wav")


printFunctions = [printRB, printRT, printLT, printLB]

while True:
  level = chooseLevel()
  play((level + 1) * 2)
  time.sleep(2)

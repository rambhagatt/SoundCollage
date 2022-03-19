
from JES import *
from random import *

# Ram Bhagat
# For March 10, 2022
# Sound Collage Project
#
# Please read the side note before running
# Side note: 
# 
# This sound collage takes too long to finish running within this repl. I had to use Google Colab, a python notebook, to run generate it.
# and run time is that long too. I recommend running the program
# and working on something else in the mean time (maybe get a 
# glass of water or do some jumping jacks). I am truly sorry.
# I wanted to shorten the audio files, but couldn't find a good
# segment to crop out. The effects of my audio manipualtions
# were also more apparent this way.
#

# Program: 

# This program creates a sound collage of five audio segments
# from two .wav files 
# The segments are: 
# 1. love hurts - vocals (.wav file 1)
# 2. butterfly effect - instrumental (.wav file 2)
# 3. a mixed sound of butterfly effect instrumental and love hurts vocal
# 4. a climbing and falling sound effect(volume incrementally rises and falls) upon audio segment 3
# 5. singing in canon effect with audio segment 3 - start time is randomized

# blends two sound inputs together in a ratio of sound1Percent to Sound2Percent
# returns the blend
def makeMixedSound(sound1,sound2, sound1Amount, sound2Amount):
  mixedSnd = makeEmptySound(getLength(sound1))
  for index in range(0, getLength(sound1)):
    val1 = getSampleValueAt(sound1, index)
    val2 = getSampleValueAt(sound2, index)
    newVal = val1*sound1Amount+val2*sound2Amount 
    setSampleValueAt(mixedSnd, index, newVal)
  return mixedSnd

# takes an input sound and adds or subtracts to the volume/wavelength of the sound every second
# For the first second, the volume of the original is transformed to be half and contininues to decrement in volume throughout the seocond 
def climbingAndFallingSound(sound):
  resultSnd = makeEmptySound(getLength(sound))
  temp = 1
  for index in range(0, getLength(sound)):
    val = getSampleValueAt(sound, index)
    if 0 <= temp <= 22050:
      newVal = int(val*(1/2)-(temp//50))
    elif 22050 <= temp <= 22050*2:
      newVal = val
    elif 22050*2 <= temp <= 22050*3:
      newVal = int(val*(1.5)+(temp//(22050*2)))
    else:
      temp = 0
    temp += 1
    setSampleValueAt(resultSnd, index, newVal)
  return resultSnd

# A canon is a form of music where one group starts 
# singing at one time and another group sings the same  
# music with a delayed start. This program develops
# a similar effect
def randomStartTimeCanon(sound):
  canonSnd = duplicateSound(sound)
  randomIndex = randrange(0, getLength(sound))
  for index in range(10000+randomIndex, getLength(sound)):
    echoSample = 0.6*getSampleValueAt(canonSnd, index-10000-randomIndex)
    comboSample = getSampleValueAt(sound, index) + echoSample
    setSampleValueAt(canonSnd, index, comboSample)
  return canonSnd

def SoundCollage():
  # create the sound modifications
  sound1 = makeSound("love hurts - vocals.wav")
  print("love hurts - vocals.wav Sampling Rate: ",getSamplingRate(sound1))
  print("sample amount", getLength(sound1))
  sound2 = makeSound("butterfly effect - instrumental.wav")
  print("butterfly effect - instrumental.wav Sampling Rate:",getSamplingRate(sound2) )    
  print("sample amount", getLength(sound2))
  sound3 = makeMixedSound(sound1, sound2, .25, .75)
  print("makeMixedSound Sampling Rate: ",getSamplingRate(sound3))
  print("sample amount", getLength(sound3))
  sound4 = randomStartTimeCanon(sound3)
  print("randomStartTimeCanon. Sampling Rate: ",getSamplingRate(sound4))
  print("sample amount", getLength(sound4))
  sound5 = climbingAndFallingSound(sound3)
  print("climbingAndFallingSound: ",getSamplingRate(sound5))
  print("sample amount", getLength(sound5))
  
  # create the canvas and find length
  canvasLen = getLength(sound1) + 6615 + getLength(sound2) + 6615 + getLength(sound3) + 6615 + getLength(sound4)+6615 + getLength(sound5)+6615
  canvas = makeEmptySound(canvasLen+6615)

  copy(sound1, canvas,  0)
  copy(sound2, canvas,  getLength(sound1) + 6615)
  copy(sound3, canvas,  getLength(sound1) + 6615 + getLength(sound2) + 6615 )
  copy(sound4, canvas,  getLength(sound1) + 6615 + getLength(sound2) + 6615 + getLength(sound3) + 6615)
  copy(sound5, canvas,  getLength(sound1) + 6615 + getLength(sound2) + 6615 + getLength(sound3) + 6615 + getLength(sound4))
  print("Sound Collage Sampling Rate: ",getSamplingRate(canvas))
  print("Sound Collage samples amount ", getSamples(canvas))
  print("Sound Collage length in seconds ", getLength(canvas)//22050)

  # write sound collage out
  writeSoundTo(canvas, "collage.wav")
  
  
SoundCollage()
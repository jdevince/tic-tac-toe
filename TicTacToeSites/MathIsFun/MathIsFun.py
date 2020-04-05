import base64
import time
import pytesseract
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.common.action_chains import ActionChains
import time
import numpy as numpy

from Models.TicTacToeBoard import TicTacToeBoard
import Services.DecisionService as DecisionService

url = 'https://www.mathsisfun.com/games/tic-tac-toe.html'
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)
actions = ActionChains(driver)

def play():
    initialSetup()
    board = TicTacToeBoard()

    time.sleep(2)
    actions.move_to_element_with_offset(driver.find_element_by_xpath('//*[@id="board"]/div[1]'), 35, 35)
    actions.click()
    actions.perform()
    time.sleep(10)

    updateBoardStatus(board)
    # while gameOver == False:
        # updateBoardStatus(board)
        #gameOver = doNextMove(board)

    #cleanup()

def initialSetup():
    driver.get(url)
    setOpponent('beginner')
    driver.find_element_by_id('optYes').click() # Start game

def cleanup():
    driver.close()

def setOpponent(difficulty):
    if difficulty == 'beginner':
        optionId = 'playerType11'
    elif difficulty == 'medium':
        optionId = 'playerType12'
    elif difficulty == 'challenging':
        optionId = 'playerType13'
    elif difficulty == 'hard':
        optionId = 'playerType14'

    driver.find_element_by_id(optionId).click()

def updateBoardStatus(board):
    # Intentionally choosing to work with a screenshot rather than HTML, for experience with OCR
    driver.save_screenshot('temp/screenshot.png')

    fullImage = Image.open('temp/screenshot.png')

    ocrConfig = r'--psm 10 -c tessedit_char_whitelist=OX'

    cellOne = fullImage.crop(getCellCoordinates(1))
    cellOne = updateImageForOCR(cellOne)
    print(pytesseract.image_to_string(cellOne, config=ocrConfig))

    cellTwo = fullImage.crop(getCellCoordinates(2))
    cellTwo = updateImageForOCR(cellTwo)
    print(pytesseract.image_to_string(cellTwo, config=ocrConfig))

    cellThree = fullImage.crop(getCellCoordinates(3))
    cellThree = updateImageForOCR(cellThree)
    print(pytesseract.image_to_string(cellThree, config=ocrConfig))

    cellFour = fullImage.crop(getCellCoordinates(4))
    cellFour = updateImageForOCR(cellFour)
    print(pytesseract.image_to_string(cellFour, config=ocrConfig))

    cellFive = fullImage.crop(getCellCoordinates(5))
    cellFive = updateImageForOCR(cellFive)
    print(pytesseract.image_to_string(cellFive, config=ocrConfig))

    cellSix = fullImage.crop(getCellCoordinates(6))
    cellSix = updateImageForOCR(cellSix)
    print(pytesseract.image_to_string(cellSix, config=ocrConfig))

    cellSeven = fullImage.crop(getCellCoordinates(7))
    cellSeven = updateImageForOCR(cellSeven)
    print(pytesseract.image_to_string(cellSeven, config=ocrConfig))

    cellEight = fullImage.crop(getCellCoordinates(8))
    cellEight = updateImageForOCR(cellEight)
    print(pytesseract.image_to_string(cellEight, config=ocrConfig))

    cellNine = fullImage.crop(getCellCoordinates(9))
    cellNine = updateImageForOCR(cellNine)
    print(pytesseract.image_to_string(cellNine, config=ocrConfig))

def getCellCoordinates(cell):
    # Result in format (startX, startY, endX, endY)
    topLeftX = 405
    topLeftY = 455
    cellSize = 60
    buffer = 10

    if cell == 1:
        result = (topLeftX + (0 * (cellSize + buffer)), topLeftY + (0 * (cellSize + buffer)), topLeftX + (1 * (cellSize + buffer)) - buffer, topLeftY + (1 * (cellSize + buffer)) - buffer)
    elif cell == 2:
        result = (topLeftX + (1 * (cellSize + buffer)), topLeftY + (0 * (cellSize + buffer)), topLeftX + (2 * (cellSize + buffer)) - buffer, topLeftY + (1 * (cellSize + buffer)) - buffer)
    elif cell == 3:
        result = (topLeftX + (2 * (cellSize + buffer)), topLeftY + (0 * (cellSize + buffer)), topLeftX + (3 * (cellSize + buffer)) - buffer, topLeftY + (1 * (cellSize + buffer)) - buffer)
    elif cell == 4:
        result = (topLeftX + (0 * (cellSize + buffer)), topLeftY + (1 * (cellSize + buffer)), topLeftX + (1 * (cellSize + buffer)) - buffer, topLeftY + (2 * (cellSize + buffer)) - buffer)
    elif cell == 5:
        result = (topLeftX + (1 * (cellSize + buffer)), topLeftY + (1 * (cellSize + buffer)), topLeftX + (2 * (cellSize + buffer)) - buffer, topLeftY + (2 * (cellSize + buffer)) - buffer)
    elif cell == 6:
        result = (topLeftX + (2 * (cellSize + buffer)), topLeftY + (1 * (cellSize + buffer)), topLeftX + (3 * (cellSize + buffer)) - buffer, topLeftY + (2 * (cellSize + buffer)) - buffer)
    elif cell == 7:
        result = (topLeftX + (0 * (cellSize + buffer)), topLeftY + (2 * (cellSize + buffer)), topLeftX + (1 * (cellSize + buffer)) - buffer, topLeftY + (3 * (cellSize + buffer)) - buffer)
    elif cell == 8:
        result = (topLeftX + (1 * (cellSize + buffer)), topLeftY + (2 * (cellSize + buffer)), topLeftX + (2 * (cellSize + buffer)) - buffer, topLeftY + (3 * (cellSize + buffer)) - buffer)
    elif cell == 9:
        result = (topLeftX + (2 * (cellSize + buffer)), topLeftY + (2 * (cellSize + buffer)), topLeftX + (3 * (cellSize + buffer)) - buffer, topLeftY + (3 * (cellSize + buffer)) - buffer)

    return result

def updateImageForOCR(image):

    # Make background white
    imageArray = numpy.array(image.convert('RGBA'))   # "imageArray" is a height x width x 4 numpy array
    red, green, blue, alpha = imageArray.T # Temporarily unpack the bands for readability
    backgroundColor = (red == 221) & (green == 238) & (blue == 255)
    imageArray[..., :-1][backgroundColor.T] = (255, 255, 255) 
    updatedImage = Image.fromarray(imageArray)

    # Apply thresholding to make blue Os and red Xs black
    threshold = 150  
    updatedImage = updatedImage.point(lambda p: p > threshold and 255)  

    return updatedImage

# def getMiddleOfCell(cell):
#     coordinates = getCellCoordinates(cell)
#     result = ( (coordinates[0] + coordinates[2]) / 2, (coordinates[1] + coordinates[3]) / 2 )
#     return result

#def doNextMove(board):
#    nextMoveCell = DecisionService.getNextMove(board)
    

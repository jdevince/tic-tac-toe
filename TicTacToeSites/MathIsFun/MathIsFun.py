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

from Models.TicTacToeBoard import TicTacToeBoard, CellState
import Services.DecisionService as DecisionService

url = 'https://www.mathsisfun.com/games/tic-tac-toe.html'
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)
actions = ActionChains(driver)

def play():
    initialSetup()
    board = TicTacToeBoard()

    gameOver = False
    while gameOver == False:
        updateBoardStatus(board)
        doMove(board)
        updateBoardStatus(board)
        gameOver = board.isGameOver()
    
    time.sleep(5)
    cleanup()

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

    for cellIndex in range(9):
        cellImage = fullImage.crop(getCellCoordinates(cellIndex))
        cellImage = updateImageForOCR(cellImage)
        cellCharacter = pytesseract.image_to_string(cellImage, config=ocrConfig)

        if (cellCharacter == 'O'):
            board.cells[cellIndex] = CellState.Ours
        elif (cellCharacter == 'X'):
            board.cells[cellIndex] = CellState.Opponent

def getCellCoordinates(cell):
    # Result in format (startX, startY, endX, endY)
    topLeftX = 405
    topLeftY = 455
    cellSize = 60
    buffer = 10

    if cell == 0:
        result = (topLeftX + (0 * (cellSize + buffer)), topLeftY + (0 * (cellSize + buffer)), topLeftX + (1 * (cellSize + buffer)) - buffer, topLeftY + (1 * (cellSize + buffer)) - buffer)
    elif cell == 1:
        result = (topLeftX + (1 * (cellSize + buffer)), topLeftY + (0 * (cellSize + buffer)), topLeftX + (2 * (cellSize + buffer)) - buffer, topLeftY + (1 * (cellSize + buffer)) - buffer)
    elif cell == 2:
        result = (topLeftX + (2 * (cellSize + buffer)), topLeftY + (0 * (cellSize + buffer)), topLeftX + (3 * (cellSize + buffer)) - buffer, topLeftY + (1 * (cellSize + buffer)) - buffer)
    elif cell == 3:
        result = (topLeftX + (0 * (cellSize + buffer)), topLeftY + (1 * (cellSize + buffer)), topLeftX + (1 * (cellSize + buffer)) - buffer, topLeftY + (2 * (cellSize + buffer)) - buffer)
    elif cell == 4:
        result = (topLeftX + (1 * (cellSize + buffer)), topLeftY + (1 * (cellSize + buffer)), topLeftX + (2 * (cellSize + buffer)) - buffer, topLeftY + (2 * (cellSize + buffer)) - buffer)
    elif cell == 5:
        result = (topLeftX + (2 * (cellSize + buffer)), topLeftY + (1 * (cellSize + buffer)), topLeftX + (3 * (cellSize + buffer)) - buffer, topLeftY + (2 * (cellSize + buffer)) - buffer)
    elif cell == 6:
        result = (topLeftX + (0 * (cellSize + buffer)), topLeftY + (2 * (cellSize + buffer)), topLeftX + (1 * (cellSize + buffer)) - buffer, topLeftY + (3 * (cellSize + buffer)) - buffer)
    elif cell == 7:
        result = (topLeftX + (1 * (cellSize + buffer)), topLeftY + (2 * (cellSize + buffer)), topLeftX + (2 * (cellSize + buffer)) - buffer, topLeftY + (3 * (cellSize + buffer)) - buffer)
    elif cell == 8:
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

def doMove(board):
   nextMoveCellIndex = DecisionService.getNextMove(board)

   xpath = '//*[@id="board"]/div[' + str(nextMoveCellIndex + 1) + ']'
   actions.move_to_element_with_offset(driver.find_element_by_xpath(xpath), 35, 35).click().perform()
    

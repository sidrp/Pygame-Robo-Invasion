import pygame
import math

# Returns the rotated image and the new image's rectangle
def getRotatedImage(image, rect, angle):
    newImage = pygame.transform.rotate(image, angle)
    newRect = newImage.get_rect(center=rect.center)
    return newImage, newRect

# returns the angle between point 1 and point 2
def angleBetweenPoints(x1, y1, x2, y2):
    xDifference = x2 - x1
    yDifference = y2 - y1
    angle = math.degrees(math.atan2(-yDifference, xDifference))
    return angle

# Returns coordinates that are at the center of the screen
def centeringCoords(thingy, screen):
    newX = screen.get_width()/2 - thingy.get_width()/2
    newY = screen.get_height()/2 - thingy.get_height()/2
    return newX, newY
    

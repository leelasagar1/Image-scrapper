import os


def getKeywords():

    return os.listdir('static')


def getImages(keyword):
    images = [keyword+"/" + image for image in os.listdir('static/'+keyword)]

    return images

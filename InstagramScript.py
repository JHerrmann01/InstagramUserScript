#Instagram API

#Grabbing most recent images from pexels.com
import urllib.request
from bs4 import BeautifulSoup
from InstagramAPI import InstagramAPI
import os
import time

def retrieveWebPageHTML(url):
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    headers={'User-Agent':user_agent,}
    #Assembling the request which we will make the the specified url
    request=urllib.request.Request(url,None,headers)
    #Making the request, and returning the response
    response = urllib.request.urlopen(request)
    return(response)

def parseHTML(html):
    soup = BeautifulSoup(html,'lxml')
    return soup.findAll('img')

def refineImageURLS(imgList):
    properURLS = []
    for img in imgList:
        img = img.get('src')
        #We want to filter out anything that is considered an "asset"
        if('assets' not in img.split("/")):
            #Appending the raw url, removing the filters from the end
            properURLS.append(img.split("?")[0])
    return properURLS

def retrieveMostRecentImage(imgList, usedImgs):
    for img in imgList:
        if(img not in usedImgs):
            return img
    return ""

def downloadImage(imgURL, storageLocation, usedFilesImage, usedImgs):
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    headers={'User-Agent':user_agent,}
    #Assembling the request which we will make the the specified url
    request=urllib.request.Request(imgURL,None,headers)
    #Making the request, and returning the response
    image = urllib.request.urlopen(request)
    
    f = open(usedFilesImage, "a")
    f.write(imgURL + "\n")
    usedImgs.append(imgURL)
    f.close()
    
    #Grabbing the extension from the original url so that we don't change the type of file
    extension = imgURL.split(".")[len(imgURL.split("."))-1]
    #Storing the image locally
    output = open(storageLocation + "RecentImage." + extension,"wb")
    output.write(image.read())
    output.close()
    return usedImgs

def postRecentImage(storageLocation, InstagramAPI):
    AllFiles = os.listdir(storageLocation)
    image = None
    for file in AllFiles:
        if("RecentImage" in file.split(".")):
            image = storageLocation + file
            break
    if(image is None):
        return

    print(image)
    try:
        caption = "Hope you are enjoying your evening!"
        InstagramAPI.uploadPhoto(image, caption=caption)
        time.sleep(60)
        os.remove(image)
    except Exception as e:
        print(str(e))
    


#Initializing the usedImages array
def init(idFilename):
    #Creating an Instagram Object which we will use to post the picture
    IGApi = InstagramAPI("", "")
    #Logging in to Instagram with the credentials
    IGApi.login()

        
    #If the USED_IMAGES_FILENAME is not there, create it
    if(not os.path.isfile(USED_IMAGES_FILENAME)):
        f = open(USED_IMAGES_FILENAME, "w+")
        f.close()

    #Open the file, grab the contents and parse it making an array of the images's we already used
    f = open(USED_IMAGES_FILENAME, "r")
    fileContents = f.read()
    if(fileContents == ""):
        UsedImages = []
    else:
        #Removing the last \n at the end of the string
        fileContents = fileContents[0:len(fileContents)-1]
        UsedImages = fileContents.split("\n")
    f.close()
    return UsedImages, IGApi

if(__name__ == "__main__"):
    PEXELS_URL = "https://www.pexels.com/search/sunset/"
    IMAGE_STORAGE_LOCATION = "/home/jeremy/Desktop/InstagramImages/"
    USED_IMAGES_FILENAME = "UsedImagesFile.txt"
    
    UsedImages, InstagramAPI = init(USED_IMAGES_FILENAME)

    #Getting the raw HTML from the specified url
    pexelsHTML = retrieveWebPageHTML(PEXELS_URL)
    #Getting all the images from the HTML we previously queried for.
    parsedHTMLImgs = parseHTML(pexelsHTML)
    #Refining the Img URLS
    parsedHTMLImgs = refineImageURLS(parsedHTMLImgs)
    #Getting the most recent image
    mostRecentImg = retrieveMostRecentImage(parsedHTMLImgs, UsedImages)
    #Saving the most recent image
    UsedImages = downloadImage(mostRecentImg, IMAGE_STORAGE_LOCATION, USED_IMAGES_FILENAME, UsedImages)
    #Posting the most recent image and updating the UsedImages
    postRecentImage(IMAGE_STORAGE_LOCATION, InstagramAPI)
    mostRecentImage = ""
    time.sleep(10)




    


import music_tag
import os
from os import path
import openai
import json
import time


def callOpenAI(fileTitleWithExtension, APIKey):
    fileTitle = fileTitleWithExtension.rstrip(".mp3")

    openai.api_key = APIKey
    try:
        completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": "give me the metadata including title and artist in the form of a JSON object for this song " + fileTitle}])
    except:
        print("ERROR: error communicating with AI")
    rawString = completion.choices[0].message.content
    try:
        resMetaData = json.loads(rawString)
    except:
        print("ERROR: unable to convert " + rawString + " to dict")
        return
    print("AI Success for " + fileTitle)
    time.sleep(21)
    return resMetaData

def modifyFileData(resMetaData, fileTitleWithExtension, directory):
    try:
        oldFile = path.join(directory, fileTitleWithExtension)
        f = music_tag.load_file(oldFile)
        f['title'] = resMetaData['title']
        f['artist'] = resMetaData['artist']
        f.save()
        os.rename(oldFile, directory + "/" + resMetaData['title'] + ".mp3")
        print("File renamed to " + resMetaData['title'])
    except:
        print("ERROR: unable to modify file data from " + fileTitleWithExtension + " to " + resMetaData['title'])

#Get array of files
def convertMetadata(directory, APIKey):
    dir_list = os.listdir(directory)
    for song in dir_list:
        print("Converting " + song)
        resMetaData = callOpenAI(song, APIKey)
        if resMetaData is not None:
            modifyFileData(resMetaData,song, directory)

def main(directory, APIKey):
    convertMetadata(directory, APIKey)
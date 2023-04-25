import music_tag
import os
from os import path
import openai
import json
from dotenv import load_dotenv
import time

load_dotenv()

def callOpenAI(fileTitleWithExtension):
    fileTitle = fileTitleWithExtension.rstrip(".mp3")

    openai.api_key = os.getenv('OPENAI_API_KEY')
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": "give me the metadata including title and artist in the form of an unnamed python dict for this song " + fileTitle}])
    rawString = completion.choices[0].message.content
    try:
        resMetaData = json.loads(rawString)
    except:
        print("unable to convert " + rawString + " to dict")
        return
    print("AI Success for " + fileTitle)
    time.sleep(21)
    return resMetaData

def modifyFileData(resMetaData, fileTitleWithExtension):
    try:
        oldFile = path.join(directory, fileTitleWithExtension)
        f = music_tag.load_file(oldFile)
        f['title'] = resMetaData['title']
        f['artist'] = resMetaData['artist']
        f.save()
        os.rename(oldFile, directory + "/" + resMetaData['title'] + ".mp3")
        print("File renamed to " + resMetaData['title'])
    except:
        print("unable to modify file data from " + fileTitleWithExtension + " to " + resMetaData['title'])

#Get array of files
directory = "C:/Users/Tyler/Music/TestSongs"
dir_list = os.listdir(directory)
for song in dir_list:
    resMetaData = callOpenAI(song)
    if resMetaData is not None:
        modifyFileData(resMetaData,song)
    


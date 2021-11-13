from pymongo import MongoClient
import certifi

client = MongoClient("mongodb+srv://ttp_coffee_love:9mj2tcB0xhrzxPuV@cluster0.vpotj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority",
                     tlsCAFile=certifi.where()) #host uri
db = client.image_predition #Select the database  
image_details = db.imageData

def addNewImage(i_name,class_name,score,time,url):
    image_details.insert({
        "file_name":i_name,
        "class":class_name,
        "score":score,
        "upload_time":time,
        "url":url
    })
    
def getAllImages():
    data = image_details.find()
    return data
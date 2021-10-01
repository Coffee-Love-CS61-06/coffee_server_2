from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017") #host uri  
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
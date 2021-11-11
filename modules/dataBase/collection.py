from pymongo import MongoClient

client = MongoClient("mongodb+srv://ttp_coffee_love:DPFi0FZhUUBpCNVH@cluster0.vpotj.mongodb.net/test", tls=True, tlsAllowInvalidCertificates=True) #host uri
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
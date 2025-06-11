from pymongo import MongoClient

client = MongoClient("mongodb+srv://sebysurfer:1234@cluster01.yklxoij.mongodb.net/?retryWrites=true&w=majority&appName=Cluster01")


db = client.todo_db #Here you instantiate the name of the database

collection_name = db["todo_collection"]


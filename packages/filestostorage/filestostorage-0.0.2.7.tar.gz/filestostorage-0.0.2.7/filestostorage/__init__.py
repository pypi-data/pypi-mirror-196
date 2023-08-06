import gridfs
import certifi
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
def mongo_conn():
    global url 
    url = input("Enter your MongoUrl:")
    try:
        conn = MongoClient(url,tlsCAFile=certifi.where(),serverSelectionTimeoutMS=5000)
        conn.admin.command('ismaster')
        print("Connected to Database")
        return conn.grid_file
    except ConnectionFailure:
        print("Wrong URL or check with your connection")
def upload_file(file_url,file_name,db1):
    file_location = file_url
    file_data = open(file_location,"rb")
    fs = gridfs.GridFS(db1)
    data = file_data.read()
    fs.put(data,filename = file_name)
    print("upload success")
def download_file(download_path,file_name,db1):
    fs1 = gridfs.GridFS(db1)
    data = db1.fs.files.find_one({'filename':file_name})
    my_id = data['_id']
    outputdata = fs1.get(my_id).read()
    download_location = download_path
    output = open(download_location,"wb")
    output.write(outputdata)
    output.close()
    print('download success')
from flask import Flask, request
from numpy import double
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from load_pyt import exerc
from flask_ngrok import run_with_ngrok
# Flask Constructor
app = Flask(__name__)

# decorator to associate
uri = "mongodb+srv://admin:admin@ecosorter.x4owlln.mongodb.net/?retryWrites=true&w=majority&appName=EcoSorter"
disc_gaz = 0
disc_electricitate = 0
ok = False
# a function with the url
@app.route("/redeem", methods=['POST'])
def redeem():
    if request.method == 'POST':
        res = "ok"
        username = request.form.get('username')
        cod = request.form.get('code')
        print("Received data: ", username, " ", cod)
        # Here you can add the logic to validate the username and password
        #Search if this code exists in the colection Redeen_code
        client = MongoClient(uri, server_api=ServerApi('1'))
        # Send a ping to confirm a successful connection
        try:
            client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
            my_query = {"code": (int)(cod)}
            mydb = client["EcoSorter"]
            mycol = mydb["Redeem_code"]
            mydoc = mycol.find(my_query)
            mydoc = list(mydoc)
            print(len(mydoc))
            if(len(mydoc)==0):
                return "Invalid code"
            else:
                #Add the points to the user
                #delte the code from the collection
                mycol.delete_one(my_query)

                mycol = mydb["accounts"]
                myquery = {"username": username}
                mydoc = mycol.find(myquery)
                mydoc = list(mydoc)
                pointes = (int)(mydoc[0]["points"])
                pointes += 100
                print(pointes)
                #Update with the new points
                myquery = {"username": username}
                newvalues = {"$set": {"points": pointes}}
                mycol.update_one(myquery, newvalues)
                print(mydoc[0]["points"])
                res = (str)(pointes)
        except Exception as e:
            print(e)
            res = "Error"
        print(res)
        return res
@app.route("/location", methods=['POST', 'GET'])
def get_location():
    if request.method == 'POST':
        #Get all the data from location collection
        client = MongoClient(uri, server_api=ServerApi('1'))
        # Send a ping to confirm a successful connection
        try:
            client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
            mydb = client["EcoSorter"]
            mycol = mydb["location"]
            mydoc = mycol.find()
            mydoc = list(mydoc)
            Lat_and_Long = {}
            for x in mydoc:
                print(x['latitude'], " ",  x['longitude'] )
                Lat_and_Long[x['latitude']] = x['longitude']
            print("Login successful ")
            print(Lat_and_Long)
            ok = True
            return Lat_and_Long
        except Exception as e:
            print(e)
            return "Error"

@app.route("/raw_", methods=['POST'])
def add_points():
    if request.method == 'POST':
        raw = request.args.get('raw')
        print(raw)
        return "Traume"
@app.route("/ard", methods=['POST'])
def ardu():
    if ok == True:
        if request.method == 'POST':
            result = exerc()
            if result is None:
                return "No plastic detected"
            else:
                return result
    else:
        return "Error"
if __name__ == "__main__":
    app.run(host="192.168.100.31")

from pymongo import MongoClient


MONGO_URI = "mongodb+srv://SpaceWalletRootUser:VvhEnifxJUkA4918@clusterspacewallet.kwbw5gv.mongodb.net/?retryWrites=true&w=majority&appName=ClusterSpaceWallet"
client = MongoClient(MONGO_URI)
db = client['security']
users_collection = db['users']
from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

items = []

# Requests for specific item 
class Item(Resource):
    def get(self,name):
        #filter item from list of items
        #next returns first occurence of the item else error
        # hence using default value as None 
        item = next(filter(lambda x : x['name']==name,items),None)
        return {'item': item}, 200 if item else 400
        

    def post(self,name):
        #check if the item is aleady present --> Bad Request 404
        if next(filter(lambda x : x['name']==name,items),None):
            return { "message": "An item with name '{}' already exists.".format(name)}, 400

        # accessing json payload from requests
        data = request.get_json() # expects client give json in request else errors.
        # to avoid error use
        # request.get_json(force=True) --> don't look at header, always do processing.
        # request.get_json(silent=True) --> returns none incase of error
        item = {"name":name,"price":data["price"]}
        items.append(item)
        return item, 201

# Itemlist to get all the items.
class ItemList(Resource):
    def get(self):
        return {"items":items}

# End points
api.add_resource(Item,'/item/<string:name>')
api.add_resource(ItemList,'/items')

# Setting to debug mode --> html page with Error logs
app.run(port=5000,debug=True)
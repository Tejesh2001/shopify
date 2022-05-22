from unittest import result
from flask import Flask, request, render_template
app = Flask(__name__)



import uuid

#Lets say each item has an id,
#I am using uuid to generate unique id 



warehouseDict = {}
itemDict = {}

class Warehouse:
    

    def __init__(self, name, itemList = None):
        self.name = name
        self.itemList = list(itemList)

    def getName(self):
        return self.name

    def getItems(self):
        return self.itemList

    def addItem(self, item):
        self.itemList.append(item)

    def removeItem(self, item):
        self.itemList.remove(item)
    
    
class Item:

    def __init__(self):
        self.id = str(uuid.uuid1())
        self.attributes = {}
        self.attributes['id'] = self.id
    
    def print(self):
        return self.attributes
    
    def getId(self):
        return self.id

    def edit(self, att, newV):
        self.attributes[att] = newV

    
    

@app.route("/")
def hello():
  return """<h1> Welcome to my submission of the shopify backend challenge </h1>
    <ul>
    Please type in the route you want:-
    <li> create = creates item </li>
    <li> edit = takes you to a form page where you can edit item </li> 
    <li> delete = deletes item </li> 
    <li> show = shows all items in inventory list</li> 
    <li> warehouse = allows you to add or delete items in a warehouse. Also allows you to create a warehouse if one isn't made </li> 
    </ul>
    
  <p> Example route for replit: https://shopify.tejeshbhaumik2.repl.co/create </p>
  """

@app.route("/create")
def createObject():
    item = Item()
    itemDict[str(item.getId())] = item
    return f"Item has been created with id  {item.getId()}"

@app.route("/edit", methods = ['POST', 'GET'])
def editObject():
    if request.method == 'GET':
        return render_template('edit.html')
        
    if request.method == 'POST':
        form_data = request.form
        id = form_data['id']
        att = form_data['attribute']
        newV = form_data['value']
        if id not in itemDict:
            return "Error: item id not in inventory list"

        item = itemDict[id]
        item.edit(att, newV)
        itemDict[item.getId()] = item
        return "Item has been edited"

@app.route("/delete",  methods = ['POST', 'GET'])
def deleteObject():
    if request.method == 'GET':
        return render_template('delete.html')
    if request.method == 'POST':
        itemDict.pop(id)
        return f"Item with id {id} has been removed"


@app.route("/show")
def showObjects():

    return render_template('template.html', my_list = list(itemDict.values()))

@app.route("/warehouse", methods=['GET', 'POST'])
def createWarehouse():

    if request.method == 'GET':
        return render_template('warehouse.html')
        
    if request.method == 'POST':
        form_data = request.form
        name = form_data['name']
        itemID = form_data['id']
        option = form_data['option']

        if itemID not in itemDict:
            return "Error: item id not in inventory list"

        item = itemDict[itemID]

        if option == 'delete':
            if name not in warehouseDict:
                return "warehouse doesn't have any items"
            warehouse = warehouseDict[name]
            warehouse.removeItem(item)
            warehouseDict[name] = warehouse
        else:
            if name not in warehouseDict:
                warehouse = Warehouse(name,[item])
                warehouseDict[name] = warehouse
            else:
                warehouse = warehouseDict[name]
                warehouse.addItem(item)
                warehouseDict[name] = warehouse


        return render_template('warehouseList.html', result = warehouseDict)
    



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=20)

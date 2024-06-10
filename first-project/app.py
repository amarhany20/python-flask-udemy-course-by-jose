import uuid

from flask import Flask, request
from flask_smorest import abort

from db import items, stores

app = Flask(__name__)


# Store API Routes

@app.get('/store')
def get_stores():
    return {"stores": list(stores.values())}


@app.get('/store/<int:store_id>')
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        abort(404, message="Store not found.")


@app.post('/store')
def create_store():
    store_data = request.get_json()

    if "name" not in store_data:
        abort(400, message="Missing 'name' parameter")
    for store in stores.values():
        if store["name"] == store_data["name"]:
            abort(400, message="Store already exists")
    store_id = uuid.uuid4().hex

    new_store = {**store_data, "id": store_id}
    stores[store_id] = new_store
    return new_store, 201


@app.delete('/store/<int:store_id>')
def delete_store(store_id):
    try:
        del stores[store_id]
        return {"message": "Store deleted"}
    except KeyError:
        abort(404, message="Store not found.")


# Item API Routes
 
@app.get('/item')
def get_all_items():
    return {"stores": list(items.values())}


@app.get('/item/<int:item_id>')
def get_item(item_id):
    # if item_id not in items:
    #     return {'message':'Item not found'}, 404
    # return items[item_id],201
    try:
        return items[item_id], 201
    except KeyError:
        abort(404, message='Item not found.')


@app.post('/item')
def create_item():
    item_data = request.get_json()
    if (
            "price" not in item_data
            or "store_id" not in item_data
            or "name" not in item_data
    ):
        abort(400,
              message="Bad request. Ensure 'price', 'store_id' and 'name' fields are included in the JSON payload.")

    for item in item_data.values():
        if item_data["name"] == item["name"] and item_data["store_id"] == item["store_id"]:
            abort(400, message=f"Item already exists.")

    if item_data["store_id"] not in stores:
        abort(404, message='Store not found.')

    item_id = uuid.uuid4().hex
    item = {**item_data, "item_id": item_id}
    items[item_id] = item
    return item, 201


@app.delete('/item/<int:item_id>')
def delete_item(item_id):
    try:
        del items[item_id]
        return {"message": "Item deleted"}
    except:
        abort(404, message="Item not found.")


@app.put('/item/<int:item_id>')
def update_item(item_id):
    item_data = request.get_json()
    if "price" not in item_data or "name" not in item_data or "store_id" not in item_data:
        abort(400,
              message="Bad Request. Enusre 'price', 'store_id' and 'name' fields are included in the JSON payload.")

    try:
        item = items[item_id]
        item |= item_data
        return item, 201
    except KeyError:
        abort(404, message="Item not found.")


if __name__ == '__main__':
    app.run()

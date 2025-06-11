'''
NoSQL databases send our models over to JSON, but it'll
be hard for python to use this as an object.

We will need to serialize and descerailize the NoSQL information
into something we can use into our appplication, the same way when
we have to make an update and send our class information to
a descent NoSQL information.

To create this serializer, we're going to convert our Todo Object into
a dictionary so we can see the ids and keys of each item.


'''

def individual_serial(todo) -> dict:
    return {
        "id": str(todo["_id"]), #MondoDB specific way to find a column/key and get the value
        "name": todo["name"],
        "description": todo["description"],
        "complete": todo["complete"]

    }

def list_serial(todos) -> list:
    return[individual_serial(todo) for todo in todos]

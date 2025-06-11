
#Lesson 1: Basics of FastAPI and creating apis *************************************************************************
'''
Important Notes:

FastAPI = Framework
Uvicorn = Swagger, its a set of tools that helps automatically generate interactive documentation
to test apis
    -> To run the swagger (Uvicorn):
    uvicorn FILE_NAME:OBJ_INSTANCE_NAME --reload

ps: '--reload' makes updates automatically on the server of uvicorn without you
having to run it again in the terminal.

'''




from fastapi import FastAPI

app = FastAPI()  #It is equal to creating an instance object of FastAPI, it can be any name really

'''
this is a normal function for an api, however, 
to make sure FastAPI knowns this is a "get" method, we need to 
call out the instance object of FastAPI and tell the type of request we're making
by a specific annotation (or rule)

This is how the framework of FastAPI workes, for each different framework, it has 
a different set of rules to define how to make apis 'their' way. This is the same
reason why FastAPI is so fast and easy to use. 

def read_api():
    return {"welcome" : "Seby"}

QuickNote: We don't even have to write code for validating data, 
pydantic (a powerful tool integrated in FastAPI) does it for us, so we 
can center our attention on the structure and functionality of our app than 
the technical tweekings of each api.     
    
'''



@app.get("/")
def read_api():
    return {"welcome": "Seby"}


#Lesson 2: Path Parameter **********************************************************************************************
'''
A path parameter is just a way for us to be able to manipulate code 
of any request method by passing a specific data beforehand. 

1. We can name path parameters in any way possible
2. We can have the same request type, only with different path parameters 
3. We can have the same path parameters, only with different request type
4. Names of the functions does NOT make any difference

'''
#(This is just to show that it gives different paths)
@app.get("/name")
def another():
    return {"welcome": "Namei"}

'''
Inputting data:
    @app.REQUEST_TYPE("/PATH/{DATA}")
    def FUNCTION(DATA: DATA_TYPE):
    <Use DATA however you want>

'''
#Example:
@app.get("/input/{name}")
def welcome_api(name: str):
    return{'Welcome': name}

# Lesson 3: Python Objects / JSON **************************************************************************************
'''
We will be using Pydantic as our data validation. Threfore when we create a new 
class or object that is going to be consumed by a request method, our pydantic
will be able to validate the data before manipulating any of the application.

And yes, pydantic will be doing this all for us so we don't have to do it. 

- We can just focus more on code
- Allow FastAPI and pydantic to do everything else behind scenes
'''
#This is how to import
from pydantic import BaseModel, Field #Field is to set rules for the input, being the field

#For using ids, or more so using unique identifiers, we do anoother type of importation:
from uuid import UUID

class Book(BaseModel):
    id: UUID
    title: str = Field(min_length=1, max_length=30) #Pydantic will arppove this validation
    description: str = Field(max_length=100)
    rating: int = Field(gt=-1, lt=6)

'''
Now to apply this example, we need to create a list of objects.

In real-world application, this list will be our database, and for every api, 
we'll be calling our database and doing certain actions upon it, being the 
CRUD. 

'''

BookDataBase = []

@app.post("/book")
def create_book(book: Book):
    BookDataBase.append(book)
    return book

@app.get("/book")
def book_list():
    return BookDataBase

'''
Before we continue, you might of realized that every time we create an object only using UUID, its not 
different for every instance. This is because UUID is a class that only HOLDS the unique identifier, 
but we need to provide a function to make unique ids, being the uuid4 (version 4). 

There are 5 different versions, some that were intended to be more upgraded than others, to create no determinism, or 
maintain determinism. Overall:

- v4 = Undeterministic randomness, extremely low chance of collisions, and always generates a different ID even if the 
same name is given 
- v5 =  Deterministic repetitiveness, generating the same ID only for the same name, and useful for caching or indexing  

How to use it:
UUID = Field(default_factory=uuid4)

'''
#How to import:
from uuid import uuid4



# Lesson 4: HTTP Exceptions ********************************************************************************************
'''

We also need to catch errors that we create using business logic that maybe 
pydantic wont catch. 

'''

#How to import:
from fastapi import HTTPException

@app.put("/{book_id}")
def update_book(book_id: UUID, book: Book):
    counter = 0
    for x in BookDataBase:
        counter+=1
        if x.id == book_id:
            BookDataBase[counter - 1] = book
            return BookDataBase[counter - 1 ]
        # so if in our list there is no uuid to be found, we want to return a
        # status code that describes that it is not found
    raise  HTTPException (
        status_code=404, detail=f"ID {book_id} : Does not exist"
    )

@app.delete("/{book_id}")
def delete_book(book_id: UUID):
    counter = 0
    for x in BookDataBase:
        counter+=1
        if x.id == book_id:
            del BookDataBase[counter - 1]
            return f"Removed {book_id}"
    raise  HTTPException (
        status_code=404, detail=f"ID {book_id} : Does not exist"
    )

#Lesson 5: Response Models *********************************************************************************************
'''
Response models are exactly the same thing as normal models/classes from BaseModels, please, dont injure yourself by 
trying to confuse yourself. The purpose of these kind of models is to adapt the original one to certain needs or criteria. 

For example, if you have an internal logic were you keep passing all the data of the user for every type of action, 
i won't think its very efficient when it comes to security, because you'll also be passing sensitive information, like 
passwords, that isn't needed in what you're asking for.

Or what if you you're asking for a GET request on a profile on a social platform, of course you wont be receiving its 
password or current ip address. This is why we create "Response" Models, to adapt our models that we create to its 
response scenario. Continuing in the example, we should create a "PublicUser" Model for the original model "User".

The only thing we do different with Response Models, we integrate it after we create the path parameter

    @app.REQUEST_TYPE("/PATH/{DATA}", response_model=RESPONSE_MODEL)

'''

#Setting the example:


class User(BaseModel):
    username: str
    email: str
    password: str # --> This criteria is sensitive information

#RESPONSE MODEL:

class PublicUser(BaseModel):
    username: str
    email: str

#Created a predefined user
UsersList = [User(username="john_doe", email="john@example.com", password="secret")]


@app.get("/user/{username}", response_model=PublicUser) #Once the return statement is executed, FastAPI will model it to the PublicUser
def get_user(name:str):
    for x in UsersList:
        if x.username == name:
            return x  #It returns a full model that includes a password on its own before it gets filtered by the response model


#See how PublicUser affects how the api returns the "user" that was just created
@app.post("/user", response_model=PublicUser)
def create_user(user: User):
    UsersList.append(user)
    return user

'''
Activity! Try removing the 'PublicUser' and see what happens
'''


#Lesson 6: Extra *******************************************************************************************************

'''
Using -> return_type:

    def get_user() -> PublicUser:
        ...

This is a Python type hint that tells your editor, linters, and tools of python that this function should return a 
PublicUser object, but its not validated through FastAPI. 

Recommended approach: do NOT use the '->' return type, because it avoids completely pydantic incredible validation.

'''





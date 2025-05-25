
#Lesson 1: Basics of FastAPI and creating apis
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


#Lesson 2: Path Parameter
'''
A path parameter is just a way for us to be able to manipulate code 
of any request method by passing a specific data beforehand. 

1. We can name path parameterns in any way possible
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

# Lesson 3: Python Objects / JSON
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




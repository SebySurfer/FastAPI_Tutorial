
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







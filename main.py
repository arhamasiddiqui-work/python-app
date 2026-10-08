# def main():
#     print("Hello from fastapi-app!")


# if __name__ == "__main__":
#     main()





from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI()

# @app.get("/api/test")
# def readItem():

#     name:str = "Arhama";
#     desc:str = f"Hello I'm {name} and I'm testing FastAPI with Python. This is a simple API endpoint that returns a greeting message."
#     print(desc)

#     return {"message": desc}

# @app.post("/api/test")
# def createItem(list: dict):
#     list = {
#         "name": "arhama",
#         "IsWorking": True,
#     }
#     print(list)
#     return {"message":list}


# @app.post("/api/test")
# def asdasd():
#     print()
#     return "asdasdasd";


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: str | None = None):
#     return {"item_id": item_id, "q": q}







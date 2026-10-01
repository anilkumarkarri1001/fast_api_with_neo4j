from fastapi import FastAPI 
app = FastAPI() 

@app.get("/")
def home():
    return {"message":"fastAPI is running"}

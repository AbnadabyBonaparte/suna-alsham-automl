from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "SUNA online com sucesso!"}

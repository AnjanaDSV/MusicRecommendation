from fastapi import FastAPI

# Initialize the FastAPI app
app = FastAPI()

# Example endpoint
@app.get("/")
def read_root():
    return {"message": "Hello World"}

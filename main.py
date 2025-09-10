from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI()

@app.get("/")
async def home():
    return FileResponse("templates/home.html")

@app.get("/privacy")
async def privacy_policy():
    return FileResponse("templates/privacy.html")

@app.get("/termsconditions")
async def terms_and_conditions():
    return FileResponse("templates/terms.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=443)
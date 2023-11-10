import uvicorn
from fastapi import FastAPI
from .cadastre import cadastre
from .server import server

app = FastAPI()
app.mount("/cadastre/", cadastre)
app.mount("/server/", server)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

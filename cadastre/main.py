import uvicorn
from fastapi import FastAPI
from sqladmin import Admin

from .database import engine
from .cadastre import cadastre
from .server import server
from .admin import QueryAdmin

app = FastAPI()
app.mount("/cadastre/", cadastre)
app.mount("/server/", server)


# Регистрация админ-панели
admin = Admin(cadastre, engine)
admin.add_view(QueryAdmin)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

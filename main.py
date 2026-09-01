from fastapi import FastAPI

from routes.auth_routes import router as auth_router

from routes.user_routes import router as user_router

from routes.document_routes import router as document_router

from routes.knowledge_base_routes import router as knowledge_router

from routes.chat_routes import router as chat_router
app = FastAPI(
    title="PrivateGPT Enterprise API"
)
app.include_router(
    chat_router,
    prefix="/chat",
    tags=["Chat"]
)
       
@app.get("/")
def home():

    return {

        "message": "PrivateGPT Enterprise API",

        "docs": "/docs"

    }


app.include_router(
    auth_router,
    prefix="/auth",
    tags=["Authentication"]
)

app.include_router(
    user_router,
    prefix="/user",
    tags=["User"]
)
app.include_router(
    document_router,
    prefix="/documents",
    tags=["Documents"]
)
app.include_router(
    knowledge_router,
    prefix="/knowledge-bases",
    tags=["Knowledge Bases"]
)
import os
import dotenv
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.configs.dotenv import load_enviroment_variables
from app.configs.docs import FASTAPI_DOC_CONFIG
from app.routes import router

# Load environment variables
load_enviroment_variables()

# Define app instance
app = FastAPI(**FASTAPI_DOC_CONFIG)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router)


# Run app
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=int(
        os.environ.get("PORT", 7860)), log_level="debug")

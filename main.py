import os
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from app.configs.dotenv import load_enviroment_variables
from app.configs.docs import FASTAPI_DOC_CONFIG
from app.routes import router
from app.utils.response import response

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


@app.exception_handler(HTTPException)
async def http_exception_handler(_, exc):
    return ORJSONResponse(
        status_code=exc.status_code,
        content=response(
            code=exc.status_code,
            message=str(exc.detail),
            data=None,
            error=exc.detail if exc.status_code == 404 else None
        )
    )


# Run app
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=int(
        os.environ.get("PORT", 7860)), log_level="debug")

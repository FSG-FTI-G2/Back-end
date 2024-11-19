# Run the server with Docker
# This scripts help docker using gpu

# ---- Create Volume ----
# Redis
docker volume create chatbot-redis-data
# MongoDB
docker volume create chatbot-mongodb-data
# Qdrant
docker volume create chatbot-qdrant-data
# MinIO
docker volume create chatbot-mino-data
# Ollama
docker volume create chatbot-ollama-model
# Celery
docker volume create chatbot-celery-cache

# ---- Run Docker ----
# Redis
docker run -d --name chatbot-redis -p 6379:6379 -v chatbot-redis-data:/data redis/redis-stack-server:latest
# Celery
docker build -t chatbot-celery-worker ~/deployment/finbot/celery
docker run -d --name chatbot-celery-worker --gpus all -e HF_HOME=/cache/huggingface -v chatbot-celery-cache:/cache/huggingface chatbot-celery-worker
# MongoDB
docker run -d --name chatbot-mongodb -p 27017:27017 -v chatbot-mongodb-data:/data/db -v ~/deployment/finbot/.docker/mongodb-config:/data/configdb mongodb/mongodb-community-server:latest
# MinIO
docker run -d --name chatbot-minio -p 9000:9000 -p 9001:9001 -v chatbot-mino-data:/data -e MINIO_ROOT_USER=adminuser -e MINIO_ROOT_PASSWORD=adminuser minio/minio server --console-address ":9001" /data
# Qdrant
docker run -d --name chatbot-qdrant -p 6333:6333 -p 6334:6334 -v chatbot-qdrant-data:/qdrant/storage qdrant/qdrant:latest
# Ollama
docker run -d --name chatbot-ollama --gpus all -p 11434:1143 -v chatbot-ollama-model:/root/.ollama -v ~/deployment/finbot/.docker/ollama-entrypoint.sh:/entrypoint.sh -e OLLAMA_KEEP_ALIVE=24h ollama/ollama:latest
# FastAPI
docker build -t chatbot-app-image ~/deployment/finbot
docker run -d --name chatbot-app -p 7860:7860 -e MINIO_ACCESS_KEY=adminuser -e MINIO_SECRET_KEY=adminuser chatbot-app-image
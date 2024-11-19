# Run the server with Docker
# This scripts help docker using gpu

# ---- Ports ----
get_free_port() {
    local port=$1
    while ss -tulwn | grep -q ":$port"; do
        port=$((port + 1))
    done
    echo $port
}
REDIS=$(get_free_port 6379)
MONGODB=$(get_free_port 27017)
MINIO=$(get_free_port 9000)
MINIO_CONSOLE=$(get_free_port 9001)
QDRANT=$(get_free_port 6333)
QDRANT_GRPC=$(get_free_port 6334)
OLAMA=$(get_free_port 11434)
FASTAPI=$(get_free_port 7860)


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
docker run -d --name chatbot-redis -p $REDIS:6379 -v chatbot-redis-data:/data redis/redis-stack-server:latest
# Celery
docker build -t chatbot-celery-worker ~/deployment/finbot/celery
docker run -d --name chatbot-celery-worker --gpus all -e HF_HOME=/cache/huggingface -v chatbot-celery-cache:/cache/huggingface chatbot-celery-worker
# MongoDB
docker run -d --name chatbot-mongodb -p $MONGODB:27017 -v chatbot-mongodb-data:/data/db -v ~/deployment/finbot/.docker/mongodb-config:/data/configdb mongodb/mongodb-community-server:latest
# MinIO
docker run -d --name chatbot-minio -p $MINIO:9000 -p $MINIO_CONSOLE:9001 -v chatbot-mino-data:/data -e MINIO_ROOT_USER=adminuser -e MINIO_ROOT_PASSWORD=adminuser minio/minio server --console-address ":9001" /data
# Qdrant
docker run -d --name chatbot-qdrant -p $QDRANT:6333 -p $QDRANT_GRPC:6334 -v chatbot-qdrant-data:/qdrant/storage qdrant/qdrant:latest
# Ollama
docker run -d --name chatbot-ollama --gpus all -p $OLAMA:1143 -v chatbot-ollama-model:/root/.ollama -v ~/deployment/finbot/.docker/ollama-entrypoint.sh:/entrypoint.sh -e OLLAMA_KEEP_ALIVE=24h ollama/ollama:latest
# FastAPI
docker build -t chatbot-app-image ~/deployment/finbot
docker run -d --name chatbot-app -p $FASTAPI:7860 -e MINIO_ACCESS_KEY=adminuser -e MINIO_SECRET_KEY=adminuser chatbot-app-image

# ---- After scripts ----
# Install Ollama model
docker exec -it chatbot-ollama ollama pull llama3.2

# ---- Print Ports ----
echo "🚀 Startup Ports"
echo "Redis: $REDIS"
echo "MongoDB: $MONGODB"    
echo "MinIO: $MINIO; Console: $MINIO_CONSOLE"
echo "Qdrant: $QDRANT, gRPC: $QDRANT_GRPC"
echo "Ollama: $OLAMA"
echo "FastAPI: $FASTAPI"
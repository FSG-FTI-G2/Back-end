# Stop the server with Docker
# This scripts help docker using gpu

# ---- Stop Docker ----
# Redis
docker stop chatbot-redis
docker rm chatbot-redis
# Celery
docker stop chatbot-celery-worker
docker rm chatbot-celery-worker
# MongoDB
docker stop chatbot-mongodb
docker rm chatbot-mongodb   
# MinIO
docker stop chatbot-minio
docker rm chatbot-minio
# Qdrant
docker stop chatbot-qdrant
docker rm chatbot-qdrant
# Ollama
docker stop chatbot-ollama
docker rm chatbot-ollama
# FastAPI
docker stop chatbot-app
docker rm chatbot-app
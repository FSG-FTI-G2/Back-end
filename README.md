# Document Retrieval APIs

### Quick start

> ⚠️ Get the .env file before run

1. Start with Docker Compose

- Start Application

```sh
docker compose up
```

- Develop synthensis

```sh
docker compose watch
```

2. Run Application Locally

- Run Qdrant VectorDB locally. [Detail](https://qdrant.tech/documentation/quickstart/)

```sh
# Create Docker volume
docker volume create qdrantdata
# Start Qdrant container
docker run --rm -d --name qdrant -p 6333:6333 -p 6334:6334 -v qdrantdata:/qdrant/storage:z qdrant/qdrant
```

- Run MongoDB locally. [Detail](https://www.mongodb.com/docs/manual/tutorial/install-mongodb-community-with-docker/)

```sh
# Create Docker volume
docker volume create mongodbdata
# Start Mongodb container
docker run --rm -d --name mongodb -p 27017:27017 -v mongodbdata:/data/db mongodb/mongodb-community-server:latest
```

- Run MinIO locally.

```sh
# Create Docker volume
docker volume create miniodata
# Start MinIO container
docker run --rm -d --name minio -p 9000:9000 -p 9001:9001 -v miniodata:/data -e MINIO_ROOT_USER=user -e MINIO_ROOT_PASSWORD=user_123123 minio/minio server --console-address ":9001" /data
```

- Start Uvicorn Server

```sh
# Start application
c

# Start application with reload detector
uvicorn main:app --port 7860 --reload
```

### Run test

```sh
python -m unittest discover -s ./test -p 'test_*.py'
```

### Containers

- FastAPI APIs
- MongoDB
- Qdrant

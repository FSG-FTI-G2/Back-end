# FinTech Bot Document Retrieval

### 🚀 How to run

1. Running locally

```sh
docker compose -f docker-compose.yml up -d
```

2. Running in server

- Connect to server via SSH (Linux)

```sh
ssh <username>@<vm_ip_address>
```

- Create an ssh key with (Server)
  - name: `finbot.ssh`.
  - passphase: ` `.

```sh
# Create a key
# This action will create 2 keys:
# - Private key
# - Public key .pub
ssh-keygen -t ed25519 -C "your-email@example.com"
# Show the public key
cat ~/.ssh/finbot.ssh.pub
```

- Config the Github Deploy keys

> Go to repository > Settings > Deploy keys > Add deploy key

- Clone the repository in server

```sh
git clone --single-branch -b develop git@github.com:FSG-FTI-G2/Back-end.git be
```

3. Running in server with CI/CD

- Create an ssh in server (Above step)

- Start Jenkins

```sh
docker compose -f .jenkins/docker-compose.yml up -d
# Open Jenkins in http://localhost:8080
# Show the initialize jenkins password
docker exec -it chatbot-jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

- Create `ngrok` port-forward

```sh
ngrok http 8080
```

- (Optional) Run Jenkins in Server

```sh
# Create volume
docker volume create chatbot-jenkins-data
# Run container
docker run -d --name chatbot-jenkins -p 8443:8080 -p 50000:50000 --restart on-failure -v chatbot-jenkins-data:/var/jenkins_home jenkins/jenkins:lts-jdk17
```

- Config url to Github webhooks

> Go to repository > Settings > Webhooks > Add webhook

Enter url: `<your-url>/github-webhook/`

- Config Credentials in Jenkins

> Go to Dashboard > Manage Jenkins > Credentials > Domain global > Add Credentials > SSH Username with private key > Enter the form

> **Form**: ID: `finbot.ssh`,

- Open Jenkins and create a pipeline

- Run the Pipeline

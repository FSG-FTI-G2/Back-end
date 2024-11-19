# FinTech Bot Document Retrieval

> The `.env` file is super secret, only Admin can be access. To run below, you must included the `.env` file in the project directory.

### 🚀 How to run

1. Running locally

```sh
docker compose -f docker-compose.yml up -d
```

2. Running in server

- Initialize `.env` file in server (First time)

```sh
# Create deployment directory
mkdir -p ~/deployment
# Copy env file
scp .env <username>@<server_host>:~/deployment/.env
```

- Connect to server via SSH

```sh
ssh <username>@<server_host>
```

- Create an ssh key (First time)
  - name: `finbot.ssh`.
  - passphase: ` `.

```sh
# Change directory to .ssh
cd ~/.ssh
# Create a key
ssh-keygen -t ed25519 -C "your-email@example.com"
# Show the public key
cat ~/.ssh/finbot.ssh.pub
# Grant permision for ssh
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/finbot.ssh
```

- Config the Github Deploy keys (First time)

> Go to repository > Settings > Deploy keys > Add deploy key

- Clone the repository in server (First time)

```sh
# Change directory
cd ~/deployment
# Clone repository
git clone --single-branch -b develop git@github.com:FSG-FTI-G2/Back-end.git finbot
```

- Run server

```sh
# Change directory
cd ~/deployment/finbot
# Copy env file
cp ~/deployment/.env ~/deployment/finbot/.env
# Docker compose
docker compose -f docker-compose.yml up -d
```

3. Running in server with CI/CD

- Extended from above option (First time)

  - Initialize `.env` file in server
  - Create an ssh key

- Copy `.jenkins` directory to server

```sh
cd ~/deployment
scp -r .jenkins <username>@<server_host>:~/deployment/.jenkins
```

- Connect to server via SSH

```sh
ssh <username>@<server_host>
```

- Start Jenkins

```sh
cd ~/deployment/.jenkins
bash jenkins-start.sh
```

- Open Jenkins and Setup

  - Enter `initialAdminPassword`
  - Install plugins
  - Go to Manages Jenkins > Plugins > Available plugins > Search `SSH Pipeline Plugin` and install

- Config url to Github webhooks

> Go to repository > Settings > Webhooks > Add webhook > Enter url `http://<server_host>:8443/github-webhook/`

- Create Github Access Token

> Go to `https://github.com/settings/tokens` > Generate new token (Classic) > Name: `finbot-jenkins`, `repo` option.

- Config Jenkins credentials

> Go to Manage Jenkins > Credentials > global > Add Credentials > Username with password > Username: `<github-id>`, Password: `access-token`, ID: `finbot-github-accesstoken`

> Go to Manage Jenkins > Credentials > global > Add Credentials > Username with password > Username: `<server_username>`, Password: `<server_password>`, ID: `finbot-azure-ssh`

> Go to Manage Jenkins > Credentials > global > Add Credentials > Secret text > Secret: `<server_host>`, ID: `finbot-azure-hostip`

- Create a pipeline

  - New Item, name: `finbot-pipeline`
  - Select Pipeline option
  - Select `GitHub hook trigger for GITScm polling` in Build Triggers
  - Select `Pipeline script from SCM` in Pipeline Definition
  - Select `Git` in Pipeline SCM
  - Enter repository url `https://github.com/FSG-FTI-G2/Back-end.git`
  - Select created Credentials
  - Branch `*/develop`
  - Script Path `.jenkins/Jenkinsfile`

### 🖥️ Server Setup

- Copy server setup script

```sh
scp azure/setup.sh <username>@<server_host>:~/setup.sh
```

- Connect to server via SSH

```sh
ssh <username>@<server_host>
```

- Run installation

```sh
chmod +x setup.sh
bash ~/setup.sh
```

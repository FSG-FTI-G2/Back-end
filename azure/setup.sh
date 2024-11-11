# Setup server manually scripts

# 0. Change directory
# cd /home/fpt_mbi_idp_vm1/.ssh

# 1. Create ssh key
# ssh-keygen -t rsa -b 4096 -C "quangminh57dng@gmail.com"

# 2. Enter name: "fsg.fti.g2", no passphrase

# 3. Show the ssh.pub
# cat fsg.fti.g2.pub

# 5. Verify ssh key
# eval "$(ssh-agent -s)"
# ssh-add fsg.fti.g2
# ssh -T git@github.com

# 6. Change directory
cd /home/fpt_mbi_idp_vm1/llm-ailab

# 7. Clone the repository
git clone --single-branch --branch develop git@github.com:FSG-FTI-G2/Back-end.git be
cd be

# 8. Restart Docker for nvidia container toolkit
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker

# Docker compose
docker compose -f ./azure/docker-compose.yml up
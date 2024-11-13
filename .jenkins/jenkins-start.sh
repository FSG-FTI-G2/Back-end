# Run jenkins in server
# Create a volume to persist data
docker volume create chatbot-jenkins-data
# Run jenkins in server
docker run -d -p 8443:8080 -p 50000:50000 --name chatbot-jenkins -v chatbot-jenkins-data:/var/jenkins_home jenkins/jenkins:lts-jdk17
# Get the initial password
docker exec -it chatbot-jenkins cat /var/jenkins_home/secrets/initialAdminPassword
FROM jenkins/jenkins:latest

LABEL MAINTAINER="Your name <your-email>"

# Disable the Setup Wizard
ENV JAVA_OPTS -Djenkins.install.runSetupWizard=false

# Config file for Jenkins
ENV CASC_JENKINS_CONFIG /var/jenkins_home/casc.yaml

# All the plugins required for Jenkins pipeline
COPY plugins.txt /usr/share/jenkins/ref/plugins.txt

# Settings for Jenkins
COPY casc.yaml /var/jenkins_home/casc.yaml

# Install all the plugins
RUN jenkins-plugin-cli -f /usr/share/jenkins/ref/plugins.txt

# Update and install the docker so can build image and everything else
RUN apt-get update && curl -sSL https://get.docker.com/ | sh
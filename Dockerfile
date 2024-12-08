FROM jenkins/jenkins:lts

USER root

RUN apt-get update

# Terraform CLI telepítése
RUN apt-get install -y wget unzip && \
    wget https://releases.hashicorp.com/terraform/1.6.0/terraform_1.6.0_linux_amd64.zip && \
    unzip terraform_1.6.0_linux_amd64.zip -d /usr/local/bin && \
    rm terraform_1.6.0_linux_amd64.zip

# Python könyvtárak telepítése
RUN apt-get install -y python3-pip
RUN apt-get install python3-pytest python3-flask python3-prometheus-client python3-requests -y

# Docker CLI telepítése
RUN apt-get install -y apt-transport-https ca-certificates curl gnupg2 software-properties-common
RUN curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add -
RUN add-apt-repository --remove "deb [arch=amd64] https://download.docker.com/linux/ubuntu sylvia stable"
RUN apt-get update
RUN add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu xenial stable"
RUN apt-get update && apt-get install -y docker-ce-cli

# Create the docker group
RUN groupadd -f docker

# Add jenkins user to the docker group
RUN usermod -aG docker jenkins

# Install sudo if not already present
RUN apt-get update && apt-get install -y sudo

# Allow jenkins user to run specific commands with sudo without password
RUN echo "jenkins ALL=(ALL) NOPASSWD: /usr/bin/chown" >> /etc/sudoers.d/jenkins

# Set up entrypoint script
COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Switch to jenkins user
USER jenkins

ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
CMD ["/usr/bin/tini", "--", "/usr/local/bin/jenkins.sh"]

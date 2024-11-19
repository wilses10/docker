# Base image
FROM ubuntu:20.04

# Set non-interactive mode to prevent issues during installation
ENV DEBIAN_FRONTEND=noninteractive

# Update packages and install dependencies
RUN apt-get update && apt-get install -y \
    openssh-server \
    python3 \
    python3-pip \
    mysql-server \
    curl \
    vim \
    && apt-get clean

# Install Python dependencies
RUN pip3 install flask pymysql

# Configure SSH
RUN mkdir /var/run/sshd
RUN echo 'root:database007' | chpasswd
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config

# Optional: Create a non-root user
RUN useradd -ms /bin/bash william && echo "william:database007" | chpasswd

# Add MySQL initialization script
COPY mysql-init.sql /docker-entrypoint-initdb.d/

# Expose necessary ports
EXPOSE 22 3306

# Start SSH and MySQL services
CMD ["bash", "-c", "service mysql start && /usr/sbin/sshd -D"]


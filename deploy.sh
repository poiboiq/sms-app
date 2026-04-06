#!/bin/bash
# ============================================================
# EC2 Deployment Script - Student Management System
# Run these commands on your EC2 instance via SSH
# ============================================================

# 1. Update system
sudo apt update -y && sudo apt upgrade -y

# 2. Install MySQL
sudo apt install mysql-server -y
sudo systemctl start mysql
sudo systemctl enable mysql

# 3. Install Python dependencies
sudo apt install python3-pip python3-full -y
pip3 install flask pymysql --break-system-packages

# 4. Setup Database
sudo mysql < /home/ubuntu/schema.sql

# 5. Run the app on port 80 (needs sudo)
sudo nohup python3 /home/ubuntu/app.py &

echo "Done! App running at http://YOUR_EC2_IP"

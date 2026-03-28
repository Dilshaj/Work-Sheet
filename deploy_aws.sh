#!/bin/bash

# ==========================================
# EduProva AWS Deployment Script
# ==========================================

# 1. Update Codebase
echo "Pulling latest code from GitHub..."
git pull origin main

# 2. Build Frontend
if [ -d "work-updates" ]; then
    echo "Building production assets with Vite..."
    cd work-updates
    npm install
    # Ensure production environment variables are correctly picked up during build
    npm run build
    cd ..
fi

# 3. Synchronize Nginx Configuration (Ensures /api proxying works correctly)
if [ -f "deployment/nginx.conf" ]; then
    echo "Updating Nginx configuration..."
    sudo cp deployment/nginx.conf /etc/nginx/sites-available/default
    # Explicitly ensure it's enabled in the sites-enabled directory
    sudo ln -sf /etc/nginx/sites-available/default /etc/nginx/sites-enabled/default
    # Force restart to ensure all proxy headers and upstream settings are active
    sudo systemctl restart nginx
fi

# 4. Restart Application Services
echo "Reloading backend services..."
sudo systemctl daemon-reload
sudo systemctl restart backend

echo "=========================================="
echo "Deployment Complete! ✅"
echo "Your live site at 16.112.203.49 is fully updated and stabilized."
echo "=========================================="

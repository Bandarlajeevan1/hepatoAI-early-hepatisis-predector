# ============================================================================
# DOCKER HUB PUSH - INTERACTIVE SETUP SCRIPT
# ============================================================================
# This script guides you through pushing your Docker images to Docker Hub
# ============================================================================

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Docker Hub Push Setup Script" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Step 1: Check Docker installation
Write-Host "[STEP 1] Checking Docker installation..." -ForegroundColor Yellow
$dockerCheck = docker --version
if ($dockerCheck) {
    Write-Host "✅ Docker installed: $dockerCheck`n" -ForegroundColor Green
} else {
    Write-Host "❌ Docker not found. Please install Docker Desktop" -ForegroundColor Red
    exit 1
}

# Step 2: Get Docker Hub username
Write-Host "[STEP 2] Docker Hub Account Setup" -ForegroundColor Yellow
Write-Host "Do you have a Docker Hub account?" -ForegroundColor Cyan
Write-Host "If not, create one at: https://hub.docker.com/" -ForegroundColor Blue
Write-Host ""

$dockerUsername = Read-Host "Enter your Docker Hub username"
if ([string]::IsNullOrWhiteSpace($dockerUsername)) {
    Write-Host "❌ Username cannot be empty" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Using username: $dockerUsername`n" -ForegroundColor Green

# Step 3: Login to Docker Hub
Write-Host "[STEP 3] Login to Docker Hub" -ForegroundColor Yellow
Write-Host "Logging in with username: $dockerUsername`n" -ForegroundColor Cyan

docker login --username $dockerUsername
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Docker login failed" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Successfully logged in to Docker Hub`n" -ForegroundColor Green

# Step 4: Verify images exist
Write-Host "[STEP 4] Verifying Docker Images" -ForegroundColor Yellow
$backendImage = docker images | Select-String "hepatitis-detection-backend"
$frontendImage = docker images | Select-String "hepatitis-detection-frontend"

if ($backendImage -and $frontendImage) {
    Write-Host "✅ Both images found:`n" -ForegroundColor Green
    Write-Host ($backendImage | Out-String).Trim()
    Write-Host ($frontendImage | Out-String).Trim()
    Write-Host ""
} else {
    Write-Host "❌ Images not found. Please run: docker-compose build" -ForegroundColor Red
    exit 1
}

# Step 5: Tag images
Write-Host "[STEP 5] Tagging Images for Docker Hub" -ForegroundColor Yellow
Write-Host "Tagging images with your username...`n" -ForegroundColor Cyan

$backendTag = "$dockerUsername/hepatitis-detection-backend:latest"
$frontendTag = "$dockerUsername/hepatitis-detection-frontend:latest"

docker tag hepatitis-detection-backend:latest $backendTag
docker tag hepatitis-detection-frontend:latest $frontendTag

Write-Host "✅ Tagged images:`n" -ForegroundColor Green
Write-Host "  Backend:  $backendTag"
Write-Host "  Frontend: $frontendTag`n"

# Step 6: Confirm push
Write-Host "[STEP 6] Ready to Push" -ForegroundColor Yellow
Write-Host "✅ All preparations complete!" -ForegroundColor Green
Write-Host "`nThe following images will be pushed to Docker Hub:`n" -ForegroundColor Cyan
Write-Host "  1. $backendTag"
Write-Host "  2. $frontendTag`n"

$confirm = Read-Host "Continue with push? (yes/no)"
if ($confirm -ne "yes") {
    Write-Host "❌ Push canceled" -ForegroundColor Yellow
    exit 0
}

# Step 7: Push backend
Write-Host "`n[STEP 7] Pushing Backend Image to Docker Hub" -ForegroundColor Yellow
Write-Host "This may take 2-5 minutes...`n" -ForegroundColor Cyan

docker push $backendTag
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Backend push failed" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Backend image pushed successfully!`n" -ForegroundColor Green

# Step 8: Push frontend
Write-Host "[STEP 8] Pushing Frontend Image to Docker Hub" -ForegroundColor Yellow
Write-Host "This may take 1-3 minutes...`n" -ForegroundColor Cyan

docker push $frontendTag
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Frontend push failed" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Frontend image pushed successfully!`n" -ForegroundColor Green

# Step 9: Version tags (optional)
Write-Host "[STEP 9] Optional: Create Version Tags" -ForegroundColor Yellow
$tagVersion = Read-Host "Enter version (e.g., v1.0.0) or press Enter to skip"

if ($tagVersion) {
    $backendVersionTag = "$dockerUsername/hepatitis-detection-backend:$tagVersion"
    $frontendVersionTag = "$dockerUsername/hepatitis-detection-frontend:$tagVersion"
    
    Write-Host "Tagging version $tagVersion...`n" -ForegroundColor Cyan
    
    docker tag hepatitis-detection-backend:latest $backendVersionTag
    docker tag hepatitis-detection-frontend:latest $frontendVersionTag
    
    docker push $backendVersionTag
    docker push $frontendVersionTag
    
    Write-Host "✅ Version tags pushed!`n" -ForegroundColor Green
}

# Final summary
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  ✅ SUCCESS - All Images Pushed!" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "Your images are now on Docker Hub!`n" -ForegroundColor Green

Write-Host "Access your repositories at:`n" -ForegroundColor Cyan
Write-Host "  https://hub.docker.com/r/$dockerUsername/hepatitis-detection-backend"
Write-Host "  https://hub.docker.com/r/$dockerUsername/hepatitis-detection-frontend`n"

Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "  1. Share docker-compose-production.yml with your team"
Write-Host "  2. They can run: docker-compose -f docker-compose-production.yml up -d"
Write-Host "  3. Edit docker-compose-production.yml with your username`n"

Write-Host "Commands for others to use your images:" -ForegroundColor Cyan
Write-Host "  docker pull $backendTag"
Write-Host "  docker pull $frontendTag`n"

Write-Host "View on Docker Hub:" -ForegroundColor Blue
Write-Host "  https://hub.docker.com/$dockerUsername`n"

Write-Host "========================================`n" -ForegroundColor Cyan

# Railway.app One-Click Deployment Guide

## **Step 1: Prepare Your Project**

Ensure your project is on GitHub:
```bash
git init
git add .
git commit -m "Initial commit - Hepatitis Detection App"
git remote add origin https://github.com/YOUR_USERNAME/hepatitis-detection.git
git push -u origin main
```

---

## **Step 2: Create Railway Account**

1. Go to: **https://railway.app**
2. Click "Login with GitHub"
3. Authorize Railway to access your GitHub account

---

## **Step 3: Create New Project**

1. Click "New Project"
2. Select "Deploy from GitHub"
3. Find your `hepatitis-detection` repository
4. Click "Deploy Now"

---

## **Step 4: Configure Environment Variables**

In Railway Dashboard:

1. Go to your project
2. Click "Variables"
3. Add these variables:

```
FLASK_ENV=production
FLASK_DEBUG=False
FLASK_PORT=5000
SECRET_KEY=your-very-secure-random-key-here-minimum-32-chars
MONGO_URI=mongodb+srv://jeevanbandarla1234_db_user:Jeevan12@cluster0.eg83ljt.mongodb.net/hepatitis_db?appName=Cluster0&retryWrites=true&w=majority
MONGODB_DATABASE=hepatitis_db
LOG_LEVEL=INFO
MODEL_PATH=model/trained_model.pkl
N_NEIGHBORS_KNN=5
RSEED=42
RISK_THRESHOLD_LOW=0.3
RISK_THRESHOLD_MEDIUM=0.7
JWT_SECRET=your-jwt-secret-key-here
```

---

## **Step 5: Set Start Command**

1. Go to "Deployments" tab
2. Edit the start command to:

```bash
cd backend && gunicorn -w 4 -b 0.0.0.0:$PORT app:app
```

---

## **Step 6: Add Frontend as Static Files**

Option A: Serve from backend (Simpler)
```bash
# Build React first, then modify Flask to serve static files
```

Option B: Deploy frontend separately on Vercel (Recommended)

---

## **Step 7: Deploy and Access**

1. Railway will auto-deploy
2. Your backend URL: `https://your-project-name.railway.app`
3. Update frontend API URL in `.env`:

```env
REACT_APP_API_URL=https://your-project-name.railway.app
```

---

## **Cost Estimate**

- Railway Free Tier: $5/month credit (usually enough)
- MongoDB Atlas: Free tier
- **Total: Usually FREE for small projects**

---

## **Issues & Solutions**

| Issue | Solution |
|-------|----------|
| Build fails | Check logs in Railway dashboard |
| Port issues | Railway auto-assigns port, use $PORT env variable |
| MongoDB not connecting | Verify MONGO_URI in environment variables |
| Static files not found | Ensure frontend build folder is committed |


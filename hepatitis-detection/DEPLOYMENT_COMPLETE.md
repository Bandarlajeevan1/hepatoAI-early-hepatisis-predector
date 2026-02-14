# Hepatitis Detection - Complete Deployment Guide

**Project Status:** ✅ Production Ready  
**Last Updated:** February 11, 2026

---

## **Deployment Options Comparison**

| Option | Difficulty | Cost | Setup Time | Best For |
|--------|------------|------|-----------|----------|
| **Railway.app** | ⭐ Easy | FREE (usually) | 10 min | Quick MVP, Free tier |
| **Vercel + Railway** | ⭐⭐ Easy | FREE tier | 15 min | Modern stacks |
| **Docker** | ⭐⭐⭐ Medium | Varies | 30 min | Full control |
| **Heroku** | ⭐ Easy | $7+/month | 10 min | Simple apps |
| **AWS/GCP/Azure** | ⭐⭐⭐⭐ Hard | Varies | 2+ hours | Enterprise |
| **DigitalOcean** | ⭐⭐⭐ Medium | $5+/month | 45 min | VPS control |

---

## **RECOMMENDED: Railway.app + Vercel (Easiest & Free)**

### **Why This Combination?**
- ✅ Free tier for both
- ✅ No credit card initially
- ✅ Fast deployment
- ✅ Auto-scaling
- ✅ GitHub integration

### **Total Cost:** FREE (usually $5-10/month after free credits)

---

## **Quick Start: Railway.app Deployment**

### **Step 1: Prepare GitHub Repository**

```powershell
cd "C:\new major\hepatitis-detection"

# Initialize git (if not already done)
git init
git add .
git commit -m "Ready for production deployment"
git remote add origin https://github.com/YOUR_USERNAME/hepatitis-detection.git
git branch -M main
git push -u origin main
```

### **Step 2: Set Up Railway.app**

1. **Create Account:** https://railway.app
2. **Sign in with GitHub**
3. **Create New Project**
4. **Select "Deploy from GitHub"**
5. **Choose your repository**

### **Step 3: Configure Variables**

In Railway Dashboard → Project Settings → Variables:

```
# Database
MONGO_URI=mongodb+srv://jeevanbandarla1234_db_user:Jeevan12@cluster0.eg83ljt.mongodb.net/hepatitis_db?appName=Cluster0&retryWrites=true&w=majority

# Flask
FLASK_ENV=production
FLASK_DEBUG=False
FLASK_PORT=5000
SECRET_KEY=generate-a-32-character-random-string-here

# JWT
JWT_SECRET=generate-another-random-string-here

# ML
MODEL_PATH=model/trained_model.pkl
LOG_LEVEL=INFO
```

### **Step 4: Set Build & Start Commands**

**Root Directory:** Select `backend` folder

**Build Command:**
```bash
pip install -r requirements.txt
```

**Start Command:**
```bash
gunicorn -w 4 -b 0.0.0.0:$PORT app:app
```

### **Step 5: Deploy Frontend on Vercel**

1. **Create Vercel Account:** https://vercel.app
2. **Import frontend folder as separate project**
3. **Configure API URL to point to Railway backend**

### **Step 6: Update CORS**

Update `backend/app.py`:

```python
CORS(app, resources={
    r"/api/*": {
        "origins": ["https://your-vercel-domain.vercel.app", "http://localhost:3000"]
    }
})
```

---

## **Complete Project File Structure for Deployment**

```
hepatitis-detection/
├── backend/
│   ├── .env                    # ✅ Environment variables
│   ├── .env.example            # Example file
│   ├── app.py
│   ├── requirements.txt        # Dependencies
│   ├── requirements-prod.txt   # Production dependencies
│   ├── Procfile               # For Heroku (optional)
│   ├── wsgi.py                # Production entry point
│   ├── model/
│   ├── database/
│   ├── utils/
│   └── venv/                  # Don't commit this
│
├── frontend/
│   ├── .env.production        # Production env
│   ├── package.json
│   ├── public/
│   └── src/
│
├── .git/                      # Git repository
├── .gitignore                 # Exclude venv, node_modules, .env
├── docker-compose.yml
├── Dockerfile
├── .dockerignore
├── README.md
└── DEPLOY_*.md                # These guides
```

---

## **Pre-Deployment Checklist**

### **Code Quality**
- [ ] No hardcoded secrets (use .env)
- [ ] Error handling on all endpoints
- [ ] CORS configured for production
- [ ] Logging configured
- [ ] Database connection pooling enabled

### **Security**
- [ ] SECRET_KEY is 32+ random characters
- [ ] JWT_SECRET is unique and strong
- [ ] HTTPS/TLS enforced
- [ ] CORS whitelist configured
- [ ] Input validation on all endpoints
- [ ] SQL injection prevention (using MongoDB native drivers)
- [ ] Rate limiting configured (optional)

### **Performance**
- [ ] Database indexes configured
- [ ] Static files minified
- [ ] Cache headers configured
- [ ] Gzip compression enabled
- [ ] Database connection pooling

### **Monitoring**
- [ ] Error logging configured
- [ ] Health check endpoint working
- [ ] Performance metrics configured
- [ ] Backup strategy defined

---

## **Environment Variables Template**

Create `.env` for development and set these on your hosting:

```env
# MongoDB
MONGO_URI=mongodb+srv://user:password@cluster.mongodb.net/database
MONGODB_DATABASE=hepatitis_db

# Flask
FLASK_ENV=production
FLASK_DEBUG=False
FLASK_PORT=5000
SECRET_KEY=your-32-character-random-secret-key-here

# JWT
JWT_SECRET=your-jwt-secret-key-here

# ML Pipeline
MODEL_PATH=model/trained_model.pkl
LOG_LEVEL=INFO
N_NEIGHBORS_KNN=5
RSEED=42

# Risk Thresholds
RISK_THRESHOLD_LOW=0.3
RISK_THRESHOLD_MEDIUM=0.7
```

---

## **Step-by-Step Deployment Walkthrough**

### **For Railway.app:**

1. **Push to GitHub**
   ```bash
   git push origin main
   ```

2. **Create Railway project**
   - Login to https://railway.app
   - New Project → Deploy from GitHub

3. **Configure variables**
   - Add all environment variables in Railway dashboard

4. **Deploy**
   - Railway automatically deploys on push
   - Monitor deployment in dashboard

5. **Get your backend URL**
   - Something like: `https://project-name.railway.app`

### **For Vercel (Frontend):**

1. **Push frontend to GitHub**
   ```bash
   git push origin main
   ```

2. **Import to Vercel**
   - https://vercel.com/import
   - Select frontend repository

3. **Set environment variables**
   - `REACT_APP_API_URL=https://your-railway-backend.railway.app`

4. **Deploy**
   - Vercel auto-deploys on every push

---

## **Troubleshooting Deployment**

| Issue | Solution |
|-------|----------|
| Build fails | Check deployment logs in dashboard |
| MongoDB connection error | Verify MONGO_URI in environment variables |
| CORS errors | Update CORS whitelist with frontend domain |
| Port already in use | Use `$PORT` environment variable (auto-assigned) |
| Static files 404 | Ensure next build includes static files |
| API returning 500 | Check backend logs for errors |
| Database not persisting | Verify MongoDB Atlas credentials |

---

## **Post-Deployment**

### **Test Your Deployment**

```powershell
# Test API
curl https://your-backend.railway.app/health

# Test authentication
curl -X POST https://your-backend.railway.app/auth/register `
  -H "Content-Type: application/json" `
  -d '{"email":"test@example.com","password":"Test123"}'

# Test frontend
Open-Browser https://your-frontend.vercel.app
```

### **Monitor Your Application**

- **Backend:** Railway dashboard → Deployments tab
- **Frontend:** Vercel dashboard → Analytics
- **Database:** MongoDB Atlas → Monitoring tab
- **Logs:** Access in respective dashboards

---

## **Scaling Your Application**

As your app grows:

1. **Database:** Consider Mongo Atlas paid tier
2. **Frontend:** Already CDN-distributed by Vercel
3. **Backend:** Railway automatically scales
4. **Add monitoring:** Sentry, DataDog, or Railway's built-in

---

## **Additional Resources**

- Railway Docs: https://docs.railway.app
- Vercel Docs: https://vercel.com/docs
- MongoDB Atlas: https://www.mongodb.com/atlas
- Flask Production Guide: https://flask.palletsprojects.com/en/2.3.x/deploying/
- React Build Optimization: https://create-react-app.dev/deployment/

---

## **Getting Help**

1. **Check deployment logs** in your dashboard
2. **Read service documentation** (Railway, Vercel)
3. **MongoDB Atlas support** for database issues
4. **GitHub Discussions** for community help

---

**You're ready to deploy! Choose Railway.app + Vercel for the easiest setup.** 🚀


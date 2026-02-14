# 🚀 Hepatitis Detection - Quick Deployment Reference

---

## **FASTEST DEPLOYMENT (Railway.app)**

### **In 5 Minutes:**

#### **1. Push to GitHub**
```powershell
cd "C:\new major\hepatitis-detection"
git init
git add .
git commit -m "Deploy to production"
git remote add origin https://github.com/YOUR_USERNAME/hepatitis-detection.git
git push -u origin main
```

#### **2. Deploy on Railway.app**
1. Go to https://railway.app
2. Sign in with GitHub
3. Click "New Project" → "Deploy from GitHub"
4. Select your repository
5. Add environment variables from table below

#### **3. Get Your Backend URL**
- Your URL: `https://hepatitis-detection-production.railway.app` (example)

#### **4. Deploy Frontend**
1. Go to https://vercel.com
2. Import your `frontend` folder
3. Set `REACT_APP_API_URL=https://your-railway-url`
4. Deploy!

#### **5. Access Your App**
- Frontend: `https://your-app.vercel.app`
- Backend API: `https://your-railway-app.railway.app`
- API Docs: `https://your-railway-app.railway.app/apidocs`

---

## **Required Environment Variables**

Copy these to Railway dashboard and Vercel:

```
MONGO_URI=mongodb+srv://jeevanbandarla1234_db_user:Jeevan12@cluster0.eg83ljt.mongodb.net/hepatitis_db?appName=Cluster0&retryWrites=true&w=majority
MONGODB_DATABASE=hepatitis_db
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=GENERATE-32-RANDOM-CHARACTERS-HERE
JWT_SECRET=GENERATE-ANOTHER-RANDOM-STRING-HERE
LOG_LEVEL=INFO
MODEL_PATH=model/trained_model.pkl
```

---

## **Generate Secure Keys**

### **In PowerShell:**
```powershell
# Generate 32-char random key
-join ([char[]]'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%' | Get-Random -Count 32)
```

Or use online generator: https://randomkeygen.com/

---

## **Deployment Checklist**

- [ ] GitHub account created
- [ ] Code pushed to GitHub
- [ ] Railway.app account created
- [ ] Environment variables set in Railway
- [ ] Backend deployed & URL working
- [ ] Vercel account created
- [ ] Frontend deployed
- [ ] API URL configured in frontend
- [ ] Login test successful
- [ ] API docs accessible

---

## **Deployment Status Commands**

### **Check Backend Status**
```powershell
$url = "https://your-railway-backend.railway.app/health"
Invoke-WebRequest -Uri $url -UseBasicParsing | ConvertFrom-Json | ConvertTo-Json
```

### **Test Login**
```powershell
$uri = "https://your-railway-backend.railway.app/auth/login"
$body = '{"email":"test@example.com","password":"password123"}'
Invoke-WebRequest -Uri $uri -Method POST -ContentType "application/json" -Body $body -UseBasicParsing
```

---

## **Common Issues & Solutions**

| Issue | Fix |
|-------|-----|
| **Build fails** | Check Railway logs → look for missing dependencies |
| **MongoDB error** | Copy-paste MONGO_URI exactly (check for spaces) |
| **CORS error** | Update CORS in backend/app.py with frontend domain |
| **404 on API** | Verify backend URL in frontend .env |
| **500 error** | Check Railway logs for stack trace |

---

## **Post-Deployment Verification**

1. **Open Frontend:** `https://your-vercel-domain.vercel.app`
2. **Register Account:** Use any email & password
3. **Try Login:** Should get JWT token
4. **Make Prediction:** Should work instantly
5. **Check API Docs:** `https://your-backend.railway.app/apidocs`

---

## **MongoDB Atlas Dashboard**

Monitor your database:
1. Go to: https://account.mongodb.com/account/login
2. Select your cluster (cluster0)
3. View:
   - Collections → users (created users)
   - Collections → predictions (if you save)
   - Monitoring → Connection stats

---

## **Continuous Deployment (Auto-Deploy)**

Both Railway and Vercel auto-deploy when you push to `main` branch:

```powershell
# Make changes locally
git add .
git commit -m "Update feature"
git push origin main

# Your apps automatically redeploy! ✅
```

---

## **Scale Later (If Needed)**

### **Backend (Railway)**
- Go to Railway → Project → Settings
- Increase replica count to scale

### **Frontend (Vercel)**
- Already globally distributed on CDN
- No action needed

### **Database (MongoDB Atlas)**
- Upgrade from M0 (free) to M10+ (paid)
- One-click upgrade in MongoDB Atlas dashboard

---

## **Monitoring & Logs**

### **Railway Backend Logs:**
1. Go to Railway dashboard
2. Select your project
3. Click "Deployments" tab
4. View real-time logs

### **Vercel Frontend Logs:**
1. Go to Vercel dashboard
2. Select your project
3. Click "Analytics" tab
4. View deployment logs

### **Database (MongoDB):**
1. Go to MongoDB Atlas
2. Click your cluster
3. View connection stats & logs

---

## **Cost After Free Trial**

Realistic monthly costs:
- **Railway:** $10-20/month (includes database)
- **Vercel:** FREE (generous free tier for frontend)
- **MongoDB Atlas:** FREE (up to 512MB)
- **Total:** ~$10-20/month

**Tip:** Free tier often sufficient for learning/demo projects!

---

## **Next Steps**

1. ✅ Complete items in checklist above
2. ✅ Test all functionality on live site
3. ✅ Share URL with users
4. ✅ Monitor logs for errors
5. ✅ Add users and collect feedback
6. ✅ Scale as needed

---

## **Support Resources**

- Railway Docs: https://docs.railway.app
- Vercel Help: https://vercel.com/support
- MongoDB Support: https://account.mongodb.com/account/support
- GitHub Issues: For project-specific bugs

---

## **Still Have Questions?**

See the detailed guides:
- `DEPLOYMENT_COMPLETE.md` - Full deployment guide
- `DEPLOY_RAILWAY.md` - Railway specific
- `DEPLOY_VERCEL.md` - Vercel specific
- `DEPLOY_DOCKER.md` - Docker deployment

---

**Ready? Start with: https://railway.app** 🚀


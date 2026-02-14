# Vercel Deployment Guide (Frontend Only)

## **Deploy React Frontend to Vercel**

### **Step 1: Create Vercel Account**

1. Go to: **https://vercel.com**
2. Sign up with GitHub account
3. Authorize Vercel to access your repositories

---

### **Step 2: Push Frontend to GitHub**

```powershell
cd "C:\new major\hepatitis-detection\frontend"

git init
git add .
git commit -m "Deploy frontend to Vercel"
git remote add origin https://github.com/YOUR_USERNAME/hepatitis-frontend.git
git push -u origin main
```

---

### **Step 3: Import Project in Vercel**

1. Go to **https://vercel.com/dashboard**
2. Click "Import Project"
3. Select "Import Git Repository"
4. Find your `hepatitis-frontend` repository
5. Click "Import"

---

### **Step 4: Configure Environment Variables**

1. In Vercel project settings
2. Go to "Environment Variables"
3. Add:

```
REACT_APP_API_URL=https://your-backend-domain.com
```

---

### **Step 5: Deploy**

1. Click "Deploy"
2. Vercel will automatically:
   - Build React app (`npm run build`)
   - Optimize assets
   - Deploy to CDN
   - Provide HTTPS

---

### **Step 6: Update Backend URL**

After backend deployment (Railway/Docker), update:
```
REACT_APP_API_URL=https://your-backend-url.com
```

And redeploy frontend:
```powershell
git push  # Auto-deploys on Vercel
```

---

### **Your URLs After Deployment**

- **Frontend:** `https://your-app.vercel.app`
- **Backend:** `https://your-backend.railway.app` (or your domain)
- **API Docs:** `https://your-backend.railway.app/apidocs`

---

### **Environment Variables in `.env.local`** (Local Development)

```env
REACT_APP_API_URL=http://localhost:5000
```

---

### **Production Checklist**

- [ ] Frontend URL: `https://your-app.vercel.app`
- [ ] Backend URL configured in frontend
- [ ] CORS enabled on backend for frontend domain
- [ ] SSL/TLS working
- [ ] API responding with correct content-type headers
- [ ] Error handling working
- [ ] Logging configured


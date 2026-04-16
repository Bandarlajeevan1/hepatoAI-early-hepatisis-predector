# 🧪 QUICK MANUAL TESTING - DO THIS NOW!

## Your Docker System is Running! ✅

Your containers are already up and running. Here's what you can test **RIGHT NOW**:

---

## 🌐 TEST 1: Open Browser (EASIEST - 10 seconds)

### Just do this:
1. Open your browser (Chrome, Edge, Firefox)
2. Go to: **http://localhost:3000**
3. You should see a **Login/Register page** with styling

### What to try:
- Click "Register"
- Enter any email & password
- Click "Register" 
- Then "Login" with your credentials
- You should see the **Prediction Form**
- Submit some patient data
- Get a prediction result

---

## 💻 TEST 2: Test Backend API (PowerShell - 5 seconds)

### Copy & paste this command:
```powershell
Invoke-WebRequest http://localhost:5000/health -UseBasicParsing | Select-Object -ExpandProperty Content
```

### You should see:
```json
{"model_loaded":true,"status":"healthy","timestamp":"2026-04-09T15:03:38.863672","version":"1.0.0"}
```

**✅ If you see this → Backend is working!**

---

## 📊 TEST 3: Check Container Status (PowerShell - 3 seconds)

### Copy & paste this:
```powershell
docker-compose ps
```

### You should see 3 containers "Up":
```
hepatitis-backend    Up ✓
hepatitis-frontend   Up ✓
hepatitis-mongo      Up ✓
```

**✅ If all show "Up" → Docker is working!**

---

## 📋 TEST 4: View Logs (PowerShell)

### See what's happening inside containers:

**Backend logs:**
```powershell
docker-compose logs backend
```

**Frontend logs:**
```powershell
docker-compose logs frontend
```

**MongoDB logs:**
```powershell
docker-compose logs mongo
```

---

## 📈 TEST 5: Monitor Resources (PowerShell)

### See CPU & Memory usage:
```powershell
docker stats
```

You should see:
```
CONTAINER          CPU %    MEM USAGE
hepatitis-backend  0.5%     250MiB
hepatitis-frontend 0.1%     60MiB
hepatitis-mongo    1.2%     200MiB
```

Press **Ctrl+C** to stop

---

## ✅ SUCCESS SIGNS

### Backend ✓
- Responds at http://localhost:5000/health
- Shows "status": "healthy"
- Shows "model_loaded": true

### Frontend ✓
- Loads at http://localhost:3000
- Shows login page with styling
- Can register and login

### MongoDB ✓
- Container runs without crashing
- Backend can save data
- Persists between restarts

### Docker ✓
- All 3 containers show "Up"
- Can access all ports (5000, 3000, 27017)
- Health checks passing

---

## 🛑 WHEN DONE TESTING

### Stop containers:
```powershell
docker-compose down
```

### Restart anytime:
```powershell
docker-compose up -d
```

---

## 📝 SUMMARY

| Test | Command | Expected | Status |
|------|---------|----------|--------|
| Browser | http://localhost:3000 | Login page | ✅ |
| Backend Health | Invoke-WebRequest http://localhost:5000/health | 200 OK + healthy | ✅ |
| Containers | docker-compose ps | 3 containers Up | ✅ |
| Logs | docker-compose logs | No errors | ✅ |
| Resources | docker stats | Normal CPU/RAM | ✅ |

---

## 🎉 THAT'S IT!

You now have a fully working Docker system with:
- ✅ Backend API running
- ✅ Frontend UI accessible
- ✅ Database ready
- ✅ Everything containerized

---

## 🚀 NEXT: Push to Docker Hub

When you're done testing:
```powershell
.\PUSH_TO_DOCKER_HUB.ps1
```

That's all! 🎉

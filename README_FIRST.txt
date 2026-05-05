================================================================================
  MBAS - Modern Business Automation System
  Quick Start Instructions
================================================================================

STEP 1: LAUNCH THE SYSTEM
--------------------------
Double-click this file:  OPEN_SYSTEM.bat

This will:
1. Start the backend server (FastAPI)
2. Start the frontend server (React)
3. Automatically open your browser

STEP 2: LOGIN
-------------
Username: admin
Password: admin123

STEP 3: EXPLORE
---------------
- Dashboard: See business metrics
- Billing: Create invoices (POS system)
- Inventory: Manage products with instant search
- Reports: Sales and Profit/Loss reports
- Settings: Customize business branding

================================================================================

CURRENT STATUS:
--------------
✅ Frontend Server: RUNNING on http://localhost:5173
⏳ Backend Server:  START MANUALLY (see below)

MANUAL BACKEND START (if needed):
---------------------------------
1. Open Command Prompt
2. Run these commands:
   cd D:\gemini_modern_business_automation_system\backend
   python -m uvicorn backend.src.main:app --host 127.0.0.1 --port 8000 --reload

3. Wait for: "Application startup complete."

================================================================================

TROUBLESHOOTING:
---------------
Q: Backend won't start?
A: Install dependencies first:
   cd backend
   pip install -r requirements.txt

Q: Frontend won't start?
A: Install dependencies first:
   cd frontend
   npm install

Q: Login doesn't work?
A: Make sure backend is running. Check http://127.0.0.1:8000/health

================================================================================

DOCUMENTATION:
-------------
📄 START_HERE.md              - Detailed startup guide
📄 SYSTEM_PREVIEW.md          - 60-page client demo guide
📄 IMPLEMENTATION_STATUS.md   - Technical details

================================================================================

DEMO FEATURES:
-------------
✅ Auto Invoice Numbers (INV-YYYYMMDD-XXXX)
✅ Full-Text Search (FTS5)
✅ Cost Price Snapshots for Profit Reports
✅ Supplier Payment Tracking
✅ Role-Based Access Control
✅ AI Sales Forecasting (Premium)
✅ Backup & Restore
✅ 100% Offline Operation

================================================================================
Ready to impress your clients! 🎉
================================================================================

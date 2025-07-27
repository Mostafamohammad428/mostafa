#!/bin/bash
echo "🚀 بدء تشغيل نظام ERP المتكامل..."
cd backend && python -m uvicorn server:app --reload --host 0.0.0.0 --port 8000 &
cd ../frontend && npm start

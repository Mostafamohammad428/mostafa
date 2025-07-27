#!/bin/bash

# نظام ERP المتكامل - سكريبت بدء التشغيل
echo "🏢 مرحباً بك في نظام ERP المتكامل"
echo "=================================="

# التحقق من وجود Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 غير مثبت. يرجى تثبيت Python 3.8+ أولاً"
    exit 1
fi

# التحقق من وجود Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js غير مثبت. يرجى تثبيت Node.js 16+ أولاً"
    exit 1
fi

# التحقق من وجود MongoDB
if ! command -v mongod &> /dev/null; then
    echo "⚠️  MongoDB غير مثبت أو غير موجود في PATH"
    echo "يرجى تثبيت MongoDB وتشغيله قبل المتابعة"
    echo "للتثبيت على Ubuntu: sudo apt-get install mongodb"
    echo "للتثبيت على macOS: brew install mongodb-community"
fi

echo "🚀 بدء تشغيل النظام..."

# إنشاء جلسة tmux جديدة للنظام
SESSION_NAME="erp_system"

# إنهاء الجلسة إذا كانت موجودة
tmux kill-session -t $SESSION_NAME 2>/dev/null

# إنشاء جلسة جديدة
tmux new-session -d -s $SESSION_NAME

# النافذة الأولى: Backend
tmux rename-window -t $SESSION_NAME:0 'Backend'
tmux send-keys -t $SESSION_NAME:0 'cd backend' C-m
tmux send-keys -t $SESSION_NAME:0 'echo "🔧 إعداد الخادم الخلفي..."' C-m

# التحقق من وجود البيئة الافتراضية وإنشاؤها إذا لم تكن موجودة
tmux send-keys -t $SESSION_NAME:0 'if [ ! -d "venv" ]; then echo "📦 إنشاء البيئة الافتراضية..."; python3 -m venv venv; fi' C-m
tmux send-keys -t $SESSION_NAME:0 'source venv/bin/activate' C-m
tmux send-keys -t $SESSION_NAME:0 'echo "📥 تثبيت المتطلبات..."' C-m
tmux send-keys -t $SESSION_NAME:0 'pip install -r requirements.txt' C-m
tmux send-keys -t $SESSION_NAME:0 'echo "🌟 تشغيل الخادم على http://localhost:8000"' C-m
tmux send-keys -t $SESSION_NAME:0 'uvicorn server:app --reload --host 0.0.0.0 --port 8000' C-m

# النافذة الثانية: Frontend
tmux new-window -t $SESSION_NAME:1 -n 'Frontend'
tmux send-keys -t $SESSION_NAME:1 'cd frontend' C-m
tmux send-keys -t $SESSION_NAME:1 'echo "🎨 إعداد الواجهة الأمامية..."' C-m

# التحقق من وجود node_modules وتثبيت المتطلبات إذا لم تكن موجودة
tmux send-keys -t $SESSION_NAME:1 'if [ ! -d "node_modules" ]; then echo "📦 تثبيت متطلبات الواجهة..."; npm install; fi' C-m
tmux send-keys -t $SESSION_NAME:1 'echo "🌟 تشغيل الواجهة على http://localhost:3000"' C-m
tmux send-keys -t $SESSION_NAME:1 'npm start' C-m

# النافذة الثالثة: معلومات النظام
tmux new-window -t $SESSION_NAME:2 -n 'Info'
tmux send-keys -t $SESSION_NAME:2 'clear' C-m
tmux send-keys -t $SESSION_NAME:2 'echo "🏢 نظام ERP المتكامل"' C-m
tmux send-keys -t $SESSION_NAME:2 'echo "===================="' C-m
tmux send-keys -t $SESSION_NAME:2 'echo ""' C-m
tmux send-keys -t $SESSION_NAME:2 'echo "🌐 روابط النظام:"' C-m
tmux send-keys -t $SESSION_NAME:2 'echo "   الواجهة الأمامية: http://localhost:3000"' C-m
tmux send-keys -t $SESSION_NAME:2 'echo "   API الخادم: http://localhost:8000"' C-m
tmux send-keys -t $SESSION_NAME:2 'echo "   وثائق API: http://localhost:8000/docs"' C-m
tmux send-keys -t $SESSION_NAME:2 'echo ""' C-m
tmux send-keys -t $SESSION_NAME:2 'echo "📋 التحكم في النوافذ:"' C-m
tmux send-keys -t $SESSION_NAME:2 'echo "   Ctrl+B ثم 0: الخادم الخلفي"' C-m
tmux send-keys -t $SESSION_NAME:2 'echo "   Ctrl+B ثم 1: الواجهة الأمامية"' C-m
tmux send-keys -t $SESSION_NAME:2 'echo "   Ctrl+B ثم 2: معلومات النظام"' C-m
tmux send-keys -t $SESSION_NAME:2 'echo ""' C-m
tmux send-keys -t $SESSION_NAME:2 'echo "🛑 لإيقاف النظام: Ctrl+C في كل نافذة أو تشغيل ./stop_erp.sh"' C-m
tmux send-keys -t $SESSION_NAME:2 'echo ""' C-m
tmux send-keys -t $SESSION_NAME:2 'echo "📊 حالة الخدمات:"' C-m

# إظهار الجلسة
echo "✅ تم بدء تشغيل النظام بنجاح!"
echo ""
echo "🌐 يمكنك الوصول للنظام على:"
echo "   الواجهة الأمامية: http://localhost:3000"
echo "   API الخادم: http://localhost:8000"
echo "   وثائق API: http://localhost:8000/docs"
echo ""
echo "📱 للدخول لوحة التحكم: tmux attach-session -t $SESSION_NAME"
echo "🛑 لإيقاف النظام: ./stop_erp.sh"

# الاتصال بالجلسة
tmux attach-session -t $SESSION_NAME
#!/bin/bash

# نظام ERP المتكامل - سكريبت الإعداد الأولي
echo "🏢 مرحباً بك في نظام ERP المتكامل"
echo "===================================="
echo "🔧 بدء الإعداد الأولي للنظام..."
echo ""

# التحقق من المتطلبات
echo "📋 التحقق من المتطلبات..."

# التحقق من وجود Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 غير مثبت. يرجى تثبيت Python 3.8+ أولاً"
    echo "للتثبيت على Ubuntu: sudo apt-get install python3 python3-pip python3-venv"
    echo "للتثبيت على macOS: brew install python3"
    exit 1
fi
echo "✅ Python 3 متوفر"

# التحقق من وجود Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js غير مثبت. يرجى تثبيت Node.js 16+ أولاً"
    echo "للتثبيت: https://nodejs.org/en/download/"
    exit 1
fi
echo "✅ Node.js متوفر"

# التحقق من وجود MongoDB
if ! command -v mongod &> /dev/null; then
    echo "⚠️  MongoDB غير مثبت أو غير موجود في PATH"
    echo "للتثبيت على Ubuntu: sudo apt-get install mongodb"
    echo "للتثبيت على macOS: brew install mongodb-community"
    echo "تأكد من تشغيل MongoDB قبل المتابعة"
else
    echo "✅ MongoDB متوفر"
fi

# التحقق من وجود tmux
if ! command -v tmux &> /dev/null; then
    echo "⚠️  tmux غير مثبت (اختياري لتشغيل النظام)"
    echo "للتثبيت على Ubuntu: sudo apt-get install tmux"
    echo "للتثبيت على macOS: brew install tmux"
else
    echo "✅ tmux متوفر"
fi

echo ""
echo "🔧 إعداد الخادم الخلفي..."

# إعداد Backend
cd backend

# إنشاء البيئة الافتراضية إذا لم تكن موجودة
if [ ! -d "venv" ]; then
    echo "📦 إنشاء البيئة الافتراضية..."
    python3 -m venv venv
fi

# تفعيل البيئة الافتراضية
echo "🔄 تفعيل البيئة الافتراضية..."
source venv/bin/activate

# تحديث pip
echo "📥 تحديث pip..."
pip install --upgrade pip

# تثبيت المتطلبات
echo "📦 تثبيت متطلبات الخادم الخلفي..."
pip install -r requirements.txt

# تهيئة قاعدة البيانات
echo "🗄️  تهيئة قاعدة البيانات..."
python init_db.py

cd ..

echo ""
echo "🎨 إعداد الواجهة الأمامية..."

# إعداد Frontend
cd frontend

# تثبيت المتطلبات
echo "📦 تثبيت متطلبات الواجهة الأمامية..."
npm install

cd ..

echo ""
echo "🎉 تم إكمال الإعداد الأولي بنجاح!"
echo ""
echo "📋 معلومات تسجيل الدخول الافتراضية:"
echo "   اسم المستخدم: admin"
echo "   كلمة المرور: admin123"
echo ""
echo "🚀 لتشغيل النظام:"
echo "   ./start_erp.sh"
echo ""
echo "🛑 لإيقاف النظام:"
echo "   ./stop_erp.sh"
echo ""
echo "🌐 روابط النظام (بعد التشغيل):"
echo "   الواجهة الأمامية: http://localhost:3000"
echo "   API الخادم: http://localhost:8000"
echo "   وثائق API: http://localhost:8000/docs"
echo ""
echo "📖 لمزيد من المعلومات، راجع ملف README.md"
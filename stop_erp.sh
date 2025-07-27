#!/bin/bash

# نظام ERP المتكامل - سكريبت إيقاف التشغيل
echo "🛑 إيقاف نظام ERP المتكامل..."

SESSION_NAME="erp_system"

# التحقق من وجود الجلسة
if tmux has-session -t $SESSION_NAME 2>/dev/null; then
    echo "📱 إنهاء جلسة النظام..."
    tmux kill-session -t $SESSION_NAME
    echo "✅ تم إيقاف النظام بنجاح!"
else
    echo "ℹ️  النظام غير قيد التشغيل"
fi

# إيقاف العمليات المتبقية إذا وجدت
echo "🔍 البحث عن العمليات المتبقية..."

# إيقاف عمليات uvicorn (Backend)
if pgrep -f "uvicorn.*server:app" > /dev/null; then
    echo "🔧 إيقاف الخادم الخلفي..."
    pkill -f "uvicorn.*server:app"
fi

# إيقاف عمليات npm start (Frontend)
if pgrep -f "npm.*start" > /dev/null; then
    echo "🎨 إيقاف الواجهة الأمامية..."
    pkill -f "npm.*start"
fi

# إيقاف عمليات react-scripts
if pgrep -f "react-scripts" > /dev/null; then
    echo "⚛️  إيقاف خدمات React..."
    pkill -f "react-scripts"
fi

echo "🏁 تم إيقاف جميع خدمات النظام"
echo "💡 لبدء التشغيل مرة أخرى، استخدم: ./start_erp.sh"
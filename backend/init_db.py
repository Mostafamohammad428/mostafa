#!/usr/bin/env python3
"""
نظام ERP المتكامل - سكريبت تهيئة قاعدة البيانات
يقوم هذا السكريبت بإنشاء البيانات الأساسية للنظام
"""

import asyncio
import os
from datetime import datetime, date
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from passlib.context import CryptContext

# تحميل متغيرات البيئة
load_dotenv()

# إعداد قاعدة البيانات
mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
db_name = os.environ.get('DB_NAME', 'erp_system')

# إعداد التشفير
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def init_database():
    """تهيئة قاعدة البيانات بالبيانات الأساسية"""
    
    print("🏢 مرحباً بك في نظام ERP المتكامل")
    print("🔧 بدء تهيئة قاعدة البيانات...")
    
    # الاتصال بقاعدة البيانات
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    try:
        # 1. إنشاء المستخدم الإداري الافتراضي
        print("👤 إنشاء المستخدم الإداري...")
        admin_user = {
            "id": "admin-001",
            "username": "admin",
            "email": "admin@erp.com",
            "full_name": "مدير النظام",
            "role": "admin",
            "is_active": True,
            "password": pwd_context.hash("admin123"),
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        # التحقق من وجود المدير
        existing_admin = await db.users.find_one({"username": "admin"})
        if not existing_admin:
            await db.users.insert_one(admin_user)
            print("✅ تم إنشاء المستخدم الإداري (admin / admin123)")
        else:
            print("ℹ️  المستخدم الإداري موجود بالفعل")
        
        # 2. إنشاء دليل الحسابات الأساسي
        print("💰 إنشاء دليل الحسابات الأساسي...")
        
        basic_accounts = [
            # الأصول
            {"code": "1000", "name": "الأصول", "type": "أصول", "parent_id": None},
            {"code": "1100", "name": "الأصول المتداولة", "type": "أصول", "parent_id": None},
            {"code": "1110", "name": "النقدية", "type": "أصول", "parent_id": None},
            {"code": "1120", "name": "البنوك", "type": "أصول", "parent_id": None},
            {"code": "1130", "name": "العملاء", "type": "أصول", "parent_id": None},
            {"code": "1140", "name": "المخزون", "type": "أصول", "parent_id": None},
            
            # الخصوم
            {"code": "2000", "name": "الخصوم", "type": "خصوم", "parent_id": None},
            {"code": "2100", "name": "الخصوم المتداولة", "type": "خصوم", "parent_id": None},
            {"code": "2110", "name": "الموردين", "type": "خصوم", "parent_id": None},
            {"code": "2120", "name": "المصروفات المستحقة", "type": "خصوم", "parent_id": None},
            
            # حقوق الملكية
            {"code": "3000", "name": "حقوق الملكية", "type": "حقوق ملكية", "parent_id": None},
            {"code": "3100", "name": "رأس المال", "type": "حقوق ملكية", "parent_id": None},
            {"code": "3200", "name": "الأرباح المحتجزة", "type": "حقوق ملكية", "parent_id": None},
            
            # الإيرادات
            {"code": "4000", "name": "الإيرادات", "type": "إيرادات", "parent_id": None},
            {"code": "4100", "name": "إيرادات المبيعات", "type": "إيرادات", "parent_id": None},
            {"code": "4200", "name": "إيرادات أخرى", "type": "إيرادات", "parent_id": None},
            
            # المصروفات
            {"code": "5000", "name": "المصروفات", "type": "مصروفات", "parent_id": None},
            {"code": "5100", "name": "تكلفة البضاعة المباعة", "type": "مصروفات", "parent_id": None},
            {"code": "5200", "name": "مصروفات التشغيل", "type": "مصروفات", "parent_id": None},
            {"code": "5210", "name": "الرواتب والأجور", "type": "مصروفات", "parent_id": None},
            {"code": "5220", "name": "الإيجار", "type": "مصروفات", "parent_id": None},
            {"code": "5230", "name": "الكهرباء والماء", "type": "مصروفات", "parent_id": None},
        ]
        
        for account_data in basic_accounts:
            account_data.update({
                "id": f"acc-{account_data['code']}",
                "balance": 0.0,
                "is_active": True,
                "created_at": datetime.utcnow()
            })
            
            # التحقق من وجود الحساب
            existing_account = await db.accounts.find_one({"code": account_data["code"]})
            if not existing_account:
                await db.accounts.insert_one(account_data)
        
        accounts_count = await db.accounts.count_documents({})
        print(f"✅ تم إنشاء دليل الحسابات ({accounts_count} حساب)")
        
        # 3. إنشاء عملاء تجريبيين
        print("👥 إنشاء عملاء تجريبيين...")
        
        sample_customers = [
            {
                "id": "cust-001",
                "code": "C001",
                "name": "شركة التقنية المتقدمة",
                "email": "info@techadvanced.com",
                "phone": "+966501234567",
                "address": "الرياض، حي الملك فهد",
                "city": "الرياض",
                "country": "السعودية",
                "tax_number": "300123456700003",
                "credit_limit": 50000.0,
                "balance": 0.0,
                "is_active": True,
                "created_at": datetime.utcnow()
            },
            {
                "id": "cust-002", 
                "code": "C002",
                "name": "مؤسسة الأعمال الحديثة",
                "email": "contact@modernbiz.com",
                "phone": "+966507654321",
                "address": "جدة، حي الزهراء",
                "city": "جدة",
                "country": "السعودية",
                "tax_number": "300987654300003",
                "credit_limit": 75000.0,
                "balance": 0.0,
                "is_active": True,
                "created_at": datetime.utcnow()
            }
        ]
        
        for customer in sample_customers:
            existing_customer = await db.customers.find_one({"code": customer["code"]})
            if not existing_customer:
                await db.customers.insert_one(customer)
        
        customers_count = await db.customers.count_documents({})
        print(f"✅ تم إنشاء العملاء التجريبيين ({customers_count} عميل)")
        
        # 4. إنشاء موردين تجريبيين
        print("🏪 إنشاء موردين تجريبيين...")
        
        sample_suppliers = [
            {
                "id": "supp-001",
                "name": "شركة المواد الأولية",
                "contact_person": "أحمد محمد",
                "phone": "+966501111111",
                "email": "ahmed@rawmaterials.com",
                "address": "الدمام، الحي الصناعي",
                "category": "مواد",
                "created_at": datetime.utcnow()
            },
            {
                "id": "supp-002",
                "name": "مؤسسة الخدمات التقنية",
                "contact_person": "فاطمة أحمد",
                "phone": "+966502222222",
                "email": "fatima@techservices.com",
                "address": "الرياض، حي العليا",
                "category": "خدمات",
                "created_at": datetime.utcnow()
            }
        ]
        
        for supplier in sample_suppliers:
            existing_supplier = await db.suppliers.find_one({"name": supplier["name"]})
            if not existing_supplier:
                await db.suppliers.insert_one(supplier)
        
        suppliers_count = await db.suppliers.count_documents({})
        print(f"✅ تم إنشاء الموردين التجريبيين ({suppliers_count} مورد)")
        
        # 5. إنشاء منتجات تجريبية
        print("📦 إنشاء منتجات تجريبية...")
        
        sample_products = [
            {
                "id": "prod-001",
                "code": "P001",
                "name": "جهاز كمبيوتر محمول",
                "description": "جهاز كمبيوتر محمول عالي الأداء",
                "category": "تقنية",
                "unit": "قطعة",
                "cost_price": 2500.0,
                "selling_price": 3500.0,
                "current_stock": 50.0,
                "min_stock": 10.0,
                "max_stock": 200.0,
                "reorder_point": 15.0,
                "supplier_id": "supp-002",
                "is_active": True,
                "created_at": datetime.utcnow()
            },
            {
                "id": "prod-002",
                "code": "P002", 
                "name": "طابعة ليزر",
                "description": "طابعة ليزر أحادية اللون",
                "category": "مكتبية",
                "unit": "قطعة",
                "cost_price": 800.0,
                "selling_price": 1200.0,
                "current_stock": 25.0,
                "min_stock": 5.0,
                "max_stock": 100.0,
                "reorder_point": 8.0,
                "supplier_id": "supp-002",
                "is_active": True,
                "created_at": datetime.utcnow()
            }
        ]
        
        for product in sample_products:
            existing_product = await db.products.find_one({"code": product["code"]})
            if not existing_product:
                await db.products.insert_one(product)
        
        products_count = await db.products.count_documents({})
        print(f"✅ تم إنشاء المنتجات التجريبية ({products_count} منتج)")
        
        # 6. إنشاء موظفين تجريبيين
        print("👨‍💼 إنشاء موظفين تجريبيين...")
        
        sample_employees = [
            {
                "id": "emp-001",
                "employee_code": "E001",
                "first_name": "محمد",
                "last_name": "أحمد",
                "email": "mohammed@company.com",
                "phone": "+966503333333",
                "department": "المحاسبة",
                "position": "محاسب رئيسي",
                "hire_date": datetime.combine(date(2023, 1, 15), datetime.min.time()),
                "salary": 8000.0,
                "status": "active",
                "created_at": datetime.utcnow()
            },
            {
                "id": "emp-002",
                "employee_code": "E002",
                "first_name": "سارة",
                "last_name": "محمد",
                "email": "sara@company.com",
                "phone": "+966504444444",
                "department": "المبيعات",
                "position": "مدير مبيعات",
                "hire_date": datetime.combine(date(2023, 3, 1), datetime.min.time()),
                "salary": 10000.0,
                "status": "active",
                "created_at": datetime.utcnow()
            }
        ]
        
        for employee in sample_employees:
            existing_employee = await db.employees.find_one({"employee_code": employee["employee_code"]})
            if not existing_employee:
                await db.employees.insert_one(employee)
        
        employees_count = await db.employees.count_documents({})
        print(f"✅ تم إنشاء الموظفين التجريبيين ({employees_count} موظف)")
        
        # 7. إنشاء مشروع تجريبي
        print("🏗️ إنشاء مشروع تجريبي...")
        
        sample_project = {
            "id": "proj-001",
            "name": "تطوير نظام إدارة المخزون",
            "description": "مشروع تطوير نظام متكامل لإدارة المخزون",
            "start_date": datetime.combine(date(2024, 1, 1), datetime.min.time()),
            "end_date": datetime.combine(date(2024, 6, 30), datetime.min.time()),
            "budget": 150000.0,
            "actual_cost": 45000.0,
            "status": "نشط",
            "client_name": "شركة التقنية المتقدمة",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        existing_project = await db.projects.find_one({"name": sample_project["name"]})
        if not existing_project:
            await db.projects.insert_one(sample_project)
        
        projects_count = await db.projects.count_documents({})
        print(f"✅ تم إنشاء المشروع التجريبي ({projects_count} مشروع)")
        
        print("\n🎉 تم إكمال تهيئة قاعدة البيانات بنجاح!")
        print("\n📋 معلومات تسجيل الدخول:")
        print("   اسم المستخدم: admin")
        print("   كلمة المرور: admin123")
        print("\n🌐 يمكنك الآن تشغيل النظام باستخدام: ./start_erp.sh")
        
    except Exception as e:
        print(f"❌ خطأ في تهيئة قاعدة البيانات: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(init_database())
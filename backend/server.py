from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional
import uuid
from datetime import datetime, date
import json
from decimal import Decimal


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ.get('DB_NAME', 'erp_system')]

# Create the main app without a prefix
app = FastAPI(title="نظام ERP المتكامل", description="نظام إدارة موارد المؤسسات المتكامل")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== MODELS ====================

# User Management
class User(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    username: str
    email: str
    full_name: str
    role: str  # admin, manager, employee, accountant
    department: str
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None

class UserCreate(BaseModel):
    username: str
    email: str
    full_name: str
    role: str
    department: str
    password: str

# Customer Management
class Customer(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    contact_person: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    tax_number: Optional[str] = None
    credit_limit: float = 0.0
    current_balance: float = 0.0
    category: str  # retail, wholesale, corporate
    created_at: datetime = Field(default_factory=datetime.utcnow)

class CustomerCreate(BaseModel):
    name: str
    contact_person: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    tax_number: Optional[str] = None
    credit_limit: float = 0.0
    category: str

# Project Management
class Project(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: Optional[str] = None
    start_date: date
    end_date: Optional[date] = None
    budget: float
    actual_cost: float = 0.0
    status: str = "نشط"  # نشط، متوقف، مكتمل
    client_name: Optional[str] = None
    customer_id: Optional[str] = None
    manager_id: Optional[str] = None
    priority: str = "عادي"  # عالي، عادي، منخفض
    progress: float = 0.0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None
    start_date: date
    end_date: Optional[date] = None
    budget: float
    client_name: Optional[str] = None
    customer_id: Optional[str] = None
    manager_id: Optional[str] = None
    priority: str = "عادي"

# Financial Management
class Account(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    account_number: str
    name: str
    type: str  # asset, liability, equity, revenue, expense
    parent_account: Optional[str] = None
    balance: float = 0.0
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)

class AccountCreate(BaseModel):
    account_number: str
    name: str
    type: str
    parent_account: Optional[str] = None

class Transaction(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    transaction_number: str
    date: date
    description: str
    debit_account: str
    credit_account: str
    amount: float
    reference: Optional[str] = None
    project_id: Optional[str] = None
    customer_id: Optional[str] = None
    supplier_id: Optional[str] = None
    created_by: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class TransactionCreate(BaseModel):
    date: date
    description: str
    debit_account: str
    credit_account: str
    amount: float
    reference: Optional[str] = None
    project_id: Optional[str] = None
    customer_id: Optional[str] = None
    supplier_id: Optional[str] = None

# Inventory Management
class Item(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    code: str
    unit: str  # متر، كيلو، قطعة، إلخ
    current_stock: float = 0.0
    min_stock: float = 0.0
    max_stock: float = 0.0
    unit_cost: float = 0.0
    selling_price: float = 0.0
    category: str
    supplier_id: Optional[str] = None
    location: Optional[str] = None
    barcode: Optional[str] = None
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)

class ItemCreate(BaseModel):
    name: str
    code: str
    unit: str
    min_stock: float = 0.0
    max_stock: float = 0.0
    unit_cost: float = 0.0
    selling_price: float = 0.0
    category: str
    supplier_id: Optional[str] = None
    location: Optional[str] = None
    barcode: Optional[str] = None

class StockMovement(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    item_id: str
    movement_type: str  # in, out, adjustment
    quantity: float
    unit_cost: float
    total_cost: float
    reference: Optional[str] = None
    project_id: Optional[str] = None
    supplier_id: Optional[str] = None
    customer_id: Optional[str] = None
    created_by: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class StockMovementCreate(BaseModel):
    item_id: str
    movement_type: str
    quantity: float
    unit_cost: float
    reference: Optional[str] = None
    project_id: Optional[str] = None
    supplier_id: Optional[str] = None
    customer_id: Optional[str] = None

# Supplier Management
class Supplier(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    contact_person: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    tax_number: Optional[str] = None
    category: str  # مواد، خدمات، معدات
    credit_limit: float = 0.0
    current_balance: float = 0.0
    payment_terms: Optional[str] = None
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)

class SupplierCreate(BaseModel):
    name: str
    contact_person: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    tax_number: Optional[str] = None
    category: str
    credit_limit: float = 0.0
    payment_terms: Optional[str] = None

# Cost Management
class Cost(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    project_id: str
    category: str  # مواد، عمالة، معدات، أخرى
    description: str
    amount: float
    date: date
    supplier_id: Optional[str] = None
    invoice_number: Optional[str] = None
    account_id: Optional[str] = None
    created_by: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class CostCreate(BaseModel):
    project_id: str
    category: str
    description: str
    amount: float
    date: date
    supplier_id: Optional[str] = None
    invoice_number: Optional[str] = None
    account_id: Optional[str] = None

# Sales Management
class Sale(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    invoice_number: str
    customer_id: str
    date: date
    due_date: date
    subtotal: float
    tax_amount: float
    discount_amount: float
    total_amount: float
    paid_amount: float = 0.0
    status: str = "معلق"  # معلق، مدفوع، ملغي
    notes: Optional[str] = None
    created_by: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class SaleCreate(BaseModel):
    customer_id: str
    date: date
    due_date: date
    subtotal: float
    tax_amount: float
    discount_amount: float
    notes: Optional[str] = None

class SaleItem(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    sale_id: str
    item_id: str
    quantity: float
    unit_price: float
    total_price: float
    created_at: datetime = Field(default_factory=datetime.utcnow)

class SaleItemCreate(BaseModel):
    sale_id: str
    item_id: str
    quantity: float
    unit_price: float

# Purchase Management
class Purchase(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    invoice_number: str
    supplier_id: str
    date: date
    due_date: date
    subtotal: float
    tax_amount: float
    discount_amount: float
    total_amount: float
    paid_amount: float = 0.0
    status: str = "معلق"  # معلق، مدفوع، ملغي
    notes: Optional[str] = None
    created_by: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class PurchaseCreate(BaseModel):
    supplier_id: str
    date: date
    due_date: date
    subtotal: float
    tax_amount: float
    discount_amount: float
    notes: Optional[str] = None

class PurchaseItem(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    purchase_id: str
    item_id: str
    quantity: float
    unit_cost: float
    total_cost: float
    created_at: datetime = Field(default_factory=datetime.utcnow)

class PurchaseItemCreate(BaseModel):
    purchase_id: str
    item_id: str
    quantity: float
    unit_cost: float

# HR Management
class Employee(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    employee_number: str
    full_name: str
    email: str
    phone: Optional[str] = None
    department: str
    position: str
    hire_date: date
    salary: float
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)

class EmployeeCreate(BaseModel):
    employee_number: str
    full_name: str
    email: str
    phone: Optional[str] = None
    department: str
    position: str
    hire_date: date
    salary: float

class Attendance(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    employee_id: str
    date: date
    check_in: Optional[datetime] = None
    check_out: Optional[datetime] = None
    total_hours: float = 0.0
    status: str = "حاضر"  # حاضر، غائب، إجازة
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class AttendanceCreate(BaseModel):
    employee_id: str
    date: date
    check_in: Optional[datetime] = None
    check_out: Optional[datetime] = None
    status: str = "حاضر"
    notes: Optional[str] = None

# Dashboard Stats
class DashboardStats(BaseModel):
    total_projects: int
    active_projects: int
    total_budget: float
    total_actual_cost: float
    total_suppliers: int
    total_customers: int
    total_items: int
    total_employees: int
    total_sales: float
    total_purchases: float
    budget_variance: float
    projects_by_status: dict
    sales_by_month: dict
    top_customers: List[dict]
    low_stock_items: List[dict]

# ==================== API ENDPOINTS ====================

# User Management Endpoints
@api_router.post("/users", response_model=User)
async def create_user(user: UserCreate):
    # Check if username or email already exists
    existing_user = await db.users.find_one({
        "$or": [{"username": user.username}, {"email": user.email}]
    })
    if existing_user:
        raise HTTPException(status_code=400, detail="اسم المستخدم أو البريد الإلكتروني موجود مسبقاً")
    
    user_dict = user.dict()
    user_dict["id"] = str(uuid.uuid4())
    user_dict["created_at"] = datetime.utcnow()
    user_dict["is_active"] = True
    
    await db.users.insert_one(user_dict)
    return user_dict

@api_router.get("/users", response_model=List[User])
async def get_users():
    users = await db.users.find({"is_active": True}).to_list(length=1000)
    return users

@api_router.get("/users/{user_id}", response_model=User)
async def get_user(user_id: str):
    user = await db.users.find_one({"id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="المستخدم غير موجود")
    return user

# Customer Management Endpoints
@api_router.post("/customers", response_model=Customer)
async def create_customer(customer: CustomerCreate):
    customer_dict = customer.dict()
    customer_dict["id"] = str(uuid.uuid4())
    customer_dict["created_at"] = datetime.utcnow()
    customer_dict["current_balance"] = 0.0
    
    await db.customers.insert_one(customer_dict)
    return customer_dict

@api_router.get("/customers", response_model=List[Customer])
async def get_customers():
    customers = await db.customers.find().to_list(length=1000)
    return customers

@api_router.get("/customers/{customer_id}", response_model=Customer)
async def get_customer(customer_id: str):
    customer = await db.customers.find_one({"id": customer_id})
    if not customer:
        raise HTTPException(status_code=404, detail="العميل غير موجود")
    return customer

@api_router.put("/customers/{customer_id}", response_model=Customer)
async def update_customer(customer_id: str, customer_update: CustomerCreate):
    customer_dict = customer_update.dict()
    customer_dict["updated_at"] = datetime.utcnow()
    
    result = await db.customers.update_one(
        {"id": customer_id},
        {"$set": customer_dict}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="العميل غير موجود")
    
    updated_customer = await db.customers.find_one({"id": customer_id})
    return updated_customer

@api_router.delete("/customers/{customer_id}")
async def delete_customer(customer_id: str):
    result = await db.customers.delete_one({"id": customer_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="العميل غير موجود")
    return {"message": "تم حذف العميل بنجاح"}

# Project Management Endpoints
@api_router.post("/projects", response_model=Project)
async def create_project(project: ProjectCreate):
    project_dict = project.dict()
    project_dict["id"] = str(uuid.uuid4())
    project_dict["actual_cost"] = 0.0
    project_dict["progress"] = 0.0
    project_dict["created_at"] = datetime.utcnow()
    project_dict["updated_at"] = datetime.utcnow()
    
    await db.projects.insert_one(project_dict)
    return project_dict

@api_router.get("/projects", response_model=List[Project])
async def get_projects():
    projects = await db.projects.find().to_list(length=1000)
    return projects

@api_router.get("/projects/{project_id}", response_model=Project)
async def get_project(project_id: str):
    project = await db.projects.find_one({"id": project_id})
    if not project:
        raise HTTPException(status_code=404, detail="المشروع غير موجود")
    return project

@api_router.put("/projects/{project_id}", response_model=Project)
async def update_project(project_id: str, project_update: ProjectCreate):
    project_dict = project_update.dict()
    project_dict["updated_at"] = datetime.utcnow()
    
    result = await db.projects.update_one(
        {"id": project_id},
        {"$set": project_dict}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="المشروع غير موجود")
    
    updated_project = await db.projects.find_one({"id": project_id})
    return updated_project

@api_router.delete("/projects/{project_id}")
async def delete_project(project_id: str):
    result = await db.projects.delete_one({"id": project_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="المشروع غير موجود")
    return {"message": "تم حذف المشروع بنجاح"}

# Financial Management Endpoints
@api_router.post("/accounts", response_model=Account)
async def create_account(account: AccountCreate):
    account_dict = account.dict()
    account_dict["id"] = str(uuid.uuid4())
    account_dict["balance"] = 0.0
    account_dict["is_active"] = True
    account_dict["created_at"] = datetime.utcnow()
    
    await db.accounts.insert_one(account_dict)
    return account_dict

@api_router.get("/accounts", response_model=List[Account])
async def get_accounts():
    accounts = await db.accounts.find({"is_active": True}).to_list(length=1000)
    return accounts

@api_router.post("/transactions", response_model=Transaction)
async def create_transaction(transaction: TransactionCreate):
    transaction_dict = transaction.dict()
    transaction_dict["id"] = str(uuid.uuid4())
    transaction_dict["transaction_number"] = f"TXN-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
    transaction_dict["created_by"] = "system"  # TODO: Get from auth
    transaction_dict["created_at"] = datetime.utcnow()
    
    # Update account balances
    debit_account = await db.accounts.find_one({"id": transaction.debit_account})
    credit_account = await db.accounts.find_one({"id": transaction.credit_account})
    
    if not debit_account or not credit_account:
        raise HTTPException(status_code=400, detail="الحساب غير موجود")
    
    await db.accounts.update_one(
        {"id": transaction.debit_account},
        {"$inc": {"balance": transaction.amount}}
    )
    
    await db.accounts.update_one(
        {"id": transaction.credit_account},
        {"$inc": {"balance": -transaction.amount}}
    )
    
    await db.transactions.insert_one(transaction_dict)
    return transaction_dict

@api_router.get("/transactions", response_model=List[Transaction])
async def get_transactions():
    transactions = await db.transactions.find().to_list(length=1000)
    return transactions

# Inventory Management Endpoints
@api_router.post("/items", response_model=Item)
async def create_item(item: ItemCreate):
    item_dict = item.dict()
    item_dict["id"] = str(uuid.uuid4())
    item_dict["current_stock"] = 0.0
    item_dict["is_active"] = True
    item_dict["created_at"] = datetime.utcnow()
    
    await db.items.insert_one(item_dict)
    return item_dict

@api_router.get("/items", response_model=List[Item])
async def get_items():
    items = await db.items.find({"is_active": True}).to_list(length=1000)
    return items

@api_router.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: str):
    item = await db.items.find_one({"id": item_id})
    if not item:
        raise HTTPException(status_code=404, detail="الصنف غير موجود")
    return item

@api_router.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: str, item_update: ItemCreate):
    item_dict = item_update.dict()
    
    result = await db.items.update_one(
        {"id": item_id},
        {"$set": item_dict}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="الصنف غير موجود")
    
    updated_item = await db.items.find_one({"id": item_id})
    return updated_item

@api_router.delete("/items/{item_id}")
async def delete_item(item_id: str):
    result = await db.items.delete_one({"id": item_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="الصنف غير موجود")
    return {"message": "تم حذف الصنف بنجاح"}

@api_router.post("/stock-movements", response_model=StockMovement)
async def create_stock_movement(movement: StockMovementCreate):
    movement_dict = movement.dict()
    movement_dict["id"] = str(uuid.uuid4())
    movement_dict["total_cost"] = movement.quantity * movement.unit_cost
    movement_dict["created_by"] = "system"  # TODO: Get from auth
    movement_dict["created_at"] = datetime.utcnow()
    
    # Update item stock
    item = await db.items.find_one({"id": movement.item_id})
    if not item:
        raise HTTPException(status_code=404, detail="الصنف غير موجود")
    
    new_stock = item["current_stock"]
    if movement.movement_type == "in":
        new_stock += movement.quantity
    elif movement.movement_type == "out":
        new_stock -= movement.quantity
        if new_stock < 0:
            raise HTTPException(status_code=400, detail="الكمية المتوفرة غير كافية")
    
    await db.items.update_one(
        {"id": movement.item_id},
        {"$set": {"current_stock": new_stock}}
    )
    
    await db.stock_movements.insert_one(movement_dict)
    return movement_dict

@api_router.get("/stock-movements", response_model=List[StockMovement])
async def get_stock_movements():
    movements = await db.stock_movements.find().to_list(length=1000)
    return movements

# Supplier Management Endpoints
@api_router.post("/suppliers", response_model=Supplier)
async def create_supplier(supplier: SupplierCreate):
    supplier_dict = supplier.dict()
    supplier_dict["id"] = str(uuid.uuid4())
    supplier_dict["current_balance"] = 0.0
    supplier_dict["is_active"] = True
    supplier_dict["created_at"] = datetime.utcnow()
    
    await db.suppliers.insert_one(supplier_dict)
    return supplier_dict

@api_router.get("/suppliers", response_model=List[Supplier])
async def get_suppliers():
    suppliers = await db.suppliers.find({"is_active": True}).to_list(length=1000)
    return suppliers

@api_router.get("/suppliers/{supplier_id}", response_model=Supplier)
async def get_supplier(supplier_id: str):
    supplier = await db.suppliers.find_one({"id": supplier_id})
    if not supplier:
        raise HTTPException(status_code=404, detail="المورد غير موجود")
    return supplier

@api_router.put("/suppliers/{supplier_id}", response_model=Supplier)
async def update_supplier(supplier_id: str, supplier_update: SupplierCreate):
    supplier_dict = supplier_update.dict()
    
    result = await db.suppliers.update_one(
        {"id": supplier_id},
        {"$set": supplier_dict}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="المورد غير موجود")
    
    updated_supplier = await db.suppliers.find_one({"id": supplier_id})
    return updated_supplier

@api_router.delete("/suppliers/{supplier_id}")
async def delete_supplier(supplier_id: str):
    result = await db.suppliers.delete_one({"id": supplier_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="المورد غير موجود")
    return {"message": "تم حذف المورد بنجاح"}

# Cost Management Endpoints
@api_router.post("/costs", response_model=Cost)
async def create_cost(cost: CostCreate):
    cost_dict = cost.dict()
    cost_dict["id"] = str(uuid.uuid4())
    cost_dict["created_by"] = "system"  # TODO: Get from auth
    cost_dict["created_at"] = datetime.utcnow()
    
    # Update project actual cost
    await db.projects.update_one(
        {"id": cost.project_id},
        {"$inc": {"actual_cost": cost.amount}}
    )
    
    await db.costs.insert_one(cost_dict)
    return cost_dict

@api_router.get("/costs", response_model=List[Cost])
async def get_costs(project_id: Optional[str] = None):
    filter_query = {}
    if project_id:
        filter_query["project_id"] = project_id
    
    costs = await db.costs.find(filter_query).to_list(length=1000)
    return costs

@api_router.get("/costs/{cost_id}", response_model=Cost)
async def get_cost(cost_id: str):
    cost = await db.costs.find_one({"id": cost_id})
    if not cost:
        raise HTTPException(status_code=404, detail="التكلفة غير موجودة")
    return cost

@api_router.delete("/costs/{cost_id}")
async def delete_cost(cost_id: str):
    cost = await db.costs.find_one({"id": cost_id})
    if not cost:
        raise HTTPException(status_code=404, detail="التكلفة غير موجودة")
    
    # Update project actual cost
    await db.projects.update_one(
        {"id": cost["project_id"]},
        {"$inc": {"actual_cost": -cost["amount"]}}
    )
    
    result = await db.costs.delete_one({"id": cost_id})
    return {"message": "تم حذف التكلفة بنجاح"}

# Sales Management Endpoints
@api_router.post("/sales", response_model=Sale)
async def create_sale(sale: SaleCreate):
    sale_dict = sale.dict()
    sale_dict["id"] = str(uuid.uuid4())
    sale_dict["invoice_number"] = f"INV-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
    sale_dict["total_amount"] = sale.subtotal + sale.tax_amount - sale.discount_amount
    sale_dict["paid_amount"] = 0.0
    sale_dict["status"] = "معلق"
    sale_dict["created_by"] = "system"  # TODO: Get from auth
    sale_dict["created_at"] = datetime.utcnow()
    
    await db.sales.insert_one(sale_dict)
    return sale_dict

@api_router.get("/sales", response_model=List[Sale])
async def get_sales():
    sales = await db.sales.find().to_list(length=1000)
    return sales

@api_router.post("/sale-items", response_model=SaleItem)
async def create_sale_item(sale_item: SaleItemCreate):
    sale_item_dict = sale_item.dict()
    sale_item_dict["id"] = str(uuid.uuid4())
    sale_item_dict["total_price"] = sale_item.quantity * sale_item.unit_price
    sale_item_dict["created_at"] = datetime.utcnow()
    
    # Update item stock
    item = await db.items.find_one({"id": sale_item.item_id})
    if not item:
        raise HTTPException(status_code=404, detail="الصنف غير موجود")
    
    if item["current_stock"] < sale_item.quantity:
        raise HTTPException(status_code=400, detail="الكمية المتوفرة غير كافية")
    
    await db.items.update_one(
        {"id": sale_item.item_id},
        {"$inc": {"current_stock": -sale_item.quantity}}
    )
    
    await db.sale_items.insert_one(sale_item_dict)
    return sale_item_dict

# Purchase Management Endpoints
@api_router.post("/purchases", response_model=Purchase)
async def create_purchase(purchase: PurchaseCreate):
    purchase_dict = purchase.dict()
    purchase_dict["id"] = str(uuid.uuid4())
    purchase_dict["invoice_number"] = f"PO-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
    purchase_dict["total_amount"] = purchase.subtotal + purchase.tax_amount - purchase.discount_amount
    purchase_dict["paid_amount"] = 0.0
    purchase_dict["status"] = "معلق"
    purchase_dict["created_by"] = "system"  # TODO: Get from auth
    purchase_dict["created_at"] = datetime.utcnow()
    
    await db.purchases.insert_one(purchase_dict)
    return purchase_dict

@api_router.get("/purchases", response_model=List[Purchase])
async def get_purchases():
    purchases = await db.purchases.find().to_list(length=1000)
    return purchases

@api_router.post("/purchase-items", response_model=PurchaseItem)
async def create_purchase_item(purchase_item: PurchaseItemCreate):
    purchase_item_dict = purchase_item.dict()
    purchase_item_dict["id"] = str(uuid.uuid4())
    purchase_item_dict["total_cost"] = purchase_item.quantity * purchase_item.unit_cost
    purchase_item_dict["created_at"] = datetime.utcnow()
    
    await db.purchase_items.insert_one(purchase_item_dict)
    return purchase_item_dict

# HR Management Endpoints
@api_router.post("/employees", response_model=Employee)
async def create_employee(employee: EmployeeCreate):
    employee_dict = employee.dict()
    employee_dict["id"] = str(uuid.uuid4())
    employee_dict["is_active"] = True
    employee_dict["created_at"] = datetime.utcnow()
    
    await db.employees.insert_one(employee_dict)
    return employee_dict

@api_router.get("/employees", response_model=List[Employee])
async def get_employees():
    employees = await db.employees.find({"is_active": True}).to_list(length=1000)
    return employees

@api_router.post("/attendance", response_model=Attendance)
async def create_attendance(attendance: AttendanceCreate):
    attendance_dict = attendance.dict()
    attendance_dict["id"] = str(uuid.uuid4())
    attendance_dict["total_hours"] = 0.0
    attendance_dict["created_at"] = datetime.utcnow()
    
    if attendance.check_in and attendance.check_out:
        time_diff = attendance.check_out - attendance.check_in
        attendance_dict["total_hours"] = time_diff.total_seconds() / 3600
    
    await db.attendance.insert_one(attendance_dict)
    return attendance_dict

@api_router.get("/attendance", response_model=List[Attendance])
async def get_attendance(employee_id: Optional[str] = None, date: Optional[date] = None):
    filter_query = {}
    if employee_id:
        filter_query["employee_id"] = employee_id
    if date:
        filter_query["date"] = date
    
    attendance = await db.attendance.find(filter_query).to_list(length=1000)
    return attendance

# Dashboard Endpoints
@api_router.get("/dashboard/stats", response_model=DashboardStats)
async def get_dashboard_stats():
    # Get counts
    total_projects = await db.projects.count_documents({})
    active_projects = await db.projects.count_documents({"status": "نشط"})
    total_suppliers = await db.suppliers.count_documents({"is_active": True})
    total_customers = await db.customers.count_documents({})
    total_items = await db.items.count_documents({"is_active": True})
    total_employees = await db.employees.count_documents({"is_active": True})
    
    # Get financial totals
    projects = await db.projects.find().to_list(length=1000)
    total_budget = sum(p["budget"] for p in projects)
    total_actual_cost = sum(p["actual_cost"] for p in projects)
    budget_variance = total_budget - total_actual_cost
    
    # Get sales and purchases totals
    sales = await db.sales.find().to_list(length=1000)
    purchases = await db.purchases.find().to_list(length=1000)
    total_sales = sum(s["total_amount"] for s in sales)
    total_purchases = sum(p["total_amount"] for p in purchases)
    
    # Get projects by status
    projects_by_status = {}
    for project in projects:
        status = project["status"]
        projects_by_status[status] = projects_by_status.get(status, 0) + 1
    
    # Get sales by month (simplified)
    sales_by_month = {"2024": total_sales}  # TODO: Implement proper monthly aggregation
    
    # Get top customers
    customers = await db.customers.find().to_list(length=10)
    top_customers = [{"name": c["name"], "balance": c["current_balance"]} for c in customers]
    
    # Get low stock items
    items = await db.items.find({"is_active": True}).to_list(length=1000)
    low_stock_items = [
        {"name": item["name"], "current_stock": item["current_stock"], "min_stock": item["min_stock"]}
        for item in items if item["current_stock"] <= item["min_stock"]
    ]
    
    return DashboardStats(
        total_projects=total_projects,
        active_projects=active_projects,
        total_budget=total_budget,
        total_actual_cost=total_actual_cost,
        total_suppliers=total_suppliers,
        total_customers=total_customers,
        total_items=total_items,
        total_employees=total_employees,
        total_sales=total_sales,
        total_purchases=total_purchases,
        budget_variance=budget_variance,
        projects_by_status=projects_by_status,
        sales_by_month=sales_by_month,
        top_customers=top_customers,
        low_stock_items=low_stock_items
    )

# Include the API router
app.include_router(api_router)

@app.get("/")
async def root():
    return {"message": "مرحباً بك في نظام ERP المتكامل", "version": "1.0.0"}

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
from fastapi import FastAPI, APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime, date, timedelta
import json
from decimal import Decimal
from enum import Enum
import hashlib
import jwt
from passlib.context import CryptContext


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ.get('DB_NAME', 'erp_system')]

# Security
security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-here')
ALGORITHM = "HS256"

# Create the main app
app = FastAPI(title="نظام ERP المتكامل", description="نظام محاسبي متكامل لجميع القطاعات")
api_router = APIRouter(prefix="/api")

# Enums
class UserRole(str, Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    ACCOUNTANT = "accountant"
    SALES = "sales"
    PURCHASE = "purchase"
    HR = "hr"
    INVENTORY = "inventory"
    USER = "user"

class TransactionType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"
    TRANSFER = "transfer"

class OrderStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class EmployeeStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    TERMINATED = "terminated"

# Authentication Models
class User(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    username: str
    email: EmailStr
    full_name: str
    role: UserRole = UserRole.USER
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    full_name: str
    role: UserRole = UserRole.USER

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user: User

# Accounting Models
class Account(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    code: str
    name: str
    type: str  # أصول، خصوم، حقوق ملكية، إيرادات، مصروفات
    parent_id: Optional[str] = None
    balance: float = 0.0
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)

class AccountCreate(BaseModel):
    code: str
    name: str
    type: str
    parent_id: Optional[str] = None

class Transaction(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    reference: str
    description: str
    date: date
    type: TransactionType
    debit_account_id: str
    credit_account_id: str
    amount: float
    created_by: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class TransactionCreate(BaseModel):
    reference: str
    description: str
    date: date
    type: TransactionType
    debit_account_id: str
    credit_account_id: str
    amount: float

# Customer & Sales Models
class Customer(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    code: str
    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    tax_number: Optional[str] = None
    credit_limit: float = 0.0
    balance: float = 0.0
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)

class CustomerCreate(BaseModel):
    code: str
    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    tax_number: Optional[str] = None
    credit_limit: float = 0.0

class SalesOrder(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    order_number: str
    customer_id: str
    date: date
    due_date: Optional[date] = None
    status: OrderStatus = OrderStatus.PENDING
    subtotal: float = 0.0
    tax_amount: float = 0.0
    discount_amount: float = 0.0
    total_amount: float = 0.0
    notes: Optional[str] = None
    created_by: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class SalesOrderCreate(BaseModel):
    customer_id: str
    date: date
    due_date: Optional[date] = None
    notes: Optional[str] = None

class SalesOrderItem(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    order_id: str
    item_id: str
    quantity: float
    unit_price: float
    discount_percent: float = 0.0
    total_amount: float = 0.0

# HR Models
class Employee(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    employee_code: str
    first_name: str
    last_name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    department: str
    position: str
    hire_date: date
    salary: float
    status: EmployeeStatus = EmployeeStatus.ACTIVE
    created_at: datetime = Field(default_factory=datetime.utcnow)

class EmployeeCreate(BaseModel):
    employee_code: str
    first_name: str
    last_name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    department: str
    position: str
    hire_date: date
    salary: float

class Payroll(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    employee_id: str
    period_start: date
    period_end: date
    basic_salary: float
    allowances: float = 0.0
    deductions: float = 0.0
    overtime_hours: float = 0.0
    overtime_rate: float = 0.0
    net_salary: float = 0.0
    created_at: datetime = Field(default_factory=datetime.utcnow)

class PayrollCreate(BaseModel):
    employee_id: str
    period_start: date
    period_end: date
    basic_salary: float
    allowances: float = 0.0
    deductions: float = 0.0
    overtime_hours: float = 0.0
    overtime_rate: float = 0.0

# Inventory Models (Enhanced)
class Product(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    code: str
    name: str
    description: Optional[str] = None
    category: str
    unit: str
    cost_price: float = 0.0
    selling_price: float = 0.0
    current_stock: float = 0.0
    min_stock: float = 0.0
    max_stock: float = 0.0
    reorder_point: float = 0.0
    supplier_id: Optional[str] = None
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)

class ProductCreate(BaseModel):
    code: str
    name: str
    description: Optional[str] = None
    category: str
    unit: str
    cost_price: float = 0.0
    selling_price: float = 0.0
    min_stock: float = 0.0
    max_stock: float = 0.0
    reorder_point: float = 0.0
    supplier_id: Optional[str] = None

class StockMovement(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    product_id: str
    movement_type: str  # in, out, adjustment
    quantity: float
    unit_cost: float
    reference: str
    notes: Optional[str] = None
    created_by: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class StockMovementCreate(BaseModel):
    product_id: str
    movement_type: str
    quantity: float
    unit_cost: float
    reference: str
    notes: Optional[str] = None

# Purchase Models
class PurchaseOrder(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    order_number: str
    supplier_id: str
    date: date
    expected_date: Optional[date] = None
    status: OrderStatus = OrderStatus.PENDING
    subtotal: float = 0.0
    tax_amount: float = 0.0
    total_amount: float = 0.0
    notes: Optional[str] = None
    created_by: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class PurchaseOrderCreate(BaseModel):
    supplier_id: str
    date: date
    expected_date: Optional[date] = None
    notes: Optional[str] = None

# Dashboard Models
class ComprehensiveDashboardStats(BaseModel):
    # Financial
    total_revenue: float
    total_expenses: float
    net_profit: float
    accounts_receivable: float
    accounts_payable: float
    
    # Sales
    total_sales_orders: int
    pending_orders: int
    total_customers: int
    
    # Inventory
    total_products: int
    low_stock_items: int
    out_of_stock_items: int
    inventory_value: float
    
    # HR
    total_employees: int
    active_employees: int
    departments_count: int
    
    # Projects
    total_projects: int
    active_projects: int
    total_budget: float
    total_actual_cost: float
    
    # Suppliers
    total_suppliers: int
    
    # Recent activities
    recent_transactions: List[Dict[str, Any]]
    recent_orders: List[Dict[str, Any]]

# Authentication functions
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = await db.users.find_one({"username": username})
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return User(**user)

# Authentication endpoints
@api_router.post("/auth/register", response_model=User)
async def register_user(user: UserCreate):
    # Check if user already exists
    existing_user = await db.users.find_one({"$or": [{"username": user.username}, {"email": user.email}]})
    if existing_user:
        raise HTTPException(status_code=400, detail="المستخدم موجود بالفعل")
    
    # Create new user
    hashed_password = get_password_hash(user.password)
    user_dict = user.dict()
    del user_dict['password']
    user_obj = User(**user_dict)
    
    user_data = user_obj.dict()
    user_data['password'] = hashed_password
    
    await db.users.insert_one(user_data)
    return user_obj

@api_router.post("/auth/login", response_model=Token)
async def login_user(user_credentials: UserLogin):
    user = await db.users.find_one({"username": user_credentials.username})
    if not user or not verify_password(user_credentials.password, user['password']):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="اسم المستخدم أو كلمة المرور غير صحيحة",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user['username']}, expires_delta=access_token_expires
    )
    
    user_obj = User(**user)
    return Token(access_token=access_token, token_type="bearer", user=user_obj)

# Account endpoints
@api_router.post("/accounts", response_model=Account)
async def create_account(account: AccountCreate, current_user: User = Depends(get_current_user)):
    account_obj = Account(**account.dict())
    await db.accounts.insert_one(account_obj.dict())
    return account_obj

@api_router.get("/accounts", response_model=List[Account])
async def get_accounts(current_user: User = Depends(get_current_user)):
    accounts = await db.accounts.find().to_list(1000)
    return [Account(**account) for account in accounts]

# Transaction endpoints
@api_router.post("/transactions", response_model=Transaction)
async def create_transaction(transaction: TransactionCreate, current_user: User = Depends(get_current_user)):
    transaction_dict = transaction.dict()
    transaction_dict['created_by'] = current_user.id
    
    # Convert date to datetime for MongoDB
    if 'date' in transaction_dict and isinstance(transaction_dict['date'], date):
        transaction_dict['date'] = datetime.combine(transaction_dict['date'], datetime.min.time())
    
    transaction_obj = Transaction(**transaction_dict)
    transaction_data = transaction_obj.dict()
    
    # Update account balances
    if transaction.type == TransactionType.INCOME:
        await db.accounts.update_one(
            {"id": transaction.debit_account_id},
            {"$inc": {"balance": transaction.amount}}
        )
        await db.accounts.update_one(
            {"id": transaction.credit_account_id},
            {"$inc": {"balance": -transaction.amount}}
        )
    elif transaction.type == TransactionType.EXPENSE:
        await db.accounts.update_one(
            {"id": transaction.debit_account_id},
            {"$inc": {"balance": -transaction.amount}}
        )
        await db.accounts.update_one(
            {"id": transaction.credit_account_id},
            {"$inc": {"balance": transaction.amount}}
        )
    
    await db.transactions.insert_one(transaction_data)
    return transaction_obj

@api_router.get("/transactions", response_model=List[Transaction])
async def get_transactions(current_user: User = Depends(get_current_user)):
    transactions = await db.transactions.find().to_list(1000)
    return [Transaction(**transaction) for transaction in transactions]

# Customer endpoints
@api_router.post("/customers", response_model=Customer)
async def create_customer(customer: CustomerCreate, current_user: User = Depends(get_current_user)):
    customer_obj = Customer(**customer.dict())
    await db.customers.insert_one(customer_obj.dict())
    return customer_obj

@api_router.get("/customers", response_model=List[Customer])
async def get_customers(current_user: User = Depends(get_current_user)):
    customers = await db.customers.find().to_list(1000)
    return [Customer(**customer) for customer in customers]

# Sales Order endpoints
@api_router.post("/sales-orders", response_model=SalesOrder)
async def create_sales_order(order: SalesOrderCreate, current_user: User = Depends(get_current_user)):
    # Generate order number
    order_count = await db.sales_orders.count_documents({}) + 1
    order_number = f"SO-{order_count:06d}"
    
    order_dict = order.dict()
    order_dict['order_number'] = order_number
    order_dict['created_by'] = current_user.id
    
    # Convert dates to datetime for MongoDB
    if 'date' in order_dict and isinstance(order_dict['date'], date):
        order_dict['date'] = datetime.combine(order_dict['date'], datetime.min.time())
    if 'due_date' in order_dict and order_dict['due_date'] and isinstance(order_dict['due_date'], date):
        order_dict['due_date'] = datetime.combine(order_dict['due_date'], datetime.min.time())
    
    order_obj = SalesOrder(**order_dict)
    await db.sales_orders.insert_one(order_obj.dict())
    return order_obj

@api_router.get("/sales-orders", response_model=List[SalesOrder])
async def get_sales_orders(current_user: User = Depends(get_current_user)):
    orders = await db.sales_orders.find().to_list(1000)
    return [SalesOrder(**order) for order in orders]

# Employee endpoints
@api_router.post("/employees", response_model=Employee)
async def create_employee(employee: EmployeeCreate, current_user: User = Depends(get_current_user)):
    employee_dict = employee.dict()
    
    # Convert date to datetime for MongoDB
    if 'hire_date' in employee_dict and isinstance(employee_dict['hire_date'], date):
        employee_dict['hire_date'] = datetime.combine(employee_dict['hire_date'], datetime.min.time())
    
    employee_obj = Employee(**employee_dict)
    await db.employees.insert_one(employee_obj.dict())
    return employee_obj

@api_router.get("/employees", response_model=List[Employee])
async def get_employees(current_user: User = Depends(get_current_user)):
    employees = await db.employees.find().to_list(1000)
    return [Employee(**employee) for employee in employees]

# Product endpoints (Enhanced)
@api_router.post("/products", response_model=Product)
async def create_product(product: ProductCreate, current_user: User = Depends(get_current_user)):
    product_obj = Product(**product.dict())
    await db.products.insert_one(product_obj.dict())
    return product_obj

@api_router.get("/products", response_model=List[Product])
async def get_products(current_user: User = Depends(get_current_user)):
    products = await db.products.find().to_list(1000)
    return [Product(**product) for product in products]

# Stock Movement endpoints
@api_router.post("/stock-movements", response_model=StockMovement)
async def create_stock_movement(movement: StockMovementCreate, current_user: User = Depends(get_current_user)):
    movement_dict = movement.dict()
    movement_dict['created_by'] = current_user.id
    
    movement_obj = StockMovement(**movement_dict)
    
    # Update product stock
    if movement.movement_type == "in":
        await db.products.update_one(
            {"id": movement.product_id},
            {"$inc": {"current_stock": movement.quantity}}
        )
    elif movement.movement_type == "out":
        await db.products.update_one(
            {"id": movement.product_id},
            {"$inc": {"current_stock": -movement.quantity}}
        )
    
    await db.stock_movements.insert_one(movement_obj.dict())
    return movement_obj

@api_router.get("/stock-movements", response_model=List[StockMovement])
async def get_stock_movements(current_user: User = Depends(get_current_user)):
    movements = await db.stock_movements.find().to_list(1000)
    return [StockMovement(**movement) for movement in movements]

# Purchase Order endpoints
@api_router.post("/purchase-orders", response_model=PurchaseOrder)
async def create_purchase_order(order: PurchaseOrderCreate, current_user: User = Depends(get_current_user)):
    # Generate order number
    order_count = await db.purchase_orders.count_documents({}) + 1
    order_number = f"PO-{order_count:06d}"
    
    order_dict = order.dict()
    order_dict['order_number'] = order_number
    order_dict['created_by'] = current_user.id
    
    # Convert dates to datetime for MongoDB
    if 'date' in order_dict and isinstance(order_dict['date'], date):
        order_dict['date'] = datetime.combine(order_dict['date'], datetime.min.time())
    if 'expected_date' in order_dict and order_dict['expected_date'] and isinstance(order_dict['expected_date'], date):
        order_dict['expected_date'] = datetime.combine(order_dict['expected_date'], datetime.min.time())
    
    order_obj = PurchaseOrder(**order_dict)
    await db.purchase_orders.insert_one(order_obj.dict())
    return order_obj

@api_router.get("/purchase-orders", response_model=List[PurchaseOrder])
async def get_purchase_orders(current_user: User = Depends(get_current_user)):
    orders = await db.purchase_orders.find().to_list(1000)
    return [PurchaseOrder(**order) for order in orders]

# Existing endpoints (Projects, Costs, Suppliers, Items) - keeping them for backward compatibility

# Dashboard Stats Model (for backward compatibility)
class DashboardStats(BaseModel):
    total_projects: int
    active_projects: int
    total_budget: float
    total_actual_cost: float
    total_suppliers: int
    total_items: int
    budget_variance: float
    projects_by_status: dict

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
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None
    start_date: date
    end_date: Optional[date] = None
    budget: float
    client_name: Optional[str] = None

class Cost(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    project_id: str
    category: str  # مواد، عمالة، معدات، أخرى
    description: str
    amount: float
    date: date
    supplier_id: Optional[str] = None
    invoice_number: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class CostCreate(BaseModel):
    project_id: str
    category: str
    description: str
    amount: float
    date: date
    supplier_id: Optional[str] = None
    invoice_number: Optional[str] = None

class Supplier(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    contact_person: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    category: str  # مواد، خدمات، معدات
    created_at: datetime = Field(default_factory=datetime.utcnow)

class SupplierCreate(BaseModel):
    name: str
    contact_person: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    category: str

class Item(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    code: str
    unit: str  # متر، كيلو، قطعة، إلخ
    current_stock: float = 0.0
    min_stock: float = 0.0
    unit_cost: float = 0.0
    category: str
    supplier_id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class ItemCreate(BaseModel):
    name: str
    code: str
    unit: str
    min_stock: float = 0.0
    unit_cost: float = 0.0
    category: str
    supplier_id: Optional[str] = None

# Projects endpoints
@api_router.post("/projects", response_model=Project)
async def create_project(project: ProjectCreate):
    project_dict = project.dict()
    # Convert date objects to datetime for MongoDB compatibility
    if 'start_date' in project_dict and project_dict['start_date']:
        project_dict['start_date'] = datetime.combine(project_dict['start_date'], datetime.min.time())
    if 'end_date' in project_dict and project_dict['end_date']:
        project_dict['end_date'] = datetime.combine(project_dict['end_date'], datetime.min.time())
    
    project_obj = Project(**project_dict)
    project_data = project_obj.dict()
    # Convert date objects to datetime for MongoDB
    if 'start_date' in project_data and isinstance(project_data['start_date'], date):
        project_data['start_date'] = datetime.combine(project_data['start_date'], datetime.min.time())
    if 'end_date' in project_data and isinstance(project_data['end_date'], date):
        project_data['end_date'] = datetime.combine(project_data['end_date'], datetime.min.time())
    
    await db.projects.insert_one(project_data)
    return project_obj

@api_router.get("/projects", response_model=List[Project])
async def get_projects():
    projects = await db.projects.find().to_list(1000)
    return [Project(**project) for project in projects]

@api_router.get("/projects/{project_id}", response_model=Project)
async def get_project(project_id: str):
    project = await db.projects.find_one({"id": project_id})
    if not project:
        raise HTTPException(status_code=404, detail="المشروع غير موجود")
    return Project(**project)

@api_router.put("/projects/{project_id}", response_model=Project)
async def update_project(project_id: str, project_update: ProjectCreate):
    project_dict = project_update.dict()
    project_dict["updated_at"] = datetime.utcnow()
    
    # Convert date objects to datetime for MongoDB compatibility
    if 'start_date' in project_dict and isinstance(project_dict['start_date'], date):
        project_dict['start_date'] = datetime.combine(project_dict['start_date'], datetime.min.time())
    if 'end_date' in project_dict and project_dict['end_date'] and isinstance(project_dict['end_date'], date):
        project_dict['end_date'] = datetime.combine(project_dict['end_date'], datetime.min.time())
    
    result = await db.projects.update_one(
        {"id": project_id}, 
        {"$set": project_dict}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="المشروع غير موجود")
    
    updated_project = await db.projects.find_one({"id": project_id})
    return Project(**updated_project)

@api_router.delete("/projects/{project_id}")
async def delete_project(project_id: str):
    result = await db.projects.delete_one({"id": project_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="المشروع غير موجود")
    return {"message": "تم حذف المشروع بنجاح"}

# Costs endpoints
@api_router.post("/costs", response_model=Cost)
async def create_cost(cost: CostCreate):
    cost_dict = cost.dict()
    # Convert date to datetime for MongoDB compatibility
    if 'date' in cost_dict and isinstance(cost_dict['date'], date):
        cost_dict['date'] = datetime.combine(cost_dict['date'], datetime.min.time())
    
    cost_obj = Cost(**cost_dict)
    cost_data = cost_obj.dict()
    # Convert date to datetime for MongoDB
    if 'date' in cost_data and isinstance(cost_data['date'], date):
        cost_data['date'] = datetime.combine(cost_data['date'], datetime.min.time())
    
    # Update project actual cost
    await db.projects.update_one(
        {"id": cost.project_id},
        {"$inc": {"actual_cost": cost.amount}}
    )
    
    await db.costs.insert_one(cost_data)
    return cost_obj

@api_router.get("/costs", response_model=List[Cost])
async def get_costs(project_id: Optional[str] = None):
    query = {}
    if project_id:
        query["project_id"] = project_id
    
    costs = await db.costs.find(query).to_list(1000)
    return [Cost(**cost) for cost in costs]

@api_router.get("/costs/{cost_id}", response_model=Cost)
async def get_cost(cost_id: str):
    cost = await db.costs.find_one({"id": cost_id})
    if not cost:
        raise HTTPException(status_code=404, detail="التكلفة غير موجودة")
    return Cost(**cost)

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
    
    await db.costs.delete_one({"id": cost_id})
    return {"message": "تم حذف التكلفة بنجاح"}

# Suppliers endpoints
@api_router.post("/suppliers", response_model=Supplier)
async def create_supplier(supplier: SupplierCreate):
    supplier_dict = supplier.dict()
    supplier_obj = Supplier(**supplier_dict)
    await db.suppliers.insert_one(supplier_obj.dict())
    return supplier_obj

@api_router.get("/suppliers", response_model=List[Supplier])
async def get_suppliers():
    suppliers = await db.suppliers.find().to_list(1000)
    return [Supplier(**supplier) for supplier in suppliers]

@api_router.get("/suppliers/{supplier_id}", response_model=Supplier)
async def get_supplier(supplier_id: str):
    supplier = await db.suppliers.find_one({"id": supplier_id})
    if not supplier:
        raise HTTPException(status_code=404, detail="المورد غير موجود")
    return Supplier(**supplier)

@api_router.put("/suppliers/{supplier_id}", response_model=Supplier)
async def update_supplier(supplier_id: str, supplier_update: SupplierCreate):
    result = await db.suppliers.update_one(
        {"id": supplier_id}, 
        {"$set": supplier_update.dict()}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="المورد غير موجود")
    
    updated_supplier = await db.suppliers.find_one({"id": supplier_id})
    return Supplier(**updated_supplier)

@api_router.delete("/suppliers/{supplier_id}")
async def delete_supplier(supplier_id: str):
    result = await db.suppliers.delete_one({"id": supplier_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="المورد غير موجود")
    return {"message": "تم حذف المورد بنجاح"}

# Items endpoints
@api_router.post("/items", response_model=Item)
async def create_item(item: ItemCreate):
    item_dict = item.dict()
    item_obj = Item(**item_dict)
    await db.items.insert_one(item_obj.dict())
    return item_obj

@api_router.get("/items", response_model=List[Item])
async def get_items():
    items = await db.items.find().to_list(1000)
    return [Item(**item) for item in items]

@api_router.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: str):
    item = await db.items.find_one({"id": item_id})
    if not item:
        raise HTTPException(status_code=404, detail="الصنف غير موجود")
    return Item(**item)

@api_router.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: str, item_update: ItemCreate):
    result = await db.items.update_one(
        {"id": item_id}, 
        {"$set": item_update.dict()}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="الصنف غير موجود")
    
    updated_item = await db.items.find_one({"id": item_id})
    return Item(**updated_item)

@api_router.delete("/items/{item_id}")
async def delete_item(item_id: str):
    result = await db.items.delete_one({"id": item_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="الصنف غير موجود")
    return {"message": "تم حذف الصنف بنجاح"}

# Dashboard stats endpoint (for backward compatibility)
@api_router.get("/dashboard/stats", response_model=DashboardStats)
async def get_dashboard_stats():
    # Get counts
    total_projects = await db.projects.count_documents({})
    active_projects = await db.projects.count_documents({"status": "نشط"})
    total_suppliers = await db.suppliers.count_documents({})
    total_items = await db.items.count_documents({})
    
    # Get financial data
    projects = await db.projects.find().to_list(1000)
    total_budget = sum(project.get("budget", 0) for project in projects)
    total_actual_cost = sum(project.get("actual_cost", 0) for project in projects)
    budget_variance = total_budget - total_actual_cost
    
    # Projects by status
    projects_by_status = {}
    for project in projects:
        status = project.get("status", "نشط")
        projects_by_status[status] = projects_by_status.get(status, 0) + 1
    
    return DashboardStats(
        total_projects=total_projects,
        active_projects=active_projects,
        total_budget=total_budget,
        total_actual_cost=total_actual_cost,
        total_suppliers=total_suppliers,
        total_items=total_items,
        budget_variance=budget_variance,
        projects_by_status=projects_by_status
    )

# Comprehensive Dashboard endpoint
@api_router.get("/dashboard/comprehensive-stats", response_model=ComprehensiveDashboardStats)
async def get_comprehensive_dashboard_stats(current_user: User = Depends(get_current_user)):
    # Financial calculations
    transactions = await db.transactions.find().to_list(1000)
    total_revenue = sum(t.get("amount", 0) for t in transactions if t.get("type") == "income")
    total_expenses = sum(t.get("amount", 0) for t in transactions if t.get("type") == "expense")
    net_profit = total_revenue - total_expenses
    
    # Sales
    total_sales_orders = await db.sales_orders.count_documents({})
    pending_orders = await db.sales_orders.count_documents({"status": "pending"})
    total_customers = await db.customers.count_documents({})
    
    # Inventory
    total_products = await db.products.count_documents({})
    products = await db.products.find().to_list(1000)
    low_stock_items = len([p for p in products if p.get("current_stock", 0) <= p.get("min_stock", 0)])
    out_of_stock_items = len([p for p in products if p.get("current_stock", 0) == 0])
    inventory_value = sum(p.get("current_stock", 0) * p.get("cost_price", 0) for p in products)
    
    # HR
    total_employees = await db.employees.count_documents({})
    active_employees = await db.employees.count_documents({"status": "active"})
    employees = await db.employees.find().to_list(1000)
    departments = set(emp.get("department") for emp in employees)
    departments_count = len(departments)
    
    # Projects (existing)
    total_projects = await db.projects.count_documents({})
    active_projects = await db.projects.count_documents({"status": "نشط"})
    projects = await db.projects.find().to_list(1000)
    total_budget = sum(project.get("budget", 0) for project in projects)
    total_actual_cost = sum(project.get("actual_cost", 0) for project in projects)
    
    # Suppliers
    total_suppliers = await db.suppliers.count_documents({})
    
    # Recent activities
    recent_transactions = await db.transactions.find().sort("created_at", -1).limit(5).to_list(5)
    recent_orders = await db.sales_orders.find().sort("created_at", -1).limit(5).to_list(5)
    
    return ComprehensiveDashboardStats(
        total_revenue=total_revenue,
        total_expenses=total_expenses,
        net_profit=net_profit,
        accounts_receivable=0.0,  # Calculate based on customer balances
        accounts_payable=0.0,     # Calculate based on supplier balances
        total_sales_orders=total_sales_orders,
        pending_orders=pending_orders,
        total_customers=total_customers,
        total_products=total_products,
        low_stock_items=low_stock_items,
        out_of_stock_items=out_of_stock_items,
        inventory_value=inventory_value,
        total_employees=total_employees,
        active_employees=active_employees,
        departments_count=departments_count,
        total_projects=total_projects,
        active_projects=active_projects,
        total_budget=total_budget,
        total_actual_cost=total_actual_cost,
        total_suppliers=total_suppliers,
        recent_transactions=recent_transactions,
        recent_orders=recent_orders
    )

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
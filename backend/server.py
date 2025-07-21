from fastapi import FastAPI, APIRouter, HTTPException, UploadFile, File
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime, date, timedelta
import json
from decimal import Decimal
import base64
from enum import Enum


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")


# Define Enums
class ProjectStatus(str, Enum):
    ACTIVE = "نشط"
    PAUSED = "متوقف"  
    COMPLETED = "مكتمل"
    CANCELLED = "ملغي"

class EmployeeStatus(str, Enum):
    ACTIVE = "نشط"
    INACTIVE = "غير نشط"
    ON_LEAVE = "في إجازة"

class ContractStatus(str, Enum):
    DRAFT = "مسودة"
    ACTIVE = "نشط"
    COMPLETED = "مكتمل"
    CANCELLED = "ملغي"

class AlertPriority(str, Enum):
    LOW = "منخفض"
    MEDIUM = "متوسط"
    HIGH = "عالي"
    CRITICAL = "حرج"

class ApprovalStatus(str, Enum):
    PENDING = "في الانتظار"
    APPROVED = "موافق عليه"
    REJECTED = "مرفوض"
    CANCELLED = "ملغي"

# Define Models
# Enhanced Project Model with advanced features
class Project(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    code: Optional[str] = None  # Project code for reference
    description: Optional[str] = None
    start_date: date
    end_date: Optional[date] = None
    budget: float
    actual_cost: float = 0.0
    status: ProjectStatus = ProjectStatus.ACTIVE
    client_name: Optional[str] = None
    project_manager_id: Optional[str] = None
    priority: AlertPriority = AlertPriority.MEDIUM
    progress_percentage: float = 0.0
    estimated_completion_date: Optional[date] = None
    profit_margin: float = 0.0
    risk_level: AlertPriority = AlertPriority.LOW
    location: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class ProjectCreate(BaseModel):
    name: str
    code: Optional[str] = None
    description: Optional[str] = None
    start_date: date
    end_date: Optional[date] = None
    budget: float
    client_name: Optional[str] = None
    project_manager_id: Optional[str] = None
    priority: AlertPriority = AlertPriority.MEDIUM
    location: Optional[str] = None

# Employee Management Models
class Employee(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    employee_number: str
    name: str
    position: str
    department: str
    email: Optional[str] = None
    phone: Optional[str] = None
    hire_date: date
    salary: float
    status: EmployeeStatus = EmployeeStatus.ACTIVE
    national_id: Optional[str] = None
    address: Optional[str] = None
    emergency_contact: Optional[str] = None
    bank_account: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class EmployeeCreate(BaseModel):
    employee_number: str
    name: str
    position: str
    department: str
    email: Optional[str] = None
    phone: Optional[str] = None
    hire_date: date
    salary: float
    national_id: Optional[str] = None
    address: Optional[str] = None
    emergency_contact: Optional[str] = None
    bank_account: Optional[str] = None

# Contract Management Models
class Contract(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    contract_number: str
    project_id: str
    contractor_name: str
    description: str
    start_date: date
    end_date: date
    total_value: float
    paid_amount: float = 0.0
    remaining_amount: float = 0.0
    status: ContractStatus = ContractStatus.DRAFT
    terms: Optional[str] = None
    penalty_clause: Optional[str] = None
    contact_person: Optional[str] = None
    contact_phone: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
class ContractCreate(BaseModel):
    contract_number: str
    project_id: str
    contractor_name: str
    description: str
    start_date: date
    end_date: date
    total_value: float
    terms: Optional[str] = None
    penalty_clause: Optional[str] = None
    contact_person: Optional[str] = None
    contact_phone: Optional[str] = None

# Alert System Models
class Alert(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    message: str
    priority: AlertPriority
    type: str  # مالي، مشروع، موظف، عقد
    related_id: Optional[str] = None  # ID of related entity
    is_read: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = None

class AlertCreate(BaseModel):
    title: str
    message: str
    priority: AlertPriority
    type: str
    related_id: Optional[str] = None
    expires_at: Optional[datetime] = None

# Document Management Models
class Document(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    type: str  # عقد، فاتورة، تقرير، صورة
    project_id: Optional[str] = None
    contract_id: Optional[str] = None
    file_data: str  # Base64 encoded file
    file_size: int
    file_type: str  # pdf, doc, image
    uploaded_by: Optional[str] = None
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class DocumentCreate(BaseModel):
    name: str
    type: str
    project_id: Optional[str] = None
    contract_id: Optional[str] = None
    file_data: str
    file_size: int
    file_type: str
    uploaded_by: Optional[str] = None
    description: Optional[str] = None

# Time Tracking Models
class TimeEntry(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    employee_id: str
    project_id: str
    task_description: str
    start_time: datetime
    end_time: Optional[datetime] = None
    duration_hours: float = 0.0
    billable_hours: float = 0.0
    hourly_rate: float = 0.0
    date: date
    created_at: datetime = Field(default_factory=datetime.utcnow)

class TimeEntryCreate(BaseModel):
    employee_id: str
    project_id: str
    task_description: str
    start_time: datetime
    end_time: Optional[datetime] = None
    duration_hours: float
    billable_hours: float = 0.0
    hourly_rate: float = 0.0
    date: date

# Approval System Models  
class Approval(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    type: str  # cost_approval, contract_approval, budget_change
    request_id: str  # ID of the item requiring approval
    requested_by: str
    approver_id: Optional[str] = None
    status: ApprovalStatus = ApprovalStatus.PENDING
    amount: Optional[float] = None
    description: str
    request_date: datetime = Field(default_factory=datetime.utcnow)
    approval_date: Optional[datetime] = None
    comments: Optional[str] = None

class ApprovalCreate(BaseModel):
    type: str
    request_id: str
    requested_by: str
    approver_id: Optional[str] = None
    amount: Optional[float] = None
    description: str
    comments: Optional[str] = None

# Enhanced Cost Model
class Cost(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    project_id: str
    category: str  # مواد، عمالة، معدات، أخرى
    subcategory: Optional[str] = None
    description: str
    amount: float
    date: date
    supplier_id: Optional[str] = None
    invoice_number: Optional[str] = None
    receipt_image: Optional[str] = None  # Base64 encoded image
    approved_by: Optional[str] = None
    approval_status: ApprovalStatus = ApprovalStatus.APPROVED
    payment_method: str = "نقدي"  # نقدي، بنكي، شيك
    reference_number: Optional[str] = None
    tax_amount: float = 0.0
    created_at: datetime = Field(default_factory=datetime.utcnow)

class CostCreate(BaseModel):
    project_id: str
    category: str
    subcategory: Optional[str] = None
    description: str
    amount: float
    date: date
    supplier_id: Optional[str] = None
    invoice_number: Optional[str] = None
    receipt_image: Optional[str] = None
    payment_method: str = "نقدي"
    reference_number: Optional[str] = None
    tax_amount: float = 0.0

# Enhanced Supplier Model
class Supplier(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    code: Optional[str] = None
    contact_person: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    category: str  # مواد، خدمات، معدات
    tax_number: Optional[str] = None
    bank_account: Optional[str] = None
    credit_limit: float = 0.0
    current_balance: float = 0.0
    rating: int = 5  # 1-5 stars
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class SupplierCreate(BaseModel):
    name: str
    code: Optional[str] = None
    contact_person: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    category: str
    tax_number: Optional[str] = None
    bank_account: Optional[str] = None
    credit_limit: float = 0.0
    rating: int = 5

# Enhanced Item Model
class Item(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    code: str
    barcode: Optional[str] = None
    unit: str  # متر، كيلو، قطعة، إلخ
    current_stock: float = 0.0
    min_stock: float = 0.0
    max_stock: float = 0.0
    unit_cost: float = 0.0
    selling_price: float = 0.0
    category: str
    subcategory: Optional[str] = None
    supplier_id: Optional[str] = None
    location: Optional[str] = None  # موقع التخزين
    expiry_date: Optional[date] = None
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class ItemCreate(BaseModel):
    name: str
    code: str
    barcode: Optional[str] = None
    unit: str
    min_stock: float = 0.0
    max_stock: float = 0.0
    unit_cost: float = 0.0
    selling_price: float = 0.0
    category: str
    subcategory: Optional[str] = None
    supplier_id: Optional[str] = None
    location: Optional[str] = None
    expiry_date: Optional[date] = None
    notes: Optional[str] = None

# Enhanced Dashboard Stats Model
class DashboardStats(BaseModel):
    total_projects: int
    active_projects: int
    completed_projects: int
    total_budget: float
    total_actual_cost: float
    total_suppliers: int
    total_employees: int
    total_items: int
    total_contracts: int
    pending_approvals: int
    unread_alerts: int
    budget_variance: float
    profit_margin: float
    projects_by_status: Dict[str, int]
    costs_by_category: Dict[str, float]
    top_projects_by_cost: List[Dict[str, Any]]
    overdue_projects: int
    low_stock_items: int
    monthly_expenses: List[Dict[str, Any]]
    
# Financial Report Models
class FinancialReport(BaseModel):
    project_id: Optional[str] = None
    start_date: date
    end_date: date
    total_income: float
    total_expenses: float
    net_profit: float
    profit_margin: float
    expenses_by_category: Dict[str, float]
    monthly_breakdown: List[Dict[str, Any]]

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

# Dashboard stats endpoint
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
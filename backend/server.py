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

# Enhanced Projects endpoints
@api_router.post("/projects", response_model=Project)
async def create_project(project: ProjectCreate):
    project_dict = project.dict()
    # Convert date objects to datetime for MongoDB compatibility
    if 'start_date' in project_dict and project_dict['start_date']:
        project_dict['start_date'] = datetime.combine(project_dict['start_date'], datetime.min.time())
    if 'end_date' in project_dict and project_dict['end_date']:
        project_dict['end_date'] = datetime.combine(project_dict['end_date'], datetime.min.time())
    
    # Auto-generate project code if not provided
    if not project_dict.get('code'):
        project_count = await db.projects.count_documents({}) + 1
        project_dict['code'] = f"PRJ-{project_count:04d}"
    
    # Calculate estimated completion date if not provided
    if project_dict.get('end_date'):
        project_dict['estimated_completion_date'] = project_dict['end_date']
    
    project_obj = Project(**project_dict)
    project_data = project_obj.dict()
    
    # Convert date objects to datetime for MongoDB
    if 'start_date' in project_data and isinstance(project_data['start_date'], date):
        project_data['start_date'] = datetime.combine(project_data['start_date'], datetime.min.time())
    if 'end_date' in project_data and isinstance(project_data['end_date'], date):
        project_data['end_date'] = datetime.combine(project_data['end_date'], datetime.min.time())
    if 'estimated_completion_date' in project_data and isinstance(project_data['estimated_completion_date'], date):
        project_data['estimated_completion_date'] = datetime.combine(project_data['estimated_completion_date'], datetime.min.time())
    
    await db.projects.insert_one(project_data)
    
    # Create alert for new project
    alert_data = AlertCreate(
        title="مشروع جديد",
        message=f"تم إنشاء مشروع جديد: {project.name}",
        priority=AlertPriority.MEDIUM,
        type="مشروع",
        related_id=project_obj.id
    )
    await create_alert(alert_data)
    
    return project_obj

@api_router.get("/projects", response_model=List[Project])
async def get_projects(status: Optional[str] = None, priority: Optional[str] = None):
    query = {}
    if status:
        query["status"] = status
    if priority:
        query["priority"] = priority
        
    projects = await db.projects.find(query).to_list(1000)
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

@api_router.put("/projects/{project_id}/progress")
async def update_project_progress(project_id: str, progress: float):
    if progress < 0 or progress > 100:
        raise HTTPException(status_code=400, detail="نسبة الإنجاز يجب أن تكون بين 0 و 100")
    
    result = await db.projects.update_one(
        {"id": project_id},
        {"$set": {"progress_percentage": progress, "updated_at": datetime.utcnow()}}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="المشروع غير موجود")
    
    # Auto-update status based on progress
    status_update = {}
    if progress == 100:
        status_update["status"] = ProjectStatus.COMPLETED
    elif progress > 0:
        status_update["status"] = ProjectStatus.ACTIVE
        
    if status_update:
        await db.projects.update_one({"id": project_id}, {"$set": status_update})
    
    return {"message": "تم تحديث نسبة الإنجاز بنجاح"}

# Employee Management endpoints
@api_router.post("/employees", response_model=Employee)
async def create_employee(employee: EmployeeCreate):
    employee_dict = employee.dict()
    if 'hire_date' in employee_dict and isinstance(employee_dict['hire_date'], date):
        employee_dict['hire_date'] = datetime.combine(employee_dict['hire_date'], datetime.min.time())
    
    employee_obj = Employee(**employee_dict)
    employee_data = employee_obj.dict()
    
    if 'hire_date' in employee_data and isinstance(employee_data['hire_date'], date):
        employee_data['hire_date'] = datetime.combine(employee_data['hire_date'], datetime.min.time())
    
    await db.employees.insert_one(employee_data)
    return employee_obj

@api_router.get("/employees", response_model=List[Employee])
async def get_employees(department: Optional[str] = None, status: Optional[str] = None):
    query = {}
    if department:
        query["department"] = department
    if status:
        query["status"] = status
        
    employees = await db.employees.find(query).to_list(1000)
    return [Employee(**employee) for employee in employees]

@api_router.get("/employees/{employee_id}", response_model=Employee)
async def get_employee(employee_id: str):
    employee = await db.employees.find_one({"id": employee_id})
    if not employee:
        raise HTTPException(status_code=404, detail="الموظف غير موجود")
    return Employee(**employee)

# Contract Management endpoints
@api_router.post("/contracts", response_model=Contract)
async def create_contract(contract: ContractCreate):
    contract_dict = contract.dict()
    
    # Convert dates to datetime
    if 'start_date' in contract_dict and isinstance(contract_dict['start_date'], date):
        contract_dict['start_date'] = datetime.combine(contract_dict['start_date'], datetime.min.time())
    if 'end_date' in contract_dict and isinstance(contract_dict['end_date'], date):
        contract_dict['end_date'] = datetime.combine(contract_dict['end_date'], datetime.min.time())
    
    # Calculate remaining amount
    contract_dict['remaining_amount'] = contract_dict['total_value']
    
    contract_obj = Contract(**contract_dict)
    contract_data = contract_obj.dict()
    
    # Convert dates for MongoDB
    for date_field in ['start_date', 'end_date']:
        if date_field in contract_data and isinstance(contract_data[date_field], date):
            contract_data[date_field] = datetime.combine(contract_data[date_field], datetime.min.time())
    
    await db.contracts.insert_one(contract_data)
    
    # Create alert for new contract
    alert_data = AlertCreate(
        title="عقد جديد",
        message=f"تم إنشاء عقد جديد مع: {contract.contractor_name}",
        priority=AlertPriority.MEDIUM,
        type="عقد",
        related_id=contract_obj.id
    )
    await create_alert(alert_data)
    
    return contract_obj

@api_router.get("/contracts", response_model=List[Contract])
async def get_contracts(project_id: Optional[str] = None, status: Optional[str] = None):
    query = {}
    if project_id:
        query["project_id"] = project_id
    if status:
        query["status"] = status
        
    contracts = await db.contracts.find(query).to_list(1000)
    return [Contract(**contract) for contract in contracts]

# Alert System endpoints
@api_router.post("/alerts", response_model=Alert)
async def create_alert(alert: AlertCreate):
    alert_obj = Alert(**alert.dict())
    await db.alerts.insert_one(alert_obj.dict())
    return alert_obj

@api_router.get("/alerts", response_model=List[Alert])
async def get_alerts(unread_only: bool = False, priority: Optional[str] = None):
    query = {}
    if unread_only:
        query["is_read"] = False
    if priority:
        query["priority"] = priority
        
    alerts = await db.alerts.find(query).sort("created_at", -1).to_list(100)
    return [Alert(**alert) for alert in alerts]

@api_router.put("/alerts/{alert_id}/read")
async def mark_alert_as_read(alert_id: str):
    result = await db.alerts.update_one(
        {"id": alert_id},
        {"$set": {"is_read": True}}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="التنبيه غير موجود")
    
    return {"message": "تم تحديد التنبيه كمقروء"}

# Document Management endpoints
@api_router.post("/documents", response_model=Document)
async def create_document(document: DocumentCreate):
    document_obj = Document(**document.dict())
    await db.documents.insert_one(document_obj.dict())
    return document_obj

@api_router.get("/documents", response_model=List[Document])
async def get_documents(project_id: Optional[str] = None, type: Optional[str] = None):
    query = {}
    if project_id:
        query["project_id"] = project_id
    if type:
        query["type"] = type
        
    documents = await db.documents.find(query).to_list(1000)
    return [Document(**doc) for doc in documents]

# Time Tracking endpoints
@api_router.post("/time-entries", response_model=TimeEntry)
async def create_time_entry(time_entry: TimeEntryCreate):
    time_entry_dict = time_entry.dict()
    
    # Convert date and datetime fields
    if 'date' in time_entry_dict and isinstance(time_entry_dict['date'], date):
        time_entry_dict['date'] = datetime.combine(time_entry_dict['date'], datetime.min.time())
    
    time_entry_obj = TimeEntry(**time_entry_dict)
    time_entry_data = time_entry_obj.dict()
    
    if 'date' in time_entry_data and isinstance(time_entry_data['date'], date):
        time_entry_data['date'] = datetime.combine(time_entry_data['date'], datetime.min.time())
    
    await db.time_entries.insert_one(time_entry_data)
    return time_entry_obj

@api_router.get("/time-entries", response_model=List[TimeEntry])
async def get_time_entries(employee_id: Optional[str] = None, project_id: Optional[str] = None):
    query = {}
    if employee_id:
        query["employee_id"] = employee_id
    if project_id:
        query["project_id"] = project_id
        
    time_entries = await db.time_entries.find(query).to_list(1000)
    return [TimeEntry(**entry) for entry in time_entries]

# Enhanced Costs endpoints with approval workflow
@api_router.post("/costs", response_model=Cost)
async def create_cost(cost: CostCreate):
    cost_dict = cost.dict()
    # Convert date to datetime for MongoDB compatibility
    if 'date' in cost_dict and isinstance(cost_dict['date'], date):
        cost_dict['date'] = datetime.combine(cost_dict['date'], datetime.min.time())
    
    # For high amount costs, require approval
    if cost_dict['amount'] > 10000:  # Costs above 10,000 need approval
        cost_dict['approval_status'] = ApprovalStatus.PENDING
        
        # Create approval request
        approval_data = ApprovalCreate(
            type="cost_approval",
            request_id=str(uuid.uuid4()),
            requested_by="system",
            amount=cost_dict['amount'],
            description=f"موافقة على تكلفة: {cost_dict['description']}"
        )
        await create_approval(approval_data)
        
        # Create alert for approval needed
        alert_data = AlertCreate(
            title="موافقة مطلوبة",
            message=f"تكلفة تتطلب موافقة: {cost_dict['description']} - {cost_dict['amount']} ر.س",
            priority=AlertPriority.HIGH,
            type="مالي",
            related_id=cost_dict.get('project_id')
        )
        await create_alert(alert_data)
    
    cost_obj = Cost(**cost_dict)
    cost_data = cost_obj.dict()
    # Convert date to datetime for MongoDB
    if 'date' in cost_data and isinstance(cost_data['date'], date):
        cost_data['date'] = datetime.combine(cost_data['date'], datetime.min.time())
    
    # Update project actual cost only if approved
    if cost_obj.approval_status == ApprovalStatus.APPROVED:
        await db.projects.update_one(
            {"id": cost.project_id},
            {"$inc": {"actual_cost": cost.amount}}
        )
    
    await db.costs.insert_one(cost_data)
    return cost_obj

@api_router.get("/costs", response_model=List[Cost])
async def get_costs(
    project_id: Optional[str] = None, 
    category: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None
):
    query = {}
    if project_id:
        query["project_id"] = project_id
    if category:
        query["category"] = category
    if start_date or end_date:
        date_query = {}
        if start_date:
            date_query["$gte"] = datetime.combine(start_date, datetime.min.time())
        if end_date:
            date_query["$lte"] = datetime.combine(end_date, datetime.max.time())
        query["date"] = date_query
    
    costs = await db.costs.find(query).sort("date", -1).to_list(1000)
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
    
    # Update project actual cost if cost was approved
    if cost.get('approval_status') == ApprovalStatus.APPROVED:
        await db.projects.update_one(
            {"id": cost["project_id"]},
            {"$inc": {"actual_cost": -cost["amount"]}}
        )
    
    await db.costs.delete_one({"id": cost_id})
    return {"message": "تم حذف التكلفة بنجاح"}

@api_router.put("/costs/{cost_id}/approve")
async def approve_cost(cost_id: str, approver_id: str):
    cost = await db.costs.find_one({"id": cost_id})
    if not cost:
        raise HTTPException(status_code=404, detail="التكلفة غير موجودة")
    
    # Update cost approval status
    await db.costs.update_one(
        {"id": cost_id},
        {"$set": {
            "approval_status": ApprovalStatus.APPROVED,
            "approved_by": approver_id
        }}
    )
    
    # Update project actual cost
    await db.projects.update_one(
        {"id": cost["project_id"]},
        {"$inc": {"actual_cost": cost["amount"]}}
    )
    
    return {"message": "تم اعتماد التكلفة بنجاح"}

# Approval System endpoints
@api_router.post("/approvals", response_model=Approval)
async def create_approval(approval: ApprovalCreate):
    approval_obj = Approval(**approval.dict())
    await db.approvals.insert_one(approval_obj.dict())
    return approval_obj

@api_router.get("/approvals", response_model=List[Approval])
async def get_approvals(status: Optional[str] = None, type: Optional[str] = None):
    query = {}
    if status:
        query["status"] = status
    if type:
        query["type"] = type
        
    approvals = await db.approvals.find(query).sort("request_date", -1).to_list(1000)
    return [Approval(**approval) for approval in approvals]

@api_router.put("/approvals/{approval_id}")
async def process_approval(approval_id: str, status: ApprovalStatus, comments: Optional[str] = None):
    result = await db.approvals.update_one(
        {"id": approval_id},
        {"$set": {
            "status": status,
            "approval_date": datetime.utcnow(),
            "comments": comments
        }}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="طلب الموافقة غير موجود")
    
    return {"message": "تم معالجة طلب الموافقة"}

# Enhanced Suppliers endpoints
@api_router.post("/suppliers", response_model=Supplier)
async def create_supplier(supplier: SupplierCreate):
    supplier_dict = supplier.dict()
    
    # Auto-generate supplier code if not provided
    if not supplier_dict.get('code'):
        supplier_count = await db.suppliers.count_documents({}) + 1
        supplier_dict['code'] = f"SUP-{supplier_count:04d}"
    
    supplier_obj = Supplier(**supplier_dict)
    await db.suppliers.insert_one(supplier_obj.dict())
    return supplier_obj

@api_router.get("/suppliers", response_model=List[Supplier])
async def get_suppliers(category: Optional[str] = None):
    query = {}
    if category:
        query["category"] = category
        
    suppliers = await db.suppliers.find(query).to_list(1000)
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

@api_router.put("/suppliers/{supplier_id}/balance")
async def update_supplier_balance(supplier_id: str, amount: float):
    result = await db.suppliers.update_one(
        {"id": supplier_id},
        {"$inc": {"current_balance": amount}}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="المورد غير موجود")
    
    return {"message": "تم تحديث رصيد المورد"}

# Enhanced Items endpoints
@api_router.post("/items", response_model=Item)
async def create_item(item: ItemCreate):
    item_dict = item.dict()
    
    # Convert expiry date
    if 'expiry_date' in item_dict and item_dict['expiry_date'] and isinstance(item_dict['expiry_date'], date):
        item_dict['expiry_date'] = datetime.combine(item_dict['expiry_date'], datetime.min.time())
    
    item_obj = Item(**item_dict)
    item_data = item_obj.dict()
    
    if 'expiry_date' in item_data and isinstance(item_data['expiry_date'], date):
        item_data['expiry_date'] = datetime.combine(item_data['expiry_date'], datetime.min.time())
    
    await db.items.insert_one(item_data)
    return item_obj

@api_router.get("/items", response_model=List[Item])
async def get_items(category: Optional[str] = None, low_stock: bool = False):
    query = {}
    if category:
        query["category"] = category
    if low_stock:
        query["$expr"] = {"$lt": ["$current_stock", "$min_stock"]}
        
    items = await db.items.find(query).to_list(1000)
    return [Item(**item) for item in items]

@api_router.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: str):
    item = await db.items.find_one({"id": item_id})
    if not item:
        raise HTTPException(status_code=404, detail="الصنف غير موجود")
    return Item(**item)

@api_router.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: str, item_update: ItemCreate):
    item_dict = item_update.dict()
    
    # Convert expiry date
    if 'expiry_date' in item_dict and item_dict['expiry_date'] and isinstance(item_dict['expiry_date'], date):
        item_dict['expiry_date'] = datetime.combine(item_dict['expiry_date'], datetime.min.time())
    
    result = await db.items.update_one(
        {"id": item_id}, 
        {"$set": item_dict}
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

@api_router.put("/items/{item_id}/stock")
async def update_item_stock(item_id: str, quantity: float, operation: str = "add"):
    """Update item stock - operation can be 'add', 'subtract', or 'set'"""
    if operation == "add":
        update_query = {"$inc": {"current_stock": quantity}}
    elif operation == "subtract":
        update_query = {"$inc": {"current_stock": -quantity}}
    else:  # set
        update_query = {"$set": {"current_stock": quantity}}
    
    result = await db.items.update_one({"id": item_id}, update_query)
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="الصنف غير موجود")
    
    # Check if stock is below minimum and create alert
    item = await db.items.find_one({"id": item_id})
    if item and item.get('current_stock', 0) < item.get('min_stock', 0):
        alert_data = AlertCreate(
            title="نفاد مخزون",
            message=f"الصنف {item.get('name')} وصل إلى الحد الأدنى للمخزون",
            priority=AlertPriority.HIGH,
            type="مخزون",
            related_id=item_id
        )
        await create_alert(alert_data)
    
    return {"message": "تم تحديث المخزون بنجاح"}

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
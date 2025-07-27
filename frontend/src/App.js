import React, { useState, useEffect } from "react";
import "./App.css";
import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || "http://localhost:8000";
const API = `${BACKEND_URL}/api`;

const App = () => {
  const [currentPage, setCurrentPage] = useState('dashboard');
  const [dashboardStats, setDashboardStats] = useState(null);
  const [projects, setProjects] = useState([]);
  const [customers, setCustomers] = useState([]);
  const [suppliers, setSuppliers] = useState([]);
  const [items, setItems] = useState([]);
  const [sales, setSales] = useState([]);
  const [purchases, setPurchases] = useState([]);
  const [employees, setEmployees] = useState([]);
  const [accounts, setAccounts] = useState([]);
  const [transactions, setTransactions] = useState([]);
  const [loading, setLoading] = useState(false);
  
  // Forms states
  const [showProjectForm, setShowProjectForm] = useState(false);
  const [showCustomerForm, setShowCustomerForm] = useState(false);
  const [showSupplierForm, setShowSupplierForm] = useState(false);
  const [showItemForm, setShowItemForm] = useState(false);
  const [showSaleForm, setShowSaleForm] = useState(false);
  const [showPurchaseForm, setShowPurchaseForm] = useState(false);
  const [showEmployeeForm, setShowEmployeeForm] = useState(false);
  const [showAccountForm, setShowAccountForm] = useState(false);

  // Fetch all data
  const fetchDashboardStats = async () => {
    try {
      const response = await axios.get(`${API}/dashboard/stats`);
      setDashboardStats(response.data);
    } catch (error) {
      console.error('Error fetching dashboard stats:', error);
    }
  };

  const fetchProjects = async () => {
    try {
      const response = await axios.get(`${API}/projects`);
      setProjects(response.data);
    } catch (error) {
      console.error('Error fetching projects:', error);
    }
  };

  const fetchCustomers = async () => {
    try {
      const response = await axios.get(`${API}/customers`);
      setCustomers(response.data);
    } catch (error) {
      console.error('Error fetching customers:', error);
    }
  };

  const fetchSuppliers = async () => {
    try {
      const response = await axios.get(`${API}/suppliers`);
      setSuppliers(response.data);
    } catch (error) {
      console.error('Error fetching suppliers:', error);
    }
  };

  const fetchItems = async () => {
    try {
      const response = await axios.get(`${API}/items`);
      setItems(response.data);
    } catch (error) {
      console.error('Error fetching items:', error);
    }
  };

  const fetchSales = async () => {
    try {
      const response = await axios.get(`${API}/sales`);
      setSales(response.data);
    } catch (error) {
      console.error('Error fetching sales:', error);
    }
  };

  const fetchPurchases = async () => {
    try {
      const response = await axios.get(`${API}/purchases`);
      setPurchases(response.data);
    } catch (error) {
      console.error('Error fetching purchases:', error);
    }
  };

  const fetchEmployees = async () => {
    try {
      const response = await axios.get(`${API}/employees`);
      setEmployees(response.data);
    } catch (error) {
      console.error('Error fetching employees:', error);
    }
  };

  const fetchAccounts = async () => {
    try {
      const response = await axios.get(`${API}/accounts`);
      setAccounts(response.data);
    } catch (error) {
      console.error('Error fetching accounts:', error);
    }
  };

  const fetchTransactions = async () => {
    try {
      const response = await axios.get(`${API}/transactions`);
      setTransactions(response.data);
    } catch (error) {
      console.error('Error fetching transactions:', error);
    }
  };

  // Load initial data
  useEffect(() => {
    fetchDashboardStats();
    fetchProjects();
    fetchCustomers();
    fetchSuppliers();
    fetchItems();
    fetchSales();
    fetchPurchases();
    fetchEmployees();
    fetchAccounts();
    fetchTransactions();
  }, []);

  // Navigation component
  const Navigation = () => (
    <nav className="bg-gradient-to-r from-blue-900 to-blue-700 text-white p-4 shadow-lg">
      <div className="container mx-auto">
        <div className="flex items-center justify-between">
          <h1 className="text-2xl font-bold">نظام ERP المتكامل</h1>
          <div className="flex space-x-4 space-x-reverse flex-wrap">
            <button
              onClick={() => setCurrentPage('dashboard')}
              className={`px-4 py-2 rounded-lg transition-colors ${
                currentPage === 'dashboard' ? 'bg-blue-600' : 'hover:bg-blue-700'
              }`}
            >
              لوحة التحكم
            </button>
            <button
              onClick={() => setCurrentPage('projects')}
              className={`px-4 py-2 rounded-lg transition-colors ${
                currentPage === 'projects' ? 'bg-blue-600' : 'hover:bg-blue-700'
              }`}
            >
              المشاريع
            </button>
            <button
              onClick={() => setCurrentPage('customers')}
              className={`px-4 py-2 rounded-lg transition-colors ${
                currentPage === 'customers' ? 'bg-blue-600' : 'hover:bg-blue-700'
              }`}
            >
              العملاء
            </button>
            <button
              onClick={() => setCurrentPage('suppliers')}
              className={`px-4 py-2 rounded-lg transition-colors ${
                currentPage === 'suppliers' ? 'bg-blue-600' : 'hover:bg-blue-700'
              }`}
            >
              الموردين
            </button>
            <button
              onClick={() => setCurrentPage('inventory')}
              className={`px-4 py-2 rounded-lg transition-colors ${
                currentPage === 'inventory' ? 'bg-blue-600' : 'hover:bg-blue-700'
              }`}
            >
              المخزون
            </button>
            <button
              onClick={() => setCurrentPage('sales')}
              className={`px-4 py-2 rounded-lg transition-colors ${
                currentPage === 'sales' ? 'bg-blue-600' : 'hover:bg-blue-700'
              }`}
            >
              المبيعات
            </button>
            <button
              onClick={() => setCurrentPage('purchases')}
              className={`px-4 py-2 rounded-lg transition-colors ${
                currentPage === 'purchases' ? 'bg-blue-600' : 'hover:bg-blue-700'
              }`}
            >
              المشتريات
            </button>
            <button
              onClick={() => setCurrentPage('finance')}
              className={`px-4 py-2 rounded-lg transition-colors ${
                currentPage === 'finance' ? 'bg-blue-600' : 'hover:bg-blue-700'
              }`}
            >
              المالية
            </button>
            <button
              onClick={() => setCurrentPage('hr')}
              className={`px-4 py-2 rounded-lg transition-colors ${
                currentPage === 'hr' ? 'bg-blue-600' : 'hover:bg-blue-700'
              }`}
            >
              الموارد البشرية
            </button>
          </div>
        </div>
      </div>
    </nav>
  );

  // Dashboard component
  const Dashboard = () => (
    <div className="container mx-auto p-6">
      <h2 className="text-3xl font-bold mb-6 text-gray-800">لوحة التحكم</h2>
      
      {dashboardStats ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div className="bg-white p-6 rounded-lg shadow-md border-r-4 border-blue-500">
            <h3 className="text-lg font-semibold text-gray-700">إجمالي المشاريع</h3>
            <p className="text-3xl font-bold text-blue-600">{dashboardStats.total_projects}</p>
            <p className="text-sm text-gray-500">مشروع نشط: {dashboardStats.active_projects}</p>
          </div>
          
          <div className="bg-white p-6 rounded-lg shadow-md border-r-4 border-green-500">
            <h3 className="text-lg font-semibold text-gray-700">إجمالي الميزانية</h3>
            <p className="text-3xl font-bold text-green-600">{dashboardStats.total_budget.toLocaleString()} ريال</p>
            <p className="text-sm text-gray-500">التكلفة الفعلية: {dashboardStats.total_actual_cost.toLocaleString()} ريال</p>
          </div>
          
          <div className="bg-white p-6 rounded-lg shadow-md border-r-4 border-purple-500">
            <h3 className="text-lg font-semibold text-gray-700">إجمالي المبيعات</h3>
            <p className="text-3xl font-bold text-purple-600">{dashboardStats.total_sales.toLocaleString()} ريال</p>
            <p className="text-sm text-gray-500">إجمالي المشتريات: {dashboardStats.total_purchases.toLocaleString()} ريال</p>
          </div>
          
          <div className="bg-white p-6 rounded-lg shadow-md border-r-4 border-orange-500">
            <h3 className="text-lg font-semibold text-gray-700">العملاء والموردين</h3>
            <p className="text-3xl font-bold text-orange-600">{dashboardStats.total_customers}</p>
            <p className="text-sm text-gray-500">العملاء: {dashboardStats.total_customers} | الموردين: {dashboardStats.total_suppliers}</p>
          </div>
        </div>
      ) : (
        <div className="text-center py-8">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto"></div>
          <p className="mt-4 text-gray-600">جاري تحميل البيانات...</p>
        </div>
      )}

      {/* Quick Actions */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-xl font-semibold mb-4 text-gray-800">إجراءات سريعة</h3>
          <div className="space-y-3">
            <button
              onClick={() => setShowProjectForm(true)}
              className="w-full bg-blue-500 text-white py-2 px-4 rounded-lg hover:bg-blue-600 transition-colors"
            >
              إضافة مشروع جديد
            </button>
            <button
              onClick={() => setShowCustomerForm(true)}
              className="w-full bg-green-500 text-white py-2 px-4 rounded-lg hover:bg-green-600 transition-colors"
            >
              إضافة عميل جديد
            </button>
            <button
              onClick={() => setShowSaleForm(true)}
              className="w-full bg-purple-500 text-white py-2 px-4 rounded-lg hover:bg-purple-600 transition-colors"
            >
              إنشاء فاتورة مبيعات
            </button>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-xl font-semibold mb-4 text-gray-800">الأصناف منخفضة المخزون</h3>
          {dashboardStats?.low_stock_items?.length > 0 ? (
            <div className="space-y-2">
              {dashboardStats.low_stock_items.slice(0, 5).map((item, index) => (
                <div key={index} className="flex justify-between items-center p-2 bg-red-50 rounded">
                  <span className="text-sm font-medium">{item.name}</span>
                  <span className="text-xs text-red-600">{item.current_stock} / {item.min_stock}</span>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-gray-500 text-sm">لا توجد أصناف منخفضة المخزون</p>
          )}
        </div>

        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-xl font-semibold mb-4 text-gray-800">أفضل العملاء</h3>
          {dashboardStats?.top_customers?.length > 0 ? (
            <div className="space-y-2">
              {dashboardStats.top_customers.slice(0, 5).map((customer, index) => (
                <div key={index} className="flex justify-between items-center p-2 bg-blue-50 rounded">
                  <span className="text-sm font-medium">{customer.name}</span>
                  <span className="text-xs text-blue-600">{customer.balance.toLocaleString()} ريال</span>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-gray-500 text-sm">لا توجد بيانات للعملاء</p>
          )}
        </div>
      </div>
    </div>
  );

  // Projects component
  const Projects = () => (
    <div className="container mx-auto p-6">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-3xl font-bold text-gray-800">إدارة المشاريع</h2>
        <button
          onClick={() => setShowProjectForm(true)}
          className="bg-blue-500 text-white px-6 py-2 rounded-lg hover:bg-blue-600 transition-colors"
        >
          إضافة مشروع جديد
        </button>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {projects.map((project) => (
          <div key={project.id} className="bg-white p-6 rounded-lg shadow-md border">
            <div className="flex justify-between items-start mb-4">
              <h3 className="text-xl font-semibold text-gray-800">{project.name}</h3>
              <span className={`px-2 py-1 rounded-full text-xs ${
                project.status === 'نشط' ? 'bg-green-100 text-green-800' :
                project.status === 'مكتمل' ? 'bg-blue-100 text-blue-800' :
                'bg-red-100 text-red-800'
              }`}>
                {project.status}
              </span>
            </div>
            <p className="text-gray-600 mb-4">{project.description}</p>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span className="text-gray-500">الميزانية:</span>
                <span className="font-medium">{project.budget.toLocaleString()} ريال</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-500">التكلفة الفعلية:</span>
                <span className="font-medium">{project.actual_cost.toLocaleString()} ريال</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-500">التقدم:</span>
                <span className="font-medium">{project.progress}%</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  // Customers component
  const Customers = () => (
    <div className="container mx-auto p-6">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-3xl font-bold text-gray-800">إدارة العملاء</h2>
        <button
          onClick={() => setShowCustomerForm(true)}
          className="bg-green-500 text-white px-6 py-2 rounded-lg hover:bg-green-600 transition-colors"
        >
          إضافة عميل جديد
        </button>
      </div>
      
      <div className="bg-white rounded-lg shadow-md overflow-hidden">
        <table className="w-full">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">الاسم</th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">جهة الاتصال</th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">الهاتف</th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">الرصيد الحالي</th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">الفئة</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {customers.map((customer) => (
              <tr key={customer.id}>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{customer.name}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{customer.contact_person}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{customer.phone}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{customer.current_balance.toLocaleString()} ريال</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{customer.category}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );

  // Suppliers component
  const Suppliers = () => (
    <div className="container mx-auto p-6">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-3xl font-bold text-gray-800">إدارة الموردين</h2>
        <button
          onClick={() => setShowSupplierForm(true)}
          className="bg-orange-500 text-white px-6 py-2 rounded-lg hover:bg-orange-600 transition-colors"
        >
          إضافة مورد جديد
        </button>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {suppliers.map((supplier) => (
          <div key={supplier.id} className="bg-white p-6 rounded-lg shadow-md border">
            <h3 className="text-xl font-semibold text-gray-800 mb-2">{supplier.name}</h3>
            <p className="text-gray-600 mb-4">{supplier.category}</p>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span className="text-gray-500">جهة الاتصال:</span>
                <span className="font-medium">{supplier.contact_person}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-500">الهاتف:</span>
                <span className="font-medium">{supplier.phone}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-500">الرصيد:</span>
                <span className="font-medium">{supplier.current_balance.toLocaleString()} ريال</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  // Inventory component
  const Inventory = () => (
    <div className="container mx-auto p-6">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-3xl font-bold text-gray-800">إدارة المخزون</h2>
        <button
          onClick={() => setShowItemForm(true)}
          className="bg-purple-500 text-white px-6 py-2 rounded-lg hover:bg-purple-600 transition-colors"
        >
          إضافة صنف جديد
        </button>
      </div>
      
      <div className="bg-white rounded-lg shadow-md overflow-hidden">
        <table className="w-full">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">الصنف</th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">الرمز</th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">المخزون الحالي</th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">الحد الأدنى</th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">سعر البيع</th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">الحالة</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {items.map((item) => (
              <tr key={item.id}>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{item.name}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{item.code}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{item.current_stock} {item.unit}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{item.min_stock} {item.unit}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{item.selling_price.toLocaleString()} ريال</td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className={`px-2 py-1 rounded-full text-xs ${
                    item.current_stock <= item.min_stock ? 'bg-red-100 text-red-800' : 'bg-green-100 text-green-800'
                  }`}>
                    {item.current_stock <= item.min_stock ? 'منخفض' : 'متوفر'}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );

  // Sales component
  const Sales = () => (
    <div className="container mx-auto p-6">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-3xl font-bold text-gray-800">إدارة المبيعات</h2>
        <button
          onClick={() => setShowSaleForm(true)}
          className="bg-purple-500 text-white px-6 py-2 rounded-lg hover:bg-purple-600 transition-colors"
        >
          إنشاء فاتورة جديدة
        </button>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {sales.map((sale) => (
          <div key={sale.id} className="bg-white p-6 rounded-lg shadow-md border">
            <div className="flex justify-between items-start mb-4">
              <h3 className="text-lg font-semibold text-gray-800">فاتورة #{sale.invoice_number}</h3>
              <span className={`px-2 py-1 rounded-full text-xs ${
                sale.status === 'مدفوع' ? 'bg-green-100 text-green-800' :
                sale.status === 'معلق' ? 'bg-yellow-100 text-yellow-800' :
                'bg-red-100 text-red-800'
              }`}>
                {sale.status}
              </span>
            </div>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span className="text-gray-500">التاريخ:</span>
                <span className="font-medium">{new Date(sale.date).toLocaleDateString('ar-SA')}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-500">المبلغ الإجمالي:</span>
                <span className="font-medium">{sale.total_amount.toLocaleString()} ريال</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-500">المدفوع:</span>
                <span className="font-medium">{sale.paid_amount.toLocaleString()} ريال</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  // Purchases component
  const Purchases = () => (
    <div className="container mx-auto p-6">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-3xl font-bold text-gray-800">إدارة المشتريات</h2>
        <button
          onClick={() => setShowPurchaseForm(true)}
          className="bg-orange-500 text-white px-6 py-2 rounded-lg hover:bg-orange-600 transition-colors"
        >
          إنشاء أمر شراء جديد
        </button>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {purchases.map((purchase) => (
          <div key={purchase.id} className="bg-white p-6 rounded-lg shadow-md border">
            <div className="flex justify-between items-start mb-4">
              <h3 className="text-lg font-semibold text-gray-800">أمر شراء #{purchase.invoice_number}</h3>
              <span className={`px-2 py-1 rounded-full text-xs ${
                purchase.status === 'مدفوع' ? 'bg-green-100 text-green-800' :
                purchase.status === 'معلق' ? 'bg-yellow-100 text-yellow-800' :
                'bg-red-100 text-red-800'
              }`}>
                {purchase.status}
              </span>
            </div>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span className="text-gray-500">التاريخ:</span>
                <span className="font-medium">{new Date(purchase.date).toLocaleDateString('ar-SA')}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-500">المبلغ الإجمالي:</span>
                <span className="font-medium">{purchase.total_amount.toLocaleString()} ريال</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-500">المدفوع:</span>
                <span className="font-medium">{purchase.paid_amount.toLocaleString()} ريال</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  // Finance component
  const Finance = () => (
    <div className="container mx-auto p-6">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-3xl font-bold text-gray-800">إدارة المالية</h2>
        <button
          onClick={() => setShowAccountForm(true)}
          className="bg-green-500 text-white px-6 py-2 rounded-lg hover:bg-green-600 transition-colors"
        >
          إضافة حساب جديد
        </button>
      </div>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-xl font-semibold mb-4 text-gray-800">الحسابات</h3>
          <div className="space-y-3">
            {accounts.map((account) => (
              <div key={account.id} className="flex justify-between items-center p-3 bg-gray-50 rounded">
                <div>
                  <p className="font-medium">{account.name}</p>
                  <p className="text-sm text-gray-500">{account.account_number}</p>
                </div>
                <span className="font-semibold">{account.balance.toLocaleString()} ريال</span>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-xl font-semibold mb-4 text-gray-800">آخر المعاملات</h3>
          <div className="space-y-3">
            {transactions.slice(0, 10).map((transaction) => (
              <div key={transaction.id} className="p-3 bg-gray-50 rounded">
                <div className="flex justify-between items-start">
                  <div>
                    <p className="font-medium">{transaction.description}</p>
                    <p className="text-sm text-gray-500">{new Date(transaction.date).toLocaleDateString('ar-SA')}</p>
                  </div>
                  <span className="font-semibold">{transaction.amount.toLocaleString()} ريال</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );

  // HR component
  const HR = () => (
    <div className="container mx-auto p-6">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-3xl font-bold text-gray-800">إدارة الموارد البشرية</h2>
        <button
          onClick={() => setShowEmployeeForm(true)}
          className="bg-blue-500 text-white px-6 py-2 rounded-lg hover:bg-blue-600 transition-colors"
        >
          إضافة موظف جديد
        </button>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {employees.map((employee) => (
          <div key={employee.id} className="bg-white p-6 rounded-lg shadow-md border">
            <h3 className="text-xl font-semibold text-gray-800 mb-2">{employee.full_name}</h3>
            <p className="text-gray-600 mb-4">{employee.position} - {employee.department}</p>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span className="text-gray-500">الرقم الوظيفي:</span>
                <span className="font-medium">{employee.employee_number}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-500">الراتب:</span>
                <span className="font-medium">{employee.salary.toLocaleString()} ريال</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-500">تاريخ التعيين:</span>
                <span className="font-medium">{new Date(employee.hire_date).toLocaleDateString('ar-SA')}</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  // Render current page
  const renderCurrentPage = () => {
    switch (currentPage) {
      case 'dashboard':
        return <Dashboard />;
      case 'projects':
        return <Projects />;
      case 'customers':
        return <Customers />;
      case 'suppliers':
        return <Suppliers />;
      case 'inventory':
        return <Inventory />;
      case 'sales':
        return <Sales />;
      case 'purchases':
        return <Purchases />;
      case 'finance':
        return <Finance />;
      case 'hr':
        return <HR />;
      default:
        return <Dashboard />;
    }
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <Navigation />
      {renderCurrentPage()}
      
      {/* Forms would be implemented here as modals */}
      {/* For brevity, I'm not including all the form components */}
    </div>
  );
};

export default App;
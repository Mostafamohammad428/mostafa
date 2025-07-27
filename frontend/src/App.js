import React, { useState, useEffect, createContext, useContext } from "react";
import "./App.css";
import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || "http://localhost:8000";
const API = `${BACKEND_URL}/api`;

// Authentication Context
const AuthContext = createContext();

const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      // Verify token validity here if needed
    }
    setLoading(false);
  }, [token]);

  const login = async (username, password) => {
    try {
      const response = await axios.post(`${API}/auth/login`, {
        username,
        password
      });
      const { access_token, user: userData } = response.data;
      setToken(access_token);
      setUser(userData);
      localStorage.setItem('token', access_token);
      axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
      return { success: true };
    } catch (error) {
      return { success: false, error: error.response?.data?.detail || 'خطأ في تسجيل الدخول' };
    }
  };

  const logout = () => {
    setToken(null);
    setUser(null);
    localStorage.removeItem('token');
    delete axios.defaults.headers.common['Authorization'];
  };

  const register = async (userData) => {
    try {
      await axios.post(`${API}/auth/register`, userData);
      return { success: true };
    } catch (error) {
      return { success: false, error: error.response?.data?.detail || 'خطأ في التسجيل' };
    }
  };

  return (
    <AuthContext.Provider value={{ user, token, login, logout, register, loading }}>
      {children}
    </AuthContext.Provider>
  );
};

// Login Component
const LoginForm = () => {
  const [formData, setFormData] = useState({ username: '', password: '' });
  const [isLogin, setIsLogin] = useState(true);
  const [registerData, setRegisterData] = useState({
    username: '',
    email: '',
    password: '',
    full_name: '',
    role: 'user'
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { login, register } = useAuth();

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    
    const result = await login(formData.username, formData.password);
    if (!result.success) {
      setError(result.error);
    }
    setLoading(false);
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    
    const result = await register(registerData);
    if (result.success) {
      setIsLogin(true);
      setError('');
      alert('تم التسجيل بنجاح! يمكنك الآن تسجيل الدخول');
    } else {
      setError(result.error);
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-900 via-purple-900 to-indigo-900 flex items-center justify-center p-4" dir="rtl">
      <div className="bg-white rounded-2xl shadow-2xl p-8 w-full max-w-md">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-800 mb-2">نظام ERP المتكامل</h1>
          <p className="text-gray-600">نظام محاسبي شامل لجميع القطاعات</p>
        </div>

        <div className="flex mb-6">
          <button
            onClick={() => setIsLogin(true)}
            className={`flex-1 py-2 px-4 rounded-l-lg transition-colors ${
              isLogin ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-700'
            }`}
          >
            تسجيل الدخول
          </button>
          <button
            onClick={() => setIsLogin(false)}
            className={`flex-1 py-2 px-4 rounded-r-lg transition-colors ${
              !isLogin ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-700'
            }`}
          >
            تسجيل جديد
          </button>
        </div>

        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
            {error}
          </div>
        )}

        {isLogin ? (
          <form onSubmit={handleLogin}>
            <div className="space-y-4">
              <input
                type="text"
                placeholder="اسم المستخدم"
                value={formData.username}
                onChange={(e) => setFormData({...formData, username: e.target.value})}
                className="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
              />
              <input
                type="password"
                placeholder="كلمة المرور"
                value={formData.password}
                onChange={(e) => setFormData({...formData, password: e.target.value})}
                className="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
              />
            </div>
            <button
              type="submit"
              disabled={loading}
              className="w-full bg-blue-600 hover:bg-blue-700 text-white py-3 rounded-lg mt-6 transition-colors disabled:opacity-50"
            >
              {loading ? 'جاري تسجيل الدخول...' : 'تسجيل الدخول'}
            </button>
          </form>
        ) : (
          <form onSubmit={handleRegister}>
            <div className="space-y-4">
              <input
                type="text"
                placeholder="اسم المستخدم"
                value={registerData.username}
                onChange={(e) => setRegisterData({...registerData, username: e.target.value})}
                className="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
              />
              <input
                type="email"
                placeholder="البريد الإلكتروني"
                value={registerData.email}
                onChange={(e) => setRegisterData({...registerData, email: e.target.value})}
                className="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
              />
              <input
                type="text"
                placeholder="الاسم الكامل"
                value={registerData.full_name}
                onChange={(e) => setRegisterData({...registerData, full_name: e.target.value})}
                className="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
              />
              <input
                type="password"
                placeholder="كلمة المرور"
                value={registerData.password}
                onChange={(e) => setRegisterData({...registerData, password: e.target.value})}
                className="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
              />
              <select
                value={registerData.role}
                onChange={(e) => setRegisterData({...registerData, role: e.target.value})}
                className="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="user">مستخدم</option>
                <option value="accountant">محاسب</option>
                <option value="sales">مبيعات</option>
                <option value="purchase">مشتريات</option>
                <option value="hr">موارد بشرية</option>
                <option value="inventory">مخزون</option>
                <option value="manager">مدير</option>
              </select>
            </div>
            <button
              type="submit"
              disabled={loading}
              className="w-full bg-green-600 hover:bg-green-700 text-white py-3 rounded-lg mt-6 transition-colors disabled:opacity-50"
            >
              {loading ? 'جاري التسجيل...' : 'إنشاء حساب جديد'}
            </button>
          </form>
        )}
      </div>
    </div>
  );
};

// Main ERP Application
const ERPApp = () => {
  const [currentPage, setCurrentPage] = useState('dashboard');
  const [dashboardStats, setDashboardStats] = useState(null);
  const [comprehensiveStats, setComprehensiveStats] = useState(null);
  const [loading, setLoading] = useState(false);
  const { user, logout } = useAuth();

  // Data states
  const [accounts, setAccounts] = useState([]);
  const [transactions, setTransactions] = useState([]);
  const [customers, setCustomers] = useState([]);
  const [salesOrders, setSalesOrders] = useState([]);
  const [employees, setEmployees] = useState([]);
  const [products, setProducts] = useState([]);
  const [purchaseOrders, setPurchaseOrders] = useState([]);
  const [projects, setProjects] = useState([]);
  const [suppliers, setSuppliers] = useState([]);

  // Form states
  const [showForms, setShowForms] = useState({});

  // Fetch functions
  const fetchDashboardStats = async () => {
    try {
      const [basicStats, comprehensiveStats] = await Promise.all([
        axios.get(`${API}/dashboard/stats`),
        axios.get(`${API}/dashboard/comprehensive-stats`)
      ]);
      setDashboardStats(basicStats.data);
      setComprehensiveStats(comprehensiveStats.data);
    } catch (error) {
      console.error('Error fetching dashboard stats:', error);
    }
  };

  const fetchAllData = async () => {
    try {
      setLoading(true);
      const [
        accountsRes, transactionsRes, customersRes, salesOrdersRes,
        employeesRes, productsRes, purchaseOrdersRes, projectsRes, suppliersRes
      ] = await Promise.all([
        axios.get(`${API}/accounts`).catch(() => ({data: []})),
        axios.get(`${API}/transactions`).catch(() => ({data: []})),
        axios.get(`${API}/customers`).catch(() => ({data: []})),
        axios.get(`${API}/sales-orders`).catch(() => ({data: []})),
        axios.get(`${API}/employees`).catch(() => ({data: []})),
        axios.get(`${API}/products`).catch(() => ({data: []})),
        axios.get(`${API}/purchase-orders`).catch(() => ({data: []})),
        axios.get(`${API}/projects`).catch(() => ({data: []})),
        axios.get(`${API}/suppliers`).catch(() => ({data: []}))
      ]);

      setAccounts(accountsRes.data);
      setTransactions(transactionsRes.data);
      setCustomers(customersRes.data);
      setSalesOrders(salesOrdersRes.data);
      setEmployees(employeesRes.data);
      setProducts(productsRes.data);
      setPurchaseOrders(purchaseOrdersRes.data);
      setProjects(projectsRes.data);
      setSuppliers(suppliersRes.data);
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboardStats();
    fetchAllData();
  }, []);

  // Navigation Component
  const Navigation = () => (
    <nav className="bg-gradient-to-r from-blue-800 to-purple-800 text-white shadow-lg">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center space-x-4 space-x-reverse">
            <h1 className="text-xl font-bold">نظام ERP المتكامل</h1>
            <span className="text-blue-200">مرحباً، {user?.full_name}</span>
          </div>
          
          <div className="flex items-center space-x-2 space-x-reverse">
            <button
              onClick={logout}
              className="bg-red-600 hover:bg-red-700 px-4 py-2 rounded-lg transition-colors"
            >
              تسجيل الخروج
            </button>
            <span className="text-blue-200 text-sm">{user?.role}</span>
          </div>
        </div>
        
        <div className="flex space-x-1 space-x-reverse pb-4 overflow-x-auto">
          {[
            { key: 'dashboard', label: 'لوحة التحكم', icon: '📊' },
            { key: 'accounting', label: 'المحاسبة', icon: '💰' },
            { key: 'sales', label: 'المبيعات', icon: '🛒' },
            { key: 'purchase', label: 'المشتريات', icon: '📦' },
            { key: 'inventory', label: 'المخزون', icon: '📋' },
            { key: 'hr', label: 'الموارد البشرية', icon: '👥' },
            { key: 'projects', label: 'المشاريع', icon: '🏗️' },
            { key: 'customers', label: 'العملاء', icon: '👤' },
            { key: 'suppliers', label: 'الموردين', icon: '🏪' },
            { key: 'reports', label: 'التقارير', icon: '📈' }
          ].map(item => (
            <button
              key={item.key}
              onClick={() => setCurrentPage(item.key)}
              className={`flex items-center space-x-2 space-x-reverse px-4 py-2 rounded-lg transition-colors whitespace-nowrap ${
                currentPage === item.key 
                  ? 'bg-white text-blue-800 shadow-md' 
                  : 'hover:bg-blue-700'
              }`}
            >
              <span>{item.icon}</span>
              <span>{item.label}</span>
            </button>
          ))}
        </div>
      </div>
    </nav>
  );

  // Dashboard Component
  const Dashboard = () => (
    <div className="container mx-auto p-6">
      <div className="mb-8">
        <h2 className="text-3xl font-bold text-gray-800 mb-4">لوحة التحكم الرئيسية</h2>
        <div className="bg-gradient-to-r from-blue-500 to-purple-600 rounded-xl p-8 text-white mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-2xl font-semibold mb-2">نظام ERP المتكامل</h3>
              <p className="text-blue-100">إدارة شاملة لجميع عمليات الشركة</p>
            </div>
            <div className="text-6xl">🏢</div>
          </div>
        </div>
      </div>

      {comprehensiveStats && (
        <>
          {/* Financial Overview */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
            <div className="bg-white rounded-xl shadow-lg p-6 border-r-4 border-green-500">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-gray-600 text-sm">إجمالي الإيرادات</p>
                  <p className="text-3xl font-bold text-green-600">{comprehensiveStats.total_revenue?.toLocaleString()} ر.س</p>
                </div>
                <div className="text-4xl">💰</div>
              </div>
            </div>

            <div className="bg-white rounded-xl shadow-lg p-6 border-r-4 border-red-500">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-gray-600 text-sm">إجمالي المصروفات</p>
                  <p className="text-3xl font-bold text-red-600">{comprehensiveStats.total_expenses?.toLocaleString()} ر.س</p>
                </div>
                <div className="text-4xl">💸</div>
              </div>
            </div>

            <div className="bg-white rounded-xl shadow-lg p-6 border-r-4 border-blue-500">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-gray-600 text-sm">صافي الربح</p>
                  <p className={`text-3xl font-bold ${comprehensiveStats.net_profit >= 0 ? 'text-blue-600' : 'text-red-600'}`}>
                    {comprehensiveStats.net_profit?.toLocaleString()} ر.س
                  </p>
                </div>
                <div className="text-4xl">📊</div>
              </div>
            </div>

            <div className="bg-white rounded-xl shadow-lg p-6 border-r-4 border-purple-500">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-gray-600 text-sm">قيمة المخزون</p>
                  <p className="text-3xl font-bold text-purple-600">{comprehensiveStats.inventory_value?.toLocaleString()} ر.س</p>
                </div>
                <div className="text-4xl">📦</div>
              </div>
            </div>
          </div>

          {/* Business Metrics */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <div className="bg-white rounded-xl shadow-lg p-6">
              <h4 className="text-lg font-semibold text-gray-800 mb-4">المبيعات</h4>
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-gray-600">إجمالي الطلبات</span>
                  <span className="font-semibold">{comprehensiveStats.total_sales_orders}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">الطلبات المعلقة</span>
                  <span className="font-semibold text-yellow-600">{comprehensiveStats.pending_orders}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">العملاء</span>
                  <span className="font-semibold">{comprehensiveStats.total_customers}</span>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-xl shadow-lg p-6">
              <h4 className="text-lg font-semibold text-gray-800 mb-4">المخزون</h4>
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-gray-600">إجمالي المنتجات</span>
                  <span className="font-semibold">{comprehensiveStats.total_products}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">مخزون منخفض</span>
                  <span className="font-semibold text-orange-600">{comprehensiveStats.low_stock_items}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">نفد المخزون</span>
                  <span className="font-semibold text-red-600">{comprehensiveStats.out_of_stock_items}</span>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-xl shadow-lg p-6">
              <h4 className="text-lg font-semibold text-gray-800 mb-4">الموارد البشرية</h4>
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-gray-600">إجمالي الموظفين</span>
                  <span className="font-semibold">{comprehensiveStats.total_employees}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">الموظفين النشطين</span>
                  <span className="font-semibold text-green-600">{comprehensiveStats.active_employees}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">الأقسام</span>
                  <span className="font-semibold">{comprehensiveStats.departments_count}</span>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-xl shadow-lg p-6">
              <h4 className="text-lg font-semibold text-gray-800 mb-4">المشاريع</h4>
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-gray-600">إجمالي المشاريع</span>
                  <span className="font-semibold">{comprehensiveStats.total_projects}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">المشاريع النشطة</span>
                  <span className="font-semibold text-green-600">{comprehensiveStats.active_projects}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">الموردين</span>
                  <span className="font-semibold">{comprehensiveStats.total_suppliers}</span>
                </div>
              </div>
            </div>
          </div>
        </>
      )}

      {/* Recent Activities */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h3 className="text-xl font-bold text-gray-800 mb-4">آخر المعاملات</h3>
          <div className="space-y-3">
            {comprehensiveStats?.recent_transactions?.slice(0, 5).map((transaction, index) => (
              <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div>
                  <p className="font-semibold text-gray-800">{transaction.description}</p>
                  <p className="text-sm text-gray-600">{transaction.reference}</p>
                </div>
                <div className="text-left">
                  <p className={`font-semibold ${transaction.type === 'income' ? 'text-green-600' : 'text-red-600'}`}>
                    {transaction.amount?.toLocaleString()} ر.س
                  </p>
                  <p className="text-sm text-gray-500">{transaction.type === 'income' ? 'إيراد' : 'مصروف'}</p>
                </div>
              </div>
            )) || (
              <p className="text-gray-500 text-center py-4">لا توجد معاملات حديثة</p>
            )}
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-lg p-6">
          <h3 className="text-xl font-bold text-gray-800 mb-4">آخر الطلبات</h3>
          <div className="space-y-3">
            {comprehensiveStats?.recent_orders?.slice(0, 5).map((order, index) => (
              <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div>
                  <p className="font-semibold text-gray-800">{order.order_number}</p>
                  <p className="text-sm text-gray-600">{order.status}</p>
                </div>
                <div className="text-left">
                  <p className="font-semibold text-blue-600">{order.total_amount?.toLocaleString()} ر.س</p>
                  <p className="text-sm text-gray-500">طلب مبيعات</p>
                </div>
              </div>
            )) || (
              <p className="text-gray-500 text-center py-4">لا توجد طلبات حديثة</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );

  // Generic List Component
  const GenericList = ({ title, data, columns, onAdd, addButtonText }) => (
    <div className="container mx-auto p-6">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-3xl font-bold text-gray-800">{title}</h2>
        {onAdd && (
          <button
            onClick={onAdd}
            className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg transition-colors"
          >
            {addButtonText}
          </button>
        )}
      </div>

      <div className="bg-white rounded-xl shadow-lg overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50">
              <tr>
                {columns.map((column, index) => (
                  <th key={index} className="px-6 py-4 text-right text-sm font-semibold text-gray-700">
                    {column.header}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {data.length > 0 ? data.map((item, index) => (
                <tr key={index} className="hover:bg-gray-50">
                  {columns.map((column, colIndex) => (
                    <td key={colIndex} className="px-6 py-4 text-sm text-gray-900">
                      {column.render ? column.render(item) : item[column.key]}
                    </td>
                  ))}
                </tr>
              )) : (
                <tr>
                  <td colSpan={columns.length} className="px-6 py-8 text-center text-gray-500">
                    لا توجد بيانات متاحة
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );

  // Page Components
  const AccountingPage = () => (
    <GenericList
      title="نظام المحاسبة"
      data={accounts}
      columns={[
        { key: 'code', header: 'رمز الحساب' },
        { key: 'name', header: 'اسم الحساب' },
        { key: 'type', header: 'نوع الحساب' },
        { key: 'balance', header: 'الرصيد', render: (item) => `${item.balance?.toLocaleString()} ر.س` }
      ]}
      onAdd={() => setShowForms({...showForms, account: true})}
      addButtonText="إضافة حساب جديد"
    />
  );

  const SalesPage = () => (
    <GenericList
      title="إدارة المبيعات"
      data={salesOrders}
      columns={[
        { key: 'order_number', header: 'رقم الطلب' },
        { key: 'customer_id', header: 'العميل' },
        { key: 'date', header: 'التاريخ', render: (item) => new Date(item.date).toLocaleDateString('ar-SA') },
        { key: 'status', header: 'الحالة' },
        { key: 'total_amount', header: 'المبلغ الإجمالي', render: (item) => `${item.total_amount?.toLocaleString()} ر.س` }
      ]}
      onAdd={() => setShowForms({...showForms, salesOrder: true})}
      addButtonText="طلب مبيعات جديد"
    />
  );

  const PurchasePage = () => (
    <GenericList
      title="إدارة المشتريات"
      data={purchaseOrders}
      columns={[
        { key: 'order_number', header: 'رقم الطلب' },
        { key: 'supplier_id', header: 'المورد' },
        { key: 'date', header: 'التاريخ', render: (item) => new Date(item.date).toLocaleDateString('ar-SA') },
        { key: 'status', header: 'الحالة' },
        { key: 'total_amount', header: 'المبلغ الإجمالي', render: (item) => `${item.total_amount?.toLocaleString()} ر.س` }
      ]}
      onAdd={() => setShowForms({...showForms, purchaseOrder: true})}
      addButtonText="طلب شراء جديد"
    />
  );

  const InventoryPage = () => (
    <GenericList
      title="إدارة المخزون"
      data={products}
      columns={[
        { key: 'code', header: 'رمز المنتج' },
        { key: 'name', header: 'اسم المنتج' },
        { key: 'category', header: 'الفئة' },
        { key: 'current_stock', header: 'المخزون الحالي' },
        { key: 'unit', header: 'الوحدة' },
        { key: 'cost_price', header: 'سعر التكلفة', render: (item) => `${item.cost_price?.toLocaleString()} ر.س` },
        { key: 'selling_price', header: 'سعر البيع', render: (item) => `${item.selling_price?.toLocaleString()} ر.س` }
      ]}
      onAdd={() => setShowForms({...showForms, product: true})}
      addButtonText="إضافة منتج جديد"
    />
  );

  const HRPage = () => (
    <GenericList
      title="إدارة الموارد البشرية"
      data={employees}
      columns={[
        { key: 'employee_code', header: 'رقم الموظف' },
        { key: 'first_name', header: 'الاسم الأول' },
        { key: 'last_name', header: 'اسم العائلة' },
        { key: 'department', header: 'القسم' },
        { key: 'position', header: 'المنصب' },
        { key: 'salary', header: 'الراتب', render: (item) => `${item.salary?.toLocaleString()} ر.س` },
        { key: 'status', header: 'الحالة' }
      ]}
      onAdd={() => setShowForms({...showForms, employee: true})}
      addButtonText="إضافة موظف جديد"
    />
  );

  const ProjectsPage = () => (
    <GenericList
      title="إدارة المشاريع"
      data={projects}
      columns={[
        { key: 'name', header: 'اسم المشروع' },
        { key: 'client_name', header: 'العميل' },
        { key: 'start_date', header: 'تاريخ البداية', render: (item) => new Date(item.start_date).toLocaleDateString('ar-SA') },
        { key: 'budget', header: 'الميزانية', render: (item) => `${item.budget?.toLocaleString()} ر.س` },
        { key: 'actual_cost', header: 'التكلفة الفعلية', render: (item) => `${item.actual_cost?.toLocaleString()} ر.س` },
        { key: 'status', header: 'الحالة' }
      ]}
      onAdd={() => setShowForms({...showForms, project: true})}
      addButtonText="إضافة مشروع جديد"
    />
  );

  const CustomersPage = () => (
    <GenericList
      title="إدارة العملاء"
      data={customers}
      columns={[
        { key: 'code', header: 'رمز العميل' },
        { key: 'name', header: 'اسم العميل' },
        { key: 'email', header: 'البريد الإلكتروني' },
        { key: 'phone', header: 'رقم الهاتف' },
        { key: 'city', header: 'المدينة' },
        { key: 'credit_limit', header: 'حد الائتمان', render: (item) => `${item.credit_limit?.toLocaleString()} ر.س` },
        { key: 'balance', header: 'الرصيد', render: (item) => `${item.balance?.toLocaleString()} ر.س` }
      ]}
      onAdd={() => setShowForms({...showForms, customer: true})}
      addButtonText="إضافة عميل جديد"
    />
  );

  const SuppliersPage = () => (
    <GenericList
      title="إدارة الموردين"
      data={suppliers}
      columns={[
        { key: 'name', header: 'اسم المورد' },
        { key: 'contact_person', header: 'الشخص المسؤول' },
        { key: 'phone', header: 'رقم الهاتف' },
        { key: 'email', header: 'البريد الإلكتروني' },
        { key: 'category', header: 'الفئة' },
        { key: 'address', header: 'العنوان' }
      ]}
      onAdd={() => setShowForms({...showForms, supplier: true})}
      addButtonText="إضافة مورد جديد"
    />
  );

  const ReportsPage = () => (
    <div className="container mx-auto p-6">
      <h2 className="text-3xl font-bold text-gray-800 mb-6">التقارير والتحليلات</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {[
          { title: 'تقرير الأرباح والخسائر', icon: '📊', description: 'تحليل الإيرادات والمصروفات' },
          { title: 'تقرير الميزانية العمومية', icon: '⚖️', description: 'الأصول والخصوم وحقوق الملكية' },
          { title: 'تقرير التدفق النقدي', icon: '💰', description: 'حركة النقد الداخل والخارج' },
          { title: 'تقرير المبيعات', icon: '📈', description: 'تحليل أداء المبيعات' },
          { title: 'تقرير المخزون', icon: '📦', description: 'حالة المخزون والحركة' },
          { title: 'تقرير الموظفين', icon: '👥', description: 'إحصائيات الموارد البشرية' },
          { title: 'تقرير المشاريع', icon: '🏗️', description: 'تقدم المشاريع والتكاليف' },
          { title: 'تقرير العملاء', icon: '👤', description: 'تحليل قاعدة العملاء' },
          { title: 'تقرير الموردين', icon: '🏪', description: 'أداء الموردين والمشتريات' }
        ].map((report, index) => (
          <div key={index} className="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-shadow cursor-pointer">
            <div className="text-4xl mb-4">{report.icon}</div>
            <h3 className="text-lg font-semibold text-gray-800 mb-2">{report.title}</h3>
            <p className="text-gray-600 text-sm mb-4">{report.description}</p>
            <button className="w-full bg-blue-600 hover:bg-blue-700 text-white py-2 rounded-lg transition-colors">
              عرض التقرير
            </button>
          </div>
        ))}
      </div>
    </div>
  );

  const renderCurrentPage = () => {
    switch (currentPage) {
      case 'dashboard': return <Dashboard />;
      case 'accounting': return <AccountingPage />;
      case 'sales': return <SalesPage />;
      case 'purchase': return <PurchasePage />;
      case 'inventory': return <InventoryPage />;
      case 'hr': return <HRPage />;
      case 'projects': return <ProjectsPage />;
      case 'customers': return <CustomersPage />;
      case 'suppliers': return <SuppliersPage />;
      case 'reports': return <ReportsPage />;
      default: return <Dashboard />;
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">جاري تحميل البيانات...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100" dir="rtl">
      <Navigation />
      <main>
        {renderCurrentPage()}
      </main>
    </div>
  );
};

// Main App Component
const App = () => {
  const { token, loading } = useAuth();

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return token ? <ERPApp /> : <LoginForm />;
};

// App with Auth Provider
const AppWithAuth = () => (
  <AuthProvider>
    <App />
  </AuthProvider>
);

export default AppWithAuth;
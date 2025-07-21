import React, { useState, useEffect } from "react";
import "./App.css";
import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const App = () => {
  const [currentPage, setCurrentPage] = useState('dashboard');
  const [dashboardStats, setDashboardStats] = useState(null);
  const [projects, setProjects] = useState([]);
  const [costs, setCosts] = useState([]);
  const [suppliers, setSuppliers] = useState([]);
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(false);
  
  // Forms states
  const [showProjectForm, setShowProjectForm] = useState(false);
  const [showCostForm, setShowCostForm] = useState(false);
  const [showSupplierForm, setShowSupplierForm] = useState(false);
  const [showItemForm, setShowItemForm] = useState(false);

  // Fetch dashboard stats
  const fetchDashboardStats = async () => {
    try {
      const response = await axios.get(`${API}/dashboard/stats`);
      setDashboardStats(response.data);
    } catch (error) {
      console.error('Error fetching dashboard stats:', error);
    }
  };

  // Fetch projects
  const fetchProjects = async () => {
    try {
      const response = await axios.get(`${API}/projects`);
      setProjects(response.data);
    } catch (error) {
      console.error('Error fetching projects:', error);
    }
  };

  // Fetch costs
  const fetchCosts = async () => {
    try {
      const response = await axios.get(`${API}/costs`);
      setCosts(response.data);
    } catch (error) {
      console.error('Error fetching costs:', error);
    }
  };

  // Fetch suppliers
  const fetchSuppliers = async () => {
    try {
      const response = await axios.get(`${API}/suppliers`);
      setSuppliers(response.data);
    } catch (error) {
      console.error('Error fetching suppliers:', error);
    }
  };

  // Fetch items
  const fetchItems = async () => {
    try {
      const response = await axios.get(`${API}/items`);
      setItems(response.data);
    } catch (error) {
      console.error('Error fetching items:', error);
    }
  };

  // Load initial data
  useEffect(() => {
    fetchDashboardStats();
    fetchProjects();
    fetchCosts();
    fetchSuppliers();
    fetchItems();
  }, []);

  // Navigation component
  const Navigation = () => (
    <nav className="bg-blue-800 text-white p-4 shadow-lg">
      <div className="container mx-auto">
        <div className="flex items-center justify-between">
          <h1 className="text-2xl font-bold">نظام إدارة التكاليف ERP</h1>
          <div className="flex space-x-4 space-x-reverse">
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
              onClick={() => setCurrentPage('costs')}
              className={`px-4 py-2 rounded-lg transition-colors ${
                currentPage === 'costs' ? 'bg-blue-600' : 'hover:bg-blue-700'
              }`}
            >
              التكاليف
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
          </div>
        </div>
      </div>
    </nav>
  );

  // Dashboard component
  const Dashboard = () => (
    <div className="container mx-auto p-6">
      <div className="mb-8">
        <h2 className="text-3xl font-bold text-gray-800 mb-4">لوحة التحكم</h2>
        <div className="bg-gradient-to-r from-blue-500 to-purple-600 rounded-xl p-8 text-white mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-2xl font-semibold mb-2">مرحباً بك في نظام إدارة التكاليف</h3>
              <p className="text-blue-100">نظام متكامل لإدارة المشاريع والتكاليف والمخزون</p>
            </div>
            <img 
              src="https://images.unsplash.com/photo-1608222351212-18fe0ec7b13b?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2Mzl8MHwxfHNlYXJjaHwyfHxidXNpbmVzcyUyMGRhc2hib2FyZHxlbnwwfHx8fDE3NTMxMTU5NjV8MA&ixlib=rb-4.1.0&q=85" 
              alt="Dashboard Analytics" 
              className="w-32 h-32 rounded-lg object-cover shadow-lg"
            />
          </div>
        </div>
      </div>

      {dashboardStats && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-xl shadow-lg p-6 border-r-4 border-blue-500">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 text-sm">إجمالي المشاريع</p>
                <p className="text-3xl font-bold text-blue-600">{dashboardStats.total_projects}</p>
              </div>
              <div className="bg-blue-100 p-3 rounded-full">
                <svg className="w-8 h-8 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M4 4a2 2 0 00-2 2v8a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2H4zm2 6a1 1 0 011-1h6a1 1 0 110 2H7a1 1 0 01-1-1zm1 3a1 1 0 100 2h6a1 1 0 100-2H7z"/>
                </svg>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-xl shadow-lg p-6 border-r-4 border-green-500">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 text-sm">المشاريع النشطة</p>
                <p className="text-3xl font-bold text-green-600">{dashboardStats.active_projects}</p>
              </div>
              <div className="bg-green-100 p-3 rounded-full">
                <svg className="w-8 h-8 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd"/>
                </svg>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-xl shadow-lg p-6 border-r-4 border-yellow-500">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 text-sm">إجمالي الميزانية</p>
                <p className="text-3xl font-bold text-yellow-600">{dashboardStats.total_budget.toLocaleString()} ر.س</p>
              </div>
              <div className="bg-yellow-100 p-3 rounded-full">
                <svg className="w-8 h-8 text-yellow-600" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M8.433 7.418c.155-.103.346-.196.567-.267v1.698a2.305 2.305 0 01-.567-.267C8.07 8.34 8 8.114 8 8c0-.114.07-.34.433-.582zM11 12.849v-1.698c.22.071.412.164.567.267.364.243.433.468.433.582 0 .114-.07.34-.433.582a2.305 2.305 0 01-.567.267z"/>
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-13a1 1 0 10-2 0v.092a4.535 4.535 0 00-1.676.662C6.602 6.234 6 7.009 6 8c0 .99.602 1.765 1.324 2.246.48.32 1.054.545 1.676.662v1.941c-.391-.127-.68-.317-.843-.504a1 1 0 10-1.51 1.31c.562.649 1.413 1.076 2.353 1.253V15a1 1 0 102 0v-.092a4.535 4.535 0 001.676-.662C13.398 13.766 14 12.991 14 12c0-.99-.602-1.765-1.324-2.246A4.535 4.535 0 0011 9.092V7.151c.391.127.68.317.843.504a1 1 0 101.51-1.31c-.562-.649-1.413-1.076-2.353-1.253V5z" clipRule="evenodd"/>
                </svg>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-xl shadow-lg p-6 border-r-4 border-red-500">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 text-sm">التكلفة الفعلية</p>
                <p className="text-3xl font-bold text-red-600">{dashboardStats.total_actual_cost.toLocaleString()} ر.س</p>
              </div>
              <div className="bg-red-100 p-3 rounded-full">
                <svg className="w-8 h-8 text-red-600" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M4 4a2 2 0 00-2 2v4a2 2 0 002 2V6h10a2 2 0 00-2-2H4zm2 6a2 2 0 012-2h8a2 2 0 012 2v4a2 2 0 01-2 2H8a2 2 0 01-2-2v-4zm6 4a2 2 0 100-4 2 2 0 000 4z" clipRule="evenodd"/>
                </svg>
              </div>
            </div>
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h3 className="text-xl font-bold text-gray-800 mb-4">آخر المشاريع</h3>
          <div className="space-y-4">
            {projects.slice(0, 5).map((project) => (
              <div key={project.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                <div>
                  <h4 className="font-semibold text-gray-800">{project.name}</h4>
                  <p className="text-sm text-gray-600">{project.status}</p>
                </div>
                <div className="text-left">
                  <p className="font-semibold text-blue-600">{project.budget.toLocaleString()} ر.س</p>
                  <p className="text-sm text-gray-500">الميزانية</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-lg p-6">
          <h3 className="text-xl font-bold text-gray-800 mb-4">إحصائيات سريعة</h3>
          <div className="space-y-4">
            <div className="flex items-center justify-between p-4 bg-blue-50 rounded-lg">
              <span className="text-gray-700">إجمالي الموردين</span>
              <span className="font-bold text-blue-600">{dashboardStats?.total_suppliers || 0}</span>
            </div>
            <div className="flex items-center justify-between p-4 bg-green-50 rounded-lg">
              <span className="text-gray-700">إجمالي الأصناف</span>
              <span className="font-bold text-green-600">{dashboardStats?.total_items || 0}</span>
            </div>
            <div className="flex items-center justify-between p-4 bg-yellow-50 rounded-lg">
              <span className="text-gray-700">فرق الميزانية</span>
              <span className={`font-bold ${dashboardStats?.budget_variance >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                {dashboardStats?.budget_variance?.toLocaleString() || 0} ر.س
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  // Projects component
  const Projects = () => (
    <div className="container mx-auto p-6">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-3xl font-bold text-gray-800">المشاريع</h2>
        <button
          onClick={() => setShowProjectForm(true)}
          className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg transition-colors"
        >
          إضافة مشروع جديد
        </button>
      </div>

      <div className="bg-white rounded-xl shadow-lg overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-4 text-right text-sm font-semibold text-gray-700">اسم المشروع</th>
                <th className="px-6 py-4 text-right text-sm font-semibold text-gray-700">العميل</th>
                <th className="px-6 py-4 text-right text-sm font-semibold text-gray-700">تاريخ البداية</th>
                <th className="px-6 py-4 text-right text-sm font-semibold text-gray-700">الميزانية</th>
                <th className="px-6 py-4 text-right text-sm font-semibold text-gray-700">التكلفة الفعلية</th>
                <th className="px-6 py-4 text-right text-sm font-semibold text-gray-700">الحالة</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {projects.map((project) => (
                <tr key={project.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 text-sm text-gray-900">{project.name}</td>
                  <td className="px-6 py-4 text-sm text-gray-600">{project.client_name || 'غير محدد'}</td>
                  <td className="px-6 py-4 text-sm text-gray-600">{project.start_date}</td>
                  <td className="px-6 py-4 text-sm font-medium text-blue-600">{project.budget.toLocaleString()} ر.س</td>
                  <td className="px-6 py-4 text-sm font-medium text-red-600">{project.actual_cost.toLocaleString()} ر.س</td>
                  <td className="px-6 py-4">
                    <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                      project.status === 'نشط' ? 'bg-green-100 text-green-800' :
                      project.status === 'مكتمل' ? 'bg-blue-100 text-blue-800' :
                      'bg-yellow-100 text-yellow-800'
                    }`}>
                      {project.status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );

  // Simple project form (can be expanded later)
  const ProjectForm = () => {
    const [formData, setFormData] = useState({
      name: '',
      description: '',
      start_date: '',
      end_date: '',
      budget: '',
      client_name: ''
    });

    const handleSubmit = async (e) => {
      e.preventDefault();
      try {
        await axios.post(`${API}/projects`, {
          ...formData,
          budget: parseFloat(formData.budget)
        });
        setShowProjectForm(false);
        fetchProjects();
        setFormData({
          name: '',
          description: '',
          start_date: '',
          end_date: '',
          budget: '',
          client_name: ''
        });
      } catch (error) {
        console.error('Error creating project:', error);
      }
    };

    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4">
        <div className="bg-white rounded-xl p-6 w-full max-w-md">
          <h3 className="text-xl font-bold mb-4">إضافة مشروع جديد</h3>
          <form onSubmit={handleSubmit}>
            <div className="space-y-4">
              <input
                type="text"
                placeholder="اسم المشروع"
                value={formData.name}
                onChange={(e) => setFormData({...formData, name: e.target.value})}
                className="w-full p-3 border rounded-lg"
                required
              />
              <input
                type="text"
                placeholder="اسم العميل"
                value={formData.client_name}
                onChange={(e) => setFormData({...formData, client_name: e.target.value})}
                className="w-full p-3 border rounded-lg"
              />
              <input
                type="date"
                placeholder="تاريخ البداية"
                value={formData.start_date}
                onChange={(e) => setFormData({...formData, start_date: e.target.value})}
                className="w-full p-3 border rounded-lg"
                required
              />
              <input
                type="number"
                placeholder="الميزانية"
                value={formData.budget}
                onChange={(e) => setFormData({...formData, budget: e.target.value})}
                className="w-full p-3 border rounded-lg"
                required
              />
              <textarea
                placeholder="وصف المشروع"
                value={formData.description}
                onChange={(e) => setFormData({...formData, description: e.target.value})}
                className="w-full p-3 border rounded-lg h-20"
              />
            </div>
            <div className="flex space-x-4 space-x-reverse mt-6">
              <button
                type="submit"
                className="flex-1 bg-blue-600 hover:bg-blue-700 text-white py-2 rounded-lg transition-colors"
              >
                حفظ
              </button>
              <button
                type="button"
                onClick={() => setShowProjectForm(false)}
                className="flex-1 bg-gray-300 hover:bg-gray-400 text-gray-700 py-2 rounded-lg transition-colors"
              >
                إلغاء
              </button>
            </div>
          </form>
        </div>
      </div>
    );
  };

  // Basic placeholder components for other sections
  const Costs = () => (
    <div className="container mx-auto p-6">
      <h2 className="text-3xl font-bold text-gray-800 mb-6">التكاليف</h2>
      <div className="bg-white rounded-xl shadow-lg p-6">
        <p className="text-gray-600 text-center">قسم التكاليف قيد التطوير...</p>
      </div>
    </div>
  );

  const Suppliers = () => (
    <div className="container mx-auto p-6">
      <h2 className="text-3xl font-bold text-gray-800 mb-6">الموردين</h2>
      <div className="bg-white rounded-xl shadow-lg p-6">
        <p className="text-gray-600 text-center">قسم الموردين قيد التطوير...</p>
      </div>
    </div>
  );

  const Inventory = () => (
    <div className="container mx-auto p-6">
      <h2 className="text-3xl font-bold text-gray-800 mb-6">المخزون</h2>
      <div className="bg-white rounded-xl shadow-lg p-6">
        <p className="text-gray-600 text-center">قسم المخزون قيد التطوير...</p>
      </div>
    </div>
  );

  const renderCurrentPage = () => {
    switch (currentPage) {
      case 'dashboard': return <Dashboard />;
      case 'projects': return <Projects />;
      case 'costs': return <Costs />;
      case 'suppliers': return <Suppliers />;
      case 'inventory': return <Inventory />;
      default: return <Dashboard />;
    }
  };

  return (
    <div className="min-h-screen bg-gray-100" dir="rtl">
      <Navigation />
      <main>
        {renderCurrentPage()}
        {showProjectForm && <ProjectForm />}
      </main>
    </div>
  );
};

export default App;
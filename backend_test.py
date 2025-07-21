#!/usr/bin/env python3
"""
Comprehensive Backend API Testing for Arabic Cost Management ERP System
Tests all CRUD operations with Arabic data and verifies ERP functionality
"""

import requests
import json
from datetime import date, datetime
import sys
import os

# Get backend URL from frontend .env file
def get_backend_url():
    try:
        with open('/app/frontend/.env', 'r') as f:
            for line in f:
                if line.startswith('REACT_APP_BACKEND_URL='):
                    base_url = line.split('=')[1].strip()
                    return f"{base_url}/api"
        return "http://localhost:8001/api"  # fallback
    except:
        return "http://localhost:8001/api"  # fallback

BASE_URL = get_backend_url()
print(f"Testing backend at: {BASE_URL}")

class ERPTestSuite:
    def __init__(self):
        self.base_url = BASE_URL
        self.session = requests.Session()
        self.test_data = {}
        self.passed_tests = 0
        self.failed_tests = 0
        
    def log_test(self, test_name, success, message=""):
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {test_name}")
        if message:
            print(f"   {message}")
        if success:
            self.passed_tests += 1
        else:
            self.failed_tests += 1
            
    def test_projects_module(self):
        """Test Projects CRUD operations with Arabic data"""
        print("\n=== Testing Projects Module ===")
        
        # Test 1: Create project with Arabic data
        project_data = {
            "name": "مشروع إنشاء مجمع سكني",
            "description": "مشروع لبناء مجمع سكني متكامل في الرياض",
            "start_date": "2024-01-15",
            "end_date": "2024-12-31",
            "budget": 5000000.0,
            "client_name": "شركة التطوير العقاري المحدودة"
        }
        
        try:
            response = self.session.post(f"{self.base_url}/projects", json=project_data)
            if response.status_code == 200:
                project = response.json()
                self.test_data['project_id'] = project['id']
                self.log_test("Create Project with Arabic Data", True, 
                            f"Project created: {project['name']}")
                
                # Verify Arabic text is preserved
                if project['name'] == project_data['name'] and project['status'] == "نشط":
                    self.log_test("Arabic Text Preservation", True)
                else:
                    self.log_test("Arabic Text Preservation", False, "Arabic text not preserved correctly")
            else:
                self.log_test("Create Project with Arabic Data", False, 
                            f"Status: {response.status_code}, Response: {response.text}")
        except Exception as e:
            self.log_test("Create Project with Arabic Data", False, f"Exception: {str(e)}")
            
        # Test 2: Get all projects
        try:
            response = self.session.get(f"{self.base_url}/projects")
            if response.status_code == 200:
                projects = response.json()
                self.log_test("Get All Projects", True, f"Retrieved {len(projects)} projects")
            else:
                self.log_test("Get All Projects", False, f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("Get All Projects", False, f"Exception: {str(e)}")
            
        # Test 3: Get specific project
        if 'project_id' in self.test_data:
            try:
                response = self.session.get(f"{self.base_url}/projects/{self.test_data['project_id']}")
                if response.status_code == 200:
                    project = response.json()
                    self.log_test("Get Specific Project", True, f"Retrieved: {project['name']}")
                else:
                    self.log_test("Get Specific Project", False, f"Status: {response.status_code}")
            except Exception as e:
                self.log_test("Get Specific Project", False, f"Exception: {str(e)}")
                
        # Test 4: Update project
        if 'project_id' in self.test_data:
            update_data = {
                "name": "مشروع إنشاء مجمع سكني - محدث",
                "description": "مشروع محدث لبناء مجمع سكني متكامل",
                "start_date": "2024-01-15",
                "budget": 5500000.0,
                "client_name": "شركة التطوير العقاري المحدودة"
            }
            try:
                response = self.session.put(f"{self.base_url}/projects/{self.test_data['project_id']}", 
                                          json=update_data)
                if response.status_code == 200:
                    self.log_test("Update Project", True, "Project updated successfully")
                else:
                    self.log_test("Update Project", False, f"Status: {response.status_code}")
            except Exception as e:
                self.log_test("Update Project", False, f"Exception: {str(e)}")
                
    def test_costs_module(self):
        """Test Costs CRUD operations with automatic project updates"""
        print("\n=== Testing Costs Module ===")
        
        if 'project_id' not in self.test_data:
            self.log_test("Costs Module Prerequisites", False, "No project ID available for testing")
            return
            
        # Test 1: Create cost with Arabic category
        cost_data = {
            "project_id": self.test_data['project_id'],
            "category": "مواد",
            "description": "شراء الأسمنت والحديد للأساسات",
            "amount": 150000.0,
            "date": "2024-02-01",
            "invoice_number": "INV-2024-001"
        }
        
        try:
            response = self.session.post(f"{self.base_url}/costs", json=cost_data)
            if response.status_code == 200:
                cost = response.json()
                self.test_data['cost_id'] = cost['id']
                self.log_test("Create Cost with Arabic Category", True, 
                            f"Cost created: {cost['description']}")
            else:
                self.log_test("Create Cost with Arabic Category", False, 
                            f"Status: {response.status_code}, Response: {response.text}")
        except Exception as e:
            self.log_test("Create Cost with Arabic Category", False, f"Exception: {str(e)}")
            
        # Test 2: Verify automatic project cost update
        try:
            response = self.session.get(f"{self.base_url}/projects/{self.test_data['project_id']}")
            if response.status_code == 200:
                project = response.json()
                if project['actual_cost'] == 150000.0:
                    self.log_test("Automatic Project Cost Update", True, 
                                f"Project actual cost updated to {project['actual_cost']}")
                else:
                    self.log_test("Automatic Project Cost Update", False, 
                                f"Expected 150000, got {project['actual_cost']}")
            else:
                self.log_test("Automatic Project Cost Update", False, f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("Automatic Project Cost Update", False, f"Exception: {str(e)}")
            
        # Test 3: Get costs by project
        try:
            response = self.session.get(f"{self.base_url}/costs?project_id={self.test_data['project_id']}")
            if response.status_code == 200:
                costs = response.json()
                self.log_test("Get Costs by Project", True, f"Retrieved {len(costs)} costs")
            else:
                self.log_test("Get Costs by Project", False, f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("Get Costs by Project", False, f"Exception: {str(e)}")
            
        # Test 4: Create additional cost with different category
        cost_data2 = {
            "project_id": self.test_data['project_id'],
            "category": "عمالة",
            "description": "أجور العمال لشهر فبراير",
            "amount": 80000.0,
            "date": "2024-02-28"
        }
        
        try:
            response = self.session.post(f"{self.base_url}/costs", json=cost_data2)
            if response.status_code == 200:
                cost2 = response.json()
                self.test_data['cost_id_2'] = cost2['id']
                self.log_test("Create Labor Cost", True, f"Labor cost created: {cost2['amount']}")
            else:
                self.log_test("Create Labor Cost", False, f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("Create Labor Cost", False, f"Exception: {str(e)}")
            
    def test_suppliers_module(self):
        """Test Suppliers CRUD operations with Arabic contact information"""
        print("\n=== Testing Suppliers Module ===")
        
        # Test 1: Create supplier with Arabic data
        supplier_data = {
            "name": "شركة مواد البناء المتقدمة",
            "contact_person": "أحمد محمد العلي",
            "phone": "+966501234567",
            "email": "ahmed@buildingmaterials.sa",
            "address": "الرياض، حي الملز، شارع الملك فهد",
            "category": "مواد"
        }
        
        try:
            response = self.session.post(f"{self.base_url}/suppliers", json=supplier_data)
            if response.status_code == 200:
                supplier = response.json()
                self.test_data['supplier_id'] = supplier['id']
                self.log_test("Create Supplier with Arabic Data", True, 
                            f"Supplier created: {supplier['name']}")
            else:
                self.log_test("Create Supplier with Arabic Data", False, 
                            f"Status: {response.status_code}, Response: {response.text}")
        except Exception as e:
            self.log_test("Create Supplier with Arabic Data", False, f"Exception: {str(e)}")
            
        # Test 2: Get all suppliers
        try:
            response = self.session.get(f"{self.base_url}/suppliers")
            if response.status_code == 200:
                suppliers = response.json()
                self.log_test("Get All Suppliers", True, f"Retrieved {len(suppliers)} suppliers")
            else:
                self.log_test("Get All Suppliers", False, f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("Get All Suppliers", False, f"Exception: {str(e)}")
            
        # Test 3: Create service supplier
        service_supplier_data = {
            "name": "شركة الخدمات الهندسية المتميزة",
            "contact_person": "فاطمة سالم الأحمد",
            "phone": "+966507654321",
            "email": "fatima@engineering-services.sa",
            "address": "جدة، حي الروضة",
            "category": "خدمات"
        }
        
        try:
            response = self.session.post(f"{self.base_url}/suppliers", json=service_supplier_data)
            if response.status_code == 200:
                supplier = response.json()
                self.test_data['service_supplier_id'] = supplier['id']
                self.log_test("Create Service Supplier", True, f"Service supplier created")
            else:
                self.log_test("Create Service Supplier", False, f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("Create Service Supplier", False, f"Exception: {str(e)}")
            
        # Test 4: Update supplier
        if 'supplier_id' in self.test_data:
            update_data = {
                "name": "شركة مواد البناء المتقدمة - الفرع الرئيسي",
                "contact_person": "أحمد محمد العلي",
                "phone": "+966501234567",
                "email": "ahmed.main@buildingmaterials.sa",
                "address": "الرياض، حي الملز، شارع الملك فهد - المبنى الجديد",
                "category": "مواد"
            }
            try:
                response = self.session.put(f"{self.base_url}/suppliers/{self.test_data['supplier_id']}", 
                                          json=update_data)
                if response.status_code == 200:
                    self.log_test("Update Supplier", True, "Supplier updated successfully")
                else:
                    self.log_test("Update Supplier", False, f"Status: {response.status_code}")
            except Exception as e:
                self.log_test("Update Supplier", False, f"Exception: {str(e)}")
                
    def test_inventory_module(self):
        """Test Inventory items with different Arabic units"""
        print("\n=== Testing Inventory Module ===")
        
        # Test 1: Create item with Arabic unit "متر"
        item_data = {
            "name": "حديد التسليح 12 مم",
            "code": "STEEL-12MM",
            "unit": "متر",
            "min_stock": 1000.0,
            "unit_cost": 25.50,
            "category": "مواد البناء",
            "supplier_id": self.test_data.get('supplier_id')
        }
        
        try:
            response = self.session.post(f"{self.base_url}/items", json=item_data)
            if response.status_code == 200:
                item = response.json()
                self.test_data['item_id'] = item['id']
                self.log_test("Create Item with Arabic Unit (متر)", True, 
                            f"Item created: {item['name']} - {item['unit']}")
            else:
                self.log_test("Create Item with Arabic Unit (متر)", False, 
                            f"Status: {response.status_code}, Response: {response.text}")
        except Exception as e:
            self.log_test("Create Item with Arabic Unit (متر)", False, f"Exception: {str(e)}")
            
        # Test 2: Create item with unit "كيلو"
        item_data2 = {
            "name": "أسمنت بورتلاندي",
            "code": "CEMENT-PORT",
            "unit": "كيلو",
            "min_stock": 50000.0,
            "unit_cost": 0.35,
            "category": "مواد البناء",
            "supplier_id": self.test_data.get('supplier_id')
        }
        
        try:
            response = self.session.post(f"{self.base_url}/items", json=item_data2)
            if response.status_code == 200:
                item = response.json()
                self.test_data['item_id_2'] = item['id']
                self.log_test("Create Item with Arabic Unit (كيلو)", True, 
                            f"Item created: {item['name']} - {item['unit']}")
            else:
                self.log_test("Create Item with Arabic Unit (كيلو)", False, f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("Create Item with Arabic Unit (كيلو)", False, f"Exception: {str(e)}")
            
        # Test 3: Create item with unit "قطعة"
        item_data3 = {
            "name": "خلاطة خرسانة متوسطة",
            "code": "MIXER-MED",
            "unit": "قطعة",
            "min_stock": 2.0,
            "unit_cost": 15000.0,
            "category": "معدات",
            "supplier_id": self.test_data.get('service_supplier_id')
        }
        
        try:
            response = self.session.post(f"{self.base_url}/items", json=item_data3)
            if response.status_code == 200:
                item = response.json()
                self.test_data['item_id_3'] = item['id']
                self.log_test("Create Item with Arabic Unit (قطعة)", True, 
                            f"Item created: {item['name']} - {item['unit']}")
            else:
                self.log_test("Create Item with Arabic Unit (قطعة)", False, f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("Create Item with Arabic Unit (قطعة)", False, f"Exception: {str(e)}")
            
        # Test 4: Get all items
        try:
            response = self.session.get(f"{self.base_url}/items")
            if response.status_code == 200:
                items = response.json()
                self.log_test("Get All Items", True, f"Retrieved {len(items)} items")
                
                # Verify different units are present
                units = [item['unit'] for item in items]
                if 'متر' in units and 'كيلو' in units and 'قطعة' in units:
                    self.log_test("Arabic Units Verification", True, "All Arabic units found")
                else:
                    self.log_test("Arabic Units Verification", False, f"Units found: {units}")
            else:
                self.log_test("Get All Items", False, f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("Get All Items", False, f"Exception: {str(e)}")
            
        # Test 5: Update item stock
        if 'item_id' in self.test_data:
            update_data = {
                "name": "حديد التسليح 12 مم - محدث",
                "code": "STEEL-12MM",
                "unit": "متر",
                "min_stock": 1500.0,
                "unit_cost": 26.00,
                "category": "مواد البناء",
                "supplier_id": self.test_data.get('supplier_id')
            }
            try:
                response = self.session.put(f"{self.base_url}/items/{self.test_data['item_id']}", 
                                          json=update_data)
                if response.status_code == 200:
                    self.log_test("Update Item", True, "Item updated successfully")
                else:
                    self.log_test("Update Item", False, f"Status: {response.status_code}")
            except Exception as e:
                self.log_test("Update Item", False, f"Exception: {str(e)}")
                
    def test_dashboard_statistics(self):
        """Test comprehensive dashboard statistics calculation"""
        print("\n=== Testing Dashboard Statistics ===")
        
        try:
            response = self.session.get(f"{self.base_url}/dashboard/stats")
            if response.status_code == 200:
                stats = response.json()
                self.log_test("Get Dashboard Statistics", True, "Dashboard stats retrieved")
                
                # Verify expected data structure
                expected_fields = ['total_projects', 'active_projects', 'total_budget', 
                                 'total_actual_cost', 'total_suppliers', 'total_items', 
                                 'budget_variance', 'projects_by_status']
                
                missing_fields = [field for field in expected_fields if field not in stats]
                if not missing_fields:
                    self.log_test("Dashboard Stats Structure", True, "All required fields present")
                else:
                    self.log_test("Dashboard Stats Structure", False, f"Missing fields: {missing_fields}")
                    
                # Verify calculations
                if stats['total_projects'] > 0:
                    self.log_test("Projects Count Calculation", True, 
                                f"Total projects: {stats['total_projects']}")
                else:
                    self.log_test("Projects Count Calculation", False, "No projects found")
                    
                if stats['total_budget'] > 0:
                    self.log_test("Budget Calculation", True, 
                                f"Total budget: {stats['total_budget']}")
                else:
                    self.log_test("Budget Calculation", False, "No budget calculated")
                    
                if stats['total_actual_cost'] > 0:
                    self.log_test("Actual Cost Calculation", True, 
                                f"Total actual cost: {stats['total_actual_cost']}")
                else:
                    self.log_test("Actual Cost Calculation", False, "No actual cost calculated")
                    
                # Verify budget variance calculation
                expected_variance = stats['total_budget'] - stats['total_actual_cost']
                if abs(stats['budget_variance'] - expected_variance) < 0.01:
                    self.log_test("Budget Variance Calculation", True, 
                                f"Budget variance: {stats['budget_variance']}")
                else:
                    self.log_test("Budget Variance Calculation", False, 
                                f"Expected: {expected_variance}, Got: {stats['budget_variance']}")
                    
                # Verify projects by status
                if 'نشط' in stats['projects_by_status']:
                    self.log_test("Arabic Status Aggregation", True, 
                                f"Active projects: {stats['projects_by_status']['نشط']}")
                else:
                    self.log_test("Arabic Status Aggregation", False, "No active projects in status")
                    
                print(f"\n📊 Dashboard Statistics Summary:")
                print(f"   Total Projects: {stats['total_projects']}")
                print(f"   Active Projects: {stats['active_projects']}")
                print(f"   Total Budget: {stats['total_budget']:,.2f}")
                print(f"   Total Actual Cost: {stats['total_actual_cost']:,.2f}")
                print(f"   Budget Variance: {stats['budget_variance']:,.2f}")
                print(f"   Total Suppliers: {stats['total_suppliers']}")
                print(f"   Total Items: {stats['total_items']}")
                print(f"   Projects by Status: {stats['projects_by_status']}")
                
            else:
                self.log_test("Get Dashboard Statistics", False, 
                            f"Status: {response.status_code}, Response: {response.text}")
        except Exception as e:
            self.log_test("Get Dashboard Statistics", False, f"Exception: {str(e)}")
            
    def test_arabic_error_messages(self):
        """Test Arabic error messages for non-existent resources"""
        print("\n=== Testing Arabic Error Messages ===")
        
        # Test 1: Get non-existent project
        try:
            response = self.session.get(f"{self.base_url}/projects/non-existent-id")
            if response.status_code == 404:
                error_data = response.json()
                if 'المشروع غير موجود' in error_data.get('detail', ''):
                    self.log_test("Arabic Error Message - Project", True, 
                                "Correct Arabic error message returned")
                else:
                    self.log_test("Arabic Error Message - Project", False, 
                                f"Unexpected error message: {error_data}")
            else:
                self.log_test("Arabic Error Message - Project", False, 
                            f"Expected 404, got {response.status_code}")
        except Exception as e:
            self.log_test("Arabic Error Message - Project", False, f"Exception: {str(e)}")
            
        # Test 2: Get non-existent supplier
        try:
            response = self.session.get(f"{self.base_url}/suppliers/non-existent-id")
            if response.status_code == 404:
                error_data = response.json()
                if 'المورد غير موجود' in error_data.get('detail', ''):
                    self.log_test("Arabic Error Message - Supplier", True, 
                                "Correct Arabic error message returned")
                else:
                    self.log_test("Arabic Error Message - Supplier", False, 
                                f"Unexpected error message: {error_data}")
            else:
                self.log_test("Arabic Error Message - Supplier", False, 
                            f"Expected 404, got {response.status_code}")
        except Exception as e:
            self.log_test("Arabic Error Message - Supplier", False, f"Exception: {str(e)}")
            
    def cleanup_test_data(self):
        """Clean up test data"""
        print("\n=== Cleaning Up Test Data ===")
        
        # Delete test costs first (to update project costs correctly)
        for cost_key in ['cost_id', 'cost_id_2']:
            if cost_key in self.test_data:
                try:
                    response = self.session.delete(f"{self.base_url}/costs/{self.test_data[cost_key]}")
                    if response.status_code == 200:
                        self.log_test(f"Delete Test Cost ({cost_key})", True)
                    else:
                        self.log_test(f"Delete Test Cost ({cost_key})", False, f"Status: {response.status_code}")
                except Exception as e:
                    self.log_test(f"Delete Test Cost ({cost_key})", False, f"Exception: {str(e)}")
                    
        # Delete test items
        for item_key in ['item_id', 'item_id_2', 'item_id_3']:
            if item_key in self.test_data:
                try:
                    response = self.session.delete(f"{self.base_url}/items/{self.test_data[item_key]}")
                    if response.status_code == 200:
                        self.log_test(f"Delete Test Item ({item_key})", True)
                    else:
                        self.log_test(f"Delete Test Item ({item_key})", False, f"Status: {response.status_code}")
                except Exception as e:
                    self.log_test(f"Delete Test Item ({item_key})", False, f"Exception: {str(e)}")
                    
        # Delete test suppliers
        for supplier_key in ['supplier_id', 'service_supplier_id']:
            if supplier_key in self.test_data:
                try:
                    response = self.session.delete(f"{self.base_url}/suppliers/{self.test_data[supplier_key]}")
                    if response.status_code == 200:
                        self.log_test(f"Delete Test Supplier ({supplier_key})", True)
                    else:
                        self.log_test(f"Delete Test Supplier ({supplier_key})", False, f"Status: {response.status_code}")
                except Exception as e:
                    self.log_test(f"Delete Test Supplier ({supplier_key})", False, f"Exception: {str(e)}")
                    
        # Delete test project last
        if 'project_id' in self.test_data:
            try:
                response = self.session.delete(f"{self.base_url}/projects/{self.test_data['project_id']}")
                if response.status_code == 200:
                    self.log_test("Delete Test Project", True)
                else:
                    self.log_test("Delete Test Project", False, f"Status: {response.status_code}")
            except Exception as e:
                self.log_test("Delete Test Project", False, f"Exception: {str(e)}")
                
    def run_all_tests(self):
        """Run all test suites"""
        print("🚀 Starting Comprehensive Arabic ERP Backend Testing")
        print("=" * 60)
        
        # Run all test modules
        self.test_projects_module()
        self.test_costs_module()
        self.test_suppliers_module()
        self.test_inventory_module()
        self.test_dashboard_statistics()
        self.test_arabic_error_messages()
        
        # Clean up test data
        self.cleanup_test_data()
        
        # Print final summary
        print("\n" + "=" * 60)
        print("🏁 TEST SUMMARY")
        print("=" * 60)
        print(f"✅ Passed Tests: {self.passed_tests}")
        print(f"❌ Failed Tests: {self.failed_tests}")
        print(f"📊 Total Tests: {self.passed_tests + self.failed_tests}")
        
        if self.failed_tests == 0:
            print("\n🎉 ALL TESTS PASSED! Arabic ERP Backend is working correctly.")
            return True
        else:
            print(f"\n⚠️  {self.failed_tests} tests failed. Please review the issues above.")
            return False

if __name__ == "__main__":
    test_suite = ERPTestSuite()
    success = test_suite.run_all_tests()
    sys.exit(0 if success else 1)
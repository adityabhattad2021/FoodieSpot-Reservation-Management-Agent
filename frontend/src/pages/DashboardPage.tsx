import { useState } from 'react';
import { Routes, Route, Link, useLocation, Navigate } from 'react-router-dom';
import {  Calendar, Users, Settings, LogOut, MessageCircle, Menu, X } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { ReservationsTab } from '../components/dashboard/Reservations';
import { CustomersTab } from '../components/dashboard/Customers';
import { SupportTickets } from '../components/dashboard/SupportTickets';

export function DashboardPage() {
  const location = useLocation();
  const { logout } = useAuth();
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  const navigation = [
    { name: 'Reservations', href: '/dashboard/reservations', icon: Calendar },
    { name: 'Customers', href: '/dashboard/customers', icon: Users },
    { name: 'Support Tickets', href: '/dashboard/support', icon: MessageCircle },
  ];

  return (
    <div className="min-h-screen bg-gray-100">
      <div className="flex h-screen">
        {/* Mobile menu button */}
        <div className="lg:hidden fixed top-0 left-0 z-50 w-full bg-white border-b border-gray-200 px-4 py-3">
          <div className="flex items-center justify-between">
            <button
              onClick={() => setIsSidebarOpen(!isSidebarOpen)}
              className="p-2 rounded-md text-gray-500 hover:text-gray-600 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-blue-500"
            >
              {isSidebarOpen ? (
                <X className="h-6 w-6" />
              ) : (
                <Menu className="h-6 w-6" />
              )}
            </button>
            <h1 className="text-lg font-semibold text-gray-900">FoodieSpot Admin</h1>
            <div className="w-6" /> {/* Spacer for alignment */}
          </div>
        </div>

        {/* Sidebar for mobile */}
        <div
          className={`fixed inset-0 flex z-40 lg:hidden ${
            isSidebarOpen ? 'translate-x-0' : '-translate-x-full'
          } transition-transform duration-300 ease-in-out`}
        >
          <div className="relative flex-1 flex flex-col max-w-xs w-full pt-14 bg-white">
            <div className="flex-1 h-0 overflow-y-auto">
              <nav className="mt-5 px-2 space-y-1">
                {navigation.map((item) => {
                  const Icon = item.icon;
                  return (
                    <Link
                      key={item.name}
                      to={item.href}
                      onClick={() => setIsSidebarOpen(false)}
                      className={`${
                        location.pathname === item.href
                          ? 'bg-blue-50 text-blue-600'
                          : 'text-gray-600 hover:bg-gray-50'
                      } group flex items-center px-2 py-2 text-base font-medium rounded-md`}
                    >
                      <Icon className={`mr-4 flex-shrink-0 h-6 w-6 ${
                        location.pathname === item.href
                          ? 'text-blue-600'
                          : 'text-gray-400 group-hover:text-gray-500'
                      }`} />
                      {item.name}
                    </Link>
                  );
                })}
              </nav>
            </div>
            <div className="flex-shrink-0 flex border-t border-gray-200 p-4">
              <button
                onClick={() => {
                  logout();
                  setIsSidebarOpen(false);
                }}
                className="flex items-center text-gray-600 hover:text-gray-900"
              >
                <LogOut className="mr-3 h-5 w-5" />
                <span>Sign out</span>
              </button>
            </div>
          </div>
          <div 
            className="flex-shrink-0 w-14 opacity-0"
            onClick={() => setIsSidebarOpen(false)}
            aria-hidden="true"
          ></div>
        </div>

        {/* Desktop sidebar */}
        <div className="hidden lg:flex lg:flex-shrink-0">
          <div className="flex flex-col w-64">
            <div className="flex flex-col flex-grow pt-5 pb-4 overflow-y-auto bg-white border-r">
              <div className="flex items-center flex-shrink-0 px-4">
                <h1 className="text-xl font-semibold">FoodieSpot Admin</h1>
              </div>
              <div className="mt-5 flex-grow flex flex-col">
                <nav className="flex-1 px-2 space-y-1">
                  {navigation.map((item) => {
                    const Icon = item.icon;
                    return (
                      <Link
                        key={item.name}
                        to={item.href}
                        className={`${
                          location.pathname === item.href
                            ? 'bg-blue-50 text-blue-600'
                            : 'text-gray-600 hover:bg-gray-50'
                        } group flex items-center px-2 py-2 text-sm font-medium rounded-md`}
                      >
                        <Icon className={`mr-3 flex-shrink-0 h-6 w-6 ${
                          location.pathname === item.href
                            ? 'text-blue-600'
                            : 'text-gray-400 group-hover:text-gray-500'
                        }`} />
                        {item.name}
                      </Link>
                    );
                  })}
                </nav>
              </div>
              <div className="flex-shrink-0 flex border-t p-4">
                <button
                  onClick={logout}
                  className="flex-shrink-0 w-full group block"
                >
                  <div className="flex items-center">
                    <div className="ml-3">
                      <p className="text-sm font-medium text-gray-700 group-hover:text-gray-900 flex items-center">
                        <LogOut className="mr-2 h-5 w-5" />
                        Sign out
                      </p>
                    </div>
                  </div>
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Main content */}
        <div className="flex-1 overflow-auto focus:outline-none">
          <main className="flex-1 relative lg:py-6">
            <div className="px-4 sm:px-6 lg:px-8 pt-16 lg:pt-0">
              <Routes>
                <Route path="/" element={<Navigate to="reservations" replace />} />
                <Route path="/reservations" element={<ReservationsTab />} />
                <Route path="/customers" element={<CustomersTab />} />
                <Route path="/support" element={<SupportTickets />} />
              </Routes>
            </div>
          </main>
        </div>
      </div>
    </div>
  );
}
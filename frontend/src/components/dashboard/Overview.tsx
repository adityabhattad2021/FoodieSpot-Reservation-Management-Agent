import React from 'react';
import { BarChart3, Users, CalendarDays, TrendingUp } from 'lucide-react';

export function Overview() {
  const stats = [
    {
      name: 'Total Reservations',
      value: '1,234',
      icon: CalendarDays,
      change: '+12.3%',
      changeType: 'increase'
    },
    {
      name: 'Active Customers',
      value: '892',
      icon: Users,
      change: '+5.4%',
      changeType: 'increase'
    },
    {
      name: 'Average Rating',
      value: '4.8',
      icon: TrendingUp,
      change: '+0.2',
      changeType: 'increase'
    },
    {
      name: 'Revenue',
      value: '$52,389',
      icon: BarChart3,
      change: '+8.1%',
      changeType: 'increase'
    }
  ];

  return (
    <div>
      <h1 className="text-2xl font-semibold text-gray-900">Dashboard Overview</h1>
      <div className="mt-6 grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        {stats.map((item) => {
          const Icon = item.icon;
          return (
            <div key={item.name} className="relative overflow-hidden rounded-lg bg-white px-4 pt-5 pb-12 shadow sm:px-6 sm:pt-6">
              <dt>
                <div className="absolute rounded-md bg-blue-500 p-3">
                  <Icon className="h-6 w-6 text-white" />
                </div>
                <p className="ml-16 truncate text-sm font-medium text-gray-500">{item.name}</p>
              </dt>
              <dd className="ml-16 flex items-baseline pb-6 sm:pb-7">
                <p className="text-2xl font-semibold text-gray-900">{item.value}</p>
                <p className={`ml-2 flex items-baseline text-sm font-semibold ${
                  item.changeType === 'increase' ? 'text-green-600' : 'text-red-600'
                }`}>
                  {item.change}
                </p>
              </dd>
            </div>
          );
        })}
      </div>
    </div>
  );
}
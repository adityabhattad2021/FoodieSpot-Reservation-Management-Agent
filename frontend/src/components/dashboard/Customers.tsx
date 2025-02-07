import { useEffect, useState } from "react";
import { api } from "../../context/AuthContext";

interface Customer{
  customer_id: number;
  name: string;
  email: string;
  phone: string;
}

export function CustomersTab() {
  const [customers, setCustomers] = useState<Customer[]>([]);

  useEffect(()=>{
    const fetchCustomers = async () => {
      try {
        const response = await api.get('/customers/');
        setCustomers(response.data);
      } catch (error) {
        console.error('Error fetching customers:', error);
      }
    };
    fetchCustomers();
  },[])

  return (
    <div>
      <h1 className="text-2xl font-semibold text-gray-900">Customers</h1>
      <div className="mt-6">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-300">
            <thead>
              <tr>
                <th className="py-3.5 pl-4 pr-3 text-left text-sm font-semibold text-gray-900">Name</th>
                <th className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Email</th>
                <th className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Phone</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {customers.map((customer) => (
                <tr key={customer.customer_id}>
                  <td className="whitespace-nowrap py-4 pl-4 pr-3 text-sm font-medium text-gray-900">{customer.name}</td>
                  <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">{customer.email}</td>
                  <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">{customer.phone}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
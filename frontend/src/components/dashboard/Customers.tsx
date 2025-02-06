
export function Customers() {
  const customers = [
    {
      id: 1,
      name: 'John Doe',
      email: 'john@example.com',
      phone: '+1 234 567 8900',
      reservations: 5,
      lastVisit: '2024-02-15'
    }
  ];

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
                <th className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Reservations</th>
                <th className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Last Visit</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {customers.map((customer) => (
                <tr key={customer.id}>
                  <td className="whitespace-nowrap py-4 pl-4 pr-3 text-sm font-medium text-gray-900">{customer.name}</td>
                  <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">{customer.email}</td>
                  <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">{customer.phone}</td>
                  <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">{customer.reservations}</td>
                  <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">{customer.lastVisit}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
import React from 'react';
import { format } from 'date-fns';

export function Reservations() {
  const reservations = [
    {
      id: 1,
      customer: 'John Doe',
      date: new Date(),
      time: '19:00',
      guests: 4,
      status: 'Confirmed',
      restaurant: 'FoodieSpot Downtown'
    },
    // Add more sample reservations as needed
  ];

  return (
    <div>
      <h1 className="text-2xl font-semibold text-gray-900">Reservations</h1>
      <div className="mt-6">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-300">
            <thead>
              <tr>
                <th className="py-3.5 pl-4 pr-3 text-left text-sm font-semibold text-gray-900">Customer</th>
                <th className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Date</th>
                <th className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Time</th>
                <th className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Guests</th>
                <th className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Status</th>
                <th className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Restaurant</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {reservations.map((reservation) => (
                <tr key={reservation.id}>
                  <td className="whitespace-nowrap py-4 pl-4 pr-3 text-sm text-gray-900">{reservation.customer}</td>
                  <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">{format(reservation.date, 'MMM d, yyyy')}</td>
                  <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">{reservation.time}</td>
                  <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">{reservation.guests}</td>
                  <td className="whitespace-nowrap px-3 py-4 text-sm">
                    <span className="inline-flex rounded-full bg-green-100 px-2 text-xs font-semibold leading-5 text-green-800">
                      {reservation.status}
                    </span>
                  </td>
                  <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">{reservation.restaurant}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
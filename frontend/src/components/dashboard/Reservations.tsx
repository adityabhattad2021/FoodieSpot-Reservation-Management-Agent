import { format } from 'date-fns';
import { useEffect, useState } from 'react';
import { api } from '../../context/AuthContext';

interface Reservation {
  customer_id: number;
  restaurant_id: number;
  table_id: number;
  reservation_date: string; // YYYY-MM-DD format
  reservation_time: string; // HH:MM:SS.SSSSSS format
  number_of_guests: number;
  special_requests: string;
  status: "Confirmed" | "Pending" | "Cancelled"; 
  reservation_id: number;
}

export function ReservationsTab() {

  const [reservations, setReservations] = useState<Reservation[]>([]);

  useEffect(()=>{
    const fetchReservations = async () => {
      try {
        const response = await api.get('/reservations/');
        setReservations(response.data);
      } catch (error) {
        console.error('Error fetching reservations:', error);
      }
    };
    fetchReservations();
  },[])

  return (
    <div>
      <h1 className="text-2xl font-semibold text-gray-900">Reservations</h1>
      <div className="mt-6">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-300">
            <thead>
              <tr>
                <th className="py-3.5 pl-4 pr-3 text-left text-sm font-semibold text-gray-900">Customer Id</th>
                <th className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Date</th>
                <th className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Time</th>
                <th className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Guests</th>
                <th className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Status</th>
                <th className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Restaurant Id</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {reservations.map((reservation) => (
                <tr key={reservation.reservation_id}>
                  <td className="whitespace-nowrap py-4 pl-4 pr-3 text-sm text-gray-900">{reservation.customer_id}</td>
                  <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">{format(reservation.reservation_date, 'MMM d, yyyy')}</td>
                  <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">{reservation.reservation_time}</td>
                  <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">{reservation.number_of_guests}</td>
                  <td className="whitespace-nowrap px-3 py-4 text-sm">
                    <span className="inline-flex rounded-full bg-green-100 px-2 text-xs font-semibold leading-5 text-green-800">
                      {reservation.status}
                    </span>
                  </td>
                  <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">{reservation.restaurant_id}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
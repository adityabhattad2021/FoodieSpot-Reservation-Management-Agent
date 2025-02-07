import { MessageSquare } from 'lucide-react';
import { api } from '../../context/AuthContext';
import { useEffect, useState } from 'react';

interface SupportTicket {
  ticket_id: number;
  customer_id: number;
  ticket_date: string; // ISO date string format (YYYY-MM-DD)
  ticket_time: string; // ISO time string format (HH:MM:SS)
  ticket_description: string;
  status: boolean; // false = Open, true = Closed
}

const getStatusColor = (status:boolean) => {
  switch (status) {
    case false:
      return 'bg-green-100 text-green-800';
    case true:
      return 'bg-gray-100 text-gray-800';
  }
};


export function SupportTickets() {

  const [tickets, setTickets] = useState<SupportTicket[]>([]);

  useEffect(()=>{
    api.get('/support/').then((response) => {
      console.log(response.data);
      setTickets(response.data);
    });
  },[])

  function closeTicket(ticketId: number) {
    api.put(`/support/${ticketId}/close/`).then((response) => {
      const updatedTickets = tickets.map((ticket) => {
        if (ticket.ticket_id === response.data.ticketId) {
          ticket.status = true;
        }
        return ticket;
      });
      setTickets(updatedTickets);
    });
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <h1 className="text-2xl font-semibold text-gray-900">Support Tickets</h1>
      </div>

      <div className="bg-white rounded-lg shadow-lg overflow-hidden">
        <div className="overflow-x-auto">
          <div className="inline-block min-w-full align-middle">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Ticket
                  </th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider hidden sm:table-cell">
                    Customer Id
                  </th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Status
                  </th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {tickets.map((ticket) => (
                  <tr key={ticket.ticket_id} className="hover:bg-gray-50">
                    <td className="px-6 py-4">
                      <div className="flex items-start">
                        <MessageSquare className="h-5 w-5 text-gray-400 mr-3 mt-1 flex-shrink-0" />
                        <div>
                          <div className="text-sm font-medium text-gray-900">{ticket.ticket_description}</div>
                          <div className="text-sm text-gray-500 hidden sm:block">{ticket.ticket_description}</div>
                          <div className="text-sm text-gray-900 sm:hidden">{ticket.customer_id}</div>
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4 hidden sm:table-cell">
                      <div className="text-sm text-gray-900">{ticket.customer_id}</div>
                    </td>
                    <td className="px-6 py-4">
                      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(ticket.status)}`}>
                        {ticket.status ? 'Closed' : 'Open'}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-sm font-medium">
                      <div className="flex space-x-3">
                        <button className="text-blue-600 hover:text-blue-900" onClick={()=>closeTicket(ticket.ticket_id)}>Close</button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}
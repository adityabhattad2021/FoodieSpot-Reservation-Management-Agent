import React from 'react';
import { MessageSquare, Clock, CheckCircle, XCircle, AlertCircle } from 'lucide-react';

type TicketStatus = 'open' | 'closed' | 'pending';

interface Ticket {
  id: number;
  customer: string;
  subject: string;
  message: string;
  status: TicketStatus;
  priority: 'low' | 'medium' | 'high';
  createdAt: string;
  lastUpdated: string;
}

const tickets: Ticket[] = [
  {
    id: 1,
    customer: "John Doe",
    subject: "Reservation Modification Request",
    message: "I need to change my reservation time from 7 PM to 8 PM tomorrow.",
    status: "open",
    priority: "medium",
    createdAt: "2024-02-28T14:30:00",
    lastUpdated: "2024-02-28T14:30:00"
  },
  {
    id: 2,
    customer: "Alice Smith",
    subject: "Special Dietary Requirements",
    message: "I have severe nut allergies. Can you confirm if the kitchen can accommodate this?",
    status: "pending",
    priority: "high",
    createdAt: "2024-02-28T12:15:00",
    lastUpdated: "2024-02-28T13:20:00"
  },
  {
    id: 3,
    customer: "Bob Wilson",
    subject: "Birthday Party Arrangement",
    message: "Looking to arrange a surprise birthday party for 15 people.",
    status: "closed",
    priority: "low",
    createdAt: "2024-02-27T09:45:00",
    lastUpdated: "2024-02-28T11:30:00"
  }
];

const getStatusColor = (status: TicketStatus) => {
  switch (status) {
    case 'open':
      return 'bg-green-100 text-green-800';
    case 'closed':
      return 'bg-gray-100 text-gray-800';
    case 'pending':
      return 'bg-yellow-100 text-yellow-800';
  }
};

const getPriorityIcon = (priority: string) => {
  switch (priority) {
    case 'high':
      return <AlertCircle className="h-5 w-5 text-red-500" />;
    case 'medium':
      return <Clock className="h-5 w-5 text-yellow-500" />;
    case 'low':
      return <CheckCircle className="h-5 w-5 text-green-500" />;
  }
};

export function SupportTickets() {
  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <h1 className="text-2xl font-semibold text-gray-900">Support Tickets</h1>
        <div className="flex flex-col sm:flex-row gap-3 w-full sm:w-auto">
          <select className="rounded-lg border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 w-full sm:w-auto">
            <option>All Tickets</option>
            <option>Open</option>
            <option>Pending</option>
            <option>Closed</option>
          </select>
          <button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors w-full sm:w-auto">
            New Ticket
          </button>
        </div>
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
                    Customer
                  </th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Status
                  </th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider hidden md:table-cell">
                    Priority
                  </th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider hidden lg:table-cell">
                    Last Updated
                  </th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {tickets.map((ticket) => (
                  <tr key={ticket.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4">
                      <div className="flex items-start">
                        <MessageSquare className="h-5 w-5 text-gray-400 mr-3 mt-1 flex-shrink-0" />
                        <div>
                          <div className="text-sm font-medium text-gray-900">{ticket.subject}</div>
                          <div className="text-sm text-gray-500 hidden sm:block">{ticket.message}</div>
                          <div className="text-sm text-gray-900 sm:hidden">{ticket.customer}</div>
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4 hidden sm:table-cell">
                      <div className="text-sm text-gray-900">{ticket.customer}</div>
                    </td>
                    <td className="px-6 py-4">
                      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(ticket.status)}`}>
                        {ticket.status.charAt(0).toUpperCase() + ticket.status.slice(1)}
                      </span>
                    </td>
                    <td className="px-6 py-4 hidden md:table-cell">
                      <div className="flex items-center">
                        {getPriorityIcon(ticket.priority)}
                        <span className="ml-2 text-sm text-gray-500">
                          {ticket.priority.charAt(0).toUpperCase() + ticket.priority.slice(1)}
                        </span>
                      </div>
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-500 hidden lg:table-cell">
                      {new Date(ticket.lastUpdated).toLocaleString()}
                    </td>
                    <td className="px-6 py-4 text-sm font-medium">
                      <div className="flex space-x-3">
                        <button className="text-blue-600 hover:text-blue-900">View</button>
                        <button className="text-green-600 hover:text-green-900">Respond</button>
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
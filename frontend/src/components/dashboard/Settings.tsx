import React from 'react';
import { Save } from 'lucide-react';

export function Settings() {
  return (
    <div>
      <h1 className="text-2xl font-semibold text-gray-900">Settings</h1>
      <div className="mt-6 space-y-8">
        <div className="bg-white shadow rounded-lg p-6">
          <h2 className="text-lg font-medium text-gray-900 mb-4">Restaurant Information</h2>
          <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
            <div>
              <label htmlFor="restaurant-name" className="block text-sm font-medium text-gray-700">
                Restaurant Name
              </label>
              <input
                type="text"
                name="restaurant-name"
                id="restaurant-name"
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
                defaultValue="FoodieSpot Downtown"
              />
            </div>
            <div>
              <label htmlFor="contact-email" className="block text-sm font-medium text-gray-700">
                Contact Email
              </label>
              <input
                type="email"
                name="contact-email"
                id="contact-email"
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
                defaultValue="contact@foodiespot.com"
              />
            </div>
            <div>
              <label htmlFor="phone" className="block text-sm font-medium text-gray-700">
                Phone Number
              </label>
              <input
                type="tel"
                name="phone"
                id="phone"
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
                defaultValue="+1 (555) 123-4567"
              />
            </div>
            <div>
              <label htmlFor="address" className="block text-sm font-medium text-gray-700">
                Address
              </label>
              <input
                type="text"
                name="address"
                id="address"
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
                defaultValue="123 Main St, City, State 12345"
              />
            </div>
          </div>
        </div>

        <div className="bg-white shadow rounded-lg p-6">
          <h2 className="text-lg font-medium text-gray-900 mb-4">Operating Hours</h2>
          <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
            <div>
              <label htmlFor="opening-time" className="block text-sm font-medium text-gray-700">
                Opening Time
              </label>
              <input
                type="time"
                name="opening-time"
                id="opening-time"
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
                defaultValue="11:00"
              />
            </div>
            <div>
              <label htmlFor="closing-time" className="block text-sm font-medium text-gray-700">
                Closing Time
              </label>
              <input
                type="time"
                name="closing-time"
                id="closing-time"
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
                defaultValue="23:00"
              />
            </div>
          </div>
        </div>

        <div className="bg-white shadow rounded-lg p-6">
          <h2 className="text-lg font-medium text-gray-900 mb-4">Notification Settings</h2>
          <div className="space-y-4">
            <div className="flex items-center">
              <input
                id="email-notifications"
                name="email-notifications"
                type="checkbox"
                className="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                defaultChecked
              />
              <label htmlFor="email-notifications" className="ml-3 block text-sm font-medium text-gray-700">
                Email notifications for new reservations
              </label>
            </div>
            <div className="flex items-center">
              <input
                id="sms-notifications"
                name="sms-notifications"
                type="checkbox"
                className="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                defaultChecked
              />
              <label htmlFor="sms-notifications" className="ml-3 block text-sm font-medium text-gray-700">
                SMS notifications for new reservations
              </label>
            </div>
          </div>
        </div>

        <div className="flex justify-end">
          <button
            type="button"
            className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            <Save className="h-4 w-4 mr-2" />
            Save Changes
          </button>
        </div>
      </div>
    </div>
  );
}
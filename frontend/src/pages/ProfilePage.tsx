import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { User, Edit, Save, Calendar, Clock, Code } from 'lucide-react';
import { api } from '../context/AuthContext';
import { Header } from '../components/Header';

interface Reservation {
  reservation_id: number;
  restaurant:{
    restaurant_name: string;
  }
  reservation_date: string;
  reservation_time: string;
  number_of_guests: number;
  status: string;
  reservation_code:string;
}

export function ProfilePage() {
  const { user, isAuthenticated, logout, updateUserProfile, fetchUserProfile } = useAuth();
  const [isEditing, setIsEditing] = useState(false);
  const [reservations, setReservations] = useState<Reservation[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');
  const [successMessage, setSuccessMessage] = useState('');
  const [aiPreferences, setAiPreferences] = useState('');
  const navigate = useNavigate();
  
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    ai_preferences: '',
  });

  async function loadUserData(api: any) { 
    try {
      setIsLoading(true);
      // Fetch user profile
      const userData = await fetchUserProfile();
      setFormData({
          name: userData.name,
          email: userData.email,
          ai_preferences: userData.ai_preferences,
      });

      setAiPreferences(userData.ai_preferences);

      // Fetch user reservations
      const reservationsResponse = await api.get('/my-reservations/');
      setReservations(reservationsResponse.data);
    } catch (error) {
      console.error('Error loading user data:', error);
      setError('Failed to load user data. Please try again.');
    } finally {
      setIsLoading(false);
    }
  }

  useEffect(() => {
      loadUserData(api);
  }, [api]);

  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/login');
      return;
    }
  }, [isAuthenticated, navigate, fetchUserProfile]);

  const handleEdit = () => {
    setIsEditing(true);
  };

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setSuccessMessage('');

    try {
      await updateUserProfile(formData);
      setIsEditing(false);
      setSuccessMessage('Profile updated successfully!');
      
      // Clear success message after 3 seconds
      setTimeout(() => {
        setSuccessMessage('');
      }, 3000);
    } catch (error) {
      console.error('Error updating profile:', error);
      setError('Failed to update profile. Please try again later.');
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleCancelReservation = async (reservationId: number) => {
    try {
      await api.delete(`/my-reservations/${reservationId}`);
      
      // Update the reservations list
      setReservations(reservations.map(res => 
        res.reservation_id === reservationId 
          ? { ...res, status: 'Cancelled' } 
          : res
      ));
      
      setSuccessMessage('Reservation cancelled successfully!');
      
      // Clear success message after 3 seconds
      setTimeout(() => {
        setSuccessMessage('');
      }, 3000);
    } catch (error) {
      console.error('Error cancelling reservation:', error);
      setError('Failed to cancel reservation. Please try again.');
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    });
  };

  const formatTime = (timeString: string) => {
    // Assuming timeString is in format "HH:MM:SS"
    const [hours, minutes] = timeString.split(':');
    const hour = parseInt(hours, 10);
    const ampm = hour >= 12 ? 'PM' : 'AM';
    const hour12 = hour % 12 || 12;
    return `${hour12}:${minutes} ${ampm}`;
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-orange-50 to-red-50 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-orange-600"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-50 to-red-50">
      <Header />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {error && (
          <div className="mb-4 bg-red-50 border-l-4 border-red-400 p-4 rounded-lg">
            <div className="flex">
              <div className="flex-shrink-0">
                <svg className="h-5 w-5 text-red-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="ml-3">
                <p className="text-sm text-red-700">{error}</p>
              </div>
            </div>
          </div>
        )}

        {successMessage && (
          <div className="mb-4 bg-green-50 border-l-4 border-green-400 p-4 rounded-lg">
            <div className="flex">
              <div className="flex-shrink-0">
                <svg className="h-5 w-5 text-green-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="ml-3">
                <p className="text-sm text-green-700">{successMessage}</p>
              </div>
            </div>
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Profile Card */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-xl shadow-lg overflow-hidden">
              <div className="bg-gradient-to-r from-orange-600 to-red-600 px-6 py-8">
                <div className="flex justify-between items-start">
                  <div className="flex items-center space-x-4">
                    <div className="bg-white p-3 rounded-full">
                      <User className="h-10 w-10 text-orange-600" />
                    </div>
                    <div>
                      <h2 className="text-2xl font-bold text-white">{user?.name}</h2>
                      <p className="text-orange-100">Foodie Enthusiast</p>
                    </div>
                  </div>
                  {!isEditing ? (
                    <button
                      onClick={handleEdit}
                      className="bg-white/20 hover:bg-white/30 text-white p-2 rounded-lg transition-colors"
                    >
                      <Edit className="h-5 w-5" />
                    </button>
                  ) : (
                    <button
                      onClick={handleSave}
                      className="bg-white text-orange-600 p-2 rounded-lg hover:bg-orange-50 transition-colors"
                    >
                      <Save className="h-5 w-5" />
                    </button>
                  )}
                </div>
              </div>
              
              <div className="px-6 py-6">
                {!isEditing ? (
                  <div className="space-y-4">
                    <div>
                      <p className="text-sm text-gray-500">Email</p>
                      <p className="text-gray-800">{user?.email}</p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-500">AI Preferences</p>
                      <p className="text-gray-800">{aiPreferences || 'No preferences set'}</p>
                    </div>
                  </div>
                ) : (
                  <form onSubmit={handleSave} className="space-y-4">
                    <div>
                      <label className="block text-sm text-gray-500 mb-1">Name</label>
                      <input
                        type="text"
                        name="name"
                        value={formData.name}
                        onChange={handleChange}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500"
                      />
                    </div>
                    <div>
                      <label className="block text-sm text-gray-500 mb-1">Email</label>
                      <input
                        type="email"
                        name="email"
                        value={formData.email}
                        onChange={handleChange}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500"
                      />
                    </div>
                    <div>
                      <label className="block text-sm text-gray-500 mb-1">AI Preferences</label>
                      <textarea
                        name="ai_preferences"
                        value={formData.ai_preferences}
                        onChange={handleChange}
                        placeholder="Tell us about your food preferences, dietary restrictions, etc."
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500"
                        rows={3}
                      />
                    </div>
                    <div className="pt-2">
                      <button
                        type="submit"
                        className="w-full bg-orange-600 text-white py-2 px-4 rounded-lg hover:bg-orange-700 transition-colors"
                      >
                        Save Changes
                      </button>
                    </div>
                  </form>
                )}
              </div>
              
              <div className="px-6 py-4 border-t border-gray-100">
                <button
                  onClick={logout}
                  className="w-full bg-red-100 text-red-600 py-2 px-4 rounded-lg hover:bg-red-200 transition-colors font-medium"
                >
                  Logout
                </button>
              </div>
            </div>
          </div>
          
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-8">
            {/* Upcoming Reservations */}
            <div className="bg-white rounded-xl shadow-lg overflow-hidden">
              <div className="px-6 py-5 border-b border-gray-100">
                <div className="flex items-center justify-between">
                  <h3 className="text-xl font-bold text-gray-900">My Reservations</h3>
                  <Calendar className="h-5 w-5 text-orange-600" />
                </div>
              </div>
              
              {reservations.length === 0 ? (
                <div className="px-6 py-8 text-center">
                  <p className="text-gray-500 mb-4">You don't have any reservations yet.</p>
                  <button
                    onClick={() => navigate('/chat')}
                    className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-orange-600 hover:bg-orange-700"
                  >
                    Book a Restaurant
                  </button>
                </div>
              ) : (
                <div className="divide-y divide-gray-100">
                  {reservations.map((reservation) => (
                    <div key={reservation.reservation_id} className="px-6 py-4">
                      <div className="flex justify-between items-start">
                        <div>
                          <h4 className="font-semibold text-gray-900">{reservation.restaurant.restaurant_name}</h4>
                          <div className="flex flex-wrap items-center gap-4 mt-1">
                            <div className="flex items-center text-sm text-gray-500">
                              <Calendar className="h-4 w-4 mr-1" />
                              {formatDate(reservation.reservation_date)}
                            </div>
                            <div className="flex items-center text-sm text-gray-500">
                              <Clock className="h-4 w-4 mr-1" />
                              {formatTime(reservation.reservation_time)}
                            </div>
                            <div className="flex items-center text-sm text-gray-500">
                              <User className="h-4 w-4 mr-1" />
                              {reservation.number_of_guests} {reservation.number_of_guests === 1 ? 'guest' : 'guests'}
                            </div>
                            {reservation.reservation_code && (
                              <div className="flex items-center text-sm text-gray-500">
                                <Code className="h-4 w-4 mr-1" />
                                Code: {reservation.reservation_code}
                              </div>
                            )}
                          </div>
                        </div>
                        <div className="flex flex-col items-end gap-2">
                          <span
                            className={`px-3 py-1 rounded-full text-xs font-medium ${
                              reservation.status === 'Confirmed' ? 'bg-green-100 text-green-800' :
                              reservation.status === 'Pending' ? 'bg-yellow-100 text-yellow-800' :
                              'bg-red-100 text-red-800'
                            }`}
                          >
                            {reservation.status}
                          </span>
                          
                          {reservation.status !== 'Cancelled' && (
                            <button
                              onClick={() => handleCancelReservation(reservation.reservation_id)}
                              className="text-xs text-red-600 hover:text-red-800 font-medium"
                            >
                              Cancel
                            </button>
                          )}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
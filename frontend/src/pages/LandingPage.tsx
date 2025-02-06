import { Link } from 'react-router-dom';
import { ChefHat, Utensils, Calendar, MessageCircle, Menu, X } from 'lucide-react';
import { useState } from 'react';

export function LandingPage() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-50">
      {/* Header */}
      <header className="bg-white shadow-lg relative">
        <nav className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <Link className="flex items-center space-x-3 cursor-pointer" to="/" >
              <ChefHat className="h-8 w-8 text-blue-600" />
              <h1 className="text-2xl font-bold text-gray-900">FoodieSpot</h1>
            </Link>
            {/* Mobile menu button */}
            <div className="flex md:hidden">
              <button
                onClick={() => setIsMenuOpen(!isMenuOpen)}
                className="text-gray-500 hover:text-gray-600"
              >
                {isMenuOpen ? (
                  <X className="h-6 w-6" />
                ) : (
                  <Menu className="h-6 w-6" />
                )}
              </button>
            </div>
            {/* Desktop menu */}
            <div className="hidden md:flex items-center space-x-4">
              <Link to="/chat" className="text-gray-600 hover:text-blue-600">Chat with AI</Link>
              <Link to="/login" className="px-4 py-2 rounded-lg bg-blue-600 text-white hover:bg-blue-700 transition-colors">
                Staff Login
              </Link>
            </div>
          </div>
          {/* Mobile menu */}
          {isMenuOpen && (
            <div className="md:hidden">
              <div className="px-2 pt-2 pb-3 space-y-1">
                <Link
                  to="/chat"
                  className="block px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-50"
                >
                  Chat with AI
                </Link>
                <Link
                  to="/login"
                  className="block px-3 py-2 rounded-md text-base font-medium bg-blue-600 text-white hover:bg-blue-700"
                >
                  Staff Login
                </Link>
              </div>
            </div>
          )}
        </nav>
      </header>

      {/* Hero Section */}
      <section className="relative overflow-hidden">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 sm:py-24">
          <div className="text-center">
            <h1 className="text-4xl sm:text-5xl md:text-6xl font-extrabold text-gray-900">
              Your Perfect Dining Experience
              <span className="block text-blue-600">Starts Here</span>
            </h1>
            <p className="mt-4 sm:mt-6 text-lg sm:text-xl text-gray-500 max-w-3xl mx-auto px-4">
              Discover and reserve tables at the finest restaurants in your city. Let our AI assistant help you find the perfect spot for any occasion.
            </p>
            <div className="mt-6 sm:mt-10 px-4">
              <Link
                to="/chat"
                className="inline-block px-6 sm:px-8 py-3 sm:py-4 bg-blue-600 text-white rounded-full text-base sm:text-lg font-semibold hover:bg-blue-700 transition-colors shadow-lg hover:shadow-xl"
              >
                Start Chatting with AI
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="py-12 sm:py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h2 className="text-2xl sm:text-3xl md:text-4xl font-extrabold text-gray-900">
              Why Choose FoodieSpot?
            </h2>
          </div>

          <div className="mt-12 sm:mt-20 grid grid-cols-1 gap-6 sm:gap-8 sm:grid-cols-2 lg:grid-cols-3">
            <div className="relative group">
              <div className="absolute -inset-0.5 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-lg blur opacity-25 group-hover:opacity-100 transition duration-1000 group-hover:duration-200"></div>
              <div className="relative p-6 bg-white ring-1 ring-gray-900/5 rounded-lg leading-none flex items-top justify-start space-x-6">
                <Utensils className="h-8 w-8 text-blue-600 flex-shrink-0" />
                <div className="space-y-2">
                  <p className="text-lg sm:text-xl font-semibold text-gray-900">Curated Restaurants</p>
                  <p className="text-sm sm:text-base text-gray-600">Handpicked selection of the finest dining establishments in your area.</p>
                </div>
              </div>
            </div>

            <div className="relative group">
              <div className="absolute -inset-0.5 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-lg blur opacity-25 group-hover:opacity-100 transition duration-1000 group-hover:duration-200"></div>
              <div className="relative p-6 bg-white ring-1 ring-gray-900/5 rounded-lg leading-none flex items-top justify-start space-x-6">
                <Calendar className="h-8 w-8 text-blue-600 flex-shrink-0" />
                <div className="space-y-2">
                  <p className="text-lg sm:text-xl font-semibold text-gray-900">Easy Reservations</p>
                  <p className="text-sm sm:text-base text-gray-600">Book your table in seconds with our AI-powered reservation system.</p>
                </div>
              </div>
            </div>

            <div className="relative group">
              <div className="absolute -inset-0.5 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-lg blur opacity-25 group-hover:opacity-100 transition duration-1000 group-hover:duration-200"></div>
              <div className="relative p-6 bg-white ring-1 ring-gray-900/5 rounded-lg leading-none flex items-top justify-start space-x-6">
                <MessageCircle className="h-8 w-8 text-blue-600 flex-shrink-0" />
                <div className="space-y-2">
                  <p className="text-lg sm:text-xl font-semibold text-gray-900">AI Assistant</p>
                  <p className="text-sm sm:text-base text-gray-600">Get personalized restaurant recommendations based on your preferences.</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-blue-600 py-12 sm:py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h2 className="text-2xl sm:text-3xl md:text-4xl font-extrabold text-white">
              Ready to Experience the Best Dining?
            </h2>
            <p className="mt-4 text-base sm:text-xl text-blue-100">
              Start chatting with our AI assistant and find your perfect restaurant today.
            </p>
            <div className="mt-6 sm:mt-8">
              <Link
                to="/chat"
                className="inline-flex items-center px-4 sm:px-6 py-2 sm:py-3 border border-transparent text-base font-medium rounded-md text-blue-600 bg-white hover:bg-blue-50 transition-colors"
              >
                Get Started
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900">
        <div className="max-w-7xl mx-auto py-8 sm:py-12 px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col sm:flex-row justify-between items-center space-y-4 sm:space-y-0">
            <div className="flex items-center">
              <ChefHat className="h-8 w-8 text-white" />
              <span className="ml-2 text-xl font-bold text-white">FoodieSpot</span>
            </div>
            <div className="flex flex-wrap justify-center space-x-4 sm:space-x-6">
              <a href="#" className="text-gray-400 hover:text-white">About</a>
              <a href="#" className="text-gray-400 hover:text-white">Contact</a>
              <a href="#" className="text-gray-400 hover:text-white">Privacy</a>
              <a href="#" className="text-gray-400 hover:text-white">Terms</a>
            </div>
          </div>
          <div className="mt-6 sm:mt-8 border-t border-gray-800 pt-6 sm:pt-8">
            <p className="text-center text-sm sm:text-base text-gray-400">
              © 2024 FoodieSpot. All rights reserved.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}
import { Link } from 'react-router-dom';
import { ChefHat, Utensils, Calendar, MessageCircle, Star, Users, Search } from 'lucide-react';
import { Header } from '../components/Header';

export function LandingPage() {

  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-50 to-red-50">
      <Header />

      <section className="relative overflow-hidden">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 sm:py-24">
          <div className="text-center">
            <span className="inline-block px-4 py-2 rounded-full bg-orange-100 text-orange-700 text-sm font-medium mb-6">
              AI-Powered Restaurant Discovery
            </span>
            <h1 className="text-4xl sm:text-5xl md:text-6xl font-extrabold text-gray-900">
              Your Perfect Dining Experience
              <span className="block text-orange-600">Starts Here</span>
            </h1>
            <p className="mt-4 sm:mt-6 text-lg sm:text-xl text-gray-600 max-w-3xl mx-auto px-4">
              Discover and reserve tables at the finest restaurants in your city. Let our AI assistant help you find the perfect spot for any occasion.
            </p>
            <div className="mt-6 sm:mt-10 space-y-4 sm:space-y-0 sm:space-x-4">
              <Link
                to="/chat"
                className="inline-block px-8 py-4 bg-orange-600 text-white rounded-xl text-lg font-semibold hover:bg-orange-700 transition-all shadow-lg hover:shadow-xl"
              >
                Start Chatting with AI
              </Link>
              <a
                href="#features"
                className="inline-block px-8 py-4 bg-white text-orange-600 rounded-xl text-lg font-semibold hover:bg-orange-50 transition-all shadow-lg hover:shadow-xl border-2 border-orange-200"
              >
                Learn More
              </a>
            </div>
          </div>
        </div>
      </section>

      <section id="features" className="py-16 sm:py-24 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <span className="inline-block px-4 py-2 rounded-full bg-orange-100 text-orange-700 text-sm font-medium mb-6">
              Why Choose FoodieSpot?
            </span>
            <h2 className="text-3xl sm:text-4xl font-extrabold text-gray-900">
              Everything you need for the perfect meal
            </h2>
          </div>

          <div className="mt-16 grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3">
            {[
              {
                icon: <Utensils className="h-8 w-8 text-orange-600" />,
                title: "Curated Restaurants",
                description: "Handpicked selection of the finest dining establishments in your area."
              },
              {
                icon: <Calendar className="h-8 w-8 text-orange-600" />,
                title: "Easy Reservations",
                description: "Book your table in seconds with our AI-powered reservation system."
              },
              {
                icon: <MessageCircle className="h-8 w-8 text-orange-600" />,
                title: "AI Assistant",
                description: "Get personalized restaurant recommendations based on your preferences."
              }
            ].map((feature, index) => (
              <div key={index} className="relative group">
                <div className="absolute -inset-0.5 bg-gradient-to-r from-orange-600 to-red-600 rounded-xl blur opacity-25 group-hover:opacity-75 transition duration-500"></div>
                <div className="relative p-8 bg-white rounded-xl shadow-lg transition-all group-hover:scale-[1.02]">
                  <div className="bg-orange-100 w-16 h-16 rounded-xl flex items-center justify-center mb-6">
                    {feature.icon}
                  </div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-4">
                    {feature.title}
                  </h3>
                  <p className="text-gray-600 h-[70px]">
                    {feature.description}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="bg-gradient-to-r from-orange-600 to-red-600 py-16 sm:py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h2 className="text-3xl sm:text-4xl font-extrabold text-white">
              Ready to Experience the Best Dining?
            </h2>
            <p className="mt-4 text-xl text-orange-100">
              Start chatting with our AI assistant and find your perfect restaurant today.
            </p>
            <div className="mt-8">
              <Link
                to="/chat"
                className="inline-flex items-center px-8 py-4 text-lg font-semibold rounded-xl text-orange-600 bg-white hover:bg-orange-50 transition-all shadow-lg hover:shadow-xl"
              >
                Get Started Now
              </Link>
            </div>
          </div>
        </div>
      </section>

      <footer className="bg-gray-900">
        <div className="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col sm:flex-row justify-between items-center space-y-6 sm:space-y-0">
            <div className="flex items-center space-x-4">
              <div className="bg-orange-100 p-2 rounded-lg">
                <ChefHat className="h-8 w-8 text-orange-600" />
              </div>
              <div>
                <span className="text-xl font-bold text-white block">FoodieSpot</span>
                <span className="text-sm text-gray-400">Your AI Restaurant Assistant</span>
              </div>
            </div>
            <div className="flex flex-wrap justify-center gap-6 sm:gap-8">
              <a href="#" className="text-gray-400 hover:text-white transition-colors">About</a>
              <a href="#" className="text-gray-400 hover:text-white transition-colors">Contact</a>
              <a href="#" className="text-gray-400 hover:text-white transition-colors">Privacy</a>
              <a href="#" className="text-gray-400 hover:text-white transition-colors">Terms</a>
            </div>
          </div>
          <div className="mt-8 pt-8 border-t border-gray-800">
            <p className="text-center text-gray-400">
              © 2025 FoodieSpot. All rights reserved.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}
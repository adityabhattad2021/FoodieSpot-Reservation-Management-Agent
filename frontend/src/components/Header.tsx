import { ChefHat, LogIn } from "lucide-react";
import { Link } from "react-router-dom";

export function Header() {
    return (
        <div className="bg-white shadow-md">
            <div className="max-w-7xl mx-auto px-6">
                <div className="flex justify-between items-center py-4">
                    <Link className="flex items-center space-x-3 group" to="/">
                        <div className="bg-orange-100 p-2 rounded-lg group-hover:bg-orange-200 transition-colors">
                            <ChefHat className="h-8 w-8 text-orange-600" />
                        </div>
                        <div>
                            <h1 className="text-2xl font-bold text-gray-900">FoodieSpot</h1>
                            <p className="text-sm text-gray-500">Your AI Restaurant Assistant</p>
                        </div>
                    </Link>
                    <Link
                        to="/login"
                        className="flex items-center space-x-2 text-gray-600 hover:text-orange-600 transition-colors bg-gray-50 px-4 py-2 rounded-lg hover:bg-gray-100"
                    >
                        <LogIn className="h-5 w-5" />
                        <span className="font-medium">Staff Login</span>
                    </Link>
                </div>
            </div>
        </div>
    )
}
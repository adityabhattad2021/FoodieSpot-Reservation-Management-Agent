export enum TableStatus {
  AVAILABLE = "Available",
  RESERVED = "Reserved",
  MAINTENANCE = "Maintenance"
}

export enum ReservationStatus {
  CONFIRMED = "Confirmed",
  CANCELLED = "Cancelled",
  PENDING = "Pending"
}

export enum CuisineType {
  NORTH_INDIAN = "North Indian",
  SOUTH_INDIAN = "South Indian",
  CHINESE = "Chinese",
  ITALIAN = "Italian",
  CONTINENTAL = "Continental",
  MUGHLAI = "Mughlai",
  THAI = "Thai",
  JAPANESE = "Japanese",
  MEXICAN = "Mexican",
  MEDITERRANEAN = "Mediterranean",
  BENGALI = "Bengali",
  GUJARATI = "Gujarati",
  PUNJABI = "Punjabi",
  KERALA = "Kerala",
  HYDERABADI = "Hyderabadi"
}

export enum PriceRange {
  BUDGET = "$",
  MODERATE = "$$",
  PREMIUM = "$$$",
  LUXURY = "$$$$"
}

export enum Ambiance {
  CASUAL = "Casual",
  FINE_DINING = "Fine Dining",
  FAMILY = "Family",
  CAFE = "Cafe",
  BISTRO = "Bistro",
  LOUNGE = "Lounge",
  OUTDOOR = "Outdoor"
}

export interface Restaurant {
  restaurant_id: number;
  name: string;
  address: string;
  phone: string;
  email: string;
  opening_time: string;
  closing_time: string;
  seating_capacity: number;
  special_event_space: boolean;
  cuisine_type: CuisineType;
  price_range: PriceRange;
  ambiance: Ambiance;
  average_rating: number;
  features?: string;
  description?: string;
  specialties?: string;
  dietary_options?: string;
}

export interface Table {
  table_id: number;
  restaurant_id: number;
  table_number: number;
  seating_capacity: number;
  table_type: string;
  status: TableStatus;
}

export interface Reservation {
  reservation_id: number;
  customer_id: number;
  restaurant_id: number;
  table_id: number;
  reservation_date: string;
  reservation_time: string;
  number_of_guests: number;
  special_requests?: string;
  status: ReservationStatus;
  customer: Customer;
  restaurant: Restaurant;
  table: Table;
}

export interface Customer {
  customer_id: number;
  name: string;
  phone: string;
  email?: string;
}

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
}
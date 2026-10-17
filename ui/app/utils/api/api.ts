// API utility functions for Fabrics Plus Curtains

/**
 * Types
 */
export interface UnavailablePeriod {
  pickup_date: string
  return_date: string
  status: string
}

export interface User {
  id: number
  email: string
  given_name: string
  family_name: string
  contact_number: string
  profile_picture: string | null
  address: string
  date_joined: string
  id_images: {
    images: string[]
  }
  status: 'Active' | 'Suspended'
  role: 'Super Admin' | 'Admin' | 'User'
  rentals: number
}

export interface UsersStats {
  total: number
  active: number
  suspended: number
}

export interface UpdateProfilePayload {
  given_name: string
  family_name: string
  email: string
  contact_number: string
  address: string
  id_images: {
      images: string[]
  }
  profile_picture?: string
  deleted_images?: string[]
}

export interface CarType {
  id: number
  name: string
  slug: string
}

export interface Feature {
  id: number
  name: string
  slug: string
}

export interface Car {
  car_id: string
  brand: string
  model: string
  year: number
  car_type: string | null
  price_per_day: string
  transmission: string
  engine: string
  fuel_type: string
  seats: number
  features: string[]
  note: string | null
  png_image: string | null
  status: 'available' | 'maintenance'
  approval_status: string
  created_at: string
  created_by: number
  updated_at: string
  meta: {
    primary_image: string | null
    images: string[]
  }
  unavailable_periods: UnavailablePeriod[]
  rental_count: number
}

export interface VehicleImage {
    url: string
    file?: File
}

export interface CarForm {
    id: string
    car_type: string | null
    brand: string
    model: string
    year: number | null
    price_per_day: number | null
    transmission: string
    engine: string
    fuel_type: string
    seats: number | null
    note: string | null
    status: 'available' | 'maintenance'
    features: string[]
    images: VehicleImage[]
    thumbnail_url: string | null
}

export interface Review {
  id: number
  car: string
  user: {
    id: number
    first_name: string
    last_name: string
    profile_picture?: string | null
  }
  rating: number
  text: string
  created_at: string
  images: string[]
  helpful_count: number
}

export interface ReviewForm {
    rating: number
    review: string
    images: string[]
}

export interface RatingBreakdown {
  star: number
  percent: number
}

export interface UsersResponse {
  count: number
  page: number
  page_size: number
  total_pages: number
  next: string | null
  previous: string | null
  results: User[]
}

export interface AdminReview {
  id: number

  car: {
      car_id: string
      brand: string
      model: string
  }

  user: {
      id: number
      first_name: string
      last_name: string
      email: string
      profile_picture?: string | null
  }

  rating: number
  text: string
  status: 'pending' | 'approved' | 'rejected'
  created_at: string
  images: string[]
  helpful_count: number
}

export interface AdminReviewsResponse {
    count: number
    next?: string | null
    previous?: string | null
    results: AdminReview[]
}

export interface ReviewsResponse {
  count: number
  next?: string | null
  previous?: string | null
  results: Review[]
  avg_rating: number
  rating_breakdown: Record<number, number>
  total_reviews: number
}

export interface CarReviewsResponse {
  results: Review[]
  count: number
  avg_rating: number
  rating_breakdown: Record<number, number>
  next?: string | null
  previous?: string | null
  total_reviews: number
  my_review: Review | null
}

export interface FilterOption {
  label: string
  count: number
}

export interface CarTypeFilterOption extends FilterOption {
    id: number
}

export interface Tab {
  label: string
  value: string
}

export interface SortOption {
  label: string
  value: string
}

export interface FleetResponse {
  count: number
  page: number
  page_size: number
  total_pages: number
  next?: string | null
  previous?: string | null
  results: Car[]
  filters: {
    categories: CarTypeFilterOption[]
    transmissions: FilterOption[]
    seats: FilterOption[]
    fuel: FilterOption[]
    features: FilterOption[]
  }
}

export interface Transaction {
  booking_reference: string
  status: string

  payment_method: string

  created_at: string
  total_price: number

  pending_approval_at: string | null
  confirmed_at: string | null
  picked_up_at: string | null
  returned_at: string | null
  completed_at: string | null
  cancelled_at: string | null
  cancel_reason: string | null

  pickup_date: string
  return_date: string

  pickup_location: string
  return_location: string

  daily_rate: number
  number_of_days: number
  subtotal: number
  discount: number

  car: {
      car_id: string
      brand: string
      model: string
      image: string
      year: number
      price_per_day: number
  }

  user: {
      id: number
      email: string
      first_name: string
      last_name: string
      contact_number: string
      address: string
      id_images: {
          images: string[]
      }
  }
}

export interface BookingForm {
    booking_reference: string
    user: number
    car: string

    status: string
    cancel_reason: string

    daily_rate: number
    number_of_days: number
    subtotal: number
    discount: number
    total_price: number

    pickup_date: string
    return_date: string
    pickup_location: string
    return_location: string
}

export interface TransactionResponse {
  count: number
  next?: string | null
  previous?: string | null
  results: Transaction[]
}

export interface UploadedFile {
  name: string;
  url: string;
}

export interface UploadResponse {
  uploaded_files: UploadedFile[];
}

export interface DeleteResponse {
  success: boolean;
  message?: string;
}

export interface NotificationBooking {
  booking_reference: string
  status: string
}

export interface Notification {
  id: number
  notification_type: string
  title: string
  message: string
  action_url: string | null
  booking: NotificationBooking | null
  is_read: boolean
  read_at: string | null
  created_at: string
}

export interface NotificationResponse {
  count: number
  next: string | null
  previous: string | null
  results: Notification[]
}

export interface FleetStatsResponse {
  total_cars: number
  available_count: number
  unavailable_count: number
  maintenance_count: number
  pending_approval_count: number
  fleet_condition: number
  available_percentage: number
  rented_count: number
}

export interface BookingStatsResponse {
  total: number
  pending_approval: number
  active_rentals: number
  completed: number
  cancelled: number
}

/**
 * Get the base API URL from runtime config
 */
export const useApiBase = (): string => {
  const config = useRuntimeConfig();
  return (config.public.apiBase as string).replace(/\/+$/, "");
};

export const useApiApp = (): string => {
  const config = useRuntimeConfig();
  return (config.public.apiApp as string).replace(/\/+$/, "");
};

/**
 * Construct full API URL
 */
export const getApiUrl = (endpoint: string): string => {
  const BASE = useApiBase();
  const clean = endpoint.replace(/^\/+/, "");
  const [path, query] = clean.split("?", 2);
  const normalizedPath = path.endsWith("/") ? path : `${path}/`;

  return query
    ? `${BASE}/${normalizedPath}?${query}`
    : `${BASE}/${normalizedPath}`;
};

/**
 * API Endpoints
 */
export const API_ENDPOINTS = {
  CARS: {
    LIST: 'cars/',
    DETAIL: (id: string) => `/cars/${id}/`,
    CREATE: '/cars/create/',
    UPDATE: (id: string) => `/cars/update/${id}/`,
    DELETE: (id: string) => `/cars/delete/${id}/`,
  },
  BOOKINGS: {
    LIST: 'bookings/',
    DETAIL: (id: string) => `/bookings/${id}/`,
    CREATE: '/bookings/create/',
    UPDATE: (id: string) => `/admin/bookings/update/${id}/`,
    DELETE: (id: string) => `/admin/bookings/delete/${id}/`,
  },
  REVIEWS: {
    LIST: '/reviews/',
    CAR: (carId: string) => `/cars/${carId}/reviews/`,
    CREATE: (carId: string) => `/reviews/cars/${carId}/create/`,
  },
  ADMIN_REVIEWS: {
    LIST: '/admin/reviews/',
    UPDATE_STATUS: (reviewId: number) => `/admin/reviews/${reviewId}/status/`,
    DELETE: (reviewId: number) => `/admin/reviews/${reviewId}/delete/`,
  }
}
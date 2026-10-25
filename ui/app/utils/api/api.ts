// API utility functions for Fabrics Plus Curtains

/**
 * Types
 */
export interface RatingBreakdown {
  star: number
  percent: number
}

export interface ReviewImage {
  url: string
  file?: File
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
  status: 'pending' | 'approved' | 'rejected'
  images: ReviewImage[]
  helpful_count: number
}

export interface ReviewForm {
    car: string
    rating: number
    review: string
    images: ReviewImage[]
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
  images: ReviewImage[]
  helpful_count: number
}

export interface AdminReviewsResponse {
    count: number
    next?: string | null
    previous?: string | null
    results: AdminReview[]
    stats: AdminReviewStats
}

export interface AdminReviewStats {
    total: number
    average_rating: number
    pending: number
    approved: number
}

export interface DashboardRevenuePoint {
    label: string
    value: number
}

export interface DashboardRevenueResponse {
    month: string
    label: string
    total: number
    previous_total: number
    percentage_change: number
    points: DashboardRevenuePoint[]
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

export interface CarReviewsResponse extends ReviewsResponse {
    my_review: Review1 | null
}

export interface Review1 {
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
  status: 'pending' | 'approved' | 'rejected'
  images: string[]
  helpful_count: number
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
    CREATE: '/admin/bookings/create/',
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

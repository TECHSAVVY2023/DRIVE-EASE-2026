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
  review_reference?: string
  car: string
  user: {
    id: number
    user_reference?: string
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
  review_reference: string

  car: {
      car_reference: string
      brand: string
      model: string
  }

  user: {
      id: number
      user_reference: string
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
  review_reference: string
  car: string
  user: {
      id: number
      user_reference: string
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

export type AdminNotificationType =
  | 'booking'
  | 'booking_status'
  | 'payment'
  | 'review'
  | 'reminder'
  | 'system'

export interface AdminNotification extends Notification {
  notification_type: AdminNotificationType
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
  const [path = "", query] = clean.split("?", 2);
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
    REFUND: (id: string) => `/admin/bookings/${id}/refund/`,
  },
  REVIEWS: {
    LIST: '/reviews/',
    CAR: (carId: string) => `/cars/${carId}/reviews/`,
    CREATE: (carId: string) => `/reviews/cars/${carId}/create/`,
  },
  ADMIN_REVIEWS: {
    LIST: '/admin/reviews/',
    UPDATE_STATUS: (reviewReference: string) => `/admin/reviews/${reviewReference}/status/`,
    DELETE: (reviewReference: string) => `/admin/reviews/${reviewReference}/delete/`,
  },
  ADMIN_NOTIFICATIONS: {
    LIST: '/admin/notifications/',
    UNREAD_COUNT: '/admin/notifications/unread-count/',
    READ_ALL: '/admin/notifications/read-all/',
    READ: (id: number) => `/admin/notifications/${id}/read/`,
    DELETE: (id: number) => `/admin/notifications/${id}/`,
  },
  HOME_CONTENT: {
    PUBLIC_HOME: '/content/home/',
    ADMIN_HOME: '/admin/content/home/',
    ADMIN_HOME_EDIT: '/admin/content/home/edit/',
    ADMIN_HOME_TRUST_ITEMS: '/admin/content/home/trust-items/',
    ADMIN_HOME_TRUST_ITEM_DETAIL: (id: string) => `/admin/content/home/trust-items/${id}/`,
    ADMIN_HOME_FEATURED_CARS: '/admin/content/home/featured-cars/',
    ADMIN_HOME_FEATURED_CAR_DETAIL: (id: string) => `/admin/content/home/featured-cars/${id}/`,
  },
  ABOUT_US_CONTENT: {
    PUBLIC_ABOUT_US: '/content/about/',
    ADMIN_ABOUT_US_EDIT: '/admin/content/about/edit/',
    ADMIN_TEAM_USERS: '/admin/content/about/team-users/',
  },
  CONTACT_CONTENT: {
    PUBLIC_CONTACT: '/content/contact/',
    ADMIN_CONTACT_EDIT: '/admin/content/contact/edit/',
  },
}

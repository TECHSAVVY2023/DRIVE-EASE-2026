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
  date_created: string
  id_images: {
    images: string[]
  }
}

export interface Car {
  car_id: string
  brand: string
  model: string
  year: number
  car_type: string
  price_per_day: string
  transmission: string
  engine: string
  fuel_type: string
  seats: number
  features: string[]
  note: string | null
  png_image: string | null
  status: string
  approval_status: string
  created_at: string
  created_by: number
  updated_at: string
  meta: {
    primary_image: string | null
    images: string[]
  }
  unavailable_periods: UnavailablePeriod[]
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
    categories: FilterOption[]
    transmissions: FilterOption[]
    seats: FilterOption[]
  }
}

export interface Transaction {
  booking_reference: string
  status: string

  pickup_date: string
  return_date: string

  daily_rate: number
  number_of_days: number
  subtotal: number
  discount: number
  total_price: number

  created_at: string

  payment_method: string

  car: {
      car_id: string
      brand: string
      model: string
      image: string
  }
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
 * Cache config
 */
let carsCache: Car[] | null = null;
let carsCacheExpiresAt = 0;
let carsRequest: Promise<Car[]> | null = null;
const CARS_CACHE_TTL_MS = 60 * 1000;

let carCache = new Map<string, Car>()
let carCacheExpiresAt = new Map<string, number>()
let carRequests = new Map<string, Promise<Car>>()
const CAR_CACHE_TTL_MS = 60 * 1000

const reviewsCache: Record<string, CarReviewsResponse> = {}
const reviewsCacheExpiresAt: Record<string, number> = {}
const reviewsRequests = new Map<string, Promise<CarReviewsResponse>>()
const REVIEWS_CACHE_TTL_MS = 60 * 1000

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
    DETAIL: (id: string) => `cars/${id}/`,
    CREATE: 'cars/create/',
    UPDATE: (id: string) => `cars/${id}/update/`,
    DELETE: (id: string) => `cars/${id}/delete/`,
  },
  REVIEWS: {
    LIST: '/reviews/',
    CAR: (carId: string) => `/cars/${carId}/reviews/`,
    CREATE: (carId: string) => `/reviews/cars/${carId}/create/`,
  }
}

/**
 * Fetch all cars
 */
export const fetchCars = async (
  { force = false }: { force?: boolean } = {}
): Promise<Car[]> => {
  const now = Date.now();

  //if this condition is true, return the cached car so the system doesn't have to make request again
  //if this condition is false, proceed to fetch the car so that the data will be updated
  if (!force && carsCache && now < carsCacheExpiresAt) {
    return carsCache;
  }

  if (!force && carsRequest) {
    return carsRequest;
  }

  carsRequest = $fetch<Car[]>(
    getApiUrl(API_ENDPOINTS.CARS.LIST)
  )
    .then((cars) => {
      carsCache = cars;
      carsCacheExpiresAt = Date.now() + CARS_CACHE_TTL_MS;
      return cars;
    })
    .finally(() => {
      carsRequest = null;
    });

  return carsRequest;
};

/**
 * Get primary image for a car
 */

/**
 * Fetch single car
 */
export const fetchCar = async (
  carId: string,
  { force = false }: { force?: boolean } = {}
): Promise<Car> => {
  const now = Date.now()

  // 1. Cache check
  const cached = carCache.get(carId)
  const expiresAt = carCacheExpiresAt.get(carId)

  //if this condition is true, return the cached car so the system doesn't have to make request again
  //if this condition is false, proceed to fetch the car so that the data will be updated
  if (!force && cached && expiresAt && now < expiresAt) {
    return cached
  }

  // prevents the same request from being being made again and returns an ongoing Promise, 
  // which is the first request, for other components that need the same data
  const existingRequest = carRequests.get(carId)
  if (!force && existingRequest) {
    return existingRequest
  }

  // 3. Fetch
  const request = $fetch<Car>(
    getApiUrl(API_ENDPOINTS.CARS.DETAIL(carId))
  )
    .then((car) => {
      carCache.set(carId, car)
      carCacheExpiresAt.set(carId, Date.now() + CAR_CACHE_TTL_MS)
      return car
    })
    .finally(() => {
      carRequests.delete(carId)
    })

  carRequests.set(carId, request)

  return request
}
// API utility functions for Fabrics Plus Curtains

/**
 * Types
 */

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
    UPDATE: (id: string) => `api/driveease/cars/${id}/update/`,
    DELETE: (id: string) => `api/driveease/cars/${id}/delete/`,
  }
}

/**
 * Fetch all cars
 */
export const fetchCars = async (
  { force = false }: { force?: boolean } = {}
): Promise<Car[]> => {
  const now = Date.now();

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

  if (!force && cached && expiresAt && now < expiresAt) {
    return cached
  }

  // 2. Deduplicate request
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
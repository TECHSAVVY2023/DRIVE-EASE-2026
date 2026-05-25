// API utility functions for Fabrics Plus Curtains

/**
 * Types
 */
export interface CMSPost {
  id: number;
  title?: string;
  content?: string;
  created_at?: string;
  updated_at?: string;
  [key: string]: unknown;
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

/**
 * Base URL for S3 assets
 */
export const BASE_ASSETS_URL =
  "https://fpstorage.sgp1.cdn.digitaloceanspaces.com/fabricsplus";

/**
 * Cache config
 */
const CMS_POSTS_CACHE_TTL_MS = 60 * 1000;

let cmsPostsCache: CMSPost[] | null = null;
let cmsPostsCacheExpiresAt = 0;
let cmsPostsRequest: Promise<CMSPost[]> | null = null;

/**
 * Normalize CMS response
 */
const normalizeCMSPostsResponse = (response: unknown): CMSPost[] => {
  if (Array.isArray(response)) {
    return response as CMSPost[];
  }

  if (
    typeof response === "object" &&
    response !== null &&
    "results" in response &&
    Array.isArray((response as any).results)
  ) {
    return (response as { results: CMSPost[] }).results;
  }

  if (
    typeof response === "object" &&
    response !== null &&
    "data" in response &&
    Array.isArray((response as any).data)
  ) {
    return (response as { data: CMSPost[] }).data;
  }

  return [];
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
  CMS: {
    LIST: "cms/list/",
    DETAIL: (id: number) => `cms/${id}/`,
    CREATE: "cms/create/",
    EDIT: (id: number) => `cms/edit/${id}/`,
    DELETE: (id: number) => `cms/delete/${id}/`,
  },
  UPLOAD: "cms/upload/",
} as const;

/**
 * Clear cache
 */
export const clearCMSPostsCache = (): void => {
  cmsPostsCache = null;
  cmsPostsCacheExpiresAt = 0;
  cmsPostsRequest = null;
};

/**
 * Upload files
 */
export const uploadFiles = async (
  files: File[]
): Promise<UploadResponse> => {
  const formData = new FormData();

  files.forEach((file) => {
    formData.append("file", file);
  });

  const uploadUrl = getApiUrl(API_ENDPOINTS.UPLOAD);

  try {
    const response = await $fetch<UploadResponse>(uploadUrl, {
      method: "POST",
      body: formData,
    });

    return response;
  } catch (error) {
    console.error("❌ File upload error:", error);
    throw error;
  }
};

/**
 * Fetch all CMS posts
 */
export const fetchCMSPosts = async (
  { force = false }: { force?: boolean } = {}
): Promise<CMSPost[]> => {
  const now = Date.now();

  if (!force && cmsPostsCache && now < cmsPostsCacheExpiresAt) {
    return cmsPostsCache;
  }

  if (!force && cmsPostsRequest) {
    return cmsPostsRequest;
  }

  cmsPostsRequest = $fetch<unknown>(
    getApiUrl(API_ENDPOINTS.CMS.LIST)
  )
    .then((response) => {
      const normalized = normalizeCMSPostsResponse(response);
      cmsPostsCache = normalized;
      cmsPostsCacheExpiresAt = Date.now() + CMS_POSTS_CACHE_TTL_MS;
      return normalized;
    })
    .finally(() => {
      cmsPostsRequest = null;
    });

  return cmsPostsRequest;
};

/**
 * Fetch single CMS post
 */
export const fetchCMSPost = async (
  id: number
): Promise<CMSPost> => {
  try {
    return await $fetch<CMSPost>(
      getApiUrl(API_ENDPOINTS.CMS.DETAIL(id))
    );
  } catch (error) {
    console.error(`Error fetching CMS post ${id}:`, error);
    throw error;
  }
};

/**
 * Create CMS post
 */
export const createCMSPost = async (
  data: Partial<CMSPost>
): Promise<CMSPost> => {
  try {
    return await $fetch<CMSPost>(
      getApiUrl(API_ENDPOINTS.CMS.CREATE),
      {
        method: "POST",
        body: data, // Nuxt $fetch auto JSON
      }
    );
  } catch (error) {
    console.error("Error creating CMS post:", error);
    throw error;
  }
};

/**
 * Update CMS post
 */
export const updateCMSPost = async (
  id: number,
  data: Partial<CMSPost>
): Promise<CMSPost> => {
  try {
    return await $fetch<CMSPost>(
      getApiUrl(API_ENDPOINTS.CMS.EDIT(id)),
      {
        method: "PUT",
        body: data,
      }
    );
  } catch (error) {
    console.error(`Error updating CMS post ${id}:`, error);
    throw error;
  }
};

/**
 * Delete CMS post
 */
export const deleteCMSPost = async (
  id: number
): Promise<DeleteResponse> => {
  try {
    return await $fetch<DeleteResponse>(
      getApiUrl(API_ENDPOINTS.CMS.DELETE(id)),
      {
        method: "DELETE",
      }
    );
  } catch (error) {
    console.error(`Error deleting CMS post ${id}:`, error);
    throw error;
  }
};
import type {
    HomepageContent,
    HomepageContentUpdatePayload,
} from "~/utils/types/content";
import { API_ENDPOINTS } from "~/utils/api/api";

let contentCache = new Map<string, HomepageContent>()
let contentCacheExpiresAt = new Map<string, number>()
let contentRequests = new Map<string, Promise<HomepageContent>>()
const CONTENT_CACHE_TTL_MS = 60 * 1000

export const useHomepageContent = () => {
    const { apiFetch } = useApiFetch()
    
    const fetchHomepageContent = async ({force = false}: {force?: boolean} = {}): Promise<HomepageContent> => {
        const now = Date.now()

        const cached = contentCache.get("homepage")
        const expiresAt = contentCacheExpiresAt.get("homepage")

        if (!force && cached && expiresAt && now < expiresAt) {
            return cached
        }

        const existingRequest = contentRequests.get("homepage")
        if (!force && existingRequest) {
            return existingRequest
        }

        const request = apiFetch<HomepageContent>(
            API_ENDPOINTS.HOME_CONTENT.PUBLIC_HOME
        )
            .then((content) => {
            contentCache.set("homepage", content)
            contentCacheExpiresAt.set("homepage", Date.now() + CONTENT_CACHE_TTL_MS)
            return content
            })
            .finally(() => {
            contentRequests.delete("homepage")
            })

        contentRequests.set("homepage", request)

        return request
    }

    const updateHomepageContent = async (
        form: HomepageContentUpdatePayload
    ): Promise<HomepageContent> => {
        const response = await apiFetch<HomepageContent>(
            API_ENDPOINTS.HOME_CONTENT.ADMIN_HOME_EDIT,
            {
                method: 'PATCH',
                body: form,
            }
        )

        // Update cache
        contentCache.set('homepage', response)
        contentCacheExpiresAt.set(
            'homepage',
            Date.now() + CONTENT_CACHE_TTL_MS
        )

        return response
    }
    
    return {
        fetchHomepageContent,
        updateHomepageContent,
    }
}

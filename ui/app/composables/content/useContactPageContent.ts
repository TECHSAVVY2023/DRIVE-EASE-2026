import type { ContactPageContent, ContactPageUpdatePayload } from '~/utils/types/content'
import { API_ENDPOINTS } from '~/utils/api/api'

let contentCache: ContactPageContent | null = null
let contentCacheExpiresAt = 0
let contentRequest: Promise<ContactPageContent> | null = null
const CONTENT_CACHE_TTL_MS = 60 * 1000

export const useContactPageContent = () => {
    const { apiFetch } = useApiFetch()

    const fetchContactPageContent = async (
        { force = false }: { force?: boolean } = {}
    ): Promise<ContactPageContent> => {
        if (!force && contentCache && Date.now() < contentCacheExpiresAt) return contentCache
        if (!force && contentRequest) return contentRequest

        contentRequest = apiFetch<ContactPageContent>(
            API_ENDPOINTS.CONTACT_CONTENT.PUBLIC_CONTACT
        ).then((content) => {
            contentCache = content
            contentCacheExpiresAt = Date.now() + CONTENT_CACHE_TTL_MS
            return content
        }).finally(() => {
            contentRequest = null
        })
        return contentRequest
    }

    const updateContactPageContent = async (
        body: ContactPageUpdatePayload
    ): Promise<ContactPageContent> => {
        const response = await apiFetch<ContactPageContent>(
            API_ENDPOINTS.CONTACT_CONTENT.ADMIN_CONTACT_EDIT,
            { method: 'PATCH', body }
        )
        contentCache = response
        contentCacheExpiresAt = Date.now() + CONTENT_CACHE_TTL_MS
        return response
    }

    return { fetchContactPageContent, updateContactPageContent }
}

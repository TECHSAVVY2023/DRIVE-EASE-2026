import type {
    AboutUsPageContent,
    AboutUsPageUpdatePayload,
    AboutTeamUserOption,
} from '~/utils/types/content'
import { API_ENDPOINTS } from '~/utils/api/api'

let contentCache: AboutUsPageContent | null = null
let contentCacheExpiresAt = 0
let contentRequest: Promise<AboutUsPageContent> | null = null
const CONTENT_CACHE_TTL_MS = 60 * 1000

export const useAboutUsPageContent = () => {
    const { apiFetch } = useApiFetch()

    const fetchAboutUsPageContent = async (
        { force = false }: { force?: boolean } = {}
    ): Promise<AboutUsPageContent> => {
        if (!force && contentCache && Date.now() < contentCacheExpiresAt) {
            return contentCache
        }
        if (!force && contentRequest) return contentRequest

        contentRequest = apiFetch<AboutUsPageContent>(
            API_ENDPOINTS.ABOUT_US_CONTENT.PUBLIC_ABOUT_US
        ).then((content) => {
            contentCache = content
            contentCacheExpiresAt = Date.now() + CONTENT_CACHE_TTL_MS
            return content
        }).finally(() => {
            contentRequest = null
        })

        return contentRequest
    }

    const updateAboutUsPageContent = async (
        body: AboutUsPageUpdatePayload
    ): Promise<AboutUsPageContent> => {
        const response = await apiFetch<AboutUsPageContent>(
            API_ENDPOINTS.ABOUT_US_CONTENT.ADMIN_ABOUT_US_EDIT,
            { method: 'PATCH', body }
        )
        contentCache = response
        contentCacheExpiresAt = Date.now() + CONTENT_CACHE_TTL_MS
        return response
    }

    const fetchAboutTeamUsers = (): Promise<AboutTeamUserOption[]> =>
        apiFetch<AboutTeamUserOption[]>(
            API_ENDPOINTS.ABOUT_US_CONTENT.ADMIN_TEAM_USERS
        )

    return {
        fetchAboutUsPageContent,
        updateAboutUsPageContent,
        fetchAboutTeamUsers,
    }
}

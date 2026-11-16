import type { HomepageContent } from "~/utils/types/content"

export const useHomepageContentLoader = () => {
    const { fetchHomepageContent } = useHomepageContent()

    const home = useState<HomepageContent | null>(
        "homepage-content",
        () => null
    )

    const isLoading = useState(
        "homepage-content-loading",
        () => false
    )

    const error = useState<string | null>(
        "homepage-content-error",
        () => null
    )

    const loadHomepageContent = async (force = false) => {
        isLoading.value = true
        error.value = null

        try {
            home.value = await fetchHomepageContent({ force })
        } catch (err) {
            error.value = "Failed to load homepage content."
        } finally {
            isLoading.value = false
        }
    }

    return {
        home,
        isLoading,
        error,
        loadHomepageContent
    }
}
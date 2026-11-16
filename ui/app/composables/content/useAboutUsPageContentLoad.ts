import type { AboutUsPageContent } from "~/utils/types/content"

export const useAboutUsPageContentLoad = () => {
    const { fetchAboutUsPageContent } = useAboutUsPageContent()

    const about = useState<AboutUsPageContent | null>(
        "aboutus-content",
        () => null
    )

    const isLoading = useState(
        "aboutus-content-loading",
        () => false
    )

    const error = useState<string | null>(
        "aboutus-content-error",
        () => null
    )

    const loadAboutUsPageContent = async (force = false) => {
        isLoading.value = true
        error.value = null

        try {
            about.value = await fetchAboutUsPageContent({ force })
        } catch (err) {
            error.value = "Failed to load about us page content."
        } finally {
            isLoading.value = false
        }
    }

    return {
        about,
        isLoading,
        error,
        loadAboutUsPageContent
    }
}

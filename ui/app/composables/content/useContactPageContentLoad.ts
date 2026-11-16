import type { ContactPageContent } from '~/utils/types/content'

export const useContactPageContentLoad = () => {
    const { fetchContactPageContent } = useContactPageContent()
    const contact = useState<ContactPageContent | null>('contact-page-content', () => null)
    const isLoading = useState('contact-page-content-loading', () => false)
    const error = useState<string | null>('contact-page-content-error', () => null)

    const loadContactPageContent = async (force = false): Promise<void> => {
        isLoading.value = true
        error.value = null
        try {
            contact.value = await fetchContactPageContent({ force })
        } catch {
            error.value = 'Failed to load Contact page content.'
        } finally {
            isLoading.value = false
        }
    }

    return { contact, isLoading, error, loadContactPageContent }
}

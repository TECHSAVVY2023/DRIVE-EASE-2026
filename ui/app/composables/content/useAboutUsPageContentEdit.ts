import type { AboutUsPageContent, HomepageContentResult } from '~/utils/types/content'
import { uploadFile } from '~/utils/api/upload'

export const useAboutUsPageContentEdit = () => {
    const { updateAboutUsPageContent } = useAboutUsPageContent()
    const { $swal } = useNuxtApp()

    const handleUpdateAboutUsPageContent = async (
        form: AboutUsPageContent,
        newImageFile: File | null,
        originalImageUrl: string | null,
    ): Promise<HomepageContentResult> => {
        const requiredText = [
            form.wwr_heading,
            form.wwr_description,
            form.mission_heading,
            form.mission_description,
            form.vission_heading,
            form.vission_description,
            ...form.wwr_stats.flatMap(item => [item.stat, item.value]),
            ...form.journey.flatMap(item => [item.year, item.title, item.description]),
        ]
        const hasIncompleteTeamMember = form.team.some(item =>
            !item.user ||
            !item.position.trim() ||
            !item.description.trim()
        )

        if (
            requiredText.some(value => !String(value ?? '').trim()) ||
            hasIncompleteTeamMember
        ) {
            await $swal.fire({
                icon: 'warning', title: 'Incomplete Form',
                text: 'Please complete all required About page fields.',
                confirmButtonColor: '#C1121F', background: '#1a1a1a', color: '#ffffff',
            })
            return { success: false, message: 'Incomplete About page fields.' }
        }

        $swal.fire({
            title: 'Saving changes...', text: 'Please wait.',
            background: '#1a1a1a', color: '#ffffff', allowOutsideClick: false,
            allowEscapeKey: false, didOpen: () => $swal.showLoading(),
        })

        try {
            // The object URL in the form is only a local preview. Upload the
            // selected file first, then save the permanent cloud URL.
            const aboutImageUrl = newImageFile
                ? await uploadFile(newImageFile)
                : form.wwr_image

            await updateAboutUsPageContent({
                wwr_heading: form.wwr_heading.trim(),
                wwr_description: form.wwr_description.trim(),
                wwr_image: aboutImageUrl,
                // The API verifies ownership before deleting the old upload.
                deleted_image: newImageFile ? originalImageUrl : null,
                mission_heading: form.mission_heading.trim(),
                mission_description: form.mission_description.trim(),
                vission_heading: form.vission_heading.trim(),
                vission_description: form.vission_description.trim(),
                wwr_stats: form.wwr_stats.map((item, order) => ({ ...item, stat: item.stat.trim(), value: item.value.trim(), order })),
                team: form.team.map((item, order) => ({
                    id: item.id,
                    user: item.user,
                    position: item.position.trim(),
                    description: item.description.trim(),
                    order,
                })),
                journey: form.journey.map((item, order) => ({ ...item, year: item.year.trim(), title: item.title.trim(), description: item.description.trim(), order })),
            })
            await $swal.fire({ icon: 'success', title: 'Success', text: 'About page content updated successfully.', confirmButtonColor: '#C1121F', background: '#1a1a1a', color: '#ffffff' })
            return { success: true, message: 'About page content updated successfully.' }
        } catch (error) {
            console.error('Failed to update About page content:', error)
            await $swal.fire({ icon: 'error', title: 'Error', text: 'Failed to update About page content.', confirmButtonColor: '#C1121F', background: '#1a1a1a', color: '#ffffff' })
            return { success: false, message: 'Failed to update About page content.' }
        }
    }

    return { handleUpdateAboutUsPageContent }
}

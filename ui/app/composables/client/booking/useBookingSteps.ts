export function useBookingSteps(
    steps: { title: string; subtitle: string }[],
    currentStep: Ref<number>,
    validateStepOne: Function,
    validateStepTwo: Function
) {

    async function nextStep(
        form: any,
        existingIdImages: string[],
        uploadedIdFiles: File[]
    ) {
        if (currentStep.value === 1) {
            const valid = await validateStepOne(
                form,
                existingIdImages,
                uploadedIdFiles
            )

            if (!valid) return false
        }

        if (currentStep.value === 2) {
            const valid = await validateStepTwo(form)

            if (!valid) return false
        }

        if (currentStep.value < steps.length) {
            currentStep.value++
            return true
        }

        return false
    }

    // function previousStep() {
    //     if (currentStep.value > 1) {
    //         currentStep.value--
    //     }
    // }

    // function reset() {
    //     currentStep.value = 1
    // }

    return {
        nextStep,
        // previousStep,
        // reset
    }
}
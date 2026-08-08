export function useFiltersCar() {

    const {
        search,
        brand,
        transmission,
        seats,
        carType,
        sort,
        currentPage,
    } = useFleetList()

    const resetFilters = async () => {
        search.value = ""
    }

    return {
        search,
        resetFilters,
    }
}
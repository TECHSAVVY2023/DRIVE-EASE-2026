<template>
  <div class="flex items-center justify-center gap-2 mt-4">
    <!-- Prev -->
    <button
      @click="prevPage"
      :disabled="props.currentPage === 1"
      class="
        flex items-center gap-1
        rounded-lg border border-[#2a2a2a]
        px-3 py-1.5 text-xs text-[#7E7E7E]
        hover:border-white hover:text-white
        disabled:opacity-30 disabled:cursor-not-allowed
        transition-colors duration-200
      "
    >
      <svg
        class="w-3 h-3"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M15 19l-7-7 7-7"
        />
      </svg>

      Prev
    </button>

    <!-- Page Numbers -->
    <template v-for="p in props.totalPages" :key="p">
      <button
        @click="changePage(p)"
        class="w-8 h-8 rounded-lg text-xs font-semibold transition-colors duration-200"
        :class="
          props.currentPage === p
            ? 'bg-[#C1121F] text-white'
            : 'border border-[#2a2a2a] text-[#7E7E7E] hover:border-white hover:text-white'
        "
      >
        {{ p }}
      </button>
    </template>

    <!-- Next -->
    <button
      @click="nextPage"
      :disabled="props.currentPage === props.totalPages"
      class="
        flex items-center gap-1
        rounded-lg border border-[#2a2a2a]
        px-3 py-1.5 text-xs text-[#7E7E7E]
        hover:border-white hover:text-white
        disabled:opacity-30 disabled:cursor-not-allowed
        transition-colors duration-200
      "
    >
      Next

      <svg
        class="w-3 h-3"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M9 5l7 7-7 7"
        />
      </svg>
    </button>
  </div>
</template>

<script setup lang="ts">
interface Props {
  currentPage: number
  totalPages: number
}

const props = defineProps<Props>()

const emit = defineEmits<{
  (e: 'update:currentPage', value: number): void
}>()

const changePage = (page: number) => {
  emit('update:currentPage', page)
}

const nextPage = () => {
  if (props.currentPage < props.totalPages) {
    emit('update:currentPage', props.currentPage + 1)
  }
}

const prevPage = () => {
  if (props.currentPage > 1) {
    emit('update:currentPage', props.currentPage - 1)
  }
}
</script>
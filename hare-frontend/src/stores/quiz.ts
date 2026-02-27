import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'

export interface QuizAnswersPayload {
  hair_types: string[]
  concerns: string[]
  porosity: string
  goals: string[]
  scalp: string | null
}

export interface RecommendedProduct {
  id?: number
  name: string
  brand: string
  price: number
  image_url: string | null
  description: string
  tags: Record<string, unknown>
  score?: number
  explanation?: string
}

export interface QuizSubmitResult {
  recommended_products: RecommendedProduct[]
  total_matched: number
  message: string
}

const TOTAL_STEPS = 7

export const useQuizStore = defineStore('quiz', () => {
  const currentStep = ref(1)
  const answers = ref<QuizAnswersPayload>({
    hair_types: [],
    concerns: [],
    porosity: '',
    goals: [],
    scalp: 'normal',
  })
  const isLoading = ref(false)
  const error = ref<string | null>(null)
  const lastResult = ref<QuizSubmitResult | null>(null)

  const isFirstStep = computed(() => currentStep.value === 1)
  const isLastStep = computed(() => currentStep.value === TOTAL_STEPS)
  const progressPercent = computed(() => (currentStep.value / TOTAL_STEPS) * 100)

  function setAnswer<K extends keyof QuizAnswersPayload>(key: K, value: QuizAnswersPayload[K]) {
    answers.value[key] = value
  }

  function nextStep() {
    if (currentStep.value < TOTAL_STEPS) currentStep.value++
  }

  function prevStep() {
    if (currentStep.value > 1) currentStep.value--
  }

  async function submitQuiz(): Promise<boolean> {
    error.value = null
    isLoading.value = true
    try {
      const { data } = await axios.post<QuizSubmitResult>('/api/v1/quiz/submit', {
        hair_types: answers.value.hair_types,
        concerns: answers.value.concerns,
        porosity: answers.value.porosity,
        goals: answers.value.goals,
        scalp: answers.value.scalp || null,
      })
      lastResult.value = data
      return true
    } catch (e: unknown) {
      error.value = axios.isAxiosError(e) && e.response?.data?.detail
        ? String(e.response.data.detail)
        : 'Erreur lors de l\'envoi du quiz.'
      return false
    } finally {
      isLoading.value = false
    }
  }

  async function downloadReportPDF(): Promise<void> {
    const products = lastResult.value?.recommended_products
    if (!products?.length) return
    try {
      const { data } = await axios.post(
        '/api/v1/quiz/export-report',
        {
          recommended_products: products,
          answers: answers.value,
        },
        { responseType: 'blob' }
      )
      const url = URL.createObjectURL(data)
      const a = document.createElement('a')
      a.href = url
      a.download = 'Rapport_HARE_Pro.pdf'
      a.click()
      URL.revokeObjectURL(url)
    } catch {
      error.value = 'Erreur téléchargement PDF'
    }
  }

  function reset() {
    currentStep.value = 1
    answers.value = { hair_types: [], concerns: [], porosity: '', goals: [], scalp: 'normal' }
    error.value = null
    lastResult.value = null
  }

  return {
    currentStep,
    answers,
    isLoading,
    error,
    lastResult,
    isFirstStep,
    isLastStep,
    progressPercent,
    setAnswer,
    nextStep,
    prevStep,
    submitQuiz,
    downloadReportPDF,
    reset,
    TOTAL_STEPS,
  }
})

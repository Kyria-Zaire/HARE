import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useAuthStore } from './auth'

export interface AdminStats {
  total_products: number
  total_leads: number
  quizzes_today: number
}

export interface Lead {
  id: number
  email: string
  quiz_profile: Record<string, unknown>
  source?: string
  created_at?: string
}

export interface ProductRow {
  id: number
  name: string
  brand: string
  price: number
  category: string
  description: string
  image_url: string | null
  is_active: boolean
}

export interface ChatbotQuestionRow {
  id: number
  question: string
  created_at?: string
}

const PER_PAGE = 10

export const useAdminStore = defineStore('admin', () => {
  const stats = ref<AdminStats | null>(null)
  const leads = ref<Lead[]>([])
  const productsPaginated = ref<ProductRow[]>([])
  const productsTotal = ref(0)
  const productsPage = ref(1)
  const productsQuery = ref('')
  const leadsQuery = ref('')
  const leadsDateFrom = ref('')
  const leadsDateTo = ref('')
  const chatbotQuestions = ref<ChatbotQuestionRow[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  const auth = useAuthStore()

  const productsTotalPages = computed(() => Math.ceil(productsTotal.value / PER_PAGE) || 1)

  function api() {
    return auth.authAxios()
  }

  async function fetchStats() {
    loading.value = true
    error.value = null
    try {
      const { data } = await api().get<AdminStats>('/api/v1/admin/stats')
      stats.value = data
    } catch {
      error.value = 'Erreur chargement stats'
    } finally {
      loading.value = false
    }
  }

  async function fetchProducts(page: number = 1, search?: string) {
    loading.value = true
    error.value = null
    try {
      const params: { page: number; per_page: number; q?: string } = { page, per_page: PER_PAGE }
      if (search !== undefined) params.q = search
      else if (productsQuery.value) params.q = productsQuery.value
      const { data } = await api().get<{ items: ProductRow[]; total: number; page: number; per_page: number }>(
        '/api/v1/admin/products',
        { params }
      )
      productsPaginated.value = data.items
      productsTotal.value = data.total
      productsPage.value = data.page
    } catch {
      error.value = 'Erreur chargement produits'
    } finally {
      loading.value = false
    }
  }

  async function fetchLeads(filters?: { q?: string; date_from?: string; date_to?: string }) {
    loading.value = true
    error.value = null
    try {
      const params: Record<string, string> = {}
      if (filters?.q !== undefined) params.q = filters.q
      else if (leadsQuery.value) params.q = leadsQuery.value
      if (filters?.date_from !== undefined) params.date_from = filters.date_from
      else if (leadsDateFrom.value) params.date_from = leadsDateFrom.value
      if (filters?.date_to !== undefined) params.date_to = filters.date_to
      else if (leadsDateTo.value) params.date_to = leadsDateTo.value
      const { data } = await api().get<Lead[]>('/api/v1/admin/leads', { params })
      leads.value = data
    } catch {
      error.value = 'Erreur chargement leads'
    } finally {
      loading.value = false
    }
  }

  async function seedDefaultAdmin(): Promise<{ ok: boolean; message?: string }> {
    try {
      const axios = (await import('axios')).default
      const { data } = await axios.post<{ ok: boolean; message: string }>('/api/v1/admin/seed-default-admin')
      return { ok: data.ok, message: data.message }
    } catch (err: unknown) {
      const msg = err && typeof err === 'object' && 'response' in err
        ? (err as { response?: { data?: { detail?: string } } }).response?.data?.detail
        : 'Erreur'
      return { ok: false, message: typeof msg === 'string' ? msg : 'Erreur' }
    }
  }

  async function fetchChatbotQuestions() {
    try {
      const { data } = await api().get<ChatbotQuestionRow[]>('/api/v1/admin/chatbot-questions')
      chatbotQuestions.value = data
    } catch {
      chatbotQuestions.value = []
    }
  }

  async function importCsv(file: File): Promise<{ ok: boolean; imported?: number; error?: string }> {
    const form = new FormData()
    form.append('file', file)
    try {
      const { data } = await api().post<{ ok: boolean; imported: number }>('/api/v1/admin/products/import', form)
      return { ok: data.ok, imported: data.imported }
    } catch (err: unknown) {
      const msg = err && typeof err === 'object' && 'response' in err
        ? (err as { response?: { data?: { detail?: string } } }).response?.data?.detail
        : 'Erreur import'
      return { ok: false, error: typeof msg === 'string' ? msg : 'Erreur import' }
    }
  }

  async function seedDemoData(): Promise<{ ok: boolean; message?: string; products_created?: number }> {
    try {
      const { data } = await api().post<{ ok: boolean; message: string; products_created: number }>('/api/v1/admin/seed-demo-data')
      return { ok: data.ok, message: data.message, products_created: data.products_created }
    } catch (err: unknown) {
      const msg = err && typeof err === 'object' && 'response' in err
        ? (err as { response?: { data?: { detail?: string } } }).response?.data?.detail
        : 'Erreur'
      return { ok: false, message: typeof msg === 'string' ? msg : 'Erreur' }
    }
  }

  return {
    stats,
    leads,
    productsPaginated,
    productsTotal,
    productsPage,
    productsQuery,
    leadsQuery,
    leadsDateFrom,
    leadsDateTo,
    chatbotQuestions,
    productsTotalPages,
    loading,
    error,
    fetchStats,
    fetchProducts,
    fetchLeads,
    seedDefaultAdmin,
    fetchChatbotQuestions,
    importCsv,
    seedDemoData,
    api,
  }
})

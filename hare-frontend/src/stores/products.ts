import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'

export interface Product {
  id: number
  name: string
  brand: string
  price: number
  category: string
  description: string
  image_url: string | null
  tags: Record<string, unknown>
  stock?: number
  sku?: string
  is_active: boolean
}

export const useProductsStore = defineStore('products', () => {
  const list = ref<Product[]>([])
  const loading = ref(false)

  async function fetchProducts() {
    loading.value = true
    try {
      const { data } = await axios.get<Product[]>('/api/v1/products')
      list.value = data
    } finally {
      loading.value = false
    }
  }

  return { list, loading, fetchProducts }
})

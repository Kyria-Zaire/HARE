import axios from 'axios'

/**
 * Client API de base (base URL depuis env en prod).
 */
export function useApi() {
  const baseURL = import.meta.env.VITE_API_BASE_URL ?? ''
  return axios.create({
    baseURL,
    headers: { 'Content-Type': 'application/json' },
  })
}

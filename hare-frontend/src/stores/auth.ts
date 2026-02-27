import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'

const TOKEN_KEY = 'hare_pro_admin_token'
const MUST_CHANGE_KEY = 'hare_pro_must_change'

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(localStorage.getItem(TOKEN_KEY))
  const mustChangePassword = ref(localStorage.getItem(MUST_CHANGE_KEY) === 'true')

  const isAuthenticated = computed(() => !!token.value)

  function setToken(t: string | null) {
    token.value = t
    if (t) localStorage.setItem(TOKEN_KEY, t)
    else localStorage.removeItem(TOKEN_KEY)
  }

  function setMustChangePassword(value: boolean) {
    mustChangePassword.value = value
    if (value) localStorage.setItem(MUST_CHANGE_KEY, 'true')
    else localStorage.removeItem(MUST_CHANGE_KEY)
  }

  async function login(username: string, password: string): Promise<boolean> {
    try {
      const { data } = await axios.post<{ access_token: string; must_change_password?: boolean }>('/api/v1/admin/login', {
        username,
        password,
      })
      setToken(data.access_token)
      setMustChangePassword(!!data.must_change_password)
      return true
    } catch {
      return false
    }
  }

  async function changePassword(newPassword: string): Promise<boolean> {
    try {
      await authAxios().post('/api/v1/admin/change-password', { new_password: newPassword })
      setMustChangePassword(false)
      return true
    } catch {
      return false
    }
  }

  function logout() {
    setToken(null)
    setMustChangePassword(false)
  }

  function authAxios() {
    const instance = axios.create({
      headers: token.value ? { Authorization: `Bearer ${token.value}` } : {},
    })
    instance.interceptors.response.use(
      (r: import('axios').AxiosResponse) => r,
      (err: import('axios').AxiosError) => {
        if (err.response?.status === 401) {
          setToken(null)
          setMustChangePassword(false)
        }
        return Promise.reject(err)
      }
    )
    return instance
  }

  return {
    token,
    mustChangePassword,
    isAuthenticated,
    setToken,
    setMustChangePassword,
    login,
    changePassword,
    logout,
    authAxios,
  }
})

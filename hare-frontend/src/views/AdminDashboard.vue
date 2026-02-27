<template>
  <div class="flex min-h-[calc(100vh-4rem)] bg-background">
    <!-- Toasts -->
    <Transition name="toast">
      <div
        v-if="toast.text"
        class="fixed right-4 top-20 z-50 max-w-sm rounded-xl px-4 py-3 shadow-lg"
        :class="toast.type === 'success' ? 'bg-green-700 text-white' : 'bg-primary text-text-inverse'"
        role="alert"
      >
        {{ toast.text }}
      </div>
    </Transition>

    <!-- Modal confirmation -->
    <Teleport to="body">
      <Transition name="modal">
        <div
          v-if="confirmOpen"
          class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4"
          @click.self="confirmResolve(false)"
        >
          <div class="w-full max-w-md rounded-2xl bg-white p-6 shadow-xl">
            <h3 class="font-serif text-lg font-bold text-primary">{{ confirmTitle }}</h3>
            <p class="mt-2 text-secondary">{{ confirmMessage }}</p>
            <div class="mt-6 flex justify-end gap-3">
              <button
                type="button"
                class="rounded-xl border-2 border-primary/30 px-4 py-2 text-primary hover:bg-primary/10"
                @click="confirmResolve(false)"
              >
                Annuler
              </button>
              <button
                type="button"
                class="rounded-xl bg-primary px-4 py-2 text-text-inverse hover:bg-bordeaux-dark"
                @click="confirmResolve(true)"
              >
                {{ confirmConfirmLabel }}
              </button>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>

    <!-- Sidebar fixe luxe bordeaux -->
    <aside
      v-if="auth.isAuthenticated"
      class="fixed left-0 top-16 z-30 flex h-[calc(100vh-4rem)] w-64 flex-col border-r-2 border-primary/20 bg-primary/5 shadow-xl max-md:w-20"
    >
      <nav class="flex flex-col gap-1 p-4">
        <p class="px-3 py-2 font-serif text-xs font-bold uppercase tracking-widest text-primary max-md:hidden">Admin</p>
        <button
          type="button"
          class="rounded-xl px-4 py-3 text-left font-medium text-secondary transition hover:bg-primary/10 hover:text-primary max-md:px-2 max-md:text-center"
          @click="auth.logout()"
        >
          <span class="max-md:hidden">Déconnexion</span>
          <span class="hidden max-md:inline">Out</span>
        </button>
      </nav>
    </aside>

    <div class="flex-1 pl-64 max-md:pl-20">
      <div class="p-4 md:p-8">
        <h1 class="font-serif text-2xl font-bold text-primary md:text-3xl">Dashboard Admin</h1>

        <!-- Écran : Changer mot de passe obligatoire -->
        <template v-if="auth.isAuthenticated && auth.mustChangePassword">
          <div class="mt-8 max-w-md rounded-2xl border-2 border-primary/20 bg-white p-8 shadow-lg">
            <h2 class="font-serif text-xl font-bold text-primary">Changer votre mot de passe</h2>
            <p class="mt-2 text-sm text-secondary">Pour des raisons de sécurité, vous devez définir un nouveau mot de passe.</p>
            <form class="mt-6" @submit.prevent="onChangePassword">
              <label class="block font-medium text-secondary">Nouveau mot de passe (min. 8 caractères)</label>
              <input
                v-model="newPassword"
                type="password"
                required
                minlength="8"
                class="mt-2 w-full rounded-xl border-2 border-primary/20 bg-cream-light px-4 py-3 focus:border-accent focus:outline-none focus:ring-2 focus:ring-accent/30"
                placeholder="••••••••"
              />
              <label class="mt-4 block font-medium text-secondary">Confirmer le mot de passe</label>
              <input
                v-model="newPasswordConfirm"
                type="password"
                required
                minlength="8"
                class="mt-2 w-full rounded-xl border-2 border-primary/20 bg-cream-light px-4 py-3 focus:border-accent focus:outline-none focus:ring-2 focus:ring-accent/30"
                placeholder="••••••••"
              />
              <p v-if="changePasswordError" class="mt-2 text-sm font-medium text-primary">Les mots de passe ne correspondent pas ou sont trop courts.</p>
              <button
                type="submit"
                class="mt-6 w-full rounded-xl bg-primary py-3 font-semibold text-text-inverse shadow transition hover:scale-[1.01] hover:bg-bordeaux-dark disabled:opacity-50"
                :disabled="changingPassword || newPassword.length < 8 || newPassword !== newPasswordConfirm"
              >
                {{ changingPassword ? 'Enregistrement…' : 'Enregistrer le nouveau mot de passe' }}
              </button>
            </form>
          </div>
        </template>

        <template v-else-if="!auth.isAuthenticated">
          <form
            class="mt-12 max-w-md rounded-2xl border-2 border-primary/20 bg-white p-8 shadow-lg transition hover:shadow-xl"
            @submit.prevent="onLogin"
          >
            <label class="block font-medium text-secondary">Email / Identifiant</label>
            <input
              v-model="username"
              type="text"
              placeholder="admin"
              required
              class="mt-2 w-full rounded-xl border-2 border-primary/20 bg-cream-light px-4 py-3 focus:border-accent focus:outline-none focus:ring-2 focus:ring-accent/30"
            />
            <label class="mt-4 block font-medium text-secondary">Mot de passe</label>
            <input
              v-model="password"
              type="password"
              placeholder="••••••••"
              required
              class="mt-2 w-full rounded-xl border-2 border-primary/20 bg-cream-light px-4 py-3 focus:border-accent focus:outline-none focus:ring-2 focus:ring-accent/30"
            />
            <button
              type="submit"
              class="mt-6 w-full rounded-xl bg-primary py-3 font-semibold text-text-inverse shadow transition hover:scale-[1.01] hover:bg-bordeaux-dark"
            >
              Connexion
            </button>
            <p v-if="loginError" class="mt-4 text-sm font-medium text-primary">Identifiants incorrects</p>
            <div class="mt-6 border-t border-primary/20 pt-4">
              <p class="text-sm text-secondary">Premier lancement ?</p>
              <button
                type="button"
                class="mt-2 rounded-lg border-2 border-accent/50 bg-accent/10 px-4 py-2 text-sm font-medium text-secondary hover:bg-accent/20"
                :disabled="seeding"
                @click="onSeedAdmin"
              >
                {{ seeding ? 'Création…' : 'Générer un admin par défaut' }}
              </button>
              <p v-if="seedMessage" class="mt-2 text-xs" :class="seedOk ? 'text-green-700' : 'text-primary'">{{ seedMessage }}</p>
            </div>
          </form>
        </template>

        <template v-else>
          <!-- Stats cards -->
          <div class="mt-8 grid gap-4 sm:gap-6 md:grid-cols-3">
            <div class="rounded-2xl border-2 border-primary/20 bg-white p-4 shadow-md transition hover:scale-[1.02] hover:shadow-lg md:p-6">
              <p class="text-sm font-medium uppercase tracking-wide text-secondary">Quiz aujourd'hui</p>
              <p v-if="admin.loading && !admin.stats" class="mt-2 h-9 w-16 animate-pulse rounded bg-primary/20" />
              <p v-else class="mt-2 font-serif text-2xl font-bold text-primary md:text-3xl">{{ admin.stats?.quizzes_today ?? '—' }}</p>
            </div>
            <div class="rounded-2xl border-2 border-primary/20 bg-white p-4 shadow-md transition hover:scale-[1.02] hover:shadow-lg md:p-6">
              <p class="text-sm font-medium uppercase tracking-wide text-secondary">Leads newsletter</p>
              <p v-if="admin.loading && !admin.stats" class="mt-2 h-9 w-16 animate-pulse rounded bg-primary/20" />
              <p v-else class="mt-2 font-serif text-2xl font-bold text-primary md:text-3xl">{{ admin.stats?.total_leads ?? '—' }}</p>
            </div>
            <div class="rounded-2xl border-2 border-primary/20 bg-white p-4 shadow-md transition hover:scale-[1.02] hover:shadow-lg md:p-6">
              <p class="text-sm font-medium uppercase tracking-wide text-secondary">Produits</p>
              <p v-if="admin.loading && !admin.stats" class="mt-2 h-9 w-16 animate-pulse rounded bg-primary/20" />
              <p v-else class="mt-2 font-serif text-2xl font-bold text-primary md:text-3xl">{{ admin.stats?.total_products ?? '—' }}</p>
            </div>
          </div>

          <!-- Données de démo + Modèle CSV -->
          <section class="mt-8 flex flex-wrap items-center gap-4">
            <button
              type="button"
              class="rounded-xl bg-primary px-4 py-2 text-text-inverse transition hover:bg-bordeaux-dark disabled:opacity-50"
              :disabled="seedLoading"
              @click="openConfirmSeed"
            >
              <span v-if="seedLoading" class="inline-block h-4 w-4 animate-spin rounded-full border-2 border-text-inverse border-t-transparent" />
              <span v-else>Charger données de démo</span>
            </button>
            <a
              href="/export-template.csv"
              download="export-template.csv"
              class="inline-flex items-center rounded-xl border-2 border-primary/30 px-4 py-2 text-primary transition hover:bg-primary/10"
            >
              Télécharger modèle CSV
            </a>
          </section>

          <!-- Import CSV -->
          <section class="mt-12">
            <h2 class="font-serif text-xl font-bold text-primary">Importer CSV produits</h2>
            <div
              class="mt-4 rounded-2xl border-2 border-dashed transition"
              :class="isDragging ? 'border-accent bg-accent/10' : 'border-primary/30 bg-cream-light'"
              @dragover.prevent="isDragging = true"
              @dragleave.prevent="isDragging = false"
              @drop.prevent="onDrop"
            >
              <input ref="fileInput" type="file" accept=".csv" class="hidden" @change="onFileSelect" />
              <div class="p-8 text-center">
                <p class="text-secondary">Glissez un fichier CSV ici ou</p>
                <button
                  type="button"
                  class="mt-2 rounded-xl bg-accent px-6 py-2 font-medium text-secondary shadow transition hover:bg-gold-light"
                  @click="fileInput?.click()"
                >
                  Choisir un fichier
                </button>
              </div>
            </div>
            <p v-if="importMessage" class="mt-2 text-sm font-medium" :class="importSuccess ? 'text-green-700' : 'text-primary'">{{ importMessage }}</p>
          </section>

          <!-- Produits : recherche + tableau -->
          <section class="mt-12">
            <h2 class="font-serif text-xl font-bold text-primary">Produits ({{ admin.productsTotal }})</h2>
            <div class="mt-4 flex flex-wrap items-center gap-4">
              <input
                v-model="admin.productsQuery"
                type="search"
                placeholder="Rechercher (nom, marque)..."
                class="rounded-xl border-2 border-primary/20 bg-white px-4 py-2 focus:border-accent focus:outline-none"
                @keyup.enter="admin.fetchProducts(1)"
              />
              <button
                type="button"
                class="rounded-xl bg-primary px-4 py-2 text-text-inverse transition hover:bg-bordeaux-dark"
                @click="admin.fetchProducts(1)"
              >
                Rechercher
              </button>
            </div>
            <div class="mt-4 overflow-x-auto rounded-2xl border-2 border-primary/20 bg-white shadow-md">
              <table class="w-full text-left text-sm">
                <thead class="bg-primary/10 text-primary">
                  <tr>
                    <th class="p-4">Nom</th>
                    <th class="p-4">Marque</th>
                    <th class="p-4">Prix</th>
                    <th class="p-4">Catégorie</th>
                  </tr>
                </thead>
                <tbody>
                  <template v-if="admin.loading && !admin.productsPaginated.length">
                    <tr v-for="i in 5" :key="i" class="border-t border-primary/10">
                      <td class="p-4"><span class="inline-block h-4 w-24 animate-pulse rounded bg-primary/20" /></td>
                      <td class="p-4"><span class="inline-block h-4 w-20 animate-pulse rounded bg-primary/20" /></td>
                      <td class="p-4"><span class="inline-block h-4 w-16 animate-pulse rounded bg-primary/20" /></td>
                      <td class="p-4"><span class="inline-block h-4 w-20 animate-pulse rounded bg-primary/20" /></td>
                    </tr>
                  </template>
                  <template v-else>
                    <tr
                      v-for="p in admin.productsPaginated"
                      :key="p.id"
                      class="border-t border-primary/10 transition hover:bg-accent/5"
                    >
                      <td class="p-4 font-medium">{{ p.name }}</td>
                      <td class="p-4">{{ p.brand }}</td>
                      <td class="p-4">{{ formatPrice(p.price) }}</td>
                      <td class="p-4">{{ p.category }}</td>
                    </tr>
                  </template>
                </tbody>
              </table>
            </div>
            <div class="mt-4 flex items-center justify-between">
              <button
                type="button"
                class="rounded-xl border-2 border-primary/30 px-4 py-2 text-primary transition hover:bg-primary/10 disabled:opacity-50"
                :disabled="admin.productsPage <= 1"
                @click="admin.fetchProducts(admin.productsPage - 1)"
              >
                Précédent
              </button>
              <span class="text-secondary">Page {{ admin.productsPage }} / {{ admin.productsTotalPages }}</span>
              <button
                type="button"
                class="rounded-xl border-2 border-primary/30 px-4 py-2 text-primary transition hover:bg-primary/10 disabled:opacity-50"
                :disabled="admin.productsPage >= admin.productsTotalPages"
                @click="admin.fetchProducts(admin.productsPage + 1)"
              >
                Suivant
              </button>
            </div>
          </section>

          <!-- Leads : recherche, filtre date, export CSV -->
          <section class="mt-12">
            <h2 class="font-serif text-xl font-bold text-primary">Leads newsletter</h2>
            <div class="mt-4 flex flex-wrap items-center gap-4">
              <input
                v-model="admin.leadsQuery"
                type="search"
                placeholder="Rechercher par email..."
                class="rounded-xl border-2 border-primary/20 bg-white px-4 py-2 focus:border-accent focus:outline-none"
                @keyup.enter="admin.fetchLeads()"
              />
              <input v-model="admin.leadsDateFrom" type="date" class="rounded-xl border-2 border-primary/20 bg-white px-4 py-2" />
              <input v-model="admin.leadsDateTo" type="date" class="rounded-xl border-2 border-primary/20 bg-white px-4 py-2" />
              <button
                type="button"
                class="rounded-xl bg-primary px-4 py-2 text-text-inverse transition hover:bg-bordeaux-dark"
                @click="admin.fetchLeads()"
              >
                Filtrer
              </button>
              <button
                v-if="admin.leads.length"
                type="button"
                class="rounded-xl bg-accent px-4 py-2 font-medium text-secondary transition hover:bg-gold-light"
                @click="exportLeadsCsv"
              >
                Exporter CSV
              </button>
            </div>
            <div class="mt-4 overflow-x-auto rounded-2xl border-2 border-primary/20 bg-white shadow-md">
              <table class="w-full text-left text-sm">
                <thead class="bg-primary/10 text-primary">
                  <tr>
                    <th class="p-4">Email</th>
                    <th class="p-4">Source</th>
                    <th class="p-4">Date</th>
                  </tr>
                </thead>
                <tbody>
                  <template v-if="admin.loading && !admin.leads.length">
                    <tr v-for="i in 4" :key="i" class="border-t border-primary/10">
                      <td class="p-4"><span class="inline-block h-4 w-40 animate-pulse rounded bg-primary/20" /></td>
                      <td class="p-4"><span class="inline-block h-4 w-24 animate-pulse rounded bg-primary/20" /></td>
                      <td class="p-4"><span class="inline-block h-4 w-24 animate-pulse rounded bg-primary/20" /></td>
                    </tr>
                  </template>
                  <template v-else>
                    <tr
                      v-for="lead in admin.leads"
                      :key="lead.id"
                      class="border-t border-primary/10 transition hover:bg-accent/5"
                    >
                      <td class="p-4 font-medium">{{ lead.email }}</td>
                      <td class="p-4">{{ lead.source ?? '—' }}</td>
                      <td class="p-4">{{ formatLeadDate(lead.created_at) }}</td>
                    </tr>
                  </template>
                </tbody>
              </table>
            </div>
          </section>

          <!-- Questions chatbot -->
          <section class="mt-12">
            <h2 class="font-serif text-xl font-bold text-primary">Questions chatbot (libres)</h2>
            <button
              type="button"
              class="mt-4 rounded-xl border-2 border-primary/30 px-4 py-2 text-primary transition hover:bg-primary/10"
              @click="admin.fetchChatbotQuestions()"
            >
              Charger les questions
            </button>
            <div v-if="admin.chatbotQuestions.length" class="mt-4 overflow-x-auto rounded-2xl border-2 border-primary/20 bg-white shadow-md">
              <table class="w-full text-left text-sm">
                <thead class="bg-primary/10 text-primary">
                  <tr>
                    <th class="p-4">Question</th>
                    <th class="p-4">Date</th>
                  </tr>
                </thead>
                <tbody>
                  <tr
                    v-for="q in admin.chatbotQuestions"
                    :key="q.id"
                    class="border-t border-primary/10 transition hover:bg-accent/5"
                  >
                    <td class="p-4">{{ q.question }}</td>
                    <td class="p-4">{{ formatLeadDate(q.created_at) }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </section>
        </template>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useAdminStore } from '@/stores/admin'

const auth = useAuthStore()
const admin = useAdminStore()
const username = ref('')
const password = ref('')
const loginError = ref(false)
const fileInput = ref<HTMLInputElement | null>(null)
const importMessage = ref('')
const importSuccess = ref(false)
const isDragging = ref(false)
const seeding = ref(false)
const seedMessage = ref('')
const seedOk = ref(false)

// Toast
const toast = ref<{ text: string; type: 'success' | 'error' }>({ text: '', type: 'success' })
let toastTimer: ReturnType<typeof setTimeout> | null = null
function showToast(text: string, type: 'success' | 'error' = 'success') {
  toast.value = { text, type }
  if (toastTimer) clearTimeout(toastTimer)
  toastTimer = setTimeout(() => {
    toast.value = { text: '', type: 'success' }
    toastTimer = null
  }, 4000)
}

// Confirmation modal
const confirmOpen = ref(false)
const confirmTitle = ref('')
const confirmMessage = ref('')
const confirmConfirmLabel = ref('Confirmer')
let confirmResolveFn: ((value: boolean) => void) | null = null
function openConfirm(
  title: string,
  message: string,
  confirmLabel = 'Confirmer'
): Promise<boolean> {
  confirmTitle.value = title
  confirmMessage.value = message
  confirmConfirmLabel.value = confirmLabel
  confirmOpen.value = true
  return new Promise((resolve) => {
    confirmResolveFn = resolve
  })
}
function confirmResolve(value: boolean) {
  confirmOpen.value = false
  if (confirmResolveFn) {
    confirmResolveFn(value)
    confirmResolveFn = null
  }
}

// Change password (premier login)
const newPassword = ref('')
const newPasswordConfirm = ref('')
const changePasswordError = ref(false)
const changingPassword = ref(false)
async function onChangePassword() {
  changePasswordError.value = false
  if (newPassword.value.length < 8 || newPassword.value !== newPasswordConfirm.value) {
    changePasswordError.value = true
    return
  }
  changingPassword.value = true
  try {
    const ok = await auth.changePassword(newPassword.value)
    if (ok) {
      showToast('Mot de passe enregistré.', 'success')
      await admin.fetchStats()
      await admin.fetchProducts(1)
    } else {
      changePasswordError.value = true
    }
  } finally {
    changingPassword.value = false
  }
}

// Seed demo
const seedLoading = ref(false)
async function openConfirmSeed() {
  const ok = await openConfirm(
    'Charger les données de démo',
    'Cela va créer 1 compte admin (admin@salon.com / change-me-123) si absent et 25 produits réalistes. Continuer ?',
    'Charger'
  )
  if (!ok) return
  seedLoading.value = true
  try {
    const result = await admin.seedDemoData()
    if (result.ok) {
      showToast(`Données de démo chargées. ${result.products_created ?? 0} produit(s) créé(s).`, 'success')
      await admin.fetchStats()
      await admin.fetchProducts(1)
    } else {
      showToast(result.message ?? 'Erreur', 'error')
    }
  } finally {
    seedLoading.value = false
  }
}

async function onLogin() {
  loginError.value = false
  const ok = await auth.login(username.value, password.value)
  if (ok) {
    showToast('Connexion réussie.', 'success')
    await admin.fetchStats()
    await admin.fetchProducts(1)
  } else {
    loginError.value = true
    showToast('Identifiants incorrects.', 'error')
  }
}

async function onSeedAdmin() {
  seeding.value = true
  seedMessage.value = ''
  try {
    const result = await admin.seedDefaultAdmin()
    seedOk.value = result.ok
    seedMessage.value = result.message ?? (result.ok ? 'Admin créé.' : 'Erreur.')
  } finally {
    seeding.value = false
  }
}

function onFileSelect(e: Event) {
  const input = e.target as HTMLInputElement
  const file = input.files?.[0]
  if (file) doImport(file)
  input.value = ''
}

function onDrop(e: DragEvent) {
  isDragging.value = false
  const file = e.dataTransfer?.files?.[0]
  if (file?.name.toLowerCase().endsWith('.csv')) doImport(file)
  else importMessage.value = 'Veuillez déposer un fichier CSV.'
}

async function doImport(file: File) {
  importMessage.value = ''
  try {
    const result = await admin.importCsv(file)
    importSuccess.value = result.ok
    importMessage.value = result.ok
      ? `Import réussi : ${result.imported ?? 0} produit(s).`
      : (result.error ?? 'Erreur import.')
    if (result.ok) {
      showToast(`Import réussi : ${result.imported ?? 0} produit(s).`, 'success')
      await admin.fetchStats()
      await admin.fetchProducts(admin.productsPage)
    } else {
      showToast(result.error ?? 'Erreur import.', 'error')
    }
  } catch {
    importSuccess.value = false
    importMessage.value = 'Erreur lors de l\'import.'
    showToast('Erreur lors de l\'import.', 'error')
  }
}

function exportLeadsCsv() {
  const headers = ['email', 'source', 'created_at']
  const rows = admin.leads.map((l: { email: string; source?: string; created_at?: string }) => [l.email, l.source ?? '', l.created_at ?? ''])
  const csv = [headers.join(','), ...rows.map((r: string[]) => r.map((c: string) => `"${String(c).replace(/"/g, '""')}"`).join(','))].join('\n')
  const blob = new Blob(['\ufeff' + csv], { type: 'text/csv;charset=utf-8' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = 'leads_newsletter.csv'
  a.click()
  URL.revokeObjectURL(url)
  showToast('Export CSV téléchargé.', 'success')
}

function formatPrice(price: number) {
  return new Intl.NumberFormat('fr-FR', { style: 'currency', currency: 'EUR' }).format(price)
}

function formatLeadDate(d?: string) {
  if (!d) return '—'
  try {
    return new Date(d).toLocaleDateString('fr-FR')
  } catch {
    return d
  }
}

onMounted(() => {
  if (auth.isAuthenticated && !auth.mustChangePassword) {
    admin.fetchStats()
    admin.fetchProducts(1)
  }
})
</script>

<style scoped>
.toast-enter-active,
.toast-leave-active {
  transition: opacity 0.25s ease, transform 0.25s ease;
}
.toast-enter-from,
.toast-leave-to {
  opacity: 0;
  transform: translateX(1rem);
}
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.2s ease;
}
.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}
.modal-enter-active .rounded-2xl,
.modal-leave-active .rounded-2xl {
  transition: transform 0.2s ease;
}
.modal-enter-from .rounded-2xl,
.modal-leave-to .rounded-2xl {
  transform: scale(0.95);
}
</style>

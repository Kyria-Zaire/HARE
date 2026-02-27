<template>
  <div class="fixed bottom-4 right-4 z-40 sm:bottom-6 sm:right-6">
    <Transition name="scale">
      <div
        v-if="open"
        class="absolute bottom-14 right-0 flex h-[420px] w-[380px] max-w-[calc(100vw-2rem)] flex-col overflow-hidden rounded-2xl border-2 border-primary/30 bg-white shadow-2xl"
      >
        <div class="flex shrink-0 items-center justify-between bg-primary px-4 py-3 text-text-inverse">
          <div class="flex flex-col">
            <span class="font-serif text-sm font-semibold leading-tight sm:text-base">Besoin d'aide ?</span>
            <span class="text-xs text-white/80">Questions rapides sur le fonctionnement du quiz</span>
          </div>
          <button
            type="button"
            class="rounded-lg bg-white/20 px-2 py-1 font-sans text-xs font-medium uppercase tracking-wide transition hover:bg-white/30"
            aria-label="Fermer la fenêtre d'aide"
            @click="open = false"
          >
            Fermer
          </button>
        </div>
        <div ref="chatContent" class="min-h-0 flex-1 overflow-y-auto bg-cream-light/60 p-4">
          <p class="mb-3 text-xs font-semibold uppercase tracking-wide text-primary/80">FAQ rapides</p>
          <ul class="space-y-2">
            <li v-for="(faq, i) in faqList" :key="i">
              <button
                type="button"
                class="w-full rounded-xl border-2 border-primary/15 bg-white px-4 py-2 text-left text-sm text-secondary transition hover:border-accent hover:bg-accent/10"
                @click="selectFaq(faq)"
              >
                {{ faq.question }}
              </button>
            </li>
          </ul>
          <div class="mt-4 rounded-2xl bg-white/80 p-3">
            <p class="text-xs font-semibold uppercase tracking-wide text-primary/80">Poser une question</p>
            <textarea
              v-model="freeQuestion"
              placeholder="Ou posez votre question libre..."
              rows="2"
              class="mt-2 w-full rounded-xl border-2 border-primary/20 px-4 py-2 text-sm focus:border-accent focus:outline-none"
            />
            <button
              type="button"
              class="mt-2 rounded-lg bg-accent px-4 py-2 text-sm font-medium text-secondary hover:bg-gold-light disabled:opacity-50"
              :disabled="!freeQuestion.trim() || sending"
              @click="sendFreeQuestion"
            >
              {{ sending ? 'Envoi…' : 'Envoyer' }}
            </button>
          </div>
          <div
            v-if="lastAnswer"
            class="mt-4 space-y-3 rounded-2xl bg-white p-4 text-sm text-secondary shadow-sm"
          >
            <p class="text-xs font-semibold uppercase tracking-wide text-primary/80">Dernier échange</p>
            <div v-if="lastQuestion" class="flex items-start gap-2">
              <span
                class="mt-0.5 rounded-full bg-primary/10 px-2 py-0.5 text-[11px] font-semibold uppercase tracking-wide text-primary"
              >
                Vous
              </span>
              <p class="flex-1">
                {{ lastQuestion }}
              </p>
            </div>
            <div class="flex items-start gap-2">
              <span
                class="mt-0.5 rounded-full bg-primary px-2 py-0.5 text-[11px] font-semibold uppercase tracking-wide text-text-inverse"
              >
                Salon
              </span>
              <p class="flex-1">
                {{ lastAnswer }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </Transition>
    <button
      type="button"
      class="flex h-14 w-14 items-center justify-center rounded-full bg-primary text-2xl shadow-lg transition hover:scale-110 hover:bg-bordeaux-dark hover:shadow-xl"
      aria-label="Ouvrir l’aide"
      @click="open = !open"
    >
      💬
    </button>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, nextTick } from 'vue'
import axios from 'axios'

const open = ref(false)
const chatContent = ref<HTMLElement | null>(null)
const faqList = ref<{ question: string; answer: string }[]>([])
const freeQuestion = ref('')
const lastQuestion = ref('')
const lastAnswer = ref('')
const sending = ref(false)

function scrollToBottom() {
  nextTick(() => {
    const el = chatContent.value
    if (el) el.scrollTop = el.scrollHeight
  })
}

watch(lastAnswer, () => scrollToBottom())

onMounted(async () => {
  try {
    const { data } = await axios.get<{ question: string; answer: string }[]>('/api/v1/chatbot/faq')
    faqList.value = data
  } catch {
    faqList.value = []
  }
})

async function selectFaq(faq: { question: string; answer: string }) {
  lastQuestion.value = faq.question
  lastAnswer.value = faq.answer
}

async function sendFreeQuestion() {
  if (!freeQuestion.value.trim() || sending.value) return
  sending.value = true
  const question = freeQuestion.value.trim()
  try {
    const { data } = await axios.post<{ answer: string | null }>('/api/v1/chatbot/ask', {
      question,
    })
    lastQuestion.value = question
    lastAnswer.value = data.answer ?? 'Votre question a été enregistrée.'
    freeQuestion.value = ''
  } catch {
    lastAnswer.value = 'Une erreur est survenue. Réessayez.'
  } finally {
    sending.value = false
  }
}
</script>

<style scoped>
.scale-enter-active,
.scale-leave-active {
  transition: transform 0.2s ease, opacity 0.2s ease;
}
.scale-enter-from,
.scale-leave-to {
  transform: scale(0.95);
  opacity: 0;
}
</style>

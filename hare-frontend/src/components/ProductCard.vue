<template>
  <article class="overflow-hidden rounded-xl border-2 border-primary/20 bg-white shadow-sm transition hover:shadow-md">
    <div class="aspect-square bg-cream-light">
      <img
        v-if="product.image_url"
        :src="product.image_url"
        :alt="product.name"
        class="h-full w-full object-cover"
      />
      <div v-else class="flex h-full w-full items-center justify-center text-secondary/70">
        Image non disponible
      </div>
    </div>
    <div class="p-4">
      <h2 class="font-serif text-lg font-bold text-primary">{{ product.name }}</h2>
      <p class="text-sm text-secondary">{{ product.brand }}</p>
      <p class="mt-1 font-bold text-primary">{{ formatPrice(product.price) }}</p>
      <p v-if="product.explanation" class="mt-2 line-clamp-2 text-sm text-secondary">{{ product.explanation }}</p>
    </div>
  </article>
</template>

<script setup lang="ts">
import type { RecommendedProduct } from '@/stores/quiz'

defineProps<{ product: RecommendedProduct }>()

function formatPrice(price: number) {
  return new Intl.NumberFormat('fr-FR', { style: 'currency', currency: 'EUR' }).format(price)
}
</script>

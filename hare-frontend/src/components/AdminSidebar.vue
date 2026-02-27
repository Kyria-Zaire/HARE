<template>
  <aside class="w-56 border-r border-stone-200 bg-cream-light p-4">
    <nav class="space-y-2">
      <router-link
        to="/admin"
        class="block rounded-lg px-4 py-2 text-stone-600 hover:bg-bordeaux/10 hover:text-bordeaux"
      >
        Tableau de bord
      </router-link>
      <router-link
        to="/admin/products"
        class="block rounded-lg px-4 py-2 text-stone-600 hover:bg-bordeaux/10 hover:text-bordeaux"
      >
        Produits
      </router-link>
      <router-link
        to="/admin/leads"
        class="block rounded-lg px-4 py-2 text-stone-600 hover:bg-bordeaux/10 hover:text-bordeaux"
      >
        Leads
      </router-link>
    </nav>
  </aside>
</template>

<script setup lang="ts">
</script>

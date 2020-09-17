<template>
  <v-app>
    <v-content>
      <router-view />
    </v-content>
    <main-footer/>
  </v-app>
</template>

<script>

import Footer from '@/components/main/Footer';


export default {
  
  name: "app",
  components: {
    'main-footer': Footer,
  },
}
</script>

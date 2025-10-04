<template>
  <div class="planet-overlay-wrapper" @mouseenter="show = true" @mouseleave="show = false">
    <slot />
    <transition name="fade">
      <div v-if="show" class="planet-overlay">
        <slot name="overlay" />
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref } from 'vue';
const show = ref(false);
</script>

<style scoped>
.planet-overlay-wrapper {
  position: relative;
  display: inline-block;
}
.planet-overlay {
  position: absolute;
  left: 50%;
  top: 100%;
  transform: translate(-50%, 20px);
  min-width: 220px;
  background: #5b5b5b;
  color: #fff;
  border-radius: 8px;
  padding: 20px 24px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.15);
  z-index: 10;
  font-family: inherit;
  text-align: center;
}
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.2s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>

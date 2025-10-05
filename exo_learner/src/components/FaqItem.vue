<template>
  <div class="faq-item">
    <button class="faq-btn" @click="toggle">
      <span>{{ title }}</span>
      <span class="faq-arrow">{{ expanded ? '▲' : '▼' }}</span>
    </button>
    <transition name="fade">
      <div v-if="expanded" class="faq-content">
        <slot />
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref } from 'vue';
const props = defineProps({ title: String });
const expanded = ref(false);
function toggle() { expanded.value = !expanded.value; }
</script>

<style scoped>
.faq-item {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.faq-btn {
  width: 100%;
  max-width: 1300px;
  background: #3c3c3c;
  color: #fff;
  font-size: 2rem;
  font-weight: 700;
  border: none;
  border-radius: 10px;
  padding: 16px 24px;
  margin-bottom: 0;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: space-between;
  transition: background 0.2s;
  box-sizing: border-box;
}
.faq-btn:hover {
  background: #222;
}
.faq-arrow {
  font-size: 1.2rem;
  margin-right: 24px;
}
.faq-content {
  width: 100%;
  max-width: 1300px;
  background: rgba(74, 74, 74, 0.861);
  border-radius: 10px;
  margin-top: 12px;
  padding: 24px 8px;
  min-height: 180px;
  color: #fff;
  font-size: 1.2rem;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  align-items: stretch;
  justify-content: center;
  overflow-x: auto;
  overflow-y: visible;
}
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.2s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>

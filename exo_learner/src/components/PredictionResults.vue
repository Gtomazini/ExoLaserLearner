<template>
  <section class="snap-section result-section">
    <div class="result-content">
      <div class="result-area">
        <div class="result-title">Predictions</div>
        <table class="result-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>%</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(pred, idx) in predictions" :key="idx" :class="{ selected: selectedPrediction && selectedPrediction.name === pred.name && selectedPrediction.percent === pred.percent }" @click="selectPrediction(pred)">
              <td>{{ pred.name }}</td>
              <td :style="{ color: pred.percent >= 50 ? '#27ae60' : '#c0392b', fontWeight: 'bold' }">{{ pred.percent }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-if="selectedPrediction" class="result-planet-side">
        <PlanetOverlay>
          <img src="@/assets/response_exoplanets_examples/amostra1.png" style="width:440px;" alt="Planeta" />
          <template #overlay>
            <div>
              <div>{{ selectedPrediction.name }}</div>
              <div :style="{ color: selectedPrediction.percent >= 50 ? '#27ae60' : '#c0392b', fontWeight: 'bold', marginTop: '8px' }">
                {{ selectedPrediction.percent >= 50 ? 'TRUE' : 'FALSE' }}
              </div>
            </div>
          </template>
        </PlanetOverlay>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue';
import PlanetOverlay from './PlanetOverlay.vue';

const predictions = ref([
  { name: 'K00757.03', percent: 71 },
  { name: 'K00754.01', percent: 31 },
  { name: 'K00757.03', percent: 86 },
  { name: 'K00754.01', percent: 19 },
]);
const selectedPrediction = ref(null);

function selectPrediction(pred) {
  selectedPrediction.value = pred;
}
</script>

<style scoped>
.result-section {
  display: flex;
  align-items: center;
  justify-content: center;
}
.result-area {
  background: rgba(74, 74, 74, 0.861);
  border-radius: 8px;
  padding: 40px 48px 32px 48px;
  min-width: 400px;
  min-height: 220px;
  display: flex;
  flex-direction: column;
  align-items: center;
  box-shadow: 0 2px 16px rgba(0,0,0,0.18);
  z-index: 2;
}
.result-title {
  font-size: 36px;
  color: #fff;
  background: #5b5b5b;
  border-radius: 8px;
  padding: 12px 0;
  width: 100%;
  text-align: center;
  margin-bottom: 32px;
  font-weight: 700;
  letter-spacing: 1px;
}
.result-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 24px;
}
.result-table th, .result-table td {
  padding: 10px 18px;
  font-size: 22px;
  color: #fff;
  text-align: left;
}
.result-table th {
  background: #444;
  font-weight: 700;
}
.result-table tr {
  cursor: pointer;
  transition: background 0.2s;
}
.result-table tr.selected, .result-table tr:hover {
  background: #5b5b5b;
}
.result-content {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  gap: 80px;
  position: relative;
}
.result-planet-side {
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 440px;
  z-index: 1;
}
.result-planet-side {
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 320px;
}
</style>

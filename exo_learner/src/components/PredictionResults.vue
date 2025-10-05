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
            <tr v-for="(pred, idx) in paginatedPredictions" :key="pred.id || idx" :class="{ selected: selectedPrediction && selectedPrediction.name === pred.name && selectedPrediction.percent === pred.percent }" @click="selectPrediction(pred, getGlobalIndex(idx))">
              <td>{{ pred.name }}</td>
              <td :style="{ color: pred.percent >= 50 ? '#27ae60' : '#c0392b', fontWeight: 'bold' }">{{ pred.percent }}</td>
            </tr>
          </tbody>
        </table>
        
        <!-- Paginação -->
        <div class="pagination-container">
          <div class="pagination-info">
            {{ startIndex + 1 }}-{{ Math.min(endIndex, predictions.length) }} item of {{ predictions.length }}
          </div>
          <div class="pagination-controls">
            <button 
              class="pagination-btn" 
              :class="{ disabled: currentPage === 1 }" 
              @click="previousPage"
              :disabled="currentPage === 1"
            >
              ◀
            </button>
            <button 
              class="pagination-btn" 
              :class="{ disabled: currentPage === totalPages }" 
              @click="nextPage"
              :disabled="currentPage === totalPages"
            >
              ▶
            </button>
          </div>
        </div>
      </div>
      <div v-if="selectedPrediction" class="result-planet-side">
        <PlanetOverlay>
          <img :src="getPlanetForSelection()" style="width:440px;" alt="Planeta" />
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
import { ref, onMounted, computed } from 'vue';
import PlanetOverlay from './PlanetOverlay.vue';

// Importar todas as imagens da pasta dinamicamente (Vite)
const planetModules = import.meta.glob('@/assets/response_exoplanets_examples/*.{png,jpg,jpeg,gif,svg}', { 
  eager: true, 
  import: 'default' 
});

// Converter para array de URLs
const availablePlanets = ref(Object.values(planetModules));

const predictions = ref([
  { name: 'K00757.03', percent: 71 },
  { name: 'K00754.01', percent: 31 },
  { name: 'K00757.03', percent: 86 },
  { name: 'K00754.01', percent: 19 },
  { name: 'K00758.02', percent: 65 },
  { name: 'K00759.01', percent: 22 },
  { name: 'K00760.03', percent: 78 },
  { name: 'K00761.01', percent: 45 },
]);

// Paginação
const currentPage = ref(1);
const itemsPerPage = 4;

// Computed properties para paginação
const totalPages = computed(() => Math.ceil(predictions.value.length / itemsPerPage));
const startIndex = computed(() => (currentPage.value - 1) * itemsPerPage);
const endIndex = computed(() => startIndex.value + itemsPerPage);
const paginatedPredictions = computed(() => 
  predictions.value.slice(startIndex.value, endIndex.value)
);

const selectedPrediction = ref(null);

// Armazena o planeta associado a cada item (índice da predição → caminho da imagem)
const planetAssignments = ref({});

function getRandomPlanet() {
  const randomIndex = Math.floor(Math.random() * availablePlanets.value.length);
  return availablePlanets.value[randomIndex];
}

// Funções de paginação
function nextPage() {
  if (currentPage.value < totalPages.value) {
    currentPage.value++;
  }
}

function previousPage() {
  if (currentPage.value > 1) {
    currentPage.value--;
  }
}

function getGlobalIndex(localIndex) {
  return startIndex.value + localIndex;
}

function selectPrediction(pred, globalIndex) {
  selectedPrediction.value = pred;
  
  // Se o item ainda não tem um planeta associado, sorteia um
  if (!planetAssignments.value[globalIndex]) {
    planetAssignments.value[globalIndex] = getRandomPlanet();
  }
}

function getPlanetForSelection() {
  if (!selectedPrediction.value) return availablePlanets.value[0];
  
  // Encontra o índice global da predição selecionada
  const selectedIndex = predictions.value.findIndex(pred => 
    pred.name === selectedPrediction.value.name && 
    pred.percent === selectedPrediction.value.percent
  );
  
  return planetAssignments.value[selectedIndex] || availablePlanets.value[0];
}

// Selecionar o primeiro item automaticamente quando o componente for montado
onMounted(() => {
  if (predictions.value.length > 0) {
    selectPrediction(predictions.value[0], 0);
  }
});
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

/* Estilos de Paginação */
.pagination-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  margin-top: 16px;
}

.pagination-info {
  color: #fff;
  font-size: 14px;
  font-weight: 500;
}

.pagination-controls {
  display: flex;
  gap: 8px;
}

.pagination-btn {
  background: #5b5b5b;
  color: #fff;
  border: none;
  border-radius: 4px;
  padding: 8px 12px;
  cursor: pointer;
  font-size: 16px;
  font-weight: bold;
  transition: all 0.2s;
  min-width: 40px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.pagination-btn:hover:not(.disabled) {
  background: #444;
  transform: translateY(-1px);
}

.pagination-btn.disabled {
  background: #333;
  color: #666;
  cursor: not-allowed;
  opacity: 0.5;
}

.pagination-btn:active:not(.disabled) {
  transform: translateY(0);
}
</style>

<script setup>
import { ref } from 'vue';
import Landing from './components/Landing.vue';
import PlanetOverlay from './components/PlanetOverlay.vue';
import FaqItem from './components/FaqItem.vue';
import InputLogicTable from './components/InputLogicTable.vue';
import PredictionResults from './components/PredictionResults.vue';
import commonsData from '@/assets/data/commons.json';

// Posições dos planetas (em porcentagem da tela)
const planetPositions = [
  { top: '10%', left: '10%' },
  { top: '40%', left: '25%' },
  { top: '65%', left: '60%' },
  { top: '20%', left: '75%' },
  { top: '70%', left: '20%' },
  { top: '55%', left: '80%' },
  { top: '10%', left: '50%' },
];

const fileInput = ref(null);
const selectedFile = ref(null);
const fileName = ref(commonsData.messages.noFileSelected);
const statusMsg = ref('');
const limitSamples = ref(false);
const url_path = 'http://localhost:8000'; // está para local host

// Dados comuns do JSON
const commons = ref(commonsData);

// Mock de resultados
const predictions = ref([
  { name: 'K00757.03', percent: 71 },
  { name: 'K00754.01', percent: 31 },
  { name: 'K00757.03', percent: 86 },
  { name: 'K00754.01', percent: 19 },
]);
const selectedPrediction = ref(null);

// Referência para o componente PredictionResults
const predictionResultsRef = ref(null);

function openFileDialog() {
  if (fileInput.value) fileInput.value.click();
}

function handleFileChange(event) {
  const file = event.target.files[0];
  if (file) {
    selectedFile.value = file;
    fileName.value = file.name;
    statusMsg.value = ''; // Limpar status anterior
    limitSamples.value = true; // Marcar checkbox por padrão quando arquivo for carregado
  }
}

function clearFile() {
  selectedFile.value = null;
  fileName.value = commons.value.messages.noFileSelected;
  statusMsg.value = '';
  // Limpar o input file
  if (fileInput.value) {
    fileInput.value.value = '';
  }
}

async function sendFile() {
  if (!selectedFile.value) {
    statusMsg.value = commons.value.messages.selectFileFirst;
    return;
  }
  statusMsg.value = commons.value.messages.uploading;
  const formData = new FormData();
  formData.append('file', selectedFile.value);
  try {
    const response = await fetch(`${url_path}/predict`, {
      method: 'POST',
      body: formData,
    });
    if (response.ok) {
      const result = await response.json();
      statusMsg.value = commons.value.messages.success;
      console.log('Resposta do backend:', result);
      
      // Atualizar predições com dados da API
      if (predictionResultsRef.value && result.predictions) {
        predictionResultsRef.value.updatePredictions(result);
      }
      
      // Rolar para a seção de resultados após sucesso
      setTimeout(() => {
        const resultSection = document.querySelector('.result-section');
        if (resultSection) {
          resultSection.scrollIntoView({ 
            behavior: 'smooth',
            block: 'center'
          });
        }
      }, 500); // Delay para permitir que a UI atualize
    } else {
      statusMsg.value = commons.value.messages.errorSending;
    }
  } catch (err) {
    statusMsg.value = commons.value.messages.connectionError;
    console.error('Erro ao enviar arquivo:', err);
  }
}

function selectPrediction(pred) {
  selectedPrediction.value = pred;
}


</script>

<template>
  <div class="app-bg">
    <div class="snap-container">
      <!-- SEÇÃO DOS PLANETAS -->
      <section class="snap-section planet-section">
        <div class="planet-space">
          <PlanetOverlay :style="{ position: 'absolute', top: planetPositions[0].top, left: planetPositions[0].left }">
            <img src="@/assets/landing_exoplanets/exo_azul.png" class="planet" alt="Exoplaneta Azul" />
            <template #overlay>
              <div>
                <div>EPIC 201126503.01</div>
                <div style="margin-top:8px;font-weight:bold;">CANDIDATE</div>
              </div>
            </template>
          </PlanetOverlay>
          
          <PlanetOverlay :style="{ position: 'absolute', top: planetPositions[1].top, left: planetPositions[1].left }">
            <img src="@/assets/landing_exoplanets/exo_gray.png" class="planet" alt="Exoplaneta Cinza" />
            <template #overlay>
              <div>
                <div>EPIC 201126503.01</div>
                <div style="margin-top:8px;font-weight:bold;">CANDIDATE</div>
              </div>
            </template>
          </PlanetOverlay>
          
          <PlanetOverlay :style="{ position: 'absolute', top: planetPositions[2].top, left: planetPositions[2].left }">
            <img src="@/assets/landing_exoplanets/exo_green_blue.png" class="planet" alt="Exoplaneta Verde-Azul" />
  
            <template #overlay>
              <div>
                <div>EPIC 201126503.01</div>
                <div style="margin-top:8px;font-weight:bold;">CANDIDATE</div>
              </div>
            </template>
          </PlanetOverlay>
          
          <PlanetOverlay :style="{ position: 'absolute', top: planetPositions[3].top, left: planetPositions[3].left }">
            <img src="@/assets/landing_exoplanets/exo_purple.png" class="planet" alt="Exoplaneta Roxo" />
            <template #overlay>
              <div>
                <div>EPIC 201126503.01</div>
                <div style="margin-top:8px;font-weight:bold;">CANDIDATE</div>
              </div>
            </template>
          </PlanetOverlay>
          
          <PlanetOverlay :style="{ position: 'absolute', top: planetPositions[4].top, left: planetPositions[4].left }">
            <img src="@/assets/landing_exoplanets/exo_red.png" class="planet" alt="Exoplaneta Vermelho" />
            <template #overlay>
              <div>
                <div>EPIC 201126503.01</div>
                <div style="margin-top:8px;font-weight:bold;">CANDIDATE</div>
              </div>
            </template>
          </PlanetOverlay>
          
          <PlanetOverlay :style="{ position: 'absolute', top: planetPositions[5].top, left: planetPositions[5].left }">
            <img src="@/assets/landing_exoplanets/exo_yellow.png" class="planet" alt="Exoplaneta Amarelo" />
            <template #overlay>
              <div>
                <div>EPIC 201126503.01</div>
                <div style="margin-top:8px;font-weight:bold;">CANDIDATE</div>
              </div>
            </template>
          </PlanetOverlay>
          
          <PlanetOverlay :style="{ position: 'absolute', top: planetPositions[6].top, left: planetPositions[6].left }">
            <img src="@/assets/landing_exoplanets/exo_blue_big.png" class="planet" alt="Exoplaneta Azul Grande" />
            <template #overlay>
              <div>
                <div>EPIC 201126503.01</div>
                <div style="margin-top:8px;font-weight:bold;">CANDIDATE</div>
              </div>
            </template>
          </PlanetOverlay>
        </div>
      </section>

      <!-- SEÇÃO IMPORT TARGET -->
      <section class="snap-section import-section">
        <div class="import-area">
            <button class="import-title" @click="openFileDialog">{{ commons.labels.importTarget }}</button>
            <input
            type="file"
            ref="fileInput"
            accept=".csv"
            style="display:none"
            @change="handleFileChange"
            />
          <div class="import-file-row">
            <span v-if="selectedFile" class="icon-x" @click="clearFile">
              <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
                <path d="M10 10L22 22M22 10L10 22" stroke="#c0392b" stroke-width="3" stroke-linecap="round"/>
              </svg>
            </span>
            <span class="import-file">{{ fileName }}</span>
            <span v-if="selectedFile" class="icon-check">
              <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
                <path d="M10 17L15 22L22 12" stroke="#27ae60" stroke-width="3" stroke-linecap="round"/>
              </svg>
            </span>
          </div>
          <div class="custom-checkbox-row" style="margin-bottom: 24px;">
            <label class="custom-checkbox-label tooltip-container" @click="limitSamples = !limitSamples" style="display:flex;align-items:center;gap:10px;cursor:pointer;position:relative;">
              <span class="custom-checkbox" :class="{ checked: limitSamples }" style="width:24px;height:24px;border:2px solid #fff;border-radius:6px;display:inline-block;position:relative;">
                <span v-if="limitSamples" style="position:absolute;top:2px;left:6px;width:10px;height:18px;border-right:3px solid #27ae60;border-bottom:3px solid #27ae60;transform:rotate(45deg);"></span>
              </span>
              <span style="color:#fff;font-size:22px;">{{ commons.labels.limitSamples }}</span>
              <div class="tooltip">
                <div class="tooltip-title">{{ commons.tooltips.limitSamples.title }}</div>
                <div class="tooltip-text">{{ commons.tooltips.limitSamples.text }}</div>
              </div>
            </label>
          </div>
          <button class="import-btn" @click="sendFile">{{ commons.labels.send }}</button>
          <div class="import-status">{{ statusMsg }}</div>
        </div>
      </section>

      <!-- SEÇÃO 3 - RESULTADO -->
      <PredictionResults ref="predictionResultsRef" />

      <!-- SEÇÃO 4 - FAQ -->
      <section class="faq-section-no-snap">
        <div class="faq-area">
          <div class="faq-title">Wiki/FAQ Area</div>
          <div class="faq-list">
            <FaqItem title="How it works?">
              <div>
                <p style="color:#fff;">Conteúdo explicativo sobre funcionamento...</p>
              </div>
            </FaqItem>
            <FaqItem title="Input Logic">
              <InputLogicTable />
            </FaqItem>

            <FaqItem title="Team Work">
              <div>
                <p style="color:#fff;">Conteúdo sobre colaboração, equipe e desenvolvimento do projeto...</p>
              </div>
            </FaqItem>
          </div>
        </div>
      </section>


    </div>
  </div>
</template>

<style>
@import url('https://fonts.googleapis.com/css2?family=Quantico:wght@400;700&display=swap');

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: 'Quantico', sans-serif;
}

html, body {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
  overflow-x: hidden;
  position: relative;
}

#app {
  width: 100%;
  height: 100%;
  overflow-x: hidden;
}

.app-bg {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  width: 100%;
  height: 100%;
  background: url('@/assets/background/background_starts.jpg') no-repeat center center fixed;
  background-size: cover;
  overflow: hidden;
}

.snap-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow-y: scroll;
  overflow-x: hidden;
  scroll-snap-type: y mandatory;
}

.snap-section {
  width: 100%;
  height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  scroll-snap-align: center;
  background: transparent;
}

/* Seção FAQ com snap no início mas altura dinâmica */
.faq-section-no-snap {
  width: 100%;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  padding: 20px 0 80px 0;
  background: transparent;
  scroll-snap-align: start;
  scroll-snap-stop: always;
}

/* SEÇÃO DOS PLANETAS */
.planet-section {
  position: relative;
  overflow: visible;
}

.planet-space {
  position: relative;
  width: 100%;
  height: 100vh;
}

.planet {
  position: absolute;
  width: 300px;
  height: auto;
  transition: transform 0.3s;
}

/* SEÇÃO IMPORT */
.import-section {
  display: flex;
  align-items: center;
  justify-content: center;
}

.import-area {
  background: rgba(74, 74, 74, 0.861);
  border-radius: 8px;
  padding: 40px 48px 32px 48px;
  min-width: 400px;
  min-height: 220px;
  display: flex;
  flex-direction: column;
  align-items: center;
  box-shadow: 0 2px 16px rgba(0,0,0,0.18);
}

.import-title {
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

.import-file-row {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  margin-bottom: 32px;
}

.import-file {
  font-size: 28px;
  color: #fff;
  font-weight: 400;
}

.icon-check svg,
.icon-x svg {
  vertical-align: middle;
}

.icon-x {
  cursor: pointer;
  transition: all 0.2s;
  border-radius: 4px;
  padding: 4px;
}

.icon-x:hover {
  background: rgba(192, 57, 43, 0.1);
  transform: scale(1.1);
}

.import-btn {
  font-size: 36px;
  color: #fff;
  background: #333;
  border: none;
  border-radius: 8px;
  padding: 10px 40px;
  cursor: pointer;
  margin-top: 8px;
  transition: background 0.2s;
  font-weight: 700;
  box-shadow: 0 2px 8px rgba(0,0,0,0.12);
}

.import-btn:hover {
  background: #222;
}

/* Custom Checkbox */
.custom-checkbox-label {
  transition: all 0.2s;
  user-select: none;
}

.custom-checkbox-label:hover {
  opacity: 0.8;
}

.custom-checkbox {
  transition: all 0.2s;
  background: transparent;
}

.custom-checkbox:hover {
  background: rgba(255, 255, 255, 0.1);
}

.custom-checkbox.checked {
  background: rgba(39, 174, 96, 0.1);
  border-color: #27ae60 !important;
}

/* Tooltip */
.tooltip-container {
  position: relative;
}

.tooltip {
  position: absolute;
  bottom: 100%;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(0, 0, 0, 0.9);
  color: #fff;
  padding: 12px 16px;
  border-radius: 8px;
  font-size: 14px;
  white-space: nowrap;
  max-width: 280px;
  white-space: normal;
  z-index: 1000;
  opacity: 0;
  visibility: hidden;
  transition: all 0.3s;
  margin-bottom: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.tooltip::after {
  content: '';
  position: absolute;
  top: 100%;
  left: 50%;
  transform: translateX(-50%);
  width: 0;
  height: 0;
  border-left: 6px solid transparent;
  border-right: 6px solid transparent;
  border-top: 6px solid rgba(0, 0, 0, 0.9);
}

.tooltip-container:hover .tooltip {
  opacity: 1;
  visibility: visible;
  transform: translateX(-50%) translateY(-4px);
}

.tooltip-title {
  font-weight: 700;
  font-size: 16px;
  margin-bottom: 4px;
  color: #27ae60;
}

.tooltip-text {
  font-size: 13px;
  line-height: 1.4;
  color: #e0e0e0;
}

/* TEXTO DAS SEÇÕES */
.snap-section h2,
.snap-section p {
  color: #ffffff;
.import-status {
  margin-top: 18px;
  font-size: 22px;
  color: #fff;
  text-align: center;
  min-height: 28px;
}
}


.faq-area {
  width: 80vw;
  max-width: 900px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.faq-title {
  width: 100%;
  background: #bdbdbd;
  color: #222;
  font-size: 2.2rem;
  text-align: center;
  font-weight: 500;
  margin-bottom: 32px;
  padding: 8px 0;
  border-radius: 2px;
}
.faq-list {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 24px;
}
</style>
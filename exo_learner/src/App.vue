<script setup>
import { ref } from 'vue';
import Landing from './components/Landing.vue';
import PlanetOverlay from './components/PlanetOverlay.vue';

// Posições dos planetas (em porcentagem da tela)
const planetPositions = [
  { top: '10%', left: '10%' },
  { top: '40%', left: '25%' },
  { top: '65%', left: '60%' },
  { top: '20%', left: '75%' },
  { top: '70%', left: '20%' },
  { top: '55%', left: '80%' },
];

const fileName = ref('Nenhum arquivo selecionado');
const fileInput = ref(null);

function openFileDialog() {
  if (fileInput.value) fileInput.value.click();
}

function handleFileChange(event) {
  const file = event.target.files[0];
  if (file) {
    fileName.value = file.name;
  }
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
        </div>
      </section>

      <!-- SEÇÃO IMPORT TARGET -->
      <section class="snap-section import-section">
        <div class="import-area">
            <button class="import-title" @click="openFileDialog">Import Target</button>
            <input
            type="file"
            ref="fileInput"
            accept=".csv"
            style="display:none"
            @change="handleFileChange"
            />
          <div class="import-file-row">
            <span class="icon-x">
              <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
                <path d="M10 10L22 22M22 10L10 22" stroke="#c0392b" stroke-width="3" stroke-linecap="round"/>
              </svg>
            </span>
            <span class="import-file">{{ fileName }}</span>
            <span class="icon-check">
              <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
                <path d="M10 17L15 22L22 12" stroke="#27ae60" stroke-width="3" stroke-linecap="round"/>
              </svg>
            </span>
          </div>
          <button class="import-btn">Send</button>
        </div>
      </section>

      <!-- SEÇÃO 3 -->
      <section class="snap-section">
        <h2>Seção 3</h2>
        <p>Conteúdo da terceira sessão.</p>
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

/* TEXTO DAS SEÇÕES */
.snap-section h2,
.snap-section p {
  color: #ffffff;
}
</style>
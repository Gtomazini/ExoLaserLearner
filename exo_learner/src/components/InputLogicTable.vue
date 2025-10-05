<template>
  <div class="campos-e-descricao">
    <div style="margin-bottom:16px;">
      <table style="width:100%;border-collapse:collapse;">
        <thead>
          <tr>
            <th style="background:#444;color:#fff;padding:8px;">Campo</th>
            <th style="background:#444;color:#fff;padding:8px;">Descrição</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in data.fieldDescriptions" :key="item.field">
            <td style="background:#222;color:#fff;padding:8px;"><code>{{ item.field }}</code></td>
            <td style="background:#333;color:#fff;padding:8px;">{{ item.description }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <table class="input-logic-table">
      <thead>
        <tr>
          <th v-for="field in data.fieldDescriptions" :key="field.field">{{ field.field }}</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="example in data.exampleData" :key="example.kepid">
          <td v-for="field in data.fieldDescriptions" :key="field.field">
            {{ example[field.field] }}
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import inputLogicData from '@/assets/data/inputLogicData.json';

const data = ref(inputLogicData);
</script>

<style scoped>
.campos-e-descricao {
  width: 100%;
}

/* Estilos para a tabela de descrição de campos */
.campos-e-descricao table {
  width: 100%;
  border-collapse: collapse;
}

.campos-e-descricao th, 
.campos-e-descricao td {
  padding: 8px;
  color: #fff;
  text-align: left;
}

.campos-e-descricao code {
  font-family: 'Courier New', monospace;
  font-weight: bold;
}

/* Estilos para a tabela input-logic */
.input-logic-table {
  width: max-content;
  min-width: 100%;
  border-collapse: collapse;
  margin: 0;
  font-size: 0.9rem;
  table-layout: auto;
}

.input-logic-table th, 
.input-logic-table td {
  padding: 8px 12px;
  font-size: 0.95rem;
  color: #fff;
  text-align: center;
  word-wrap: break-word;
  min-width: 90px;
  white-space: nowrap;
}

.input-logic-table th {
  background: #444;
  font-weight: 700;
  font-size: 0.9rem;
}

.input-logic-table td {
  background: #5b5b5b;
}

.input-logic-table tr {
  transition: background 0.2s;
}

.input-logic-table tr:hover {
  background: #666;
}
</style>
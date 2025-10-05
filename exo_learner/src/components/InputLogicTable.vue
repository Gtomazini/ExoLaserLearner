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
          <tr>
            <td style="background:#222;color:#fff;padding:8px;"><code>kepid</code></td>
            <td style="background:#333;color:#fff;padding:8px;">ID do Kepler</td>
          </tr>
          <tr>
            <td style="background:#222;color:#fff;padding:8px;"><code>kepoi_name</code></td>
            <td style="background:#333;color:#fff;padding:8px;">Nome do KOI</td>
          </tr>
          <tr>
            <td style="background:#222;color:#fff;padding:8px;"><code>koi_disposition</code></td>
            <td style="background:#333;color:#fff;padding:8px;">Status oficial</td>
          </tr>
          <tr>
            <td style="background:#222;color:#fff;padding:8px;"><code>koi_period</code></td>
            <td style="background:#333;color:#fff;padding:8px;">Período orbital</td>
          </tr>
          <tr>
            <td style="background:#222;color:#fff;padding:8px;"><code>koi_prad</code></td>
            <td style="background:#333;color:#fff;padding:8px;">Raio do planeta</td>
          </tr>
          <tr>
            <td style="background:#222;color:#fff;padding:8px;"><code>koi_teq</code></td>
            <td style="background:#333;color:#fff;padding:8px;">Temperatura de equilíbrio</td>
          </tr>
          <tr>
            <td style="background:#222;color:#fff;padding:8px;"><code>koi_depth</code></td>
            <td style="background:#333;color:#fff;padding:8px;">Profundidade do trânsito</td>
          </tr>
          <tr>
            <td style="background:#222;color:#fff;padding:8px;"><code>koi_duration</code></td>
            <td style="background:#333;color:#fff;padding:8px;">Duração do trânsito</td>
          </tr>
          <tr>
            <td style="background:#222;color:#fff;padding:8px;"><code>koi_steff</code></td>
            <td style="background:#333;color:#fff;padding:8px;">Temperatura da estrela</td>
          </tr>
          <tr>
            <td style="background:#222;color:#fff;padding:8px;"><code>koi_srad</code></td>
            <td style="background:#333;color:#fff;padding:8px;">Raio da estrela</td>
          </tr>
        </tbody>
      </table>
    </div>
    <table class="input-logic-table">
      <thead>
        <tr>
          <th>kepid</th>
          <th>kepoi_name</th>
          <th>koi_disposition</th>
          <th>koi_period</th>
          <th>koi_prad</th>
          <th>koi_teq</th>
          <th>koi_depth</th>
          <th>koi_duration</th>
          <th>koi_steff</th>
          <th>koi_srad</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>10797460</td>
          <td>K00757.03</td>
          <td>CONFIRMED</td>
          <td>9.488</td>
          <td>2.26</td>
          <td>793</td>
          <td>615.8</td>
          <td>2.96</td>
          <td>5455</td>
          <td>0.927</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

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
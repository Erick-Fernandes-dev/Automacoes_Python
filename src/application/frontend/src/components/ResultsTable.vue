<template>
  <div class="results-container">
    <table v-if="results.length > 0" class="results-table">
      <thead>
        <tr>
          <th>Registro ANS</th>
          <th>Razão Social</th>
          <th>Nome Fantasia</th>
          <th>Modalidade</th>
          <th>Cidade/UF</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="op in results" :key="op.registro_ans">
          <td>{{ op.registro_ans }}</td>
          <td>{{ op.razao_social }}</td>
          <td>{{ op.nome_fantasia || '-' }}</td>
          <td>{{ op.modalidade }}</td>
          <td>{{ op.cidade }}/{{ op.uf }}</td>
        </tr>
      </tbody>
    </table>
    <div v-else class="no-results">
      Nenhum resultado encontrado
    </div>
  </div>
</template>

<script>
export default {
  props: {
    results: {
      type: Array,
      required: true
    }
  }
};
</script>

<style scoped>
.results-container {
  margin-top: 20px;
}
.results-table {
  width: 100%;
  border-collapse: collapse;
}
.results-table th, .results-table td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}
.results-table th {
  background-color: #f2f2f2;
}
.results-table tr:nth-child(even) {
  background-color: #f9f9f9;
}
.no-results {
  padding: 20px;
  text-align: center;
  color: #666;
}
</style>
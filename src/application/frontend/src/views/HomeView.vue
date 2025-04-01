<template>
  <div class="home">
    <h1>Busca de Operadoras de Saúde - ANS</h1>
    <SearchForm @search="performSearch" />
    <ResultsTable :results="searchResults" />
  </div>
</template>

<script>
import SearchForm from '@/components/SearchForm.vue';
import ResultsTable from '@/components/ResultsTable.vue';
import api from '@/services/api';

export default {
  name: 'HomeView',
  components: {
    SearchForm,
    ResultsTable
  },
  data() {
    return {
      searchResults: []
    };
  },
  methods: {
    async performSearch({ query, limit }) {
      try {
        const response = await api.searchOperators(query, limit);
        this.searchResults = response.data.results;
      } catch (error) {
        console.error('Erro na busca:', error);
        this.searchResults = [];
      }
    }
  }
};
</script>

<style scoped>
.home {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}
h1 {
  margin-bottom: 30px;
  color: #2c3e50;
}
</style>
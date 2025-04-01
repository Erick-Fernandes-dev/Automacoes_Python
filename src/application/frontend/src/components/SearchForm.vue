<template>
  <div class="search-form">
    <input 
      v-model="searchQuery" 
      @input="onSearch" 
      placeholder="Buscar operadoras..."
      class="search-input"
    />
    <select v-model="resultLimit" @change="onSearch" class="limit-select">
      <option value="5">5 resultados</option>
      <option value="10">10 resultados</option>
      <option value="20">20 resultados</option>
    </select>
  </div>
</template>

<script>
export default {
  data() {
    return {
      searchQuery: '',
      resultLimit: 10
    };
  },
  methods: {
    onSearch() {
      this.$emit('search', {
        query: this.searchQuery,
        limit: this.resultLimit
      });
    }
  }
};
</script>

<style scoped>
.search-form {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}
.search-input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}
.limit-select {
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}
</style>
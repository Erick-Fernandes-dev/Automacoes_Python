import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8010/api',
});

export default {
  searchOperators(query, limit = 10) {
    return api.get('/search', {
      params: { query, limit }
    });
  }
};
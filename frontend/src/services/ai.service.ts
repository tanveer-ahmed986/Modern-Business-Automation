import api from './api';

const aiService = {
  async queryAI(prompt: string) {
    const response = await api.post('/ai/query', null, { params: { prompt } });
    return response.data;
  },

  async getSalesPrediction(nDays: number = 30) {
    const response = await api.get('/ai/predict', { params: { n_days: nDays } });
    return response.data;
  },
};

export default aiService;

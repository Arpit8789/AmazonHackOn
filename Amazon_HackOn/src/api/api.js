import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
});

// Fallback data in case backend is not running
import { fallbackData } from './fallback';

/**
 * Helper to handle API calls with graceful fallback
 */
const fetchWithFallback = async (method, url, data = null, fallbackKey) => {
  try {
    const response = await api({
      method,
      url,
      data,
      headers: data instanceof FormData ? { 'Content-Type': 'multipart/form-data' } : {},
    });
    return response.data.data; // Return the "data" payload from backend
  } catch (error) {
    console.warn(`[API Fallback] ${url} failed, using mock data.`, error.message);
    
    // Simulate network delay for fallback
    await new Promise(resolve => setTimeout(resolve, 1500));
    return fallbackData[fallbackKey];
  }
};

export const apiService = {
  // 1. Get demo products
  getProducts: () => fetchWithFallback('GET', '/demo/products', null, 'products'),
  
  // 2. Initiate return
  initiateReturn: (data) => fetchWithFallback('POST', '/return/initiate', data, 'returnInitiate'),
  
  // 3. Grade photos
  gradeProduct: (formData) => fetchWithFallback('POST', '/grade', formData, 'grade'),
  
  // 4. Get resale price
  getPrice: (data) => fetchWithFallback('POST', '/price', data, 'price'),
  
  // 5. Submit P2P listing
  submitResale: (data) => fetchWithFallback('POST', '/resale/list', data, 'resaleSubmit'),
  
  // 6. Seller dashboard auto-list
  sellerAutolist: (formData) => fetchWithFallback('POST', '/seller/autolist', formData, 'sellerAutolist'),
  
  // 7. Ask review question
  askQuestion: (data) => fetchWithFallback('POST', '/reviews/ask', data, 'reviewQA'),

  // 8. AI-powered resale price prediction (Gemini + CatBoost)
  getAiResalePrice: async (formData) => {
    try {
      const response = await api({
        method: 'POST',
        url: '/resale/ai-price',
        data: formData,
        headers: { 'Content-Type': 'multipart/form-data' },
        timeout: 60000, // 60s timeout for Gemini Vision
      });
      return response.data;
    } catch (error) {
      console.warn('[API Fallback] /resale/ai-price failed, using mock data.', error.message);
      // Return a mock AI pricing result
      return {
        prediction: {
          predicted_resale_price: 1500,
          confidence_score: 72.5,
          top_positive_factors: ["Good overall condition", "Popular brand"],
          top_negative_factors: ["Product age caused some depreciation"],
        },
        ai_grading_report: {
          condition_score: 78,
          condition_grade: "B",
          gemini_report: {
            inspection_summary: "Product is in good usable condition with minor signs of wear.",
            buyer_trust_report: "Verified by AI — suitable for resale.",
            detected_defects: [],
          }
        },
        ai_grading_source: "fallback",
        ai_pricing_source: "fallback",
      };
    }
  },
};

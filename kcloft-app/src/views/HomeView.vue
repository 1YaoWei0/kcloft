<template>
  <div class="home">
    <h1>Welcome to KCLoft</h1>
    <div v-if="loading">Loading questions...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else>
      <h2>Questions ({{ questions.length }})</h2>
      <ul v-if="questions.length > 0">
        <li v-for="question in questions" :key="question.id">
          {{ question.title || question.text }}
        </li>
      </ul>
      <p v-else>No questions found.</p>
    </div>
    <button @click="fetchQuestions" :disabled="loading">Refresh Questions</button>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import apiClient from "../services/api";

interface Question {
  id: number;
  title?: string;
  text?: string;
}

const questions = ref<Question[]>([]);
const loading = ref(false);
const error = ref<string | null>(null);

async function fetchQuestions() {
  loading.value = true;
  error.value = null;
  try {
    const response = await apiClient.get("/questions/");
    questions.value = response.data;
  } catch (err: any) {
    const errorDetail = err.response?.data?.detail || err.message || "Failed to fetch questions";
    error.value = errorDetail;
    console.error("Error fetching questions:", err);
    console.error("Backend error detail:", err.response?.data);
  } finally {
    loading.value = false;
  }
}

onMounted(() => {
  fetchQuestions();
});
</script>

<style scoped>
.home {
  padding: 2rem;
  max-width: 800px;
  margin: 0 auto;
}

.error {
  color: red;
  margin: 1rem 0;
}

ul {
  list-style: none;
  padding: 0;
}

li {
  padding: 0.5rem;
  margin: 0.5rem 0;
  background: #f5f5f5;
  border-radius: 4px;
}

button {
  margin-top: 1rem;
  padding: 0.5rem 1rem;
  background: #4a8cff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:disabled {
  background: #ccc;
  cursor: not-allowed;
}
</style>
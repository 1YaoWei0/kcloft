<template>
  <div class="page">
    <div class="login-box">
      <h1 class="title">Sign In</h1>

      <form class="form" @submit.prevent>
        <input
          type="email"
          placeholder="Email"
          class="input"
          required
        />
        <input
          type="password"
          placeholder="Password"
          class="input"
          required
        />
        <button class="btn" type="submit">Login</button>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
// UI only, no logic yet
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

.page {
  min-height: 100vh;
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #f7f9fc;
  font-family: 'Inter', 'Segoe UI', 'Helvetica Neue', sans-serif;
  padding: 2rem;
}

.login-box {
  width: 400px;
  max-width: 90%;
  padding: 2rem;
  border-radius: 12px;
  background: white;
  box-shadow: 0 6px 22px rgba(0,0,0,0.08);
  text-align: center;
}

.title {
  margin-bottom: 1.8rem;
  font-size: 22px; /* reduced from 28px */
  font-weight: 500;
  color: #333;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.input {
  padding: 0.8rem 1rem;
  border-radius: 6px;
  border: 1px solid #c6c6c6;
  font-size: 14px; /* slightly smaller for technical feel */
  outline: none;
  transition: border-color 0.2s ease;
  font-family: 'Inter', monospace;
}

.input:focus {
  border-color: #4a8cff;
}

.btn {
  margin-top: 10px;
  padding: 0.8rem 1rem;
  border: none;
  border-radius: 6px;
  background: #4a8cff;
  color: white;
  font-size: 15px;
  cursor: pointer;
  transition: background-color 0.2s;
  font-family: 'Inter', monospace;
}

.btn:hover {
  background: #3974e0;
}
</style>
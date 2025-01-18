<template>
  <div>
    <h1>{{ isRegister ? 'Register' : 'Login' }}</h1>
    <form @submit.prevent="handleSubmit">
      <label>Username:</label>
      <input v-model="username" type="text" required />
      <label>Password:</label>
      <input v-model="password" type="password" required />
      <label v-if="isRegister">Email:</label>
      <input v-if="isRegister" v-model="email" type="email" required />
      <button type="submit">{{ isRegister ? 'Register' : 'Login' }}</button>
    </form>
    <p v-if="message" :class="success ? 'success' : 'error'">{{ message }}</p>
    <button @click="toggleMode">Switch to {{ isRegister ? 'Login' : 'Register' }}</button>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      username: '',
      password: '',
      email: '',
      isRegister: false,
      message: null,
      success: false,
    }
  },
  methods: {
    async handleSubmit() {
      if (this.isRegister) {
        await this.register()
      } else {
        await this.login()
      }
    },
    // 登入邏輯
    async login() {
      try {
        const response = await axios.post(
          '/login/',
          {
            username: this.username,
            password: this.password,
          },
          {
            withCredentials: true, // 跨域請求時需要攜帶 cookie
          },
        )

        if (response.data.success) {
          this.success = true
          this.message = response.data.message
          const redirectUrl = `http://localhost:1000/day1?username=${encodeURIComponent(this.username)}`
          window.location.href = redirectUrl // 登入成功後導向首頁
          console.log('Login successful!')
        } else {
          this.success = false
          this.message = response.data.message
        }
      } catch (error) {
        console.error('Login error:', error)
        this.success = false
        this.message = 'An error occurred while logging in.'
      }
    },
    // 註冊邏輯
    async register() {
      try {
        const response = await axios.post('/register/', {
          username: this.username,
          password: this.password,
          email: this.email,
        })

        if (response.data.success) {
          console.log('Registration successful!', response.data.success)
          this.success = true
          this.message = response.data.message
          this.isRegister = false // 切換回登入模式
          this.clearFields()
        } else {
          console.log('Registration successful!', response.data.success)
          this.success = false
          this.message = response.data.message
        }
      } catch (error) {
        console.error('Registration error:', error)
        this.success = false
        this.message = 'An error occurred during registration.'
      }
    },
    // 切換模式
    toggleMode() {
      this.isRegister = !this.isRegister
      this.clearFields()
    },
    // 清空表單欄位
    clearFields() {
      this.username = ''
      this.password = ''
      this.email = ''
      this.message = null
    },
  },
}
</script>

<style scoped>
div {
  background: #ffffff;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  padding: 20px;
  max-width: 400px;
  width: 100%;
  text-align: center;
}

/* 標題樣式 */
h1 {
  font-size: 24px;
  margin-bottom: 20px;
  color: #333;
}

/* 表單樣式 */
form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

label {
  font-size: 14px;
  color: #555;
  text-align: left;
}

input {
  padding: 10px;
  font-size: 14px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

input:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 5px rgba(0, 123, 255, 0.5);
}

button {
  background: #007bff;
  color: white;
  border: none;
  padding: 10px;
  font-size: 14px;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

button:hover {
  background: #0056b3;
}

/* 狀態訊息樣式 */
.success {
  color: #28a745;
  font-weight: bold;
}

.error {
  color: #dc3545;
  font-weight: bold;
}

/* 切換模式按鈕樣式 */
button:last-of-type {
  background: transparent;
  color: #007bff;
  text-decoration: underline;
}

button:last-of-type:hover {
  color: #0056b3;
}

/* 響應式設計 */
@media (max-width: 480px) {
  div {
    padding: 15px;
  }

  h1 {
    font-size: 20px;
  }

  input,
  button {
    font-size: 12px;
    padding: 8px;
  }
}
</style>

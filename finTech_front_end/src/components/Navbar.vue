<template>
  <nav class="navbar">
    <ul>
      <li><router-link to="/day1">股票分析</router-link></li>
      <li><router-link to="/day2">股票定價結果</router-link></li>
      <li><router-link to="/day3-1">本益比河流圖</router-link></li>
      <li><router-link to="/day3-2">天花板地板線</router-link></li>
      <li>
        <a @click="Logout">Logout</a>
      </li>
    </ul>
  </nav>
</template>
<script setup>
import axios from 'axios'

const Logout = async () => {
  try {
    const username = localStorage.getItem('username')
    console.log('username:', username)
    const response = await axios.post('http://localhost:8001/login_manager/logout/', {
      username: username,
    })
    localStorage.removeItem('username')
    console.log('Logout successful!', response.data)

    // 登出成功後跳轉到登入頁
    window.location.href = 'http://localhost:5173'
  } catch (error) {
    console.error('Logout failed:', error)
  }
}
</script>

<style>
/* Navbar Styles */
.navbar {
  position: fixed;
  background-color: #2e8b57; /* 深綠色背景 */
  padding: 10px 20px;
  display: flex;
  justify-content: center;
  align-items: center;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  height: 50px;
  top: 0;
  width: 100%;
  z-index: 1000;
}

.navbar ul {
  list-style: none;
  display: flex;
  gap: 20px;
  margin: 0;
  padding: 0;
}

.navbar li {
  display: inline;
}

.navbar a {
  text-decoration: none;
  background-color: white;
  border: 2px solid #2e8b57;
  border-radius: 5px;
  color: #2e8b57;
  padding: 10px 15px;
  font-weight: bold;
  font-size: 1em;
  transition: all 0.3s ease;
  box-sizing: border-box;
}

.navbar a:hover {
  background-color: #2e8b57;
  color: white;
  cursor: pointer;
}

/* 高亮當前路由 */
.router-link-active {
  background-color: #2e8b57;
  color: white;
}
</style>

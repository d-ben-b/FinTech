<template>
  <nav class="navbar">
    <ul>
      <li><router-link to="/day1">Day1</router-link></li>
      <li><router-link to="/day2">Day2</router-link></li>
      <li><router-link to="/day3-1">Day3-1</router-link></li>
      <li><router-link to="/day3-2">Day3-2</router-link></li>
      <li><router-link to="/day4">Day4</router-link></li>
      <li><router-link to="/day5">Day5</router-link></li>
      <li><router-link to="/logout">Logout</router-link></li>
    </ul>
  </nav>
</template>

<script setup></script>

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
}

/* 高亮當前路由 */
.router-link-active {
  background-color: #2e8b57;
  color: white;
}
</style>

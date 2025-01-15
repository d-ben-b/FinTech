<template>
  <div class="wait-container">
    <h2>查詢中，請稍候...</h2>
    <p>試著點擊動物來消磨時間！</p>

    <div class="game-area">
      <img
        v-for="(animal, index) in animals"
        :key="index"
        :src="animal.src"
        :alt="animal.name"
        class="animal"
        :style="{ top: animal.top + 'px', left: animal.left + 'px' }"
        @click="clickAnimal(index)"
      />
    </div>

    <p class="score">分數: {{ score }}</p>
  </div>
</template>

<script>
import { ref } from 'vue'

export default {
  name: 'Wait',
  setup() {
    const animals = ref([
      { name: 'cat', src: 'https://placekittens.com/50/50', top: 100, left: 100 },
      { name: 'dog', src: 'https://placedog.net/50/50?random', top: 200, left: 200 },
    ])
    const score = ref(0)

    const clickAnimal = (index) => {
      // 隨機移動動物位置
      animals.value[index].top = Math.random() * 300
      animals.value[index].left = Math.random() * 300
      score.value++
    }

    return {
      animals,
      score,
      clickAnimal,
    }
  },
}
</script>

<style scoped>
.wait-container {
  text-align: center;
  font-family: Arial, sans-serif;
}

h2 {
  color: #2c3e50;
}

.game-area {
  position: relative;
  width: 400px;
  height: 400px;
  border: 2px solid #ccc;
  margin: 20px auto;
  border-radius: 10px;
  background-color: #f9f9f9;
  overflow: hidden;
}

.animal {
  position: absolute;
  width: 50px;
  height: 50px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.score {
  font-size: 1.2em;
  color: #28a745;
}
</style>

<script setup lang="ts">
const props = defineProps({
  todos: Array,
});
</script>

<template>
  <div
    className="text-center h-screen flex justify-center flex-col items-center p-4"
  >
    <ul>
      <h1>Todos</h1>

      <li v-for="todo in todos" :key="todo.id">
        {{ todo.name }}
      </li>
    </ul>
  </div>
</template>

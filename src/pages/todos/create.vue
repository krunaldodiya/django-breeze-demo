<script setup lang="ts">
import { useForm } from '@inertiajs/vue3';

const form = useForm({
  name: '',
});

const submit = (e: Event) => {
  form.post('/todos/store', {
    data: { name: form.name },
  });
};
</script>

<template>
  <div
    className="text-center h-screen flex justify-center flex-col items-center p-4"
  >
    <form @submit.prevent="submit">
      <div>
        <input type="text" placeholder="todo name" v-model="form.name" />
      </div>

      <div><button type="submit">add</button></div>
    </form>
  </div>
</template>

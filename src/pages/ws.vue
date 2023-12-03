<script setup lang="ts">
import { useForm } from '@inertiajs/vue3';

const form = useForm({
  message: '',
});

const url = `ws://${window.location.host}/ws/ticker/1`;

const socket = new WebSocket(url);

socket.onopen = () => {
  console.log('WebSocket connected');
};

socket.onerror = (error) => {
  console.error('WebSocket error:', error);
};

socket.onmessage = (event) => {
  console.log('Received message:', event.data);
};

socket.onclose = () => {
  console.log('WebSocket closed');
};

const submit = (e: Event) => {
  const message = JSON.stringify({ message: form.message });
  socket.send(message);
};
</script>

<template>
  <div
    className="text-center h-screen flex justify-center flex-col items-center p-4"
  >
    <form @submit.prevent="submit">
      <div>
        <input
          type="text"
          isFocused="true"
          placeholder="write a message"
          v-model="form.message"
        />
      </div>

      <div>
        <button type="submit">send</button>
      </div>
    </form>
  </div>
</template>

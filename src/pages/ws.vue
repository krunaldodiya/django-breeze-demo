<script setup lang="ts">
import { useForm } from '@inertiajs/vue3';

const form = useForm({
  message: '',
});

const url = `ws://${window.location.host}/ws/ticker/1`;

const websocket = new WebSocket(url);

websocket.onmessage = function (e) {
  const data = JSON.parse(e.data);
  console.log({ data });
};

const submit = (e: Event) => {
  console.log({ message: form.message });
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

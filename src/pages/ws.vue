<template>
  <div
    className="text-center h-screen flex justify-center flex-col items-center p-4"
  >
    chat
  </div>
</template>

<script lang="ts">
const url = `ws://${window.location.host}/ws/ticker`;

const websocket = new WebSocket(url);

websocket.onmessage = function (e) {
  const data = JSON.parse(e.data);
  console.log({ data });
};
</script>

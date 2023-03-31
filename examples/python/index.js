// eslint-disable-next-line import/no-extraneous-dependencies
import { WebSocketHandler } from "dagre-d3-lite";

document.addEventListener("DOMContentLoaded", async () => {
  const handler = new WebSocketHandler();
  await handler.open();
});

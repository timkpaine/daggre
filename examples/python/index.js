// eslint-disable-next-line import/no-extraneous-dependencies
import { Graph, WebSocketClient, JSONTransport } from "dagre-d3-lite";

document.addEventListener("DOMContentLoaded", async () => {
  const jst = new JSONTransport();
  const handler = new WebSocketClient({ transport: jst });

  jst.hosts(Graph);
  try {
    const graph = await handler.initial();
    const div = document.querySelector("div.dagred3");
    graph.render(div);
    await handler.handle();
  } catch {
    // nothing to do
  }
});

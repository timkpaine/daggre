/* eslint-disable */

export class WebSocketHandler {
  constructor(options = {}) {
    this._transport = options.transport;
    this._model = options.model;
    this._config = options.config;

    this._protocol =
      options.protocol || window.location.protocol === "http:" ? "ws:" : "wss:";
    this._host = options.host || window.location.host;
    this._path = options.path || "ws";
    this.open.bind(this);
    this.on_open.bind(this);
    this.on_receive.bind(this);
  }

  async open() {
    this._websocket = new WebSocket(
      `${this._protocol}//${this._host}/${this._path}`,
    );
    this._websocket.onopen = this.on_open;
    this._websocket.onmessage = this.on_receive;
  }

  async on_open(event) {}

  async on_receive(event) {
    document.body.innerHTML = event.data;
    // document.body.innerHTML = JSON.parse(event.data);
  }

  async close() {}

  async on_initial() {}

  async receive() {}

  async send() {}
}

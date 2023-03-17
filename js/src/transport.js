/* eslint-disable */

export class Transport {
  constructor() {}

  async connectAsync(model, client_id, shared, readonly) {}

  async disconnectAsync(client_id) {}

  async initialAsync(client_id) {}

  async sendAsync(client_id) {}

  async receiveAsync(client_id, update) {}
}

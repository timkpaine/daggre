import { Model } from "../transports";

export class Node extends Model {
  static name = "Node";

  constructor(data) {
    super();
    Object.keys(data).forEach((key) => {
      // TODO
      this[key] = data[key];
    });
  }
}

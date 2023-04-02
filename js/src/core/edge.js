import { Model } from "../transports";
import { Node } from "./node";

export class Edge extends Model {
  static name = "Edge";

  constructor(data) {
    super();
    Object.keys(data).forEach((key) => {
      // TODO
      this[key] = data[key];
    });
  }

  static submodels() {
    return [Node];
  }
}

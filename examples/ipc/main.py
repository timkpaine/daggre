import sys
from asyncio import new_event_loop
from threading import Thread
from time import sleep

import uvicorn
import uvloop
from fastapi import FastAPI, WebSocket

sys.path.append("../../python")  # noqa
from daggre import Graph  # noqa: E402
from daggre import (AioHttpWebSocketClient, JSONTransport,
                    StarletteWebSocketServer)


def run_server():
    # create a new event loop here
    loop = new_event_loop()

    # use uvloop
    uvloop.install()

    # create FastAPI app
    app = FastAPI()

    # construct graph routine to match JS example
    graph = Graph(direction="left-to-right")

    # function to add nodes to graph
    def generate_graph():
        SCALE = 10
        begin = 0

        # print initial state
        sleep(1)
        print(f"Server[ Nodes: {len(graph.nodes)} - Edges: {len(graph.edges)} ]")

        while True:
            sleep(5)
            for i in range(begin, begin + SCALE):
                if i > 0:
                    if i % 2 == 0:
                        graph.addNode(f"test{i}", color="red")
                    else:
                        graph.addNode(f"test{i}", backgroundColor="lightblue")
                    graph.addEdge(f"test{i-1}", f"test{i}")
                else:
                    graph.addNode(f"test{i}", backgroundColor="lightgreen")

                if i > 2:
                    for j in range(4):
                        if i % (j + 2) == 0:
                            graph.addEdge(
                                f"test{int(i / (j + 2))}",
                                f"test{i}",
                                arrowhead="vee",
                                line="dash",
                            )
            begin += SCALE
            print(f"Server[ Nodes: {len(graph.nodes)} - Edges: {len(graph.edges)} ]")

    transport = JSONTransport(event_loop=loop)

    @app.websocket("/ws")
    async def websocket_endpoint(websocket: WebSocket):
        handler = StarletteWebSocketServer(websocket=websocket, transport=transport, model=graph)
        await handler.handle()

    Thread(target=uvicorn.run, args=(app,), kwargs={"port": 6000}, daemon=True).start()

    # run forever
    generate_graph()


def run_client():
    # create new loop
    loop = new_event_loop()

    # use uvloop
    uvloop.install()

    async def listen(url="ws://localhost:6000/ws"):
        # create the transport
        transport = JSONTransport(event_loop=loop)

        # host the type
        transport.hosts(Graph)

        # make websocket client
        handler = AioHttpWebSocketClient(url, transport)

        # pull out the initial object
        graph: Graph = await handler.initial()

        def print_graph(graph: Graph):
            while True:
                print(f"Client[ Nodes: {len(graph.nodes)} - Edges: {len(graph.edges)} ]")
                sleep(5)

        t = Thread(target=print_graph, args=(graph,), daemon=True)
        t.start()

        await handler.handle()

    loop.run_until_complete(listen())


if __name__ == "__main__":
    server_thread = Thread(target=run_server, daemon=True)
    client_thread = Thread(target=run_client, daemon=True)

    server_thread.start()
    sleep(2)
    client_thread.start()

    server_thread.join()
    client_thread.join()

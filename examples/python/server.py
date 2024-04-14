import sys
from asyncio import get_event_loop
from random import choice, randint
from threading import Thread
from time import sleep

import uvloop
from fastapi import FastAPI, WebSocket
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

sys.path.append("../../python")  # noqa
from dagred3 import (Graph, JSONTransport,  # noqa: E402
                     StarletteWebSocketServer)


def build_app():
    # use uvloop
    uvloop.install()

    # create FastAPI app
    app = FastAPI()

    # serve index.html at /
    @app.get("/", response_class=FileResponse)
    def index():
        return "index.html"

    # construct graph routine to match JS example
    graph = Graph(direction="left-to-right")

    # function to add nodes to graph
    def generate_graph(graph):
        scale = 10
        begin = 0
        stop = 100
        interval = 0.1

        # start by generating a bunch node nodes
        while begin < stop:
            # add nodes
            for i in range(begin, begin + scale):
                if i > 0:
                    if i % 2 == 0:
                        graph.addNode(f"test{i}", color="red")
                    else:
                        graph.addNode(f"test{i}", backgroundColor="lightblue")
                else:
                    graph.addNode(f"test{i}", backgroundColor="lightgreen")
                sleep(interval)

            # add edges
            for i in range(begin, begin + scale):
                if begin >= scale:
                    graph.addEdge(
                        f"test{i-scale}",
                        f"test{i}",
                        arrowhead="vee",
                        line="dash",
                    )
                elif i > 0:
                    graph.addEdge("test0", f"test{i}")
                sleep(interval)

            # add same level edges
            for i in range(begin + 1, begin + scale):
                graph.addEdge(f"test{i-1}", f"test{i}")
                sleep(interval)

            # shift to next batch
            begin += scale
            sleep(interval)

        # then after just flicker the lights forever
        while True:
            index = randint(0, stop)
            color = choice(["red", "blue", "green", "yellow", "orange", "black", "cyan", "magenta"])
            backgroundColor = choice(["red", "blue", "green", "yellow", "orange", "black", "cyan", "magenta"])
            graph.addNode(f"test{index}", color=color, backgroundColor=backgroundColor)
            sleep(interval)

    t = Thread(target=generate_graph, args=(graph,), daemon=True)
    t.start()

    transport = JSONTransport(event_loop=get_event_loop())

    @app.websocket("/ws")
    async def websocket_endpoint(websocket: WebSocket):
        handler = StarletteWebSocketServer(websocket=websocket, transport=transport, model=graph)
        await handler.handle()

    # mount js assets from js dir
    app.mount("/js/", StaticFiles(directory="../../js"), name="js")

    # mount everything else in this dir after
    app.mount("/", StaticFiles(directory="."))

    return app


app = build_app()

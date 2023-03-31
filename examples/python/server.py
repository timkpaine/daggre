import sys
import uvloop
from asyncio import get_event_loop
from fastapi import FastAPI, WebSocket
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from time import sleep
from threading import Thread


sys.path.append("../../python")  # noqa
from dagred3 import Graph, JSONTransport, StarletteWebSocketServer  # noqa: E402


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
        SCALE = 10
        begin = 0
        while True:
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
            sleep(5)

    t = Thread(target=generate_graph, args=(graph,), daemon=True)
    t.start()

    transport = JSONTransport(event_loop=get_event_loop())

    @app.websocket("/ws")
    async def websocket_endpoint(websocket: WebSocket):
        handler = StarletteWebSocketServer(
            websocket=websocket, transport=transport, model=graph
        )
        await handler.handle()

    # mount js assets from js dir
    app.mount("/js/", StaticFiles(directory="../../js"), name="js")

    # mount everything else in this dir after
    app.mount("/", StaticFiles(directory="."))

    return app


app = build_app()

from server_playground.views import index, delayed, query_strings


def setup_routes(app):
    app.router.add_get("/", index)
    app.router.add_get("/delay", delayed)
    app.router.add_get("/query_strings", query_strings)
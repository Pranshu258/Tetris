import json
from django.http import HttpResponse
from .apps import ServerConfig
from django.views.decorators.http import require_http_methods
from atlas.server import OriginServer

@require_http_methods(["POST"])
async def register(request):
    try:
        data = json.loads(request.body)
        server = data.get('origin_server')
        if server:
            server = OriginServer(**server)
        if not server:
            return HttpResponse("Invalid request - Origin host name not provided.", status=400)
    except Exception as e:
        return HttpResponse(f"Error reading request body: {str(e)}", status=400)
    print(f"Registering server: {server.host}, with weight {server.weight}")
    await ServerConfig.loadbalancer.add_server(server)
    return HttpResponse("Current State: " + str(ServerConfig.loadbalancer))

async def forward(request, path):
    return await ServerConfig.loadbalancer.forward_request(request, path)
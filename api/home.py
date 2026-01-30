"""
API endpoints для главной страницы и информации о API
"""

from fastapi import APIRouter, Request

router = APIRouter()


@router.get("/")
async def get_api_info(request: Request):
    """
    Получить список всех доступных API endpoints

    Returns:
        JSON со списком всех маршрутов и их описаниями
    """
    routes_info = []

    for route in request.app.routes:
        if hasattr(route, "methods") and hasattr(route, "path"):
            if route.path in ["/openapi.json", "/"]:
                continue

            route_info = {
                "path": route.path,
                "methods": list(route.methods),
                "name": route.name,
                "description": route.endpoint.__doc__.strip()
                if route.endpoint.__doc__
                else "Нет описания",
            }
            routes_info.append(route_info)

    # Сортируем по пути
    routes_info.sort(key=lambda x: x["path"])

    return {
        "name": "Michalangelo bot API",
        "version": "1.0.0",
        "total_endpoints": len(routes_info),
        "endpoints": routes_info,
    }

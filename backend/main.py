import os
import mimetypes

from fastapi import (
    FastAPI,
    HTTPException,
)
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException


from apps.v1.main import app as v1_app
from env import CACHE_DIR, STATIC_DIR, FRONTEND_BUILD_DIR

app = FastAPI()


class SPAStaticFiles(StaticFiles):
    async def get_response(self, path: str, scope):
        try:
            return await super().get_response(path, scope)
        except (HTTPException, StarletteHTTPException) as ex:
            if ex.status_code == 404:
                return await super().get_response("index.html", scope)
            else:
                raise ex


# Include the v1 app
app.mount("/api/v1", v1_app)


app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
app.mount("/cache", StaticFiles(directory=CACHE_DIR), name="cache")


if os.path.exists(FRONTEND_BUILD_DIR):
    mimetypes.add_type("text/javascript", ".js")
    app.mount(
        "/",
        SPAStaticFiles(directory=FRONTEND_BUILD_DIR, html=True),
        name="spa-static-files",
    )
else:
    print(
        f"Frontend build directory not found at '{FRONTEND_BUILD_DIR}'. Serving API only."
    )

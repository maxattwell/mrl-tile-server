import os
from fastapi import FastAPI, Response, File, UploadFile
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

origins = [
        "*",
]

app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
)

@app.post("/upload_tiff/")
async def upload_tile(tiff: UploadFile=File()):
    # Check type of file
    print(tiff.content_type)
    if tiff.content_type != "image/tiff":
        return Response(status_code=422)
    tiff_content = await tiff.read()
    tiff_file = open("../uploads/tiff_upload.tiff", "wb")
    tiff_file.write(tiff_content)
    # Generate new tile set
    os.system("gdal2tiles.py --xyz ../uploads/tiff_upload.tiff ../raster-tiles/")
    return Response(status_code=204)

@app.get("/raster_tiles/{z}/{y}/{x}.png")
async def get_tile(z: str, y: str, x: str):
    filepath = '../raster-tiles/%s/%s/%s.png' % (z, y, x)
    if os.path.isfile(filepath):
        return FileResponse(filepath)
    return Response(status_code=204)

# =============================================
# PROXY IMPLEMENTATION
# =============================================

# def _proxy(z, y, x):
#     t_resp = requests.request(
#         method="GET",
#         url = 'https://ibasemaps-api.arcgis.com/arcgis/rest/services/World_Imagery/MapServer/tile/{z}/{x}/{y}?token=AAPKa25367b955cb4757970c8c423f0b70a9JX_PBjQbZU5NpCVPFngauXXugPVoS6HttCW1S8_6TVMn6t2zyj7MNXhmABKJkbxV'.format(z=z, y=y, x=x),
#         allow_redirects=False)
#     response = Response(content=t_resp.content, status_code=t_resp.status_code)
#     return response
#
# @app.get("/raster_tiles/{z}/{y}/{x}.png")
# async def get_tile_using_proxy(z: str, y: str, x: str):
#     filepath = '../raster-tiles/%s/%s/%s.png' % (z, y, x)
#     if os.path.isfile(filepath):
#         return FileResponse(filepath)
#     return _proxy(z, y, x)

# =============================================


@app.get("/")
async def healthcheck():
    return Response(status_code=204)


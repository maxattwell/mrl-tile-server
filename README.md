# mrl-tile-server
## Running the tile server
- In the rest-api directory run `uvicorn main:app --reload`
## Uploading a raster tile
1. Start with a .jpg and .jwg file that have the same name.
2. Translate to geotiff format with the following command
    "gdal_translate -if JPEG -of GTiff -a_srs EPSG:3857 <name-of-input-file>.jpg <name-of-output-file>.tif"
        + '-if' flag defines the input drive format for JPEG/JFIF (uses a .jpg and a .jgw file)
2a. Merging tif files.
  Move gdal_merge.py script into directory containing tifs to merge 
  Run: 
    "gdal_merge.py -o <name-of-output-file>.tif <name-of-input-file-1>.tif <name-of-input-file-N>.tif"
3. Send a POST request to the `/upload_tiff` where the server is running, with the newly created .tiff file as form data under the name 'tiff'
Note: will likely have to refresh and clear the cache on the client side to see the newly uploaded tile.
## Tech Stack
1. GDAL
    - Installation: https://mothergeo-py.readthedocs.io/en/latest/development/how-to/gdal-ubuntu-pkg.html
    - Geospatial data abstraction library
    - Used for writing raster formats
    - Commands:
        - 'gdalinfo' give info on a geo image file eg. .tif or .jpg with .jgw
        - 'gdal_translate' switched between different filetypes
        - 'gdal_warp' allow the projection type of a geofile to be changed
        - 'gdal2tile.py' a script to transform .tif files into a tileset that can be used by a tile server
        - 'gdal_merge.py' a script used to combine multiple tiffs into a single tiff file.
2. Geotiff
    - file type which allows georeferencing
3. Qgis (optional)
    - desktop  geographic information system application to
    view and edit geospatial data
- Projections:
    + EPSG:3857 (Spherical/Web Mercator) commonly used for web mapping
    + EPSG:4326 (Lat/Long) based on Earths center of mass and used by GPS
- JGW file type description:
    JGW and TFW files contain geographic information on bitmaps, are ASCII text
    files describing the location, scale and orientation of and image.
    They should be stored in the same directory as a JPG image with the same
    name.
    + line 1: length of a pixel in the x direction (horizontal)
    + line 2: angle of rotation  (usually 0 or ignored)
    + line 3: angle of rotation  (usually 0 or ignored)
    + line 4: _negative_ length of a pixel in the y direction (vertical)
    + line 5: x coordinate at the center of the pixel in the top left corner of the image
    + line 6: y coordinate at the center of the pixel in the top left corner of the image
## Gameplan
1. Create geoTiff files from images and geodata.
 a) Start with jpg and jgw files of the same name
 b) translate to geotiff format with the following command
    "gdal_translate -if JPEG -of GTiff -a_srs EPSG:3857 <name-of-input-file>.jpg <name-of-output-file>.tif"
        + '-if' flag defines the input drive format for JPEG/JFIF (uses a .jpg and a .jgw file)
        + '-of' flag defines the output driver format GeoTiff
        + '-a_srs' flag defines the projection to be used
2. Create tileset from geotiff file
    a) Make empty directory to store tiles "mkdir <name-of-tileset-dir>"
    b) move gdal2tiles.py script into parent directory??
    c) run gdal2tiles.py script to create tile set
        "gdal2tiles.py --xyz <name-of-geotiff-file>.tif <name-of-tileset-dir>/"
            + '-xyz' flag generates xyz (OSM Slippy Map standard) instead of TMS. [TMS y=0 for southern-most tile, OSM y=0 for northern-most tiles]
3. Merge the tilesets
    - Just use gdal2tiles.py again and it will automatically merge them into the original tileset directory
    Note: I think it will use the most recent if there are two in the same location
4. Run a tileset server
    - Have copied a basic tile server using Flask
    - Look into fastAPI to make a proper one
5. Create an endpoint that will accept a tiff and add it to the tile set
6. Clean up tile server
    - add attribution
    - separate function to add tiff to tile set. Still async
    - add things to readme (check mrl backend)
7.

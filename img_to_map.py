import sys
from PIL import Image

def cropMapTiles(image_path):
    """
    Crop map tiles from a single image into individual images

    Parameters
    -----
    image_path: str : Path tot the image containing all the map tiles

    Returns
    -----
    List[PIL.Image] : List of cropped tiles
    """
    img = Image.open(image_path)
    tiles = []

    # crop first column (corner tiles) 1063px
    first_col = img.crop((0, 1479, 1063, 5807))
    # the space between each row is 24px and each row is 1064px high, 4 rows total
    tiles.extend([first_col.crop((0, i*1064+ i*24, 1064, i*1064+ i*24+1063)) for i in range(4)])


    for i in range(5):
        # crop center columns (street tiles)
        first_col = img.crop((1077+i*(709+35), 0, 1076+(i+1)*(709+35)-35, 6502))
        # the space between each row is 24px and each row is 1064px high, 6 rows total
        tiles.extend([first_col.crop((0, i*1064+i*24, 709, i*1064+ i*24+1063)) for i in range(6)])
    tiles.append(img.crop((4797,2176,5506,3239)))
    tiles.append(img.crop((4797,3264,5506,4327)))
    return tiles

def createImgFromTiles(tiles, output_path, center_img_path, background_color="white"):
    """
    Create a monopoly board from individual map tiles.

    Parameters
    -----
    tiles: List[PIL.Image] : List containing the individual tiles to be combined into a single image
    output_path: str : Path to save the result image (e.g. "outputs/map.png")
    center_img_path: str : Path to the image that will be displayed in the center of the board, can be None
    background_color: str : Color of the background
    """
    width = 9*709+2*1063
    map_image = Image.new('RGB', (width, width), background_color)

    # create bottom row
    map_image.paste(tiles[1], (0,7446))
    map_image.paste(tiles[8], (1064,7446))
    map_image.paste(tiles[7], (1774,7446))
    map_image.paste(tiles[34],(2483,7446))
    map_image.paste(tiles[6], (3192,7446))
    map_image.paste(tiles[27],(3901,7446))
    map_image.paste(tiles[32],(4610,7446))
    map_image.paste(tiles[5], (5319,7446))
    map_image.paste(tiles[35],(6028,7446))
    map_image.paste(tiles[4], (6737,7446))
    map_image.paste(tiles[0], (7446,7446))

    # create left column
    map_image.paste(tiles[2].rotate(-90, expand=True),  (0,0))
    map_image.paste(tiles[14].rotate(-90, expand=True), (0,1064))
    map_image.paste(tiles[13].rotate(-90, expand=True), (0,1774))
    map_image.paste(tiles[35].rotate(-90, expand=True), (0,2483))
    map_image.paste(tiles[12].rotate(-90, expand=True), (0,3192))
    map_image.paste(tiles[28].rotate(-90, expand=True), (0,3901))
    map_image.paste(tiles[11].rotate(-90, expand=True), (0,4610))
    map_image.paste(tiles[10].rotate(-90, expand=True), (0,5319))
    map_image.paste(tiles[30].rotate(-90, expand=True), (0,6028))
    map_image.paste(tiles[9].rotate(-90, expand=True),  (0,6737))

    # create top row
    map_image.paste(tiles[15].rotate(180, expand=True), (1064,0))
    map_image.paste(tiles[34].rotate(180, expand=True), (1774,0))
    map_image.paste(tiles[16].rotate(180, expand=True), (2483,0))
    map_image.paste(tiles[17].rotate(180, expand=True), (3192,0))
    map_image.paste(tiles[29].rotate(180, expand=True), (3901,0))
    map_image.paste(tiles[18].rotate(180, expand=True), (4610,0))
    map_image.paste(tiles[19].rotate(180, expand=True), (5319,0))
    map_image.paste(tiles[31].rotate(180, expand=True), (6028,0))
    map_image.paste(tiles[20].rotate(180, expand=True), (6737,0))
    map_image.paste(tiles[3].rotate(180, expand=True), (7446,0))

    # create right column
    map_image.paste(tiles[21].rotate(90, expand=True), (7446,1064))
    map_image.paste(tiles[22].rotate(90, expand=True), (7446,1774))
    map_image.paste(tiles[35].rotate(90, expand=True), (7446,2483))
    map_image.paste(tiles[23].rotate(90, expand=True), (7446,3192))
    map_image.paste(tiles[26].rotate(90, expand=True), (7446,3901))
    map_image.paste(tiles[34].rotate(90, expand=True), (7446,4610))
    map_image.paste(tiles[24].rotate(90, expand=True), (7446,5319))
    map_image.paste(tiles[33].rotate(90, expand=True), (7446,6028))
    map_image.paste(tiles[25].rotate(90, expand=True), (7446,6737))

    if center_img_path:
        center_img = Image.open(center_img_path)
        map_image.paste(center_img.resize((width-2*1063, width-2*1063)), (1064,1064))

    if output_path:
        map_image.save(output_path)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python img_to_map.py tiles.png output_path <background image path> <background color>")
    else:
        mapTilePath = sys.argv[1]
        output_path = sys.argv[2]
        backgroundImagePath = sys.argv[3] if len(sys.argv) >= 4 else None
        backgroundColor =  sys.argv[4] if len(sys.argv) >=5 else None

        tiles = cropMapTiles(mapTilePath)
        createImgFromTiles(tiles, output_path, backgroundImagePath, backgroundColor)

        print(f"Map saved as {output_path}")
import bs4
from pathlib import Path
from PIL import Image
import os
from collections.abc import Sequence
from typing import cast

# def hello(string: str) -> str:
#     """Returns a string with a greeting."""
#     return f"Hello, {string}!"

class TMXpy:
    spriteSheetFolderPaths: Sequence[Path|str] = []
    inputFile: bs4.BeautifulSoup
    tileDimensions: tuple[int, int] = (0, 0)
    tmxDimensions: tuple[int, int] = (0, 0)
    tiles: dict = {}

    def __init__(self, sheets: Sequence[Path|str], path: str | Path = '', xml: str = ''):
        """Initializes the TMXpy class"""
        
        if path != '':
            self.path = path
            self.inputFile = bs4.BeautifulSoup(open(path), "xml")
        elif xml != '':
            self.inputFile = bs4.BeautifulSoup(xml, "xml")
        else:
            raise Exception("TMXpy: No path or xml given")

        self.spriteSheetFolderPaths = sheets
    
    def generateGIDDict(self) -> None:
        """Generates a dictionary of GIDs to tile information"""
        tilesets = self.inputFile.find_all("tileset")
        layer1 = cast(dict, self.inputFile.find('layer'))

        

        self.tmxDimensions = (int(layer1['width']), int(layer1['height']))
        for tileset in tilesets:
            self.tileDimensions = (int(tileset["tilewidth"]), int(tileset["tileheight"]))
            src = tileset.find("image")["source"]

            for i in range(int(tileset["firstgid"]), int(tileset["tilecount"]) + int(tileset["firstgid"])):
                #<tileset firstgid="33" name="untitled tile sheet" tilewidth="16" tileheight="16" tilecount="1975" columns="25">
                self.tiles[str(i)] = {
                    "src": src,
                    "x": int((i - int(tileset["firstgid"])) % int(tileset["columns"])),
                    "y": int((i - int(tileset["firstgid"])) / int(tileset["columns"])),
                    "width": int(tileset["tilewidth"]),
                    "height": int(tileset["tileheight"])
                }

    def renderTile(self, gid: str) -> Image.Image:
        """Renders a tile from the TMX file"""
        tile = self.tiles[gid]
        
        #path = os.path.join(self.spriteSheetFolderPaths[0], tile["src"]) + ".png"
        for path in self.spriteSheetFolderPaths:
            if os.path.exists(os.path.join(path, tile["src"] + ".png")):
                path = os.path.join(path, tile["src"]) + ".png"
                break
        else:
            raise Exception(f"TMXpy: Could not find tileset {tile['src']} in any of the given paths {self.spriteSheetFolderPaths}")
        tilesheet = Image.open(path)
        
        tile = tilesheet.crop((tile["x"] * tile["width"], tile["y"] * tile["height"], tile["x"] * tile["width"] + tile["width"], tile["y"] * tile["height"] + tile["height"]))
        return tile

    def renderLayer(self, layerID: int) -> Image.Image:
        """Renders a layer in the TMX file"""
        
        layers = self.inputFile.find_all("layer")
        # print(layers)
        layer = layers[layerID]
        # self.tmxDimensions = (int(layer['width']), int(layer['height']))
        tiles = layer.text.split(",")

        img = Image.new("RGBA", 
            (int(layer['width']) * int(self.tileDimensions[0]),
                int(layer['height']) * int(self.tileDimensions[1])))

        for i, tile in enumerate(tiles):
            tile = tile.strip()
            if tile == "0":
                continue
            img.paste(self.renderTile(tile), (int(i % int(layer['width'])) * int(self.tileDimensions[0]), int(i / int(layer['width'])) * int(self.tileDimensions[1])))

        return img
    
    def renderAllLayers(self, blocked: list[str] = []) -> Image.Image:
        """Renders all layers in the TMX file, except for the ones in the blocked list"""
        width = int(self.tmxDimensions[0]) * int(self.tileDimensions[0])
        height = int(self.tmxDimensions[1]) * int(self.tileDimensions[1])
        img = Image.new("RGBA", (width, height))



        
        for i, layer in enumerate(self.inputFile.find_all("layer")):
            if layer['name'] in blocked or str(i) in blocked or i in blocked:
                print(f'Skipping layer {layer["name"]} - {i}')
                continue
            print(f'Rendering layer {layer["name"]} - {i}')
            layer = self.renderLayer(i)
            #stick it on top of the last layer, and not overwriting the transparent pixels
            img.paste(layer, (0, 0), layer)
            print(f'Layer {i} rendered, layer width: {layer.width}, layer height: {layer.height} - img width: {width}, img height: {height}')
        return img
            



        
        


        



    
    
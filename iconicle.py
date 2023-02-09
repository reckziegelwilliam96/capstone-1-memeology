
import os
from PIL import Image

class Iconicle():

    def __init__(self):
        self.image_dir = "images"
        self.tile_dir = "tiles"
        self.image = self.open_image()
        self.phrase = self.get_filename()
        self.words = """get words from phrase"""
        self.board = []


    def open_image(self):
        image_files = [f for f in os.listdir(self.image_dir) if f.endswith(".png")]
        if image_files:
            return os.path.join(self.image_dir, image_files[0])
        else:
            raise FileNotFoundError("No image files found in directory")
    
    def get_filename(self):
        """Get Image Name from image directory."""
        image_files = [f for f in os.listdir(self.image_dir) if f.endswith(".png")]
        if image_files:
            return image_files[0]

    def split_image(self):
        """Split image src into 16 tiles and save."""
        img = Image.open(self.image)

        width, height = img.size

        tile_size = int(width / 4), int(height / 4)

        for row in range(4):
            for col in range(4):
                left = col * tile_size[0]
                upper = row * tile_size[1]
                right = left + tile_size[0]
                lower = upper + tile_size[1]

                tile = img.crop((left, upper, right, lower))
                tile.save(os.path.join(self.tile_dir, "tile_{}_{}.png".format(row, col)))
    
    def make_board(self):
        """Append board to game, only displaying board """

        self.split_image()
        return self.board

    def check_value(self, form, word):
        """Check form value and compare to meme words."""
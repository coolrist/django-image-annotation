from a0_image_annotation import settings
import skimage as ski
import matplotlib.pyplot as plt
import matplotlib.figure as mfg
import io, base64
from urllib import parse

class ImageContrast:
    """
    This class allows us to annotate images by enhancing contrast and visualizing data more easily
    """

    __effects = {
        'sequential1' : ['viridis', 'plasma', 'inferno', 'magma', 'cividis'],
        'sequential2' : ['Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds', 'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd',
                            'RdPu', 'BuPu', 'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn'],
        'sequential3' : ['binary', 'gist_yarg', 'gist_gray', 'gray', 'bone', 'pink', 'spring', 'summer', 'autumn',
                            'winter', 'cool', 'Wistia', 'hot', 'afmhot', 'gist_heat', 'copper'],
        'diverging' : ['PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu', 'RdYlBu', 'RdYlGn', 'Spectral', 'coolwarm',
                        'bwr', 'seismic'],
        'cyclic' : ['twilight', 'twilight_shifted', 'hsv'],
        'qualitative' : ['Pastel1', 'Pastel2', 'Paired', 'Accent', 'Dark2', 'Set1', 'Set2', 'Set3', 'tab10', 'tab20',
                            'tab20b', 'tab20c'],
        'miscellaneous' : ['flag', 'prism', 'ocean', 'gist_earth', 'terrain', 'gist_stern', 'gnuplot', 'gnuplot2',
                'CMRmap', 'cubehelix', 'brg', 'gist_rainbow', 'rainbow', 'jet', 'turbo', 'nipy_spectral', 'gist_ncar'],
    }
    
    def __init__(self, image: str) -> None:
        my_image = plt.imread(f"{settings.MEDIA_ROOT}/..{image}")
        self.image = ski.util.img_as_float64(my_image)

    def get_effects(self) -> dict:
        """
        This method returns a dictionary of different contrast effects
        """
        return self.__effects

    def demos(self):
        """
        This method returns the original image
        """
        imgplot = plt.imshow(self.image)
        return self.__render_image(imgplot.figure)
                
    def pseudocolor(self, effect: str):
        """
        This method returns an image with a specific contrast effect
        -------------------
        PARAM
        effect: A specific contrast effect in the dictionary returned by the function self.get_effects()
        """
        image = self.image[:, :, 0]

        imgplot = plt.imshow(image, effect)
        plt.colorbar()
        plt.title(effect.title())
        return self.__render_image(imgplot.figure)
    
    def other(self):
        """
        This method convert BGR to RGB or vice versa
        """
        image = self.image[:, :, ::-1]
        imgplot = plt.imshow(image)
        return self.__render_image(imgplot.figure)
    
    def __render_image(self, image: mfg.Figure) -> str:
        """
        This method returns the image directory path
        """      
        fig = image
        buffer = io.BytesIO()
        fig.savefig(buffer, format='png')
        buffer.seek(0)
        plt.close()
        return parse.quote(base64.b64encode(buffer.read()))
        
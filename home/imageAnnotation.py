from app import settings
from urllib import parse
from ultralytics import YOLO
from PIL import Image
import skimage as ski
import io, base64

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.figure as mfg


class ObjectDetector:
    """
    This class allows us to detect objects on an image and add annotations using the YOLOv8 model
    """
    def __init__(self, image: str) -> None:
        self.image = f"{settings.MEDIA_ROOT}/..{image}"
        self.__model = YOLO('yolov8n.pt')        

    def get_annotated_images(self):
        """
        This method implements object detection on the image and generates an annotated version accordingly
        """
        annotated_images_path = []
        results = self.__model.predict(self.image, imgsz=1024)

        for result in results:
            # Plot results image
            img_bgr = result.plot() # BGR-order numpy array
            img_rgb = Image.fromarray(img_bgr[..., ::-1])   # RGB-order PIL image
            annotated_images_path.append(self.__render_image_to_base64(img_rgb))

        return annotated_images_path
    
    def __render_image_to_base64(self, image: Image) -> str:
        """
        Convert Image to Base64
        """
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        return parse.quote(base64.b64encode(buffer.getvalue()))



class ImageContrast:
    """
    This class allows us to improve the contrast of images and view them more easily
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
        return self.__render_figure_to_base64(imgplot.figure)
                
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
        return self.__render_figure_to_base64(imgplot.figure)
    
    def other(self):
        """
        This method convert BGR to RGB or vice versa
        """
        image = self.image[:, :, ::-1]
        imgplot = plt.imshow(image)
        return self.__render_figure_to_base64(imgplot.figure)
    
    def __render_figure_to_base64(self, image: mfg.Figure) -> str:
        """
        This method returns the image directory path
        """      
        fig = image
        buffer = io.BytesIO()
        fig.savefig(buffer, format='png')
        buffer.seek(0)
        plt.close()
        return parse.quote(base64.b64encode(buffer.read()))
        
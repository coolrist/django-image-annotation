from django.shortcuts import render, redirect
from django.urls import reverse
from django.db.models import Max
from django.core.files.storage import FileSystemStorage
from app import settings
from .imageAnnotation import ImageContrast, ObjectDetector
from .models import Image
from .utils import is_number

import time, random

# Create your views here.

# Home page function
def homepage(request):
    return render(request, 'homepage.html', {"my_images": Image.objects.all().values()})

# Image adding page function
def image_adding(request):
    if request.method == 'POST':
        image_to_add = request.FILES["image_to_add"]
        
        image_validation, extension = False, str.lower(image_to_add.content_type)
        file_type = ["image/gif", "image/jpeg", "image/png", "image/tiff"]

        try:
            file_type.index(extension)
            image_validation = True
        except ValueError:
            pass
        
        if image_validation:
            extension = extension.removeprefix('image/')

            fs = FileSystemStorage()
            image_name=f"{int(time.time())}.{extension}"
            
            file = fs.save(f"{settings.MEDIA_ROOT}/image/{image_name}", image_to_add)
            image_path = fs.url(file)

            image_model = Image(name=image_name, path=image_path)
            image_model.save()

            context = {
                "image_path": image_path,
                "image_id":Image.objects.aggregate(Max('id'))['id__max']
            }
            return render(request, 'image_adding.html', context)
            
    return redirect(reverse('home'))

# Image annotation page function
def image_annotation(request):
    if request.method == 'POST':
        image_to_annotate = request.POST['image_to_annotate']

        if is_number(image_to_annotate):
            image = Image.objects.filter(id=image_to_annotate)
            
            if len(image) > 0:
                renderings = []
                for i in range(len(image)):
                    contrasting_images = []                    
                    img_contrast, img_annotated = ImageContrast(image[i].path), ObjectDetector(image[i].path)
                    
                    contrasting_images.append(img_contrast.other())                   
                    for key, x in img_contrast.get_effects().items():
                        contrasting_images.append(img_contrast.pseudocolor(random.choice(x)))

                    renderings.append({
                        "main_image": img_contrast.demos(),
                        "annotated_images": img_annotated.get_annotated_images(),
                        "contrasting_images": contrasting_images})
                
                return render(request, 'image_annotation.html', {"renderings": renderings})
    
    return redirect(reverse('home'))

# Image removing page function
def image_removing (request):
    if request.method == 'POST':
        image_to_remove = request.POST['image_to_remove']

        if is_number(image_to_remove):
            image = Image.objects.filter(id=image_to_remove).first()

            fs = FileSystemStorage()
            fs.delete(f"{settings.MEDIA_ROOT}/..{image.path}")
            
            image.delete()
    
    return redirect(reverse('home'))

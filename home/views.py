from django.shortcuts import render, redirect
from django.urls import reverse
from django.db.models import Max
from django.core.files.storage import FileSystemStorage
import time, random
from a0_image_annotation import settings
from .imageAnnotation import ImageContrast
from .models import Image
from .utils import is_number

import django.core.files.uploadedfile as dup
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
                graph, img_contrast = [], ImageContrast(image[0].path)

                try:
                    graph.append(img_contrast.demos())
                    for key, x in img_contrast.get_effects().items():
                        graph.append(img_contrast.pseudocolor(random.choice(x)))
                    graph.append(img_contrast.other())
                except RuntimeError:
                    print("Something went wrong! You must restart this app 🫠")
                
                return render(request, 'image_annotation.html', {"graph": graph})
    
    return redirect(reverse('home'))

# Image removing page function
def image_removing (request):
    if request.method == 'POST':
        image_to_remove = request.POST['image_to_remove']

        if is_number(image_to_remove):
            image = Image.objects.filter(id=image_to_remove).first()
            print(image.path)

            fs = FileSystemStorage()
            fs.delete(f"{settings.MEDIA_ROOT}/..{image.path}")
            
            image.delete()
    
    return redirect(reverse('home'))

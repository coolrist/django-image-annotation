from django.shortcuts import render, redirect
from django.urls import reverse
from django.db.models import Max
from django.core.files.storage import FileSystemStorage
import time, random
from a0_image_annotation import settings
from .ImageAnnotation import ImageAnnotation
from .models import Image
from .utils import is_number

# Create your views here.

def homepage(request):
    return render(request, 'homepage.html', {"my_images": Image.objects.all().values()})

def image_adding(request):
    if request.method == 'POST':
        image_to_add = request.FILES["image_to_add"]

        image_validation = False
        for file_type in ["image/gif", "image/jpeg", "image/png", "image/tiff", "image/svg+xml"]:
            if str.lower(image_to_add.content_type) == file_type:
                image_validation = True
                break
        
        if image_validation:
            fs = FileSystemStorage()
            image_name=f"{int(time.time())}_{image_to_add.name}"
            
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

def image_annotation(request):
    if request.method == 'POST':
        image_to_annotate = request.POST['image_to_annotate']

        if is_number(image_to_annotate):
            image = Image.objects.filter(id=image_to_annotate)
            
            if len(image) > 0:        
                graph, img_annotation = [], ImageAnnotation(image[0].path)

                try:
                    graph.append(img_annotation.demos())
                    for key, x in img_annotation.get_effects().items():
                        graph.append(img_annotation.pseudocolor(random.choice(x)))
                    graph.append(img_annotation.other())
                except RuntimeError:
                    print("Something went wrong! You must restart this app 🫠")
                
                return render(request, 'image_annotation.html', {"graph": graph})
    
    return redirect(reverse('home'))


                                

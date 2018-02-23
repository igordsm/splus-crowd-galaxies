from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse

from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.contrib import messages

from .models import GalaxyImage, GalaxyClassification

from django.forms.models import ModelForm



def index(request):
    return render(request, 'index.html')
   
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            pwd = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=pwd)
            login(request, user)
            return redirect('core:dashboard')
    else: 
        form = UserCreationForm()
    return  render(request, 'signup.html', {'form': form})


@login_required
def user_dashboard(request):
    if request.user.profile.completed_tutorial:
        return render(request, 'dashboard.html')
    return redirect('core:tutorial')
    

class ClassificationForm(ModelForm):
    class Meta:
        model = GalaxyClassification
        fields = ('galaxy_type',)


@login_required
def classify_image(request):
    if request.method == 'GET':
        my_images = GalaxyClassification.objects.filter(user=request.user)
        images_to_classify = GalaxyImage.objects.exclude(tutorial_image=True).exclude(id__in=my_images.values_list('image', flat=True)).filter(is_consensus=False)
        print(my_images, images_to_classify)
        gal = images_to_classify.order_by('?')
        if gal.exists():
            gal = gal.first()
            print(gal.is_consensus, gal.tutorial_image)
            form = ClassificationForm({'image': gal, 'user': request.user})
            return render(request, 'classify_galaxy.html', {'galaxy': gal, 'form': form})
        else:
            return render(request, 'classify_galaxy.html', {'no_galaxy': True})
    else:
        galaxy_id = request.POST.get('galaxy_id')
        gal = GalaxyImage.objects.get(id=galaxy_id)
        gal_class = GalaxyClassification(user=request.user, image=gal, galaxy_type=request.POST['galaxy_type'])
        gal_class.save()
        return redirect('core:classify')

@login_required
def my_contributions(request):
    info = {'images_classified': GalaxyClassification.objects.filter(user=request.user).count()}
    if 'json' in request.GET and request.GET['json'] == 1:
        return JsonResponse(info)
    else:
        return render(request, 'my_contributions.html', info)

@login_required
def project_status(request):
    info = {'images_posted': GalaxyImage.objects.count()}
    if 'json' in request.GET and request.GET['json'] == 1:
        return JsonResponse(info)
    else:
        return render(request, 'project_status.html', info)


@login_required
def tutorial(request):
    if 'image_num' in request.GET:
        image_num = int(request.GET['image_num'])
        
        image = GalaxyImage.objects.filter(tutorial_image=True)
        count = image.count()
        if image_num >= count:
            request.user.profile.completed_tutorial = True
            request.user.profile.save()
            messages.add_message(request, messages.INFO, 'Você completou o tutorial!')
            return redirect('core:dashboard')        
        
        return render(request, 'tutorial.html', {'galaxy': image[image_num], 'next': image_num+1})
    else:
        return render(request, 'tutorial.html')


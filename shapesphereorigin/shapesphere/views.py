from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
from .models import KullaniciBilgileri
from django.urls import reverse
from .models import Contact
import requests
from django.http import JsonResponse
from django.core.cache import cache
from django.http import JsonResponse
from django.views.decorators.cache import cache_page


def cache_test_view(request):
    # Cache'e bir değer kaydediyoruz
    cache.set('my_key', 'Hello from Redis!', timeout=60)  # 60 saniye boyunca cache'te kalacak
    
    # Cache'den değeri okuyoruz
    value = cache.get('my_key')

    return JsonResponse({'cached_value': value})
def generate_llm_response(request):
    prompt = request.GET.get("prompt", "Merhaba!")
    response = requests.post(
        "http://ollama-llm:11434/api/generate",
        json={
            "model": "smollm2:360m",
            "prompt": prompt,
            "stream": False
        }
    )

    return JsonResponse(response.json())
def custom_logout(request):
    logout(request)
    return redirect(reverse('index'))
@cache_page(60 * 5)
def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            print("Form submitted")  
            return redirect('login')  # Redirect to login page
        else:
            print("Form is not valid")  
            print(form.errors)
    else:
        form = UserCreationForm()
    
    return render(request, 'register.html', {'form': form})
@login_required
def beginner(request):
    if request.method == 'POST':
        isim = request.POST.get('isim')
        soyisim = request.POST.get('soyisim')
        program = 'BEGINNER'
        telefon = request.POST.get('telefon')
        kredi_karti_numarasi = request.POST.get('kredi_karti_numarasi')
        son_kullanma_tarihi = request.POST.get('son_kullanma_tarihi')
        cvv = request.POST.get('cvv')
        
       
        yeni_kullanici = KullaniciBilgileri(
            isim=isim,
            soyisim=soyisim,
            program=program,
            telefon=telefon,
            kredi_karti_numarasi=kredi_karti_numarasi,
            son_kullanma_tarihi=son_kullanma_tarihi,
            cvv=cvv
        )
        yeni_kullanici.save()

        response = f"""
        <h1>Success</h1>
        """
        return HttpResponse(response)

       
    return render(request, 'beginner.html')
@login_required
def intermediate(request):
    if request.method == 'POST':
        isim = request.POST.get('isim')
        soyisim = request.POST.get('soyisim')
        program = 'INTERMEDIATE'
        telefon = request.POST.get('telefon')
        kredi_karti_numarasi = request.POST.get('kredi_karti_numarasi')
        son_kullanma_tarihi = request.POST.get('son_kullanma_tarihi')
        cvv = request.POST.get('cvv')
        
       
        yeni_kullanici = KullaniciBilgileri(
            isim=isim,
            soyisim=soyisim,
            program=program,
            telefon=telefon,
            kredi_karti_numarasi=kredi_karti_numarasi,
            son_kullanma_tarihi=son_kullanma_tarihi,
            cvv=cvv
        )
        yeni_kullanici.save()

        response = f"""
        <h1>Success</h1>
        """
        return HttpResponse(response)

       
    return render(request, 'intermediate.html')
@login_required
def advanced(request):
    if request.method == 'POST':
        isim = request.POST.get('isim')
        soyisim = request.POST.get('soyisim')
        program = 'ADVANCED'
        telefon = request.POST.get('telefon')
        kredi_karti_numarasi = request.POST.get('kredi_karti_numarasi')
        son_kullanma_tarihi = request.POST.get('son_kullanma_tarihi')
        cvv = request.POST.get('cvv')
        
       
        yeni_kullanici = KullaniciBilgileri(
            isim=isim,
            soyisim=soyisim,
            program=program,
            telefon=telefon,
            kredi_karti_numarasi=kredi_karti_numarasi,
            son_kullanma_tarihi=son_kullanma_tarihi,
            cvv=cvv
        )
        yeni_kullanici.save()

        response = f"""
        <h1>Success</h1>
        """
        return HttpResponse(response)
    return render(request, 'advanced.html')
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm(request, initial={'username': ''})  

    return render(request, 'login.html', {'form': form})

def contact_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        name = request.POST.get('name')
        message = request.POST.get('message')
        
        
        contact = Contact(email=email, name=name, message=message)
        contact.save()
        
        return HttpResponse(f"Thank you {name}, your message has been received.")
    
    return render(request, 'contact.html')

def logout_request(request):
	logout(request)
	return redirect('login')
	

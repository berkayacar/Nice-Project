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
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import ChatMessage
from .models import Product
from django.shortcuts import render, redirect
import json
from django.http import JsonResponse
from .models import Product

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import Product
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from .models import Order, Cart
from .models import Cart


@login_required
def submit_order(request):
    if request.method == 'POST':
        Order.objects.create(
            user=request.user,
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            country=request.POST['country'],
            address=request.POST['address'],
            phone=request.POST['phone'],
            email=request.POST['email'],
            order_notes=request.POST.get('order_notes', '')
        )
        Cart.objects.filter(user=request.user).delete()
        user_cart = Cart.objects.filter(user=request.user)
        total_price = sum(cart_item.product.price for cart_item in user_cart)  # sepeti temizle
        return render(request, 'check.html', {'cart_items': user_cart, 'total_price': total_price}) 
    user_cart = Cart.objects.filter(user=request.user)     # başarılı sayfasına yönlendirme
    total_price = sum(cart_item.product.price for cart_item in user_cart)
    return render(request, 'check.html', {'cart_items': user_cart, 'total_price': total_price})
    
    
def check(request):
    user_cart = Cart.objects.filter(user=request.user)
    total_price = sum(cart_item.product.price for cart_item in user_cart)
    return render(request, 'check.html', {'cart_items': user_cart, 'total_price': total_price})

@csrf_exempt
def add_to_cart(request):
    if request.method == 'POST':
        try:
            
            data = json.loads(request.body)  
            product_name = data.get('product_name')
            product_description = data.get('product_description')
            product_price = data.get('product_price')
            product_image = data.get('product_image')

         
            if not request.user.is_authenticated:
                return JsonResponse({'message': 'Kullanıcı giriş yapmamış.'}, status=401)
            
            user = request.user  

           
            if not product_name or not product_price or not product_image:
                return JsonResponse({'message': 'Product name, price, and image are required.'}, status=400)

           
            product = Product.objects.create(
                user=user,  
                name=product_name,
                description=product_description,
                price=product_price,
                image=product_image  
            )
            Cart.objects.create(user=user, product=product)
           
            return JsonResponse({'message': 'Ürün başarıyla eklendi!', 'product_id': product.id}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON format.'}, status=400)

        except Exception as e:
            return JsonResponse({'message': str(e)}, status=500)

    return JsonResponse({'message': 'Invalid method'}, status=400)



def products(request):
    
    return render(request, 'products.html')
# views.py Django
@login_required
def cart(request):
    user_cart = Cart.objects.filter(user=request.user)  
    total_price = sum(cart_item.product.price for cart_item in user_cart) 
    return render(request, 'cart.html', {'cart_items': user_cart, 'total_price': total_price})
    
def cache_test_view(request):
    
    cache.set('my_key', 'Hello from Redis!', timeout=60) 
    
   
    value = cache.get('my_key')

    return JsonResponse({'cached_value': value})


@login_required
def get_user_messages(request):
    messages = ChatMessage.objects.filter(user=request.user).order_by("timestamp")
    data = [
        {"prompt": m.prompt, "response": m.response, "timestamp": m.timestamp.isoformat()}
        for m in messages
    ]
    return JsonResponse(data, safe=False)
    
@login_required
def generate_llm_response(request):
    prompt = request.GET.get("prompt", "")
    if not prompt:
        return JsonResponse({"error": "Boş prompt"}, status=400)

    llm_response = requests.post(
        "http://ollama-llm:11434/api/generate",
        json={
            "model": "smollm2:360m",
            "prompt": prompt,
            "stream": False
        }
    ).json()

    response_text = llm_response.get("response", "Cevap alınamadı.")

    # Veritabanına kaydet
    ChatMessage.objects.create(
        user=request.user,
        prompt=prompt,
        response=response_text
    )

    return JsonResponse({"response": response_text})
def custom_logout(request):
    logout(request)
    return redirect(reverse('index'))
#@cache_page(60 * 5)
def index(request):
    return render(request, 'index.html')
@csrf_exempt
@cache_page(60 * 5)
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            print("Form submitted")  
            return redirect('login')  
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
@csrf_exempt
@cache_page(60 * 5)
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
	
@login_required(login_url='login')
def test(request):
    return render(request, 'test.html')	

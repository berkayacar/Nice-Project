# Python ve Django için uygun bir base image seçiyoruz
FROM python:3.10

# Çalışma dizinini belirleyin
WORKDIR /app

# Bağımlılıkları yüklemek için gerekli dosyaları kopyala
COPY requirements.txt /app/

# Bağımlılıkları yükle
RUN pip install --no-cache-dir -r requirements.txt

# Proje dosyalarını konteynere kopyala
COPY . /app/

# Gerekli portları aç
EXPOSE 8000

# Django migration işlemlerini çalıştır
RUN python manage.py migrate

# Django server'ı başlat
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# Gunakan gambar Python dari Docker Hub
FROM python:3.10

# Set working directory
WORKDIR /app

# Salin file requirements.txt ke dalam kontainer
COPY requirements.txt .

# Install dependensi Python
RUN pip install --no-cache-dir -r requirements.txt

# Salin semua konten aplikasi ke dalam kontainer
COPY . .

# Expose port yang akan digunakan oleh aplikasi FastAPI
EXPOSE 8080

# Perintah untuk menjalankan aplikasi FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]

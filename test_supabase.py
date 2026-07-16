import requests
import json
import time
import random

SUPABASE_URL = 'https://dzpwcvzrpiilmqwvbhpj.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImR6cHdjdnpycGlpbG1xd3ZiaHBqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODQxNjQ4NjcsImV4cCI6MjA5OTc0MDg2N30.9CAKCC4--8Pynb_7-NpghA1y3ys6TZeKbbJnkY0fOmk'

headers = {
    'apikey': SUPABASE_KEY,
    'Authorization': f'Bearer {SUPABASE_KEY}',
    'Content-Type': 'application/json'
}

email = f"testuser{random.randint(1000,9999)}@example.com"
password = "Password123!"

print(f"Signing up {email}...")
res = requests.post(
    f"{SUPABASE_URL}/auth/v1/signup",
    headers=headers,
    json={"email": email, "password": password}
)
print("SignUp Response:", res.status_code, res.text)

print("\nTrying to log in immediately...")
res2 = requests.post(
    f"{SUPABASE_URL}/auth/v1/token?grant_type=password",
    headers=headers,
    json={"email": email, "password": password}
)
print("SignIn Response:", res2.status_code, res2.text)

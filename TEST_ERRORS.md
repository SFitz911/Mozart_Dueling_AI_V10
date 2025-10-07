# 🧪 Test Errors for Mozart Dueling AI

**Break free from AI coding error loops with these real-world test cases!**

## 🎯 How to Use This File

1. **Copy any code snippet** from the sections below
2. **Paste it into Mozart AI** 
3. **Add context** about what the code should do
4. **Run Fast Mode or Full Mode** to see how 2-3 AI agents solve it
5. **Compare solutions** and see the judge's combined result!

Perfect for testing when you're stuck with Cursor AI, Claude, GitHub Copilot, or any other coding assistant!

---

## 🚀 Quick Test Cases (Copy & Paste Ready)

### 1. **Infinite Loop Error** (Beginner)
```python
# This should count from 1 to 10, but it's stuck!
def count_to_ten():
    i = 1
    while i <= 10:
        print(f"Count: {i}")
        # Bug: forgot to increment i
    return "Done counting"

count_to_ten()
```
**Context**: "This function should count from 1 to 10 but it's causing an infinite loop."

### 2. **List Index Error** (Beginner)
```python
# This should find the average of test scores
def calculate_average(scores):
    total = 0
    for i in range(len(scores) + 1):  # Bug: +1 causes index error
        total += scores[i]
    return total / len(scores)

test_scores = [85, 92, 78, 96, 88]
print(calculate_average(test_scores))
```
**Context**: "Calculate average test scores but getting IndexError."

### 3. **API Connection Error** (Intermediate)
```python
import requests

def get_weather_data(city):
    # Bug: wrong URL and no error handling
    url = f"http://api.weather.com/current/{city}"  
    response = requests.get(url)
    data = response.json()  # Will fail if response is bad
    return data['temperature']

# This crashes when API fails
weather = get_weather_data("New York")
print(f"Temperature: {weather}°F")
```
**Context**: "Getting weather data from API but it keeps failing with different errors."

---

## 🔄 Common AI Agent Error Loops

### 4. **Cursor AI Gets Confused** (Database Connection)
```python
import sqlite3

class UserDatabase:
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = sqlite3.connect(db_path)
    
    def add_user(self, username, email):
        cursor = self.connection.cursor()
        # Bug: SQL injection vulnerability + connection not closed
        query = f"INSERT INTO users (username, email) VALUES ('{username}', '{email}')"
        cursor.execute(query)
        self.connection.commit()
    
    def get_user(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        return cursor.fetchone()

# Cursor AI keeps suggesting band-aid fixes for this
db = UserDatabase("users.db")
db.add_user("test_user", "test@email.com")
```
**Context**: "Cursor AI keeps suggesting small fixes but this database class has multiple fundamental problems."

### 5. **Claude Loop Example** (Authentication Logic)
```python
import hashlib
import random

class UserAuth:
    def __init__(self):
        self.users = {}
    
    def register_user(self, username, password):
        # Bug: storing plain text password
        self.users[username] = password
        return True
    
    def login(self, username, password):
        if username in self.users:
            # Bug: comparing plain text with what should be hashed
            stored_password = self.users[username]
            if password == stored_password:
                # Bug: predictable session token
                session_token = str(random.randint(1000, 9999))
                return session_token
        return None
    
    def hash_password(self, password):
        # Bug: no salt, weak hashing
        return hashlib.md5(password.encode()).hexdigest()

# Claude keeps getting confused about the security issues
auth = UserAuth()
auth.register_user("admin", "password123")
token = auth.login("admin", "password123")
```
**Context**: "Claude keeps fixing one security issue at a time but missing the bigger picture of secure authentication."

---

## 💔 Performance & Algorithm Issues

### 6. **Inefficient Algorithm** (Intermediate)
```python
def find_duplicates(numbers):
    duplicates = []
    # Bug: O(n²) complexity - very slow for large lists
    for i in range(len(numbers)):
        for j in range(i + 1, len(numbers)):
            if numbers[i] == numbers[j] and numbers[i] not in duplicates:
                duplicates.append(numbers[i])
    return duplicates

# This takes forever with large datasets
large_list = list(range(10000)) * 2  # 20,000 items with duplicates
result = find_duplicates(large_list)
```
**Context**: "This function finds duplicates but is extremely slow with large lists."

### 7. **Memory Leak Simulation** (Advanced)
```python
class DataProcessor:
    def __init__(self):
        self.cache = {}
        self.large_data = []
    
    def process_data(self, data_id, data):
        # Bug: cache grows infinitely, never cleaned
        processed = [x * 2 for x in data]
        self.cache[data_id] = processed
        
        # Bug: storing references that never get cleaned
        self.large_data.append(data)
        self.large_data.append(processed)
        
        return processed
    
    def get_cached_data(self, data_id):
        return self.cache.get(data_id)

# Memory usage keeps growing
processor = DataProcessor()
for i in range(1000):
    big_data = list(range(1000))  # 1000 integers each time
    processor.process_data(f"dataset_{i}", big_data)
```
**Context**: "This data processor is consuming more and more memory over time."

---

## 🌐 Real-World Integration Problems

### 8. **File I/O Nightmare** (Intermediate)
```python
import json
import os

def save_user_preferences(user_id, preferences):
    filename = f"user_{user_id}_prefs.json"
    # Bug: no path validation, file handling issues
    file = open(filename, "w")  # Not using with statement
    json.dump(preferences, file)
    # Bug: file never closed!

def load_user_preferences(user_id):
    filename = f"user_{user_id}_prefs.json"
    # Bug: no error handling for missing files
    file = open(filename, "r")
    data = json.load(file)
    file.close()
    return data

def delete_user_data(user_id):
    filename = f"user_{user_id}_prefs.json"
    os.remove(filename)  # Bug: no check if file exists

# This breaks in multiple ways
prefs = {"theme": "dark", "language": "en"}
save_user_preferences(123, prefs)
loaded_prefs = load_user_preferences(999)  # User doesn't exist!
```
**Context**: "File operations that work sometimes but fail unpredictably in production."

### 9. **API Rate Limiting Chaos** (Advanced)
```python
import requests
import time

class APIClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.example.com"
    
    def make_request(self, endpoint, params=None):
        url = f"{self.base_url}/{endpoint}"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        
        # Bug: no rate limiting, retry logic, or error handling
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 429:  # Rate limited
            # Bug: naive retry without exponential backoff
            time.sleep(1)
            return self.make_request(endpoint, params)
        
        return response.json()
    
    def bulk_data_fetch(self, item_ids):
        results = []
        # Bug: making too many requests too fast
        for item_id in item_ids:
            data = self.make_request(f"items/{item_id}")
            results.append(data)
        return results

# Gets rate limited and crashes
client = APIClient("fake_api_key")
item_ids = list(range(1, 101))  # 100 API calls in rapid succession
data = client.bulk_data_fetch(item_ids)
```
**Context**: "API client that gets rate limited and fails when trying to fetch lots of data."

---

## 🔥 Expert Level Challenges

### 10. **Concurrency Nightmare** (Expert)
```python
import threading
import time

class BankAccount:
    def __init__(self, initial_balance):
        self.balance = initial_balance
        # Bug: no thread synchronization
    
    def deposit(self, amount):
        # Bug: race condition in balance update
        current_balance = self.balance
        time.sleep(0.001)  # Simulate processing time
        self.balance = current_balance + amount
    
    def withdraw(self, amount):
        # Bug: race condition + no balance check
        current_balance = self.balance
        time.sleep(0.001)
        self.balance = current_balance - amount
    
    def get_balance(self):
        return self.balance

def simulate_transactions(account):
    # Multiple threads doing transactions simultaneously
    for _ in range(100):
        account.deposit(10)
        account.withdraw(5)

# This should result in balance of 1500, but doesn't
account = BankAccount(1000)
threads = []

for _ in range(3):
    thread = threading.Thread(target=simulate_transactions, args=(account,))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

print(f"Final balance: {account.get_balance()}")  # Should be 1500, but isn't!
```
**Context**: "Bank account simulation with threading - the final balance is always wrong due to race conditions."

---

## 🎯 Testing Instructions

### For Each Error:
1. **Copy the code block** 
2. **Paste into Mozart AI**
3. **Add the provided context** in the goal/context field
4. **Select relevant criteria** (Security, Performance, Logic, Error Handling, etc.)
5. **Run Fast Mode** to see competing solutions
6. **Try Full Mode** for detailed analysis with judge arbitration

### What to Look For:
- 🔍 **Different approaches** from each AI reviewer
- ⚖️ **Judge's combined solution** that takes the best from both
- 📊 **Scoring differences** between reviewers
- 💡 **Insights you might not have considered**

### Pro Tips:
- Try the same error with **different context descriptions**
- Test with **only specific criteria selected**
- Compare **Fast Mode vs Full Mode** results
- Use these as **learning examples** for common coding pitfalls

---

## 🎵 Break the Loop!

These test cases represent the kinds of errors that often trap developers in endless loops with single AI assistants. Mozart AI's multi-AI approach gives you:

- **Multiple perspectives** on the same problem
- **Competing solutions** to choose from  
- **Judge arbitration** for complex decisions
- **Fresh insights** when you're stuck

Stop going in circles - get multiple AI minds working on your toughest coding challenges! 🚀
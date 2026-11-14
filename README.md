# 🌐 Free Proxy List – Updated Every 5 Minutes

Access a **reliable, constantly updated list of free HTTP/SOCKS proxies** for SEO, SMM, web scraping, and online privacy.

Support our project:  
<img src="https://i.postimg.cc/Njt7JY8T/IMG-1768123407827.png" alt="Donate" width="200"/>

---

## 🔗 Latest Proxy Lists

Download or use directly:

| Type | Raw URL |
|------|---------|
| 🌐 **HTTP/HTTPS** | [http.txt](https://raw.githubusercontent.com/Cheagjihvg/simple-proxylist/refs/heads/main/http.txt) |
| 🧦 **SOCKS4** | [socks4.txt](https://raw.githubusercontent.com/Cheagjihvg/simple-proxylist/refs/heads/main/socks4.txt) |
| 🧦 **SOCKS5** | [socks5.txt](https://raw.githubusercontent.com/Cheagjihvg/simple-proxylist/refs/heads/main/socks5.txt) |

- Updated automatically **every 5 minutes**
- Removes duplicates and invalid proxies
- Split by protocol for easy use

---

## 💻 How to Use

### Python Example – HTTP Proxy
```python
import requests, random

# Load HTTP proxy list
proxy_url = "https://raw.githubusercontent.com/Cheagjihvg/simple-proxylist/refs/heads/main/http.txt"
proxies = requests.get(proxy_url).text.splitlines()

# Pick a random proxy
proxy = random.choice(proxies)
proxies_dict = {
    "http": f"http://{proxy}",
    "https": f"http://{proxy}"
}

# Test request
response = requests.get("https://httpbin.org/ip", proxies=proxies_dict, timeout=10)
print(response.text)
```

### Python Example – SOCKS5 Proxy
```python
import requests, random

# pip install requests[socks]
proxy_url = "https://raw.githubusercontent.com/Cheagjihvg/simple-proxylist/refs/heads/main/socks5.txt"
proxies = requests.get(proxy_url).text.splitlines()

proxy = random.choice(proxies)
proxies_dict = {
    "http": f"socks5://{proxy}",
    "https": f"socks5://{proxy}"
}

response = requests.get("https://httpbin.org/ip", proxies=proxies_dict, timeout=10)
print(response.text)
```

### Python Example – SOCKS4 Proxy
```python
import requests, random

# pip install requests[socks]
proxy_url = "https://raw.githubusercontent.com/Cheagjihvg/simple-proxylist/refs/heads/main/socks4.txt"
proxies = requests.get(proxy_url).text.splitlines()

proxy = random.choice(proxies)
proxies_dict = {
    "http": f"socks4://{proxy}",
    "https": f"socks4://{proxy}"
}

response = requests.get("https://httpbin.org/ip", proxies=proxies_dict, timeout=10)
print(response.text)
```

---

## ⚠️ Disclaimer

These proxies are collected from public sources. Use responsibly and only for legal purposes.

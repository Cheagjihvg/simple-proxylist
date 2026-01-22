# 🌐 Free Proxy List – Updated Every 5 Minutes

Access a **reliable, constantly updated list of free HTTP/SOCKS proxies** for SEO, SMM, web scraping, and online privacy.  

Support our project:  
<img src="https://i.postimg.cc/Njt7JY8T/IMG-1768123407827.png" alt="Donate" width="200"/>

---
 
## 🔗 Latest Proxy List

Download or use directly:

**Raw URL:**  
[https://raw.githubusercontent.com/Cheagjihvg/simple-proxylist/refs/heads/main/proxy.txt](https://raw.githubusercontent.com/Cheagjihvg/simple-proxylist/refs/heads/main/proxy.txt)

- Updated automatically **every 5 minutes**  
- Removes duplicates and invalid proxies  
- Mix of HTTP, HTTPS, and SOCKS proxies 

---

## 💻 How to Use
 
### Python Example
```python
import requests, random

# Load proxy list
proxy_url = "https://raw.githubusercontent.com/Cheagjihvg/simple-proxylist/refs/heads/main/proxy.txt"
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

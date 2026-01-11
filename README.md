# 🌐 Free Proxy List (Updated Every 5 Minutes)

Support our project by using and sharing this free proxy list!  
If you like it, consider supporting us:

![Support Us](https://i.postimg.cc/Njt7JY8T/IMG-1768123407827.png)

---

## Access the Proxy List

The latest `proxy.txt` is automatically updated every 5 minutes.  
You can use it directly without any setup:

- **Raw URL:** [proxy.txt](https://raw.githubusercontent.com/Cheagjihvg/simple-proxylist/refs/heads/main/proxy.txt)

---

## Quick Usage Examples

### Python

```python
import requests
import random

# Load proxies
proxy_url = "https://raw.githubusercontent.com/Cheagjihvg/simple-proxylist/refs/heads/main/proxy.txt"
proxies = requests.get(proxy_url).text.splitlines()

# Use a random proxy
proxy = random.choice(proxies)
proxies_dict = {
    "http": f"http://{proxy}",
    "https": f"http://{proxy}"
}

# Test request
response = requests.get("https://httpbin.org/ip", proxies=proxies_dict, timeout=10)
print(response.text)

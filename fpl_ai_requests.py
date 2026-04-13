import requests

# 您的 API Key
api_key = "14914cd6-fa0a-4d5e-8bd8-93fa4a1de68f:e7ffdc8feeee684a3d5a766643dc9568"

# 测试端点
url = "https://queue.fal.run/health"  # 健康检查端点，不需要认证

# 先测试网络连通性
print("测试网络连通性...")
try:
    response = requests.get(url, timeout=10)
    print(f"✓ 网络连通正常，状态码: {response.status_code}")
except Exception as e:
    print(f"✗ 网络连接失败: {e}")
    exit()

# 使用两种不同的认证方式测试API
print("\n测试API认证...")

# 方式1: 使用 Key 前缀
url2 = "https://api.fal.ai/v1/models"
headers1 = {
    "Authorization": f"Key {api_key}",
    "Content-Type": "application/json"
}

# 测试方式1
print("\n--- 测试方式1: Key 前缀 ---")
response1 = requests.get(url2, headers=headers1)
print(f"状态码: {response1.status_code}")
if response1.status_code != 200:
    print(f"响应: {response1.text[:200]}")  # 只显示前200字符

import requests
import os
from dotenv import load_dotenv

load_dotenv()

def verify_api_key():
    api_key = os.getenv("DEEPSEEK_API_KEY")
    
    if not api_key or api_key == "sk-你的真实密钥":
        print("❌ 请先在 .env 文件中设置真实的 API 密钥")
        return False
    
    # 测试密钥有效性
    test_url = "https://api.deepseek.com/v1/models"
    headers = {"Authorization": f"Bearer {api_key}"}
    
    try:
        response = requests.get(test_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            print("✅ API密钥有效！")
            print(f"密钥前8位: {api_key[:8]}...")
            
            # 显示可用模型
            models = response.json().get("data", [])
            print(f"可用模型数量: {len(models)}")
            for model in models[:3]:  # 显示前3个模型
                print(f"  - {model.get('id')}")
            return True
        elif response.status_code == 401:
            print("❌ API密钥无效或认证失败")
            print("错误信息:", response.text)
            return False
        else:
            print(f"❌ 请求失败，状态码: {response.status_code}")
            print("响应:", response.text[:200])
            return False
    except Exception as e:
        print(f"❌ 请求异常: {e}")
        return False

if __name__ == "__main__":
    verify_api_key()
import os
import sys
import requests
import time

# ！！！强烈建议：测试成功后，不要把真实的 Key 写死在代码里提交到 Github ！！！
os.environ['FAL_KEY'] = '14914cd6-fa0a-4d5e-8bd8-93fa4a1de68f:e7ffdc8feeee684a3d5a766643dc9568'

try:
    import fal_client
except ImportError:
    print("错误：未找到 'fal-client' 库。请在终端运行: pip install fal-client")
    sys.exit(1)

def download_image(image_url, filename_prefix="flux_image"):
    """从URL下载图片到脚本所在的目录"""
    try:
        print(f"⏳ 正在下载图片: {image_url}")
        response = requests.get(image_url, timeout=30)
        if response.status_code == 200:
            # 👇 核心修改：获取当前 Python 脚本所在的绝对路径
            script_dir = os.path.dirname(os.path.abspath(__file__))
            # 👇 将文件保存到脚本同级目录下
            filename = os.path.join(script_dir, f"{filename_prefix}_{int(time.time())}.jpg")
            
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"💾 图片已成功保存至: {filename}")
            return filename
        else:
            print(f"⚠️ 图片下载失败，HTTP状态码: {response.status_code}")
    except Exception as e:
        print(f"⚠️ 下载异常: {e}")
    return None

# 打印日志的回调函数 (完美还原你的 JS onQueueUpdate 逻辑)
def on_queue_update(update):
    if isinstance(update, fal_client.InProgress):
        for log in update.logs:
            print(f"日志: {log['message']}")

def generate_image(prompt, model_id="fal-ai/flux-1/schnell"):
    print(f"🚀 正在调用模型: {model_id}")
    print(f"📝 提示词: {prompt}")
    
    try:
        # fal_client.subscribe 会自动处理等待和轮询，直到生成完毕才往下执行
        result = fal_client.subscribe(
            model_id,
            arguments={
                "prompt": prompt,
                "image_size": "square_hd"
            },
            with_logs=True,
            on_queue_update=on_queue_update
        )
        
        # 直接提取最终结果
        if "images" in result and len(result["images"]) > 0:
            image_url = result["images"][0]["url"]
            print(f"\n✅ 图片生成完成！")
            print(f"📸 临时URL (带签名): {image_url}")
            
            # 执行下载逻辑
            download_image(image_url)
        else:
            print("❌ 返回数据中没有找到图片信息。")
            print("原始返回:", result)

    except Exception as e:
        print(f"❌ 生成过程中发生致命错误: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("Fal.ai 极简版图片生成器")
    print("=" * 60)
    
    user_prompt = "A beautiful sunset over a calm ocean"
    generate_image(user_prompt)
    
    print("=" * 60)
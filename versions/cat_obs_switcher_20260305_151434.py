import time
import json
import queue
import sys
import pyaudio
from vosk import Model, KaldiRecognizer
import obsws_python as obs

# ================= 配置区 =================
OBS_PASSWORD = "1122334455" 
MODEL_PATH = "/Users/liliming/vosk"  # 确保解压后的模型文件夹路径正确

# 场景名称
SCENE_DEFAULT = "说话的小猫"  
SCENE_TALK = "写代码的小猫"    

# 触发词
KEYWORDS_TALK = ["大家好", "概念", "理论", "原理", "应用", "场景","定义"]
KEYWORDS_CODE = ["代码", "编程", "程序", "写一下", "示例","select","from"]

# 自动返回默认场景的秒数
SILENCE_TIMEOUT = 10 
# =========================================

# 音频回调队列
q = queue.Queue()

def audio_callback(in_data, frame_count, time_info, status):
    """将捕获的音频放入队列"""
    q.put(in_data)
    return (None, pyaudio.paContinue)

def main():
    # 1. 初始化 OBS 连接
    try:
        client = obs.ReqClient(host="localhost", port=4455, password=OBS_PASSWORD)
        print("✅ OBS 连接成功")
        client.set_current_program_scene(SCENE_DEFAULT)
    except Exception as e:
        print(f"❌ OBS 连接失败: {e}")
        return

    # 2. 加载 Vosk 模型
    try:
        model = Model(MODEL_PATH)
        rec = KaldiRecognizer(model, 16000)
    except Exception as e:
        print(f"❌ 模型加载失败，请检查路径: {e}")
        return

    # 3. 初始化 PyAudio 录音流
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=16000,
                    input=True,
                    frames_per_buffer=8000,
                    stream_callback=audio_callback)

    print(f"🎤 Vosk 离线识别启动... (当前默认场景: {SCENE_DEFAULT})")
    
    last_action_time = time.time()
    current_scene = SCENE_DEFAULT

    try:
        stream.start_stream()
        while stream.is_active():
            # 从队列获取音频数据
            data = q.get()
            
            # 检查超时逻辑（自动回说话场景）
            if current_scene != SCENE_DEFAULT and (time.time() - last_action_time) > SILENCE_TIMEOUT:
                print(f"🕒 超过 {SILENCE_TIMEOUT}s 未说话，自动切回默认...")
                client.set_current_program_scene(SCENE_DEFAULT)
                current_scene = SCENE_DEFAULT

            # 处理音频数据
            if rec.AcceptWaveform(data):
                # 获取完整结果
                result = json.loads(rec.Result())
                text = result.get("text", "").replace(" ", "")
            else:
                # 获取部分结果（Vosk 的特性，能够极大降低响应延迟）
                partial = json.loads(rec.PartialResult())
                text = partial.get("partial", "").replace(" ", "")

            if text:
                # 匹配逻辑
                found_talk = any(word in text for word in KEYWORDS_TALK)
                found_code = any(word in text for word in KEYWORDS_CODE)

                if found_talk:
                    last_action_time = time.time() # 只要检测到说话就重置时间
                    if current_scene != SCENE_TALK:
                        print(f"🚀 识别到关键词 -> 切换至: {SCENE_DEFAULT}")
                        client.set_current_program_scene(SCENE_DEFAULT)
                        current_scene = SCENE_DEFAULT
                        # 切换后清除识别缓冲区，防止重复触发
                        rec.Reset()
                
                elif found_code:
                    last_action_time = time.time()
                    if current_scene != SCENE_TALK:
                        print(f"🚀 识别到关键词 -> 切换至: {SCENE_TALK}")
                        client.set_current_program_scene(SCENE_TALK)
                        current_scene = SCENE_TALK
                        rec.Reset()

    except KeyboardInterrupt:
        print("\n🛑 脚本已停止")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

if __name__ == "__main__":
    main()
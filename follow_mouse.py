import obspython as obs
import pyautogui # 需要终端运行 pip install pyautogui

# --- 全局配置变量 ---
source_name = ""       # 你要跟随的屏幕源名称
filter_name = "鼠标跟随裁剪" # 你手动给源添加的“裁剪/填充”滤镜名称
zoom_width = 720       # 竖屏视野宽度 (例如 720 或 1080)
zoom_height = 1280     # 竖屏视野高度 (例如 1280 或 1920)
screen_width = 2560    # MacBook Air M1 默认点宽
screen_height = 1600   # MacBook Air M1 默认点高

def script_description():
    return "让画面通过【裁剪/填充】滤镜跟随 Mac 鼠标移动（适配 Aitum Vertical 竖屏）。\n⚠️ 请在 Mac 终端执行：pip install pyautogui\n⚠️ 若画面偏移，请将视口和屏幕分辨率乘以 2 (Retina 缩放)。"

def script_properties():
    props = obs.obs_properties_create()
    
    # 绑定源列表
    p_sources = obs.obs_properties_add_list(props, "source_name", "选择屏幕源", obs.OBS_COMBO_TYPE_EDITABLE, obs.OBS_COMBO_FORMAT_STRING)
    sources = obs.obs_enum_sources()
    if sources is not None:
        for source in sources:
            name = obs.obs_source_get_name(source)
            obs.obs_property_list_add_string(p_sources, name, name)
        obs.source_list_release(sources)
        
    obs.obs_properties_add_text(props, "filter_name", "裁剪滤镜名称", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_int(props, "zoom_width", "竖屏显示区域-宽", 100, 3840, 1)
    obs.obs_properties_add_int(props, "zoom_height", "竖屏显示区域-高", 100, 3840, 1)
    obs.obs_properties_add_int(props, "screen_width", "Mac屏幕总宽", 100, 5120, 1)
    obs.obs_properties_add_int(props, "screen_height", "Mac屏幕总高", 100, 5120, 1)
    
    return props

def script_update(settings):
    global source_name, filter_name, zoom_width, zoom_height, screen_width, screen_height
    source_name = obs.obs_data_get_string(settings, "source_name")
    filter_name = obs.obs_data_get_string(settings, "filter_name")
    zoom_width = obs.obs_data_get_int(settings, "zoom_width")
    zoom_height = obs.obs_data_get_int(settings, "zoom_height")
    screen_width = obs.obs_data_get_int(settings, "screen_width")
    screen_height = obs.obs_data_get_int(settings, "screen_height")

def script_tick(seconds):
    if not source_name or not filter_name:
        return
        
    try:
        # 1. 获取 Mac 鼠标实际物理坐标
        mx, my = pyautogui.position()
        
        # 2. 计算裁剪边界，让鼠标处于视野中央
        left = mx - (zoom_width / 2)
        top = my - (zoom_height / 2)
        
        # 3. 边缘防穿帮（不超出 Mac 屏幕边界）
        if left < 0: left = 0
        if top < 0: top = 0
        if left + zoom_width > screen_width: left = screen_width - zoom_width
        if top + zoom_height > screen_height: top = screen_height - zoom_height
        
        right = screen_width - (left + zoom_width)
        bottom = screen_height - (top + zoom_height)
        
        # 4. 找到屏幕源和滤镜
        source = obs.obs_get_source_by_name(source_name)
        if source:
            crop_filter = obs.obs_source_get_filter_by_name(source, filter_name)
            if crop_filter:
                f_settings = obs.obs_source_get_settings(crop_filter)
                
                # 写入裁剪值
                obs.obs_data_set_int(f_settings, "left", int(left))
                obs.obs_data_set_int(f_settings, "top", int(top))
                obs.obs_data_set_int(f_settings, "right", int(right))
                obs.obs_data_set_int(f_settings, "bottom", int(bottom))
                
                obs.obs_source_update(crop_filter, f_settings)
                obs.obs_data_release(f_settings)
                obs.obs_source_release(crop_filter)
            obs.obs_source_release(source)
            
    except Exception:
        pass
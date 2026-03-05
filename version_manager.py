import os
import datetime
import shutil

def backup_current_version():
    """备份当前版本"""
    source_file = "cat_obs_switcher.py"
    
    if not os.path.exists(source_file):
        print("❌ 文件不存在")
        return
    
    # 创建备份目录
    backup_dir = "versions"
    os.makedirs(backup_dir, exist_ok=True)
    
    # 生成带时间戳的备份文件名
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"{backup_dir}/cat_obs_switcher_{timestamp}.py"
    
    # 复制文件
    shutil.copy2(source_file, backup_file)
    print(f"✅ 已创建版本备份: {backup_file}")
    
    # 统计版本数量
    versions = [f for f in os.listdir(backup_dir) if f.startswith("cat_obs_switcher_")]
    print(f"📊 当前共有 {len(versions)} 个历史版本")

if __name__ == "__main__":
    backup_current_version()

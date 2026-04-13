import libtorrent as lt
import time
import sys

def download_magnet(magnet_link, save_path="."):
    # 1. 初始化会话
    ses = lt.session({'listen_interfaces': '0.0.0.0:6881'})
    
    # 2. 添加磁力链接
    params = lt.parse_magnet_uri(magnet_link)
    params.save_path = save_path
    handle = ses.add_torrent(params)
    trackers = [
        "udp://tracker.opentrackr.org:1337/announce",
        "udp://9.rarbg.com:2810/announce",
        "udp://exodus.desync.com:6969/announce",
        "http://tracker.openbittorrent.com:80/announce"
    ]
    for t in trackers:
        handle.add_tracker({"url": t})
    print("正在连接 Peer 节点，请稍候...")
    
    # 3. 循环监控下载进度
    while not handle.status().has_metadata:
        time.sleep(1)

    print(f"已获取元数据: {handle.status().name}")
    print("开始下载...")

    while handle.status().state != lt.torrent_status.seeding:
        s = handle.status()
        # 打印进度条
        progress = s.progress * 100
        print(f'\r进度: {progress:.2f}% | 下载速度: {s.download_rate / 1000:.1f} kB/s | Peers: {s.num_peers}', end='')
        sys.stdout.flush()
        time.sleep(1)

    print("\n下载完成！")

# 使用示例（替换为你截图中的磁力链接）
magnet = "magnet:?xt=urn:btih:8339AEAC1B6A3ECDED42A9A2F5ACAD6A7F3276CB"
download_magnet(magnet)
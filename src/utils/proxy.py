import time
import subprocess
import winreg
import requests

# 現在のプロキシ設定をレジストリから読む
def get_manual_proxy_settings():
    settings = {}
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Internet Settings") as key:
            proxy_enable, _ = winreg.QueryValueEx(key, "ProxyEnable")
            proxy_server, _ = winreg.QueryValueEx(key, "ProxyServer")
            settings["ProxyEnable"] = proxy_enable
            settings["ProxyServer"] = proxy_server
    except OSError as e:
        print(f"Error reading proxy settings: {e}")
    return settings

def set_manual_proxy_settings(settings):
    # プロキシ設定をレジストリに書き込む
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Internet Settings", 0, winreg.KEY_SET_VALUE) as key:
            winreg.SetValueEx(key, "ProxyEnable", 0, winreg.REG_DWORD, settings["ProxyEnable"])
            winreg.SetValueEx(key, "ProxyServer", 0, winreg.REG_SZ, settings["ProxyServer"])
    except OSError as e:
        print(f"Error writing proxy settings: {e}")

def toggle_proxy_auto_detect():
    try:
        # プロキシ自動検出をオフにする
        subprocess.run(
            ["reg", "add", r"HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings", "/v", "AutoDetect", "/t", "REG_SZ", "/d", "0", "/f"],
            check=True,
        )
        
        # 少し待機
        time.sleep(1)
        
        # プロキシ自動検出をオンにする
        subprocess.run(
            ["reg", "add", r"HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings", "/v", "AutoDetect", "/t", "REG_SZ", "/d", "1", "/f"],
            check=True,
        ) 
    except subprocess.CalledProcessError as e:
        print(f"Error toggling proxy auto detect settings: {e}")

def handle_proxy_request(max_retries=3, retry_interval=5):
    original_proxy_settings = get_manual_proxy_settings()  # 現在の手動プロキシ設定を保存
    for attempt in range(max_retries):
        try:
            # やりたいこと ↓↓↓↓↓
            response = requests.get("https://bank.teraren.com", proxies=None, timeout=10)
            
            # やりたいこと ↑↑↑↑↑
            break
        except Exception as e:
            # プロキシ失敗したとき用
            if "proxy" in str(e).lower():
                toggle_proxy_auto_detect()
            time.sleep(retry_interval)
    else:
        still_processing = True
    
    # 最後にプロキシ設定を元に戻す
    set_manual_proxy_settings(original_proxy_settings)
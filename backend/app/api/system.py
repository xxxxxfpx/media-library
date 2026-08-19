"""系统信息 API"""

import platform
import socket
from datetime import datetime

from fastapi import APIRouter, Depends

from app.api.deps import get_user_id

router = APIRouter(prefix="/system", tags=["system"])


@router.get("/info")
async def get_system_info(user_id: int = Depends(get_user_id)):
    """获取系统信息（需登录）"""
    try:
        # 获取 IP 地址
        hostname = socket.gethostname()
        try:
            ip = socket.gethostbyname(hostname)
        except Exception:
            ip = "127.0.0.1"

        # 获取系统信息
        info = {
            "ip": ip,
            "platform": platform.platform(),
            "python_version": platform.python_version(),
            "cpu": 0.0,  # 需要额外实现
            "memory_percent": 0.0,
            "memory_used": "0 GB",
            "memory_total": "0 GB",
            "disk_percent": 0.0,
            "disk_used": "0 GB",
            "disk_total": "0 GB",
            "uptime": "0:00:00",
            "load": "0.0, 0.0, 0.0"
        }

        # 尝试获取更详细的系统信息
        try:
            import psutil

            # CPU 使用率
            info["cpu"] = psutil.cpu_percent(interval=1)

            # 内存信息
            mem = psutil.virtual_memory()
            info["memory_percent"] = mem.percent
            info["memory_used"] = f"{mem.used / (1024**3):.1f} GB"
            info["memory_total"] = f"{mem.total / (1024**3):.1f} GB"

            # 磁盘信息
            disk = psutil.disk_usage('/')
            info["disk_percent"] = disk.percent
            info["disk_used"] = f"{disk.used / (1024**3):.1f} GB"
            info["disk_total"] = f"{disk.total / (1024**3):.1f} GB"

            # 运行时间
            boot_time = datetime.fromtimestamp(psutil.boot_time())
            uptime = datetime.now() - boot_time
            hours, remainder = divmod(uptime.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            info["uptime"] = f"{uptime.days}天 {hours:02d}:{minutes:02d}:{seconds:02d}"

            # 负载
            if hasattr(psutil, 'getloadavg'):
                load1, load5, load15 = psutil.getloadavg()
                info["load"] = f"{load1:.2f}, {load5:.2f}, {load15:.2f}"

        except ImportError:
            pass  # psutil 未安装，使用默认值

        return info

    except Exception as e:
        return {
            "ip": "127.0.0.1",
            "platform": platform.platform(),
            "python_version": platform.python_version(),
            "cpu": 0.0,
            "memory_percent": 0.0,
            "memory_used": "0 GB",
            "memory_total": "0 GB",
            "disk_percent": 0.0,
            "disk_used": "0 GB",
            "disk_total": "0 GB",
            "uptime": "0:00:00",
            "load": "0.0, 0.0, 0.0",
            "error": str(e)
        }

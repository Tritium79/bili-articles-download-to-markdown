## 简介

批量提取B站专栏文章并转换为 Markdown ，自动提取标题、作者及发布时间，图片以url链接格式保留

## 安装说明

### 1. 获取项目

克隆或下载本项目到本地：

Bash

```
git clone https://github.com/Tritium79/bili-read-getter.git
```

### 2. 环境配置

- **Windows**:
    
    PowerShell
    
    ```
    # 创建虚拟环境
    python -m venv venv
    # 激活虚拟环境
    .\venv\Scripts\activate
    ```
    
- **macOS / Linux**:
    
    Bash
    
    ```
    # 创建虚拟环境
    python3 -m venv venv
    # 激活虚拟环境
    source venv/bin/activate
    ```
    

### 3. 安装依赖

Bash

```
pip install -r requirements.txt
```

## 使用

1. **下载单篇文章**：

```bash
python main.py B站专栏URL

```

2. **批量下载全部文章**：

```bash
python main.py 用户UID

```

3. **交互模式**：
直接运行 `python main.py`，根据提示输入 URL 或 UID。


## 免责声明

本工具仅供学习交流使用，请勿用于任何形式的商业用途。

### 原项目

* **@罗橙二 (哔哩哔哩)**
* **地址：** [https://gitee.com/StarVase/bili-read-getter](https://gitee.com/StarVase/bili-read-getter)	[https://www.bilibili.com/video/BV19dY4zvEcy](https://www.bilibili.com/video/BV19dY4zvEcy)

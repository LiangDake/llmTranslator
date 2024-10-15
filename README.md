# 中科网航大模型平台

## 产品介绍
这是使用 Flask, Langchain, Ollama构建的本地大模型翻译网页系统。
服务器使用 Python `os` 模块与 `Linux` 文件系统交互以执行任务。
每个用户在服务器上都有自己的私有根文件夹，他们可以在其中执行基本操作，例如
- 创建文件夹和上传文件
- 翻译文件和文件夹
- 删除文件和文件夹。

### 如何下载
##### 通过ollama下载本地大模型（目前没有设置自定义模型功能）：
```bash
ollama pull qwen2:7b
ollama pull yxl/m3e
```

##### 下载Tesseract及其语言包并安装 PDF 处理库（Arch Linux）：
```bash
sudo pacman -S tesseract
sudo pacman -S tesseract-data

sudo mv srp.traineddata /usr/share/tessdata/
ls /usr/share/tessdata/
```

##### 下载Tesseract及其语言包并安装 PDF 处理库（Ubuntu Linux）：
```bash
sudo apt update
sudo apt install tesseract-ocr
sudo apt install libtesseract-dev

sudo apt install tesseract-ocr-*

sudo apt install poppler-utils

```

##### 下载Tesseract及其语言包并安装 PDF 处理库（MacOS）：
```bash
brew install tesseract
brew install tesseract-lang

brew install imagemagick


```
##### Github下载并进入文件夹
```bash
git clone https://github.com/LiangDake/llmTranslator
cd llmTranslator
```

##### 创建虚拟环境
```bash
python -m venv env
source ./env/bin/activate
```

##### 下载 requirements.txt 并创建 db 数据库
```bash
pip install -r requirements.txt

python
from localbin import db
db.create_all()
exit()
```

##### 运行网页
```bash
flask --app run run --debug
```



# 扫描发票到 Excel
## 系统支持
只适用于macOS和Linux。
## 运行环境
Python 3
## 安装依赖
```shell
brew install imagemagisk poppler
conda create -n invoice_ocr python
conda activate invoice_ocr
conda install cnocr pdf2image pandas
```
## 使用方法
- 将py文件复制到发票所在文件夹
- 进入目录执行python invoice.py

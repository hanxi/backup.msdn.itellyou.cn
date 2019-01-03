echo '"大分类","小分类","语言","名字","更新时间","下载地址","SHA1","大小"' > msdn.csv
python fetch.py >> msdn.csv

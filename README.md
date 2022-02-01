# Scrapy233Exam
获取233网校的题目转换成云班课的题目模版

## Step 1
登录233网校Web端，通过F12功能，将response下载保存为json文件

## Step 2
修改main.py中的方法入参，指定为文件路径

## Step 3
运行main.py，生成的Excel模版，上传到云班课的后台

## Step 4
登录云班课的后台，通过搜索"233"过滤出题干中含有图片的题目，手工插入图片

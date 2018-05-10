# tesseract_application

转载或者有疑问可以联系我，欢迎交流使用心得: 
  邮箱：yvette_suyu@163.com
  
  
tesseract安装训练等 Blog记录分享：
https://blog.csdn.net/github_38657489


关于批量训练自己的数据集

准备好训练数据集： tif图像/box标记文件（注意命名格式 见上一篇）

批量训练时，可以通过jTessBoxEditor软件将多个tif图片合并，然后box文件可以通过Windows批处理命令合并。这里需要注意的是！！！Box文件得格式，是 char x y w h page，因此在合并时要把page按对应得tif图像顺序修改为0...1...2...

然后在CMD命令行输入 copy *.box all.box 随后按照tif合并时的名字改为同名box文件.

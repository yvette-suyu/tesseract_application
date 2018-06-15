Windows tesseract 3.05。


训练前的说明
要训练自己的语言对应的traineddata文件，需要产生下列过程文件：

lang.config
lang.unicharset  //语料的所有字符                                 √
lang.unicharambigs  //取代了原来的DangAmbigs文件，手工设置的
lang.inttemp                                                     √
lang.pffmtable                                                   √
lang.normproto                                                   √
lang.punc-dawg
lang.word-dawg
lang.number-dawg
lang.freq-dawg
但不是全部需要，最重要的是后面打勾的几个。这些文件都准备好之后，再使用combine_tessdata进行最后的合并工作，
生成lang.traineddata ，这个文件就是最终训练出来语言库，他只是一些输入文件的串联，用一张表记录这与已知文件类型的偏移量。


tesseract训练自己的字库需要的命令

rem 执行改批处理前先要目录下创建font_properties文件 

echo Run Tesseract for Training.. 
tesseract.exe num.font.exp0.tif num.font.exp0 nobatch box.train     
这里可以生成需要的 .tr 文件

 
echo Compute the Character Set.. 
unicharset_extractor.exe num.font.exp0.box 
这里生成需要的unicharset文件

mftraining -F font_properties.txt -U unicharset -O num.unicharset num.font.exp0.tr 
这里会生成需要的 inttemp,num.unicharset ,pffmtable, shapetable文件

echo Clustering.. 
cntraining.exe num.font.exp0.tr 
这里会生成 normproto文件

echo Rename Files.. 
rename normproto num.normproto 
rename inttemp num.inttemp 
rename pffmtable num.pffmtable 
rename shapetable num.shapetable  

echo Create Tessdata.. 
combine_tessdata.exe num. 
合并完成后生成最终的 traineddata文件

echo. & pause
将num.traineddata文件移入tessdata文件夹中，测试自己的test.png识别效果。

##################################################################################################

                                  important!!!!!!!!!
##################################################################################################
小批量训练自己的字库
准备好训练数据集： tif图像/box标记文件（注意命名格式 见上一篇）

训练命令如上，只是要将文件名全都输入到命令行

example：

..\tesseract test.font.exp1.tif test.font.exp1 nobatch box.train
..\tesseract test.font.exp2.tif test.font.exp2 nobatch box.train
..\tesseract test.font.exp3.tif test.font.exp3 nobatch box.train
..\training\unicharset_extractor test.font.exp1.box test.font.exp2.box test.font.exp3.box
..\training\mftraining -F font_properties.txt -U unicharset -O unicharset test.font.exp1.tr test.font.exp2.tr test.font.exp3.tr
..\training\cntraining test.font.exp1.tr test.font.exp2.tr test.font.exp3.tr
rename normproto test.normproto
rename Microfeat test.Microfeat
rename inttemp test.inttemp
rename pffmtable test.pffmtable
..\training\combine_tessdata test.

将生成的test.traineddata复制到tessdata中 即可进行测试。

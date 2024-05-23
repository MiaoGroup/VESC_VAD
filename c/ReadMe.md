简述：
	此目录为基于CNN模型的VAD算法的C代码。

说明：
	conv.h/conv.c：提供了卷积相关的函数的声明和实现；
	vad.h/vad.c：提供了VAD的预测函数的声明和实现；
	algo_error_code.h：提供了算法错误码类型的枚举；
	model_paramters.h：CNN模型的参数；
	main.c：算法测试的主函数，其中包含了数据读取，流式处理和预测的功能；
	data.txt：用于测试该代码的audio原始数据；
	pred.txt: 算法实际预测的结果。

# how to run

```ps1
$data_i="data_1" # or 2, 3
python .\generate_data.py $data_i
gcc *.c
./a.exe
cp pred.txt "predict/$data_i.txt"
python .\evaluate.py $data_i
```

## data_1

f1_score:  0.9211778447162968
accuracy:  0.9615808552885514
recall:  0.8668749276871457
precision:  0.9827387198321091

## data_2

f1_score:  0.9057907949790794
accuracy:  0.9599275955848199
recall:  0.8601557533375715
precision:  0.9565394132202192

## data_3

f1_score:  0.8669993648489248
accuracy:  0.8970084366132595
recall:  0.7875103021169378
precision:  0.9643367935409458
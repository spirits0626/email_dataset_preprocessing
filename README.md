# email_dataset_preprocessing
对邮件数据集 (Enron Email Dataset. 2015. (2015). https://www.cs.cmu.edu/~./enron)  进行预处理


分词/初步过滤：
py nltk-seg.py "需要处理的文档路径"

移除重复单词，为计算频率打基础
py remove-duplicates.py "分词之后的文档路径"

获取出现频率超过一定阈值的单词集合
py word-frequency.py "一处重复词之后的文档路径" 阈值1 阈值2 阈值3

从第一步得到的结果中过滤掉 高频词
py filter.py "分词之后的文档路径" "C:\Users\spirits\Desktop\word_frequency.txt"

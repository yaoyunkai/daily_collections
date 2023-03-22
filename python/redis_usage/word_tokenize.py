"""

!pip install nltk
import nltk
nltk.download('stopwords')
nltk.download('punkt')


在自然语言处理中，语料库（corpus）是指由大量文本数据组成的集合。
这些文本可以是书籍、新闻文章、博客、社交媒体帖子、电子邮件等等。
语料库是自然语言处理任务的基础，因为它们可以用于训练和评估各种文本分析和处理算法。




Created at 2023/3/22
"""

# from nltk.corpus import stopwords
# from nltk.tokenize import word_tokenize
#
# # 加载文本数据
# text = "This is a sample sentence, showing off the stop words filtration."
#
# # 将文本转换为小写，以便于分词和处理
# text = text.lower()
#
# # 分词
# words = word_tokenize(text)
#
# # 去除停用词
# stop_words = set(stopwords.words("english"))
# filtered_words = [word for word in words if word.casefold() not in stop_words]
#
# print(filtered_words)

import string

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# 加载文本数据
text = "This is a sample sentence, showing off the stop words filtration."

# 将文本转换为小写，以便于分词和处理
text = text.lower()

# 分词
words = word_tokenize(text)

# 去除标点符号
table = str.maketrans("", "", string.punctuation)
stripped = [word.translate(table) for word in words]

# 去除停用词
stop_words = set(stopwords.words("english"))
filtered_words = [word for word in stripped if word.casefold() not in stop_words]

print(filtered_words)


"""
import jieba
import string

text = "这是一个中英文混合的句子，This is a sentence with both Chinese and English."

# 分词并去除标点符号
seg_list = jieba.cut(text)
seg_list = [word for word in seg_list if word not in string.punctuation]

# 输出结果
print(" ".join(seg_list))
"""

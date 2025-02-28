from gensim import corpora, models
from nltk.tokenize import word_tokenize

# 示例文档
text = "贺岁 档 电影 哪吒 无疑 一部 合格 商业片 故事 节奏快 至少 看着 无聊 围绕 亲情"

# # 预处理：分词
texts = [word_tokenize(word) for word in text.split(" ")]

# 创建字典和文档-词频矩阵
dictionary = corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]

# 训练 LDA 模型，设定主题数 K=2
lda_model = models.LdaModel(corpus, num_topics=2, id2word=dictionary, passes=10)

# 输出每个主题的前 5 个关键词
topics = lda_model.print_topics(num_words=5)
for topic in topics:
    print(topic)

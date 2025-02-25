import re


def clean_text(text: str, stopwords: list) -> str:
    """
    清洗文本，去除停用词、空行、多余空格和 URL。

    :param text: 需要清洗的文本
    :param stopwords: 停用词列表
    :return: 清洗后的文本
    """
    # 去除URL
    text = re.sub(r"http[s]?://\S+", "", text)

    # 去除多余空格
    text = re.sub(r"\s+", " ", text).strip()

    # 按行分割，去除空行
    lines = [line.strip() for line in text.split("\n") if line.strip()]

    # 去除停用词
    clean_lines = []
    for line in lines:
        words = line.split()
        filtered_words = [word for word in words if word not in stopwords]
        clean_lines.append(" ".join(filtered_words))

    return "\n".join(clean_lines)


stopwords = [
    line.strip() for line in open("stopwords.txt", "r", encoding="utf-8").readlines()
]
stopwords[:10]

text = input("输入需要清洗的文本：")
cleaned_text = clean_text(text, stopwords)

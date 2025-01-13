import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
import seaborn as sns
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Step 1: 讀取資料
# 請將 'reddit.csv' 替換為你的檔案路徑
df = pd.read_csv("reddit_data.csv")

# 取前100筆
df = df.head(100)

# 移除 comments 欄位
df = df.drop(columns=['comments'])

# Step 2: 檢查資料
print("資料摘要:")
print(df.head())

# Step 3: 文字前處理
# 下載所需資源
nltk.download('stopwords')
nltk.download('vader_lexicon')

# 清理文字函式
def clean_text(text):
    text = re.sub(r'[^\w\s]', '', text)  # 移除標點符號
    text = re.sub(r'\d+', '', text)      # 移除數字
    text = text.lower()                   # 全部轉小寫
    stop_words = set(stopwords.words('english'))
    text = ' '.join([word for word in text.split() if word not in stop_words])  # 移除停用詞
    return text

# 提取正向字詞函式
def extract_positive_words(text):
    # 分詞並移除停用詞
    stop_words = set(stopwords.words('english'))
    words = [word for word in text.split() if word not in stop_words]
    
    # 找出正向詞
    positive_words = []
    for word in words:
        score = sia.polarity_scores(word)['pos']  # 檢查正向分數
        if score > 0:
            positive_words.append(word)
    
    return positive_words

# 提取負向字詞函式
def extract_negative_words(text):
    # 分詞並移除停用詞
    stop_words = set(stopwords.words('english'))
    words = [word for word in text.split() if word not in stop_words]
    
    # 找出負向詞
    negative_words = []
    for word in words:
        score = sia.polarity_scores(word)['neg']  # 檢查負向分數
        if score > 0:
            negative_words.append(word)
    
    return negative_words

# 對 title 和 body 欄位進行處理
df['cleaned_title'] = df['title'].apply(clean_text)
df['cleaned_body'] = df['body'].apply(clean_text)

# Step 4: 情緒分析
sia = SentimentIntensityAnalyzer()

def get_sentiment(text):
    return sia.polarity_scores(text)['compound']

# 計算情緒分數
df['title_sentiment'] = df['cleaned_title'].apply(get_sentiment)
df['body_sentiment'] = df['cleaned_body'].apply(get_sentiment)

# 綜合判斷正負向
df['overall_sentiment'] = df.apply(
    lambda x: 'positive' if (x['title_sentiment'] + x['body_sentiment']) > 0 else 'negative', axis=1
)

# 提取正向與負向字詞
df['positive_words'] = df['cleaned_body'].apply(extract_positive_words)
df['negative_words'] = df['cleaned_body'].apply(extract_negative_words)

# Step 5: 結果檢視
print("情緒分析結果:")
print(df[['title', 'body', 'overall_sentiment', 'positive_words', 'negative_words']].head())

# Step 6: 統計與視覺化
# 正負向文章數量
sentiment_counts = df['overall_sentiment'].value_counts()
print("正負向文章分佈:")
print(sentiment_counts)

# 繪製情緒分數分佈圖
plt.figure(figsize=(10, 6))
sns.histplot(df['title_sentiment'], kde=True, color='blue', label='Title Sentiment')
sns.histplot(df['body_sentiment'], kde=True, color='orange', label='Body Sentiment')
plt.legend()
plt.title('Sentiment Distribution')
plt.xlabel('Sentiment Score')
plt.ylabel('Frequency')
plt.show()

# Step 7: 文字雲視覺化
# 組合所有正向和負向字詞
all_positive_words = ' '.join([' '.join(words) for words in df['positive_words']])
all_negative_words = ' '.join([' '.join(words) for words in df['negative_words']])

# 繪製正向文字雲
positive_wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_positive_words)
plt.figure(figsize=(10, 6))
plt.imshow(positive_wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Positive Words Word Cloud')
plt.show()

# 繪製負向文字雲
negative_wordcloud = WordCloud(width=800, height=400, background_color='black', colormap='Reds').generate(all_negative_words)
plt.figure(figsize=(10, 6))
plt.imshow(negative_wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Negative Words Word Cloud')
plt.show()

# Step 8: 儲存結果
# 將處理後的資料儲存為新檔案
df.to_csv("reddit_sentiment_analysis_100.csv", index=False)

# Step 9: 找出情緒最強的文章
# 排序後輸出正向與負向情緒分數最高的文章
top_positive = df.nlargest(5, 'body_sentiment')
top_negative = df.nsmallest(5, 'body_sentiment')

print("\n前五高正向文章:")
print(top_positive[['title', 'body', 'body_sentiment']])

print("\n前五高負向文章:")
print(top_negative[['title', 'body', 'body_sentiment']])

print("分析完成，結果已儲存為 'reddit_sentiment_analysis_100.csv'")

import matplotlib.pyplot as plt
import numpy as np
from constants import STOPWORDS
from wordcloud import WordCloud  # , STOPWORDS, ImageColorGenerator


def show_words(text):
    stopwords = set(STOPWORDS)

    x, y = np.ogrid[:300, :300]
    mask = (x - 150) ** 2 + (y - 150) ** 2 > 130 ** 2
    mask = 255 * mask.astype(int)
    # plt.imshow(mask, interpolation="bilinear")

    wc = WordCloud(
        stopwords=stopwords,
        background_color="white",
        repeat=True,
        mask=mask
    ).generate(text)

    plt.figure(figsize=(14, 10), facecolor=None)
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")

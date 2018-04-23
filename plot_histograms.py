# https://www.zanaducloud.com/CC6612B2-B42A-4765-A0C8-4FDB3CEF50E2
import seaborn as sns
from scipy.stats import norm
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
sns.set_palette("deep", desat=.6)
sns.set_context(rc={"figure.figsize": (12, 9)})

# heatmap

mdf = pd.read_csv('heatmap.csv' ,skiprows=0)
sns.heatmap(mdf, xticklabels=5 ,fmt="f" )

#sns.heatmap(mdf, xticklabels=5 ,fmt="f" , linewidths=.05)
#sns.heatmap(mdf, fmt="f", linewidths=.1 ,   cbar=False) # annot=True,

#sns.heatmap(mdf, cbar=False) #Remove color bar
#sns.plt.show()

#sns.heatmap(mdf, xticklabels=1 ,  fmt="f") #Hide a few axis labels to avoid overlapping
sns.plt.show()




#book_distance_from_global_books_sample
df = pd.DataFrame()
df = pd.read_csv('book_distance_from_global_books_sample.csv' ,skiprows=0)
print df.head(4)
my_palette = ["SlateGray", "CornflowerBlue", "PeachPuff", "MediumSeaGreen"]
current_palette = sns.color_palette(my_palette)
sns.set_palette(current_palette, 10)
# Add the x-axis title
plt.xlabel("Distance of book from corpus", fontsize=10)
# Add the y-axis title
plt.ylabel("Number of books", fontsize=10)
# Add the plot title
plt.title("Distance of book from corpus", fontsize=14)
ax = sns.distplot(df.distance.dropna(), fit=norm ,  label='Distance of book from corpus')  # hist_kws={"alpha": 1, "color": "MediumSeaGreen"})#  fit=norm , hist_kws={"alpha": 1, "color": "SlateGray"}) #, kde_kws={"color": "SlateGray", "lw": 2 },hist_kws={"alpha": 1, "color": "MediumSeaGreen"})
plt.legend()
#sns.plt.show()


df = pd.DataFrame()
df = pd.read_csv('distance_of_chapter_from_its_book_NN.csv' ,skiprows=0)
print df.head(4)
my_palette = ["SlateGray", "CornflowerBlue", "PeachPuff", "MediumSeaGreen"]
current_palette = sns.color_palette(my_palette)
sns.set_palette(current_palette, 10)
# Add the x-axis title
plt.xlabel("Distance of chapter from its book", fontsize=10)
# Add the y-axis title
plt.ylabel("Number of chapters", fontsize=10)
# Add the plot title
plt.title("Distance of chapters from their books", fontsize=14)
ax = sns.distplot(df.distance.dropna(), fit=norm ,  label='Distance of chapter from its book' ,color="mediumpurple")  # hist_kws={"alpha": 1, "color": "MediumSeaGreen"})#  fit=norm , hist_kws={"alpha": 1, "color": "SlateGray"}) #, kde_kws={"color": "SlateGray", "lw": 2 },hist_kws={"alpha": 1, "color": "MediumSeaGreen"})
plt.legend()
sns.plt.show()


plt.title("Distance of chapter from other chapter", fontsize=14)
df = pd.read_csv('inter_chapter_distances.csv' ,skiprows=0)
ax.set_title('Distance of chapters from other chapters')
sns.set_palette(current_palette, 10)
ax=sns.distplot(df.same_book.dropna()  , fit=norm ,  label='within the same book'  )
ay=sns.distplot(df.other_book.dropna() , fit=norm ,  label='from other book' )
sns.plt.suptitle('Nouns , 10 chapters per book , different authors')
plt.ylabel("Number of chapters", fontsize=10)
plt.xlabel("inter chapter Distance", fontsize=10)
plt.legend()
sns.plt.show()


plt.title("Distance of chapter from other chapter", fontsize=14)
df = pd.read_csv('inter_chapter_distances_jane.csv' ,skiprows=0)
sns.set_palette(current_palette, 10)
ax.set_title('Distance of chapters from other chapters')
ax=sns.distplot(df.same_book.dropna()  , fit=norm ,  label='within the same book'  )
ay=sns.distplot(df.other_book.dropna() , fit=norm ,  label='from other book' )
sns.plt.suptitle('Nouns , 10 chapters per book , same author')
plt.ylabel("Number of chapters", fontsize=10)
plt.xlabel("inter chapter Distance", fontsize=10)
plt.legend()
sns.plt.show()


#game


sns.kdeplot(df.same_book.dropna(), shade=True , label="within the same book")
sns.kdeplot(df.other_book.dropna(), shade=True, label="from other book" )
sns.plt.show()




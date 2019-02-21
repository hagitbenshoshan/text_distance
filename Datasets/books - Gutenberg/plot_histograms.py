# https://www.zanaducloud.com/CC6612B2-B42A-4765-A0C8-4FDB3CEF50E2
import seaborn as sns
from scipy.stats import norm
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

sns.set_palette("deep", desat=.6)
sns.set_context(rc={"figure.figsize": (12, 9)})

# heatmap
#
# reverse colors

"""
mdf = pd.read_csv('heatmap_jane.csv' ,skiprows=0)

g=sns.heatmap(mdf,   annot=False,fmt=".3f",vmin=0.3,cmap = 'YlGnBu_r' ) #'Blues_r') # , cbar_kws={"orientation": "horizontal"})
#Colormap Possible values are: Accent, Accent_r, Blues, Blues_r, BrBG, BrBG_r, BuGn, BuGn_r, BuPu, BuPu_r, CMRmap, CMRmap_r, Dark2, Dark2_r, GnBu, GnBu_r, Greens, Greens_r, Greys, Greys_r, OrRd, OrRd_r, Oranges, Oranges_r, PRGn, PRGn_r, Paired, Paired_r, Pastel1, Pastel1_r, Pastel2, Pastel2_r, PiYG, PiYG_r, PuBu, PuBuGn, PuBuGn_r, PuBu_r, PuOr, PuOr_r, PuRd, PuRd_r, Purples, Purples_r, RdBu, RdBu_r, RdGy, RdGy_r, RdPu, RdPu_r, RdYlBu, RdYlBu_r, RdYlGn, RdYlGn_r, Reds, Reds_r, Set1, Set1_r, Set2, Set2_r, Set3, Set3_r, Spectral, Spectral_r, Vega10, Vega10_r, Vega20, Vega20_r, Vega20b, Vega20b_r, Vega20c, Vega20c_r, Wistia, Wistia_r, YlGn, YlGnBu, YlGnBu_r, YlGn_r, YlOrBr, YlOrBr_r, YlOrRd, YlOrRd_r, afmhot, afmhot_r, autumn, autumn_r, binary, binary_r, bone, bone_r, brg, brg_r, bwr, bwr_r, cool, cool_r, coolwarm, coolwarm_r, copper, copper_r, cubehelix, cubehelix_r, flag, flag_r, gist_earth, gist_earth_r, gist_gray, gist_gray_r, gist_heat, gist_heat_r, gist_ncar, gist_ncar_r, gist_rainbow, gist_rainbow_r, gist_stern, gist_stern_r, gist_yarg, gist_yarg_r, gnuplot, gnuplot2, gnuplot2_r, gnuplot_r, gray, gray_r, hot, hot_r, hsv, hsv_r, inferno, inferno_r, jet, jet_r, magma, magma_r, nipy_spectral, nipy_spectral_r, ocean, ocean_r, pink, pink_r, plasma, plasma_r, prism, prism_r, rainbow, rainbow_r, seismic, seismic_r, spectral, spectral_r, spring, spring_r, summer, summer_r, tab10, tab10_r, tab20, tab20_r, tab20b, tab20b_r, tab20c, tab20c_r, terrain, terrain_r, viridis, viridis_r, winter, winter_r
g.set_yticklabels(['10','9','8','7','6','5','4','3','2','Pride 1',
                   '10','9','8','7','6','5','4','3','2','Emma 1 ',
                   '10','9','8','7','6','5','4','3','2','Alice 1'],
                   rotation=0,  fontsize=10)
g.set_xticklabels(['Alice 1','2','3','4','5','6','7','8','9','10',
                   'Emma 1' ,'2','3','4','5','6','7','8','9','10',
                   'Pride 1','2','3','4','5','6','7','8','9','10'],
                   rotation=90,  fontsize=10)
g.set_ylabel('Book\'s chapters',fontdict={'fontsize' : 12, 'fontweight':'bold'})
g.set_xlabel('Book\'s chapters',fontdict={'fontsize' : 12, 'fontweight':'bold'})
#sns.heatmap(mdf, cbar=False) #Remove color bar
#sns.plt.show()
plt.title("Distance of chapter from other chapter, 3 books , 2 different authors", fontsize=14)
#sns.heatmap(mdf, xticklabels=1 ,  fmt="f") #Hide a few axis labels to avoid overlapping
sns.plt.show()
 


#book_distance_from_global_books_sample
df = pd.DataFrame()
df = pd.read_csv('distance_of_book_from_DVR_JJ_NN.csv' ,skiprows=0)
print df.head(4)
my_palette = ["CornflowerBlue", "PeachPuff", "MediumSeaGreen","SlateGray"]
current_palette = sns.color_palette(my_palette)
sns.set_palette(current_palette, 10)
# Add the x-axis title
plt.xlabel("Distance of dataset from corpus", fontsize=10)
# Add the y-axis title
plt.ylabel("Number of datasets", fontsize=10)
# Add the plot title
plt.title("Distance of single dataset from corpus", fontsize=14)
ax = sns.distplot(df.distance.dropna(), fit=norm ,  label='Distance of book from corpus')  # hist_kws={"alpha": 1, "color": "MediumSeaGreen"})#  fit=norm , hist_kws={"alpha": 1, "color": "SlateGray"}) #, kde_kws={"color": "SlateGray", "lw": 2 },hist_kws={"alpha": 1, "color": "MediumSeaGreen"})
plt.legend()
sns.plt.show()
 

"""
df = pd.DataFrame()
df = pd.read_csv('distance_of_virtual_chapter_from_its_book_NN.csv' ,skiprows=0)
print df.head(4)
my_palette = ["SlateGray", "CornflowerBlue", "PeachPuff", "MediumSeaGreen"]
current_palette = sns.color_palette(my_palette)
sns.set_palette(current_palette, 10)
# Add the x-axis title
plt.xlabel("Distance of chapter from its virtual book", fontsize=10)
# Add the y-axis title
plt.ylabel("Number of chapters", fontsize=10)
# Add the plot title
plt.title("Distance of chapters", fontsize=14)
#ax = sns.distplot(df.distance.dropna(), fit=norm ,  label='Distance of chapter from its virtual book JJ' ,color="SlateGray",hist_kws={'range': (0.0, 1.0)})  # hist_kws={"alpha": 1, "color": "MediumSeaGreen"})#  fit=norm , hist_kws={"alpha": 1, "color": "SlateGray"}) #, kde_kws={"color": "SlateGray", "lw": 2 },hist_kws={"alpha": 1, "color": "MediumSeaGreen"})
ax = sns.distplot(df.distance.dropna(), fit=norm ,  label='Distance of chapter its virtual book' ,color="MediumSeaGreen")  # hist_kws={"alpha": 1, "color": "MediumSeaGreen"})#  fit=norm , hist_kws={"alpha": 1, "color": "SlateGray"}) #, kde_kws={"color": "SlateGray", "lw": 2 },hist_kws={"alpha": 1, "color": "MediumSeaGreen"})

plt.legend()
df = pd.DataFrame()
df = pd.read_csv('distance_of_virtual_chapter_from_its_book_NN.csv' ,skiprows=0)
print df.head(4)
my_palette = ["SlateGray", "CornflowerBlue", "PeachPuff", "MediumSeaGreen"]
current_palette = sns.color_palette(my_palette)
sns.set_palette(current_palette, 10)
# Add the x-axis title
plt.xlabel("Distance of chapter from corpus", fontsize=10)
# Add the y-axis title
plt.ylabel("Number of chapters", fontsize=10)
# Add the plot title
plt.title("Distance of chapters", fontsize=14)
ax = sns.distplot(df.dist_from_corpus.dropna(), fit=norm ,  label='Distance of chapter from corpus' ,color="CornflowerBlue")  # hist_kws={"alpha": 1, "color": "MediumSeaGreen"})#  fit=norm , hist_kws={"alpha": 1, "color": "SlateGray"}) #, kde_kws={"color": "SlateGray", "lw": 2 },hist_kws={"alpha": 1, "color": "MediumSeaGreen"})
plt.xlabel("Distance of chapter from corpus / virtual book", fontsize=10)

#ax = sns.distplot(df.distance.dropna(), fit=norm ,  label='Distance of chapter from its virtual book NN' ,color="mediumpurple", hist_kws={'range': (0.0, 1.0)})  # hist_kws={"alpha": 1, "color": "MediumSeaGreen"})#  fit=norm , hist_kws={"alpha": 1, "color": "SlateGray"}) #, kde_kws={"color": "SlateGray", "lw": 2 },hist_kws={"alpha": 1, "color": "MediumSeaGreen"})
plt.legend()
sns.plt.show()

"""

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


"""

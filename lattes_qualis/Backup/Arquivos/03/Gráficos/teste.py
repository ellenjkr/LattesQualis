import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
import matplotlib
import openpyxl
from openpyxl.drawing.image import Image
import PIL

df = pd.read_csv("teste.csv", sep=";", encoding="utf-8")

soma_irestrito = 0
for pos, i in enumerate(df["Irestrito"]):
	df["Irestrito"][pos] = float(i.replace(",", "."))
	soma_irestrito += df["Irestrito"][pos]
	# porcentagens.append(100/16 * df["Irestrito"][pos])

irestrito = pd.DataFrame(columns=["Nome", "Irestrito", "Porcentagem", "Porcentagem Acumulada"])
irestrito["Nome"] = df["Nome"]
irestrito["Irestrito"] = df["Irestrito"]
irestrito = irestrito.sort_values(by='Irestrito', ascending=False).reset_index(drop=True)

for pos, i in enumerate(irestrito["Irestrito"]):
	irestrito["Porcentagem"][pos] = 100/soma_irestrito * i
	if pos == 0:
		irestrito["Porcentagem Acumulada"][pos] = irestrito["Porcentagem"][pos]
	else:
		irestrito["Porcentagem Acumulada"][pos] = irestrito["Porcentagem Acumulada"][pos-1]+irestrito["Porcentagem"][pos]

matplotlib.rc('xtick', labelsize=15) 
matplotlib.rc('ytick', labelsize=15) 

fig = plt.figure(figsize=(10,6))
ax = fig.add_subplot(1, 1, 1)

ax.set_title("Irestrito", size=18, pad=25)
rects = ax.bar(irestrito["Nome"], irestrito["Irestrito"], color="C0", zorder=3)
ax.set_ylim([0, 16])
ax.tick_params(axis="y", colors="C0")
ax.set_xticklabels(irestrito["Nome"], size=15, rotation=75)
ax.axes.yaxis.set_ticklabels([])

ax2 = ax.twinx()
ax2.plot(irestrito["Nome"], irestrito["Porcentagem Acumulada"], color="C1", marker="o", ms=5)
ax2.set_yticks([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
ax2.yaxis.set_major_formatter(PercentFormatter())
ax2.tick_params(axis="y", colors="C1")
ax2.set_ylim([0, 100])

ax.spines["top"].set_visible(False) 
ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)

ax2.spines["top"].set_visible(False) 
ax2.spines["right"].set_visible(False)
ax2.spines["left"].set_visible(False)

def autolabel(rects, xpos='center'):
    xpos = xpos.lower()  # normalize the case of the parameter
    ha = {'center': 'center', 'right': 'left', 'left': 'right'}
    offset = {'center': 0.5, 'right': 0.57, 'left': 0.43}  # x_txt = x + w*off

    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()*offset[xpos], 1.01*height,
                '{}'.format(height), ha=ha[xpos], va='bottom', fontdict={"fontsize":13})

fig.tight_layout()
ax2.yaxis.grid(color="C0")
autolabel(rects)
ax.tick_params(
    axis='y',
    which='both',
    right=False,
    left=False) 

# plt.show()
plt.savefig('teste.png')

wb = openpyxl.Workbook()
ws = wb.active

img = PIL.Image.open('teste.png')
basewidth = 600
wpercent = (basewidth/float(img.size[0]))
hsize = int((float(img.size[1])*float(wpercent)))
img = img.resize((basewidth,hsize), PIL.Image.ANTIALIAS)
img.save('teste.png') 

img = Image('teste.png')
ws.add_image(img, 'A1')
wb.save("imagem.xlsx")
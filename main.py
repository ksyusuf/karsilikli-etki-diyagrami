from kesit_hesaplayici import NoktaBulucu
from pprint import pprint
import matplotlib.pyplot as plt

nokta_bulucu = NoktaBulucu()
Nr_Mr_tablosu = []
Nr_Mr_tablosu.append(nokta_bulucu.Eksenel_cekme_durumu())
for i in range(20, 600, 2):
    # 20den 700e 30ar artış
    # sanki üst sınırı 700 verince son iki momenti negatif buldu ????
    Nr_Mr_tablosu.append(nokta_bulucu.Nr_Mr_bulucu(i))

Nr_Mr_tablosu.append(nokta_bulucu.Eksenel_basinc_durumu())

pprint(Nr_Mr_tablosu)

x = [x[0] for x in Nr_Mr_tablosu]
y = [y[1] for y in Nr_Mr_tablosu]

plt.plot(y, x, '-', c='red')
plt.scatter(y, x, c='blue', s=30)
plt.xlabel('Mr (kN.m)')
plt.ylabel('Nr (kN)')
plt.title('Karşılıklı Etki Diyagramı')
plt.grid(linestyle='--', alpha=0.7)

ax = plt.gca()
ax.spines['left'].set_position('zero')
ax.spines['left'].set_linewidth(1)
ax.spines['left'].set_color('red')
ax.spines['bottom'].set_position('zero')
ax.spines['bottom'].set_linewidth(1)
ax.spines['bottom'].set_color('red')
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
plt.show()

if __name__ == "__main__":
    print("main içeriden çalıştırıldı.")
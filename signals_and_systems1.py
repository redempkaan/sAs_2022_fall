###################################################################
#myConv fonksiyonum
def myConv():
    x = []
    y = []
    conv = []
    n = input("X isaretinin boyutunu giriniz.\n") # x[n]'in boyut girdisi
    m = input("Y isaretinin boyutunu giriniz.\n") # y[n]'in boyut girdisi
    n = int(n)
    m = int(m)
    for p in range(n):
        x.append(int(input("X isaretinin " + str(p + 1) + ". degerini giriniz.\n"))) # x[n]'in deger girdisi
    print(x)
    sifirx = int(input("X isareti n = 0'da kac numarali degeri veriyor?\n")) - 1 # x[n]'in n = 0'daki degeri
    for l in range(m):
        y.append(int(input("Y isaretinin " + str(l + 1) + ". degerini giriniz.\n"))) # y[n]'in deger girdisi
    print(y)
    sifiry = int(input("Y isareti n = 0'da kac numarali degeri veriyor?\n")) - 1  # x[n]'in n = 0'daki degeri
    for i in range(n + m - 1):
        conv.append(int(0))
        for j in range(n):                 # Konvolusyon toplam fonksiyonu
            if(i - j >= 0 and m > i - j):
                conv[i] = conv[i] + x[j] * y[i - j]
    print("{} ve n = 0'daki degeri = {}".format(conv, conv[sifirx + sifiry])) # Konvolusyon sonuc ciktisi

###############################################################
#Convolusyon fonksiyonlarini ayri ayri grafige dokmek icin kullandigim kod(kendi fonksiyonumdaki degerleri cizdirmek icin yukaridaki myConv fonksiyonumun icine entegre ettim.).
import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True
markerline, stemlines, baseline = plt.stem(np.convolve(x, y), linefmt='grey', markerfmt='*', bottom=1.1)
markerline.set_markerfacecolor('red')

##############################################################
#Ses kayit icin kullandigim kod.
import sounddevice as sd
from scipy.io.wavfile import write

freq = 44100

duration = 5 # 5s - 10s

kayit = sd.rec(int(duration * freq),
                   samplerate=freq, channels=1)

sd.wait()

write("kayit.wav", freq, kayit)

#############################################################
#Kaydedilen .wav uzantili dosyayi okuma ve m=x durtu yaniti icin numpy'in convolusyon fonksiyonunu uygulama.
from scipy.io import wavfile
import numpy as np
import sounddevice as sd
samplerate, data = wavfile.read('kayit.wav')

deneme = [1, 0.8, 1.6] # m=2, m=3 icin deneme.append(2.4) ve m=4 icin deneme.append(2,4) ve deneme.append(3,2)
denemen = np.array(deneme)
conv = np.convolve(denemen, data)

sd.play(conv, 44100, blocking=True)



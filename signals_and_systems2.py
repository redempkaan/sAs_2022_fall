######################### MAIN ###############################################
from scipy.io import wavfile
import numpy as np
import matplotlib.pyplot as plt

#Ilgili .wav dosyasini okuma
samplerate, data = wavfile.read('Ornek.wav')
#Frekans eksenine gecmeden once okudugumuz .wav dosyasinin numpy dizisini 11 esit parcaya bolme
newarray = np.array_split(data, 11)
button_freqs = []
#Dtmf sinuzoidlerini tespit edebilmek icin yaklasik genlik degerleri(verdiginiz .wav dosyasinda aradigimiz sinuzoidlerin genlik seviyeleri yaklasik 20k idi)
amplitude = 20000

#Yukarida tanimladigimiz genligin ustundeki frekanslari tespit etme
for x in range(11):
    fourier = abs(np.fft.fft(newarray[x]))
    freqs = np.fft.fftfreq(len(fourier), 1/samplerate)
    spikes = np.where(fourier >= amplitude)
    listed_spikes = spikes[0].tolist()
    valid_spikes = []
    #Sifir frekansli spike'lari cikarma
    if(listed_spikes[0] == 0):
        listed_spikes.remove(0)
    for p in listed_spikes:
        #Listeledigimiz spikelar icinde aradigimiz frekans degerlerine gore filtreleyip "button_freqs" dizisine aktarma
        if(freqs[p] >= 690 and freqs[p] <=1485):
            valid_spikes.append(freqs[p])
    button_freqs.append(valid_spikes)

buttons = [] #Bos tus dizisi

#Yaklasik degerde olan frekans degerlerini duzeltme
for n in button_freqs:
    for z in range(2):
        if(n[z] >= 687 and n[z] <= 705):
            n[z] = 697
        elif(n[z] >= 760 and n[z] <= 780):
            n[z] = 770
        elif(n[z] >= 842 and n[z] <= 862):
            n[z] = 852
        elif(n[z] >= 931 and n[z] <= 951):
            n[z] = 941
        elif(n[z] >= 1200 and n[z] <= 1219):
            n[z] = 1209
        elif(n[z] >= 1330 and n[z] <= 1340):
            n[z] = 1336
        else:
            n[z] = 1477

# Ilgili frekans ikililerine tuslari atama
for lp in range(len(button_freqs)):
    if(button_freqs[lp] == [697, 1209]):
        buttons.append(1)
    elif(button_freqs[lp] == [697, 1336]):
        buttons.append(2)
    elif(button_freqs[lp] == [697, 1477]):
        buttons.append(3)
    elif(button_freqs[lp] == [770, 1209]):
        buttons.append(4)
    elif(button_freqs[lp] == [770, 1336]):
        buttons.append(5)
    elif(button_freqs[lp] == [770, 1477]):
        buttons.append(6)
    elif(button_freqs[lp] == [852, 1209]):
        buttons.append(7)
    elif(button_freqs[lp] == [852, 1336]):
        buttons.append(8)
    elif(button_freqs[lp] == [852, 1477]):
        buttons.append(9)
    elif(button_freqs[lp] == [941, 1209]):
        buttons.append("*")
    elif(button_freqs[lp] == [941, 1336]):
        buttons.append(0)
    else:
        buttons.append("#")



print(button_freqs) #Her bir tusun 2 boyutlu frekans dizisi
print(buttons) #Her bir tusun 2 boyutlu frekans dizisinin karsilik geldigi tus

#########################################################################################
#Rapordaki grafik cizelgeleri icin kullandigim kod
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

samplerate, data = wavfile.read('Ornek.wav') #Kendi numaramin grafiklerini cizdirmek icin "05062221467.wav"
newarray = np.array_split(data, 11)

fourier = abs(np.fft.fft(newarray[x])) #X yerine 1'den 11'e kadar olan degerleri girdim
freqs = np.fft.fftfreq(len(fourier), 1/samplerate)

plt.plot(freqs[range(int(len(fourier)/2))], fourier[range(int(len(fourier)/2))])
plt.xlabel("Frequency HZ")
plt.ylabel("Amplitude")
plt.show()

#########################################################################################
#"my_number" kismina girilen numarayi dtmf formatinda sentezleyip kaydederken kullandigim kod
import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write

my_number = [0, 5, 0, 6, 2, 2, 2, 1, 4, 6, 7] #Numaram

length = len(my_number)

sound = [] #Icini dolduracagim bos dizi

time = 0.3 #Her bir tus icin ayrilan sure
delayTime = 0.1 #Tuslar arasi bosluk icin ayrilan sure

Fs = 8000 #Ornekleme frekansi

runningTime = np.linspace(0,time,int(time*Fs+1)) #Peakleri kademeli olarak vermek icin olusturdugum aralik(ekleyecegim sinuzoidlerle carpmak icin kullanacagim)

lofreq = 0
hifreq = 0
totalfreq = 0

delay = np.sin(2*np.pi*20000*delayTime) #Aralik sinuzoidi


for x in range(11): #11 basamakli telefon numarasina uygun sinuzoidleri sirayla "sound" dizisinin icine ekleme

    if my_number[x] == 1:
        lofreq = np.sin(2 * np.pi * 697 * runningTime)
        hifreq = np.sin(2 * np.pi * 1209 * runningTime)
        totalfreq = lofreq + hifreq
        sound.append(lofreq + hifreq) #Ikili sinuzoidleri ekleme
        sound.append(delay) #Aralik ekleme(her adimda var)

    elif my_number[x] == 2:
        lofreq = np.sin(2 * np.pi * 697 * runningTime)
        hifreq = np.sin(2 * np.pi * 1336 * runningTime)
        totalfreq = lofreq + hifreq
        sound.append(lofreq + hifreq)
        sound.append(delay)

    elif my_number[x] == 3:
        lofreq = np.sin(2 * np.pi * 697 * runningTime)
        hifreq = np.sin(2 * np.pi * 1477 * runningTime)
        totalfreq = lofreq + hifreq
        sound.append(lofreq + hifreq)
        sound.append(delay)


    elif my_number[x] == 4:
        lofreq = np.sin(2 * np.pi * 770 * runningTime)
        hifreq = np.sin(2 * np.pi * 1209 * runningTime)
        totalfreq = lofreq + hifreq
        sound.append(lofreq + hifreq)
        sound.append(delay)

    elif my_number[x] == 5:
        lofreq = np.sin(2 * np.pi * 770 * runningTime)
        hifreq = np.sin(2 * np.pi * 1336 * runningTime)
        totalfreq = lofreq + hifreq
        sound.append(lofreq + hifreq)
        sound.append(delay)

    elif my_number[x] == 6:
        lofreq = np.sin(2 * np.pi * 770 * runningTime)
        hifreq = np.sin(2 * np.pi * 1477 * runningTime)
        totalfreq = lofreq + hifreq
        sound.append(lofreq + hifreq)
        sound.append(delay)


    elif my_number[x] == 7:
        lofreq = np.sin(2 * np.pi * 852 * runningTime)
        hifreq = np.sin(2 * np.pi * 1209 * runningTime)
        totalfreq = lofreq + hifreq
        sound.append(lofreq + hifreq)
        sound.append(delay)

    elif my_number[x] == 8:
        lofreq = np.sin(2 * np.pi * 852 * runningTime)
        hifreq = np.sin(2 * np.pi * 1336 * runningTime)
        totalfreq = lofreq + hifreq
        sound.append(lofreq + hifreq)
        sound.append(delay)

    elif my_number[x] == 9:
        lofreq = np.sin(2 * np.pi * 852 * runningTime)
        hifreq = np.sin(2 * np.pi * 1477 * runningTime)
        totalfreq = lofreq + hifreq
        sound.append(lofreq + hifreq)
        sound.append(delay)


    elif my_number[x] == '*':
        lofreq = np.sin(2 * np.pi * 941 * runningTime)
        hifreq = np.sin(2 * np.pi * 1209 * runningTime)
        totalfreq = lofreq + hifreq
        sound.append(lofreq + hifreq)
        sound.append(delay)

    elif my_number[x] == 0:
        lofreq = np.sin(2 * np.pi * 941 * runningTime)
        hifreq = np.sin(2 * np.pi * 1336 * runningTime)
        totalfreq = lofreq + hifreq
        sound.append(lofreq + hifreq)
        sound.append(delay)

    elif my_number[x] == '#':
        lofreq = np.sin(2 * np.pi * 941 * runningTime)
        hifreq = np.sin(2 * np.pi * 1477 * runningTime)
        totalfreq = lofreq + hifreq
        sound.append(lofreq + hifreq)
        sound.append(delay)



signal = np.hstack(sound) #"Signal" dizisi icerisindeki farkli boyutta olan degerleri tek bir boyut icerisinde toplama
signal = signal.astype(np.float32) #Media playerlarin .wav dosyasini acabilmesi icin format degistirme(aksi takdirde acilmiyor fakat icerigi oynatilabiliyor)
write("05062221467.wav", 8000, signal) #"Signal" dizisini "Number.wav" adiyla kaydetme

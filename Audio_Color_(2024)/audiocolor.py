#audiocolor.py
#Created by Max Figura, 2024

import wave, struct

#What envelope values should be normalised to
weight = 0.5

#Filter audio should be mapped to
command = "colorkey@r similarity"

#Open soundfile
filename = "crux-of-night_padclip.wav"
wavefile = wave.open(filename, mode="rb")

#Collect soundfile data
length = wavefile.getnframes()
rate = wavefile.getframerate()

#Set resolution of envelope
#groupsize = 256
persecond = 100
seg = rate//persecond

print(length)
print(rate)
#print(wavefile.getparams())

data = []

#Read file and construct envelope
for i in range(0,length//seg):
    wavedata = wavefile.readframes(seg)
    #print(wavedata)
    #print(struct.unpack("<"+str(seg)+"h", wavedata))
    data.append(abs(max(struct.unpack("<"+str(seg)+"h", wavedata),key=abs)))

wavefile.close()

#Normalise envelope to filter input range
peak = max(data)
normalised = []
for item in data: normalised.append(max(weight*item/peak,0.01))

print(normalised)
print(len(normalised))

#Print to cmd file
outfile = open(filename.split('.')[0]+"_"+weight+".cmd", 'w')
delt = seg/rate
t = 0.0
for item in normalised:
    t+=delt
    outfile.write("{:.3f} [enter] "+command+" {:.3f};\n".format(t,item))

outfile.close()

import urllib.request, json
import requests

# url = "https://console.developers.google.com/apis/credentials?project=myprojecthigor"

file = open('output.txt', 'w')

# keys:
keys = {
  0: "Au6nf_Hd8U1P4yzxWZcScLHX3SCg5e5zr_HZe3Cj4BxLAjrsG-Se-FiwjN4x22S1",
  1: "AmPsIl8Ju0AfGmdyYFnuYvmnue5fMPL5j589ElF3SV1K7Wn3gwD1_NFD9UF_ggLN",
  2: "Al-BojSmkfANHYOh0l3HWMfKrRMKnX_IYBSpucQQ_MhHvrL1g6fV8jY5GS3TLt07",
  3: "AvJ4JPRcaejt8Uf5ZToqXbtSQdZotUOWokICfoTMlC6thCSlf0h_Hlibt1hoAs16",
  4: "Aj2bD6YctIAVi41UTk0OhNIRu1Z3eamOBqC_jvM8ECwNk4MSalbMpP_PvJQw5XGw"
}

dados = [
	('m', '-5.782087, -35.197515'),
	('e', '-5.791346, -35.208820'),
	('e', '-5.780970, -35.201846'),
	('e', '-5.788314, -35.199164'),
	('e', '-5.783703, -35.197940'),
	('c', '-5.790278, -35.197833'),
	('c', '-5.791581, -35.202232'),
	('c', '-5.785261, -35.197919'),
	('c', '-5.788250, -35.204828'),
	('c', '-5.778222, -35.202532'),
	('c', '-5.777229, -35.198380'),
	('c', '-5.773418, -35.204560'),
	('c', '-5.787241, -35.209302'),
	('c', '-5.790475, -35.206512'),
	('c', '-5.784796, -35.204806'),
	('c', '-5.787891, -35.195729'),
	('c', '-5.785607, -35.201898'),
	('c', '-5.779941, -35.198030'),
	('c', '-5.779641, -35.198230')
]


def jsonToLineCod(dt_orig, dt_json):
	d = dt_orig[1].split(', ')
	x = list(map(lambda x: x['travelDistance'], dt_json['resourceSets'][0]['resources'][0]['results']))
	s = dt_orig[0] + ' p ' + d[0] + ' ' + d[1] + ' d '
	for i in range(0,len(x)-1):
		s += str(x[i]) + ' '	
	return s + str(x[len(x)-1]) + '\n'


i = 0
while i < len(dados):
	origin = dados[i][1]
	dest = ''
	k = 0
	while k < len(dados):
		#if k != i:
		dest += dados[k][1] + ';'
		k += 1 
	dest = dest[:len(dest)-1]
	url = "https://dev.virtualearth.net/REST/v1/Routes/DistanceMatrix?origins=" + origin + "&destinations=" + dest + "&travelMode=driving&key=" + keys[int(i) % len(keys)]
	response = requests.get(url) 
	data = response.json()
	file.write(jsonToLineCod(dados[i], data))
	i += 1

file.close()



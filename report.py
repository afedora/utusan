import requests, re, time, random, os
from bs4 import BeautifulSoup as Scraping
from concurrent.futures import ThreadPoolExecutor as Thread

R='\033[31m'
G='\033[32m'
Y='\033[33m'
B='\033[34m'
P='\033[35m'
C='\033[36m'
W='\033[37m'
O='\033[33m'
E='\033[31m'

session=requests.Session()
home_url = 'https://mbasic.facebook.com'
header = {
	'Host':'mbasic.facebook.com',
		'cache-control':'max-age=0',
	'upgrade-insecure-requests':'1',
		'user-agent':'Mozilla/5.0 (Linux; Android 11; SM-A325F Build/RP1A.200720.012; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/95.0.4638.74 Mobile Safari/537.36',
	'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
		'x-requested-with':'mark.via.gp',
	'sec-fetch-site':'none',
		'sec-fetch-mode':'navigate',
	'sec-fetch-user':'?1',
		'sec-fetch-dest':'document',
	'accept-encoding':'gzip, deflate',
		'accept-language':'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7'
}

def login () :
	os.system('clear')
	cok = input('{}({}+{}) {}Cookie {}:{} '.format(W,O,W,B,P,G))
	header.update({"cookie" : str(cok) })
	try :
		f=session.get(home_url, headers=header).text
		if 'mbasic_logout_button' in str(f):
			save=open('coki.log', 'w')
			save.write(str(cok))
			save.close()
			print (f"{G}[●] Login berhasil ")
			time.sleep(2),Report().menu()
		else :
			print(
				'{}({}!{}){} Cookie salah'.format(W,R,W,Y))
			time.sleep(2),login ()
	except Exception as E:
		exit('{}({}!{}){} kesalahan : {}'.format(W,R,W,Y, E))

def load_cookie():
	try :
		Get = open('coki.log', 'r').read()
		return {'cookie': str(Get) }
	except :
		login ()
		
def webGet(home_url):
	x = session.get(
		home_url, headers=header, cookies=load_cookie()).text
	return x
		
def webPost(home_url, data):
	x = session.post(
		home_url, headers=header, cookies=load_cookie(), data=data).text
	return x

class Report():

	def __init__(self):
		self.xx=[]
		self.wh=[]
		self.count=[]
		
	def menu(self):
		try :
			orein=Scraping(webGet(home_url+"/profile.php?"), "html.parser")
			if 'mbasic_logout_button' in str(orein):
				name=str(orein.find('title').text)
			else :
				exit('{}({}!{}){} Cookies mati'.format(W,R,W,Y))
				time.sleep(2),login()
		except(requests.exceptions.ConnectionError):
			exit('{}({}!{}){} Koneksi bermasalah'.format(W,R,W,Y))
		except Exception as E:
			exit('{}({}!{}){} kesalahan : {}'.format(W,R,W,Y, E))
		else :
			os.system('clear')
			print (f"{W}({O}●{W}){B} WELCOME {P}: {G}{name} ")
			print('{}─'.format(W)*45)
			print('{}({}01{}). {}Auto report orang'.format(W,O,W,B))
			print('{}({}02{}). {}Auto report grup'.format(W,O,W,B))
			print('{}({}03{}). {}Auto report halaman'.format(W,O,W,B))
			print('{}─'.format(W)*45)
			while True:
				ask=input('{}({}+{}) {}pilih {}:{} '.format(W,O,W,B,P,G))
				if ask in ['01', '1']:
					self.metode=self.next_people
					self.people()
				elif ask in ['02', '2']:
					self.metode=self.next_grup
					self.grup()
				elif ask in ['03', '3']:
					self.metode=self.next_people
					self.fanspage()
				else :
					continue
		
	def people(self):
		stop=False
		while True:
			ure=input('{}({}+{}) {}id/username teman {}:{} '.format(W,O,W,B,P,G))
			if ure=="":
				continue
			g=Scraping(webGet(home_url+'/'+ure+'?v=timeline'), "html.parser")
			if 'Anda Diblokir Sementara' in str(g):
				exit('{}({}!{}){} akun anda terkena blokir/limit'.format(W,R,W,Y))
			elif not 'Minta dukungan atau laporkan postingan' in str(g):
				print('{}({}!{}){} id/username salah / profil tidak publik'.format(W,R,W,Y))
				continue
			else:
				name=str(g.find('title').string)
				print('{}({}+{}) {}nama target {}: {}{}'.format(W,O,W,B,P,G,name))
				break
		while True:
			try:
				max=int(input('{}({}+{}) {}Jumlah post yang ingin di report {}:{} '.format(W,O,W,B,P,G)))
			except:
				continue
			ure=home_url+'/'+ure+'?v=timeline'
			while True:
				try:
					g=Scraping(webGet(ure), "html.parser")
					for a in g.find_all('a', string='Minta dukungan atau laporkan postingan', href=True):
						self.xx.append(home_url+a['href'])
						print(f"\r{W}({R}•{W}){B} mengumpulkan post {P}: {W}({R}{len(self.xx)}{W})",end="")
						if len(self.xx) == max or len(self.xx) > max:
							stop=True
							print(),exit(self.thread())
					if stop==False:
						if 'Lihat Berita Lain' in str(g):
							ure=home_url+g.find('a', string='Lihat Berita Lain')['href']
						else:
							if 'Anda Diblokir' in str(g):
								if bool(self.xx)==True:
									print('\n{}({}!{}){} akun anda terkena blokir/limit'.format(W,R,W,Y))
									print(),exit(self.thread())
								else:
									exit('\n{}({}!{}){} akun anda terkena blokir/limit'.format(W,R,W,Y))
							else:
								if bool(self.xx)==True:
									print(),exit(self.thread())
								else:
									print('{}({}!{}){} semua post tidak publik'.format(W,R,W,Y))
									self.people()
					else:
						print(),exit(self.thread())
				except(requests.exceptions.ConnectionError):
					for load in ["|", "/", "-", "\\"]:
						print(f'\r{W}({R}{load}{W}){Y} menunggu koneksi ...', end='       ')
						time.sleep(000.07)
				except Exception as E:
					exit('{}({}!{}){} kesalahan : {E}'.format(W,R,W,Y))
		
	def grup(self):
		stop=False
		while True:
			ure=input('{}({}+{}) {}id/username grup {}:{} '.format(W,O,W,B,P,G))
			if ure=="":
				continue
			g=Scraping(webGet(home_url+'/groups/'+ure), "html.parser")
			if 'Anda Diblokir Sementara' in str(g):
				exit('{}({}!{}){} akun anda terkena blokir/limit'.format(W,R,W,Y))
			elif not 'Lainnya' in str(g.find('a', string='Lainnya', href=True)):
				print('{}({}!{}){} id/username salah / grup tidak publik'.format(W,R,W,Y))
				continue
			else:
				name=str(g.find('title').string)
				print('{}({}+{}) {}nama grup {}: {}{}'.format(W,O,W,B,P,G,name))
				break
		while True:
			try:
				max=int(input('{}({}+{}) {}Jumlah post yang mau di report {}:{} '.format(W,O,W,B,P,G)))
			except:
				continue
			target=home_url+'/groups/'+ure
			while True:
				try:
					owe=Scraping(webGet(target), "html.parser")
					for nex in owe.find_all('a', string='Lainnya', href=True):
						self.xx.append(home_url+nex['href'])
						print(f"\r{W}({R}•{W}){B} mengumpulkan post {P}: {W}({R}{len(self.xx)}{W})",end="")
						if len(self.xx) == max or len(self.xx) > max:
							stop=True
							print(),exit(self.thread())
					if stop==False:
						if 'Lihat Postingan Lainnya' in str(owe):
							target=home_url+owe.find('a',string='Lihat Postingan Lainnya')['href']
						else:
							if 'Anda Diblokir' in str(owe):
								if bool(self.xx)==True:
									print('\n{}({}!{}){} akun anda terkena blokir/limit'.format(W,R,W,Y))
									print(),exit(self.thread())
								else:
									exit('{}({}!{}){} akun anda terkena blokir/limit'.format(W,R,W,Y))
							else:
								if bool(self.xx)==True:
									print(),exit(self.thread())
								else:
									print('{}({}!{}){} id/username salah atau tidak publik'.format(W,R,W,Y))
									exit(self.grup())
					else: 
						print(),exit(self.thread())
				except(requests.exceptions.ConnectionError):
					for load in ["|", "/", "-", "\\"]:
						print(f'\r{W}({R}{load}{W}){Y} menunggu koneksi ...', end='       ')
						time.sleep(000.07)
				except Exception as E:
					exit('{}({}!{}){} kesalahan : {}'.format(W,R,W,Y, E))
			
	def fanspage(self):
		stop=False
		while True:
			ure=input('{}({}+{}) {}id/username halaman {}:{} '.format(W,O,W,B,P,G))
			if ure=="":
				continue
			g=Scraping(webGet(home_url+'/'+ure), "html.parser")
			if 'Anda Diblokir Sementara' in str(g):
				print('{}({}!{}){} akun terkena blokir'.format(W,R,W,Y))
				continue
			elif not 'Minta dukungan atau laporkan postingan' in str(g):
				print(g)
				print('{}({}!{}){} id/username salah / halaman tidak publik'.format(W,R,W,Y))
				continue
			else:
				name=str(g.find('title').string)
				print('{}({}+{}) {}nama halaman {}: {}{}'.format(W,O,W,B,P,G,name))
				break
		while True:
			try:
				max=int(input('{}({}+{}) {}Jumlah post yang mau di report {}:{} '.format(W,O,W,B,P,G)))
			except:
				continue
			ure=home_url+'/'+ure
			while True:
				try:
					g=Scraping(webGet(ure), "html.parser")
					for a in g.find_all('a', string='Minta dukungan atau laporkan postingan', href=True):
						self.xx.append(home_url+a['href'])
						print(f"\r{W}({R}•{W}){B} mengumpulkan post {P}: {W}({R}{len(self.xx)}{W})",end="")
						if len(self.xx) == max or len(self.xx) > max:
							stop=True
							print(),exit(self.thread())
					if stop==False:
						if 'Tampilkan lainnya' in str(g):
							ure=home_url+g.find('a', string='Tampilkan lainnya')['href']
						else:
							if 'Anda Diblokir' in str(g):
								if bool(self.xx)==True:
									print('\n{}({}!{}){} akun anda terkena blokir/limit'.format(W,R,W,Y))
									print(),exit(self.thread())
								else:
									exit('\n{}({}!{}){} akun anda terkena blokir/limit'.format(W,R,W,Y))
							else:
								if bool(self.xx)==True:
									print(),exit(self.thread())
								else:
									print('{}({}!{}){} id/username halaman salah'.format(W,R,W,Y))
									self.people()
					else:
						print(),exit(self.thread())
				except(requests.exceptions.ConnectionError):
					for load in ["|", "/", "-", "\\"]:
						print(f'\r{W}({R}{load}{W}){Y} menunggu koneksi ...', end='       ')
						time.sleep(000.07)
				except Exception as E:
					exit('{}({}!{}){} kesalahan : {E}'.format(W,R,W,Y))
	
	def thread(self):
		print('{}─'.format(W)*45)
		print('{}({}01{}). {}report ketelanjangan'.format(W,O,W,B))
		print('{}({}02{}). {}report kekerasan'.format(W,O,W,B))
		print('{}({}03{}). {}report pelecehan'.format(W,O,W,B))
		print('{}({}04{}). {}report penjualan tidak resmi'.format(W,O,W,B))
		print('{}({}05{}). {}report ujaran kebencian'.format(W,O,W,B))
		print('{}({}06{}). {}report terorisme'.format(W,O,W,B))
		print('{}({}07{}). {}report konten vulgar'.format(W,O,W,B))
		print('{}─'.format(W)*45)
		while True:
			ow=input('{}({}+{}) {}pilih {}:{} '.format(W,O,W,B,P,G))
			if ow in ['01','1']:
				self.wh.append('nudity')
				print('{}─'.format(W)*45),;break
			elif ow in ['02','2']:
				self.wh.append('violence')
				print('{}─'.format(W)*45),;break
			elif ow in ['03','3']:
				self.wh.append('harassment')
				print('{}─'.format(W)*45),;break
			elif ow in ['04','4']:
				self.wh.append('unauthorized_sales')
				print('{}─'.format(W)*45),;break
			elif ow in ['05','5']:
				self.wh.append('hate_speech')
				print('{}─'.format(W)*45),;break
			elif ow in ['06','6']:
				self.wh.append('terrorism')
				print('{}─'.format(W)*45),;break
			elif ow in ['07','7']:
				self.wh.append('gross')
				print('{}─'.format(W)*45),;break
			else:
				continue
		with Thread(max_workers=1) as exe:
			exe.map(self.metode, self.xx)
		exit('+ Report selesai')
		
	def next_people(self, arg):
		try:
			oye=Scraping(webGet(arg), "html.parser")
			if 'Anda Diblokir Sementara' in str(oye):
				self.count.append('.')
				print(
					f"\r{P}\__{W}({R}{str(len(self.count)).zfill(2)}{W}){R} gagal melaporkan        \n{P}\__{W}({R}●{W}){R} alasan {P}:{R} Anda Diblokir Sementara\n")
			else:
				self.exes(oye)
		except Exception :
			pass
		
	def next_grup(self, arg):
		try:
			oxe=Scraping(webGet(arg), "html.parser")
			if 'Anda Diblokir Sementara' in str(oxe):
				self.count.append('.')
				print(
					f"\r{P}\__{W}({R}{str(len(self.count)).zfill(2)}{W}){R} gagal melaporkan        \n{P}\__{W}({R}●{W}){R} alasan {P}:{R} Anda Diblokir Sementara\n"
				)
			else:
				act=oxe.find("form",{"method":"post"})
				pay={
					'fb_dtsg':oxe.find('input', {'name':'fb_dtsg'})['value'],
						'jazoest':oxe.find('input', {'name':'jazoest'})['value'],
					'action_key':'RESOLVE_PROBLEM',
						'submit':'Kirim' 
				}
				oye=Scraping(webPost(home_url+act["action"], data=pay), "html.parser")
				self.exes(oye)
		except(requests.exceptions.ConnectionError):
			for load in ["|", "/", "-", "\\"]:
				print(f'\r{W}({R}{load}{W}){Y} menunggu koneksi ...', end='       ')
				time.sleep(000.07)
		except Exception :
			pass

	def exes(self, oye):
		try:
			if 'nudity' in (self.wh):
				type=random.choice([
					'nudity_adult_nudity',
						'nudity_sexually_suggestive',
					'nudity_sexual_activity',
						'nudity_sexual_exploitation',
					'nudity_sexual_services',
						'nudity_involves_a_child',
					'nudity_sharing_private_images'
				])
				typer={
					'nudity_adult_nudity' : 'Ketelanjangan Orang Dewasa',
						'nudity_sexually_suggestive' : 'Bersifat Seksual',
					'nudity_sexual_activity' : 'Aktivitas Seksual',
						'nudity_sexual_exploitation' : 'Eksploitasi Seksual',
					'nudity_sexual_services' : 'Layanan Seksual',
						'nudity_involves_a_child' : 'Melibatkan Anak',
					'nudity_sharing_private_images' : 'Membagikan Gambar Pribadi'
				}
			elif 'violence' in (self.wh):
				type=random.choice([
					'graphic_violence',
						'death_or_severe_injury',
					'violent_threat',
						'animal_abuse',
					'violence_something_else'
				])
				typer={
					'graphic_violence' : 'Konten Sadis',
						'death_or_severe_injury' : 'Kematian atau Cedera Parah',
					'violent_threat' : 'Ancaman Kekerasan',
						'animal_abuse' : 'Penyiksaan Hewan',
					'violence_something_else' : 'Hal Lain'
				}
			elif 'harassment' in (self.wh):
				type=(
					'harassment_me'
				)
				typer={
					'harassment_me' : 'Pelecehan Terhadap Saya'
				}
			elif 'unauthorized_sales' in (self.wh):
				type=random.choice([
					'unauthorized_drugs_sales',
						'unauthorized_weapons_sales',
					'endangered_animals',
						'other_animals',
					'unauthorized_sales_something_else'
				])
				typer={
					'unauthorized_drugs_sales' : 'Obat Terlarang',
						'unauthorized_weapons_sales' : 'Penjualan Senjata',
					'endangered_animals' : 'Hewan Langka',
						'other_animals' : 'Hewan Lain',
					'unauthorized_sales_something_else' : 'Hal Lain'
				}
			elif 'hate_speech' in (self.wh):
				type=random.choice([
					'hate_speech_race_or_ethnicity',
						'hate_speech_national_origin',
					'hate_speech_religious_affiliation',
						'hate_speech_social_caste',
					'hate_speech_sexual_orientation',
						'hate_speech_sex_or_gender_identity',
					'hate_speech_disability_or_disease',
						'hate_speech_something_else'
				])
				typer={
					'hate_speech_race_or_ethnicity':'Ras atau Etnis',
						'hate_speech_national_origin':'Asal Negara',
					'hate_speech_religious_affiliation':'Afiliasi Agama',
						'hate_speech_social_caste':'Kasta Sosial',
					'hate_speech_sexual_orientation':'Orientasi Seksual',
						'hate_speech_sex_or_gender_identity':'Jenis Kelamin atau Identitas Gender',
					'hate_speech_disability_or_disease':'Disabilitas atau Penyakit',
						'hate_speech_something_else':'Hal Lain'
				}
			elif 'terrorism' in (self.wh) :
				type=(
					'terrorism'
				)
				typer={
					'terrorism' : 'Terorisme'
				}
			elif 'gross' in (self.wh) :
				type=(
					'gross'
				)
				typer={
					'gross' : 'Konten Vulgar'
				}
			exa=oye.find("form",{"method":"post"})
			pay={
				'fb_dtsg' : oye.find('input', {'name':'fb_dtsg'})['value'],
					'jazoest' : oye.find('input', {'name':'jazoest'})['value'],
				'tag' : type,
					'action' : 'Kirim'
			}
			ome=Scraping(webPost(home_url+exa["action"], data=pay), "html.parser")
			pero=ome.find("form",{"method":"post"})
			pal={
				'fb_dtsg' : pero.find('input', {'name':'fb_dtsg'})['value'],
					'jazoest' : pero.find('input', {'name':'jazoest'})['value'],
				'checked' : 'yes',
					'action' : 'Kirim'
			}
			ove=Scraping(webPost(home_url+pero["action"], data=pal), "html.parser")
			if 'Terima kasih sudah memberi tahu kami.' in str(ove):
				self.count.append('.')
				print(
					f"\r{P}\__{W}({G}{str(len(self.count)).zfill(2)}{W}){G} berhasil melaporkan        \n{P}\__{W}({G}●{W}){G} laporan {P}:{G} {typer[type]}\n"
				)
			else:
				self.count.append('.')
				why=str(ove.find('title').text)
				print(
					f"\r{P}\__{W}({R}{str(len(self.count)).zfill(2)}{W}){R} gagal melaporkan        \n{P}\__{W}({R}●{W}){R} alasan {P}:{R} {why}\n")
		except(requests.exceptions.ConnectionError):
			self.exes(oye)
		except : pass
		
if __name__ == '__main__':
	Report().menu()
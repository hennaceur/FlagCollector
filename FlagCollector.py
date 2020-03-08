from selenium import webdriver
import urllib.request
from termcolor import colored
import requests
import json
import sys
import smtplib
from email.mime.text import MIMEText
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

CountryList = []


#This function is used to read Json file to get email list and country list
def ReadJsonData():
	
	countryIdListArray=["1000","4000","5000","348032","6000","7000","8000","9000","10000","11000","14000","343000","17000","18000","19000","900","21000","22000","24000","25000","27000","28000","29000","30000","31000","32000","33000","345000","35000","36000","38000","40000","41000","42000","43000","44000","50000","46000","47000","348027","51000","52000","53000","54000","55000","60000","62000","339000","67000","137000","68000","69000","346000","70000","71000","332000","73000","75000","76000","77000","78000","79000","80000","82000","83000","84000","280000","85000","348028","89000","90000","92000","93000","94000","95000","96000","99000","100000","101000","348029","106000","107000","109000","110000","111000","112000","114000","115000","116000","117000","121000","120000","124000","125000","128000","130000","132000","133000","134000","135000","136000","138000","140000","144000","147000","149000","151000","154000","155000","156000","157000","158000","159000","160000","161000","162000","163000","164000","166000","167000","168000","170000","171000","172000","173000","174000","176000","179000","180000","181000","348031","184000","186000","191000","192000","193000","348000","196000","197000","198000","200000","201000","202000","205000","206000","338000","215000","216000","217000","218000","219000","152000","183000","224000","225000","199000","229000","230000","233000","234000","236000","238000","239000","241000","242000","243000","244000","63000","245000","248000","249000","250000","348033","252000","253000","337000","254000","255000","327000","256000","257000","258000","260000","195500","262000","263000","265000","337500","266000","267000","268000","269000","270000","153000","348030","274000","276000","277000","278000","281000","282000","283000","284000","285000","286000","290000","344000","293000","294000","295000","297000","299000","300000","301000","302000","303000","304000","305000","306000","307000","308000","309000","311000","312000","313000","316000","318000","330000","333000","335000"]
	with open('data.json') as db:
		data = json.load(db)
	
	for Id in countryIdListArray:
		for value in data['data'][Id]['offices']:
			EmailList.extend([value['eng']['email-1']])
			CountryList.extend([value['eng']['country']])
	SanitizedEmailList = list(dict.fromkeys(EmailList))
	SanitizedCountryList = list(dict.fromkeys(CountryList))

	return SanitizedEmailList
				
#Function used to send emails to list of receivers
def SendEmails():
	
	with open('data.json') as db:
		FinalEmailList = json.load(db)
	s = smtplib.SMTP("smtp.gmail.com", 587)
	#s.set_debuglevel(1)
	s.ehlo()
	s.starttls()
	s.ehlo()
	s.login('email', 'password')
	msg = MIMEText("""Hello""")
	sender = 'yourEmail@Email.com'
	recipients = FinalEmailList
	msg['subject'] = ""
	msg['From'] = sender

	for receiver in recipients:
		s.sendmail(sender, receiver, msg.as_string())
		print(colored("Email sent to " + receiver, 'green'))
	print(colored("Job Done!", 'red'))
	s.quit()

#Uses Selenium module to scrape website for email info
def GetJsonDataFromURL():
	
	EmailListCanada = []
	#req = Request('', headers={'User-Agent': 'Mozilla/5.0'})
	#webpage = urlopen(req).read()
	#soup = BeautifulSoup(webpage , 'html.parser')
	#links = soup.find_all("div", attrs={"class":"posts-container col-md-6"})
	#print(links)
	options = webdriver.ChromeOptions()
	options.add_argument('user-agent = Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36')

	chrome_driver_binary = '/mnt/c/Users/Hazem/Desktop/repos/project/chromedriver.exe'
	driver = webdriver.Chrome(chrome_driver_binary)
	driver.get('')
	DataList = driver.find_elements_by_css_selector('#posts-container > div.posts-container.col-md-6')
	elems = driver.find_elements_by_xpath("//a[@href]")
	print(elems)
	for value in elems:
		#print(value.get_attribute("href"))
		EmailListCanada.extend([value.get_attribute("href")])
	print(EmailListCanada)
	#WebElement = DataList.findElement(By.tagName("a"));
	#for value in WebElement:
	#	print(value.text)

def GetEmailAddress():
	
	EmailListCanada = []
	with open('EmailList.json') as db:
		data = json.load(db)

	options = webdriver.ChromeOptions()
	options.add_argument('user-agent = Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36')
	chrome_driver_binary = '/project/chromedriver.exe'
	driver = webdriver.Chrome(chrome_driver_binary)
	
	for value in data:
		driver.get(value)
		try:
			email = driver.find_element_by_id('email')
			label = email.find_element_by_class_name("label")
			text = email.text.replace(label.text, '').strip()
			print(colored(text,'green'))
			EmailListCanada.extend([text])
			
		except Exception:
			pass
	driver.quit()
	print(EmailListCanada)
	
		
		

#GetEmailAddress()
#ReadJsonData()
#SendEmails()
#GetJsonDataFromURL()



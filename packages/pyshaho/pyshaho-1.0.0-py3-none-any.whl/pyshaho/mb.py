from requests import post,get
import datetime
import urllib
from urllib import request,parse
from pyshaho.encryption import encryption
from pyshaho.An_Wb import SetClines,Server
from re import findall
from pathlib import Path
from random import randint, choice
from json import loads, dumps
from socket import (gaierror,)
from PIL import Image , ImageFont, ImageDraw
from json.decoder import (JSONDecodeError,)
import io
import base64
from base64 import b64decode
from string import ascii_lowercase, ascii_uppercase, digits
import math
import traceback


class test:
	downloadURL, DCsURL, getDCsURL, wsURL = "https://messengerX.iranlms.ir/GetFile.ashx", "https://messengerg2cX.iranlms.ir/", "https://getdcmess.iranlms.ir", "wss://msocket1.iranlms.ir:80"
	
	defaultUserAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0"
	
	defaultDevice = {
		"token_type": "Web",
		"token": "",
		"app_version": "WB_4.3.3",
		"lang_code": "fa",
		"system_version": "Windows 10",
		"device_model": "Firefox 113",
		"device_hash" : "2"+''.join(findall(r'\d+', defaultUserAgent))
	}
	
	def POST(json: dict, method, url: str = None, platform="web.rubika.ir", enc: encryption = None, isEncrypted: bool = True) -> dict:
	    while 1:
	        try:
	            response = post(url=url, json=json, headers={
	                    'Origin': 'https://'+platform,
						'Referer': f'https://{platform}/',
						'Host': url.replace("https://","").replace("/",""),
						'User-Agent': test.defaultUserAgent
	            }).text
	            response = loads(str(enc.decrypt(loads(response).get("data_enc")))) if "data_enc" in loads(response).keys() and isEncrypted else loads(response)
	            if "status" in response.keys() and response.get("status") != "OK":
	                if response.get("status_det") == "NOT_REGISTERED":
	                    raise NotRegistered("the auth is incorrect. please sure about your account's health then login again.")
	                elif response.get("status_det") == "INVALID_INPUT":
	                    raise InvalidInput(f"the inserted argument(s) is invaild in the {platform}/{method}. if you're sure about your argument(s), please report this message.")
	                elif response.get("status_det") == "TOO_REQUESTS":
	                    raise TooRequests(f"the {platform}/{method} method has been limited. please try again later.")
	                elif response.get("status_det") == 'INVALID_AUTH':
	                    raise InvalidAuth(f"the inserted argument(s) in {platform}/{method} is vaild but is not related to other argument(s) or maybe for other reasons, anyway now this method can't run on server. please don't enter fake argument(s) and fix anything can return this exception")
	            else:
	                return response
	        except:
	        	traceback.print_exc()
	
	
	def tmpGeneration():
	    randStr = lambda length, choices=[*ascii_lowercase, *ascii_uppercase,*digits, *"-_"]: "".join([choice(choices) for i in range(length)])
	    return randStr(32, [*ascii_lowercase, *digits])
	
	
	
	retries = 0
	def _getURL(key="default_api_urls", DCsURL: str = "https://messengerg2cX.iranlms.ir/", getDCsURL: str = "https://getdcmess.iranlms.ir", dc_id: int = None):
	    global retries
	    while 1:
	        try:
	            pwa = {"app_name": "Main","app_version": "1.2.1","platform": "PWA","package": "m.rubika.ir","lang_code": "fa"}
	            res = post(json={"api_version": 4, "client": pwa, "method": "getDCs"}, url=getDCsURL).json().get("data").get(key)
	            return DCsURL.replace('X', dc_id) if dc_id is not None else choice(list(res))
	        except requests.exceptions.ConnectionError:
	            retries += 1
	            if retries == 3:
	                retries = 0
	                break
                
       
	                
	def makeData(auth:str, enc:encryption, method:str, data:dict, client:dict=SetClines.web, url:str = None) -> dict:
	    url = url or test._getURL()
	    outerJson = {
	        "api_version": "6",
	        "auth": auth,
	        "data_enc": {
	            "method": method,
	            "input": data,
	            "client": client
	        }
	    }
	    outerJson["data_enc"] = enc.encrypt(dumps(outerJson["data_enc"]))
	    outerJson["sign"] = enc.makeSignFromData(outerJson["data_enc"])
	    return test.POST(outerJson, url=url, platform="web.rubika.ir", method=method, enc=enc)
	    
	    
	    
	def _create(auth, pr, method, data, client=SetClines.web):
		return test.makeData(auth, encryption(encryption.changeAuthType(auth), private_key=pr), method, dict(data))

	                   
                                  
                                           
                                                    
                                                             
                                                                               
	def makeTmpData(method: str, data: dict, url: str = None, tmp:str=None) -> dict:
	    url, tmp = url or test._getURL(), encryption.changeAuthType(tmp or test.tmpGeneration())
	    enc = encryption(tmp)
	    outerJson = {
	        "api_version": "6",
	        "tmp_session": tmp,
	        "data_enc": enc.encrypt(dumps({
	            "method": method,
	            "input": data,
	            "client": SetClines.web
	        }))
	    }
	
	    resp = test.POST(outerJson, method, url=url, platform="web.rubika.ir", enc=enc)
	    resp['tmp'] = tmp
	    return resp
	
	def _createTMP(method, data, tmp=None):
		return test.makeTmpData(method, dict(data), tmp=tmp, url=test._getURL(DCsURL=test.DCsURL, getDCsURL=test.getDCsURL, dc_id=None))
		

	def sendCode(phoneNumber, passKey: str =None, Type="SMS"):
		return test._createTMP("sendCode", {"phone_number": phoneNumber, "pass_key": passKey, "send_type": Type})


	def signIn(tmp, phoneNumber, phone_code_hash, phone_code):
		public, private = encryption.rsaKeyGenerate()
		resp = test._createTMP("signIn", {"phone_number": phoneNumber, "phone_code_hash": phone_code_hash, "phone_code": phone_code, "public_key": public}, tmp=tmp)
		if resp['status'] == "OK" and resp['data']['status'] == "OK":
			auth = encryption.decryptRsaOaep(private, resp['data']['auth'])
			guid = resp['data']['user']['user_guid']
			private = private
		return auth , guid , private











class Bot:
	def __init__(self, auth,privateKey):
		self.auth = auth
		auth = encryption.changeAuthType(auth)
		self.Auth =  auth
#		privateKey = loads(b64decode(privateKey).decode('utf-8'))['d']
		self.enc = encryption(encryption.changeAuthType(auth),privateKey)
		
	def _getURL():
		return choice(Server.matnadress)

	def _SendFile():
		return choice(Server.filesadress)
	
	def _rubino():
	    return choice(Server.rubino)
	    
	def socket():
	    return choice(Server.gtes)
	def send_post_file(self,inData):
		enc = self.enc
		data = dumps(inData)
		url = Bot._SendFile()
		Indata = {"api_version": "6","auth": self.Auth,"data_enc":enc.encrypt(data),"sign": enc.makeSignFromData(enc.encrypt(data))}
	
		headers={
                    'Origin': 'https://web.rubika.ir',
					'Referer': f'https://web.rubika.ir/',
					'Host':url.replace("https://","").replace("/",""),
					'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0"}
		
		while True:
		      try:
		      	return post(url,json=Indata,headers=headers).text
		      except:continue
		      
	def send_post(self,inData):
		enc = self.enc
		data = dumps(inData)
		url = Bot._getURL()
		Indata = {"api_version": "6","auth": self.Auth,"data_enc":enc.encrypt(data),"sign": enc.makeSignFromData(enc.encrypt(data))}
	
		headers={
                    'Origin': 'https://web.rubika.ir',
					'Referer': f'https://web.rubika.ir/',
					'Host':url.replace("https://","").replace("/",""),
					'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0"}
		
		while True:
		      try:
		      	return post(url,json=Indata,headers=headers).text
		      except:continue

	def registerDevice(self,systemversion,device_model,device_hash):
	    inData = {"method":"registerDevice","input":{'token_type': 'Web','token': '','app_version': 'WB_4.3.3','lang_code': 'fa','system_version': systemversion,'device_model': device_model,'device_hash': device_hash},"client": SetClines.web}
	    print(inData)
	    while 1:
	        try:
	            return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"]))
	        except:continue
	        
	def deleteContact(self, user_guid):
	    inData = {"method": "deleteContact","input":{"user_guid": user_guid},"client":SetClines.web}
	    while 1:
	        try:
	            return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"]))
	        except:continue
	        
	def isExist(self, username):
	    inData = {"method": "isExistUserame","input":{"username": username},"client":SetClines.web}
	    while 1:
	        try:
	            return loads(self.enc.decrypt(loads(request.urlopen(request.Request(Bot.rubino(), data=dumps({"api_version":"5","auth": self.Auth,"data_enc":self.enc.encrypt(dumps(inData))}).encode(), headers={'Content-Type': 'application/json'})).read()).get('data_enc')))
	        except:continue
	def turnOffTwoStep(self, password):
	    
	    inData = {"method":"turnOffTwoStep","input":{"password":password},"client":SetClines.web}
	    while 1:
	        try:
	            return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"]))
	        except:continue
	def setupTwoStepVerification(self, hint,password):
	    inData = {"method":"setupTwoStepVerification","input":{"hint":hint,"password":password},"client":SetClines.web}
	    while 1:
	        try:
	            return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"]))
	        except:continue
	    while 1:
	        try:
	            return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"]))
	        except:continue
	def sendMessage(self, chat_id,text,metadata=[],message_id=None):
		inData = {
			"method":"sendMessage",
			"input":{
				"object_guid":chat_id,
				"rnd":f"{randint(100000,999999999)}",
				"text":text,
				"reply_to_message_id":message_id
			},
			"client": SetClines.web
		}
		if metadata != [] : inData["input"]["metadata"] = {"meta_data_parts":metadata}

		while 1:
			try:
				return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"]))
				break
			except: continue


	def editMessage(self, gap_guid, newText, message_id):
		inData = {
			"method":"editMessage",
			"input":{
				"message_id":message_id,
				"object_guid":gap_guid,
				"text":newText
			},
			"client": SetClines.web
		}

		while 1:
			try:
				return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"]))
				break
			except: continue

	def sendChatActivity(self, object_guid):
	    inData = {"method":"sendChatActivity","input":{"activity":"Typing","object_guid":object_guid},"client": SetClines.web}
	    while 1:
	        try:
	            return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"]))
	        except:continue
	def getChatAds(self):
	    time_stamp = str(round(datetime.datetime.today().timestamp()) - 200)
	    inData = {"method":"getChatAds","input":{"state":time_stamp},"client": SetClines.web}
	    while 1:
	        try:
	            return loads(elf.enc.decrypt(loads(self.send_post(inData))["data_enc"]))
	        except:continue
	def getMessagesInterval(self):
	    inData = {"method":"getMessagesInterval","input":{"object_guid":"s0B0e8da28a4fde394257f518e64e800","middle_message_id":"0"},"client":SetClines.web}
	    while 1:
	        try:
	            return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"])).get("data").get("messages")
	        except:continue
	        
	        
	def makeRandomTmpSession():
		chars = "abcdefghijklmnopqrstuvwxyz"
		tmp = ""
		for i in range(32):
			tmp += choice(chars)
		return tmp

	def sendCode(phone:str,pass_key=None,type="SMS"):
	    inData = {"method":"sendCode","input":{"phone_number":phone,"send_type":type},"client":SetClines.web}
	    if pass_key != None:inData["input"]["pass_key"] = pass_key
	    data = dumps(inData)
	    goh = Bot.makeRandomTmpSession()
	    en = encryption.changeAuthType(goh)
	    url = Bot._getURL()
	    hh = encryption.encrypt(data)
	    print(hh)
	
	def signIn(tmp,phone,phone_code,hash,public_key=None):
	    public, private = encryption.rsaKeyGenerate()
	    
	    inData = {"method":"signIn","input":{"phone_number":phone,"phone_code_hash":hash,"phone_code":str(phone_code),
"public_key":public if not public_key else public_key},"client":SetClines.web}
	    r = loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"]))
	    if r['status'] == "OK" and r['data']['status'] == "OK":
	    	auth = encryption.decryptRsaOaep(private,r['data']['auth'])
	    	guid = r['data']['user']['user_guid']
	    	return auth , guid, private
	    else:
	    	return None
	    	

	
	def addFolder(self, name):
	    inData = {"method":"addFolder","input":{"is_add_to_top":True,"name":name},"client":SetClines.web}
	    while True:
	        try:
	            return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"]))
	        except:continue
	def leaveChannelAction(self, channel_guid):
	    inData = {"method":"joinChannelAction","input":{"action":"Leave","channel_guid":channel_guid},"client":SetClines.web}
	    while 1:
	        try:
	            return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"]))
	        except:continue
	def mrgohst(self):
	    inData = {"method":"getDCs","input":{},"client":{"app_name":"Main","app_version":"4.1.4","platform":"Web","package":"web.rubika.ir","lang_code":"fa"}}
	    while 1:
	        try:
	            return loads(self.enc.decrypt(loads(request.urlopen(request.Request(Bot.socket(), data=dumps({"api_version":"5","auth": self.Auth,"data_enc":self.enc.encrypt(dumps(inData))}).encode(), headers={'Content-Type': 'application/json'})).read()).get('data_enc')))
	        except:continue
	def joinChannelAction(self, channel_guid):
	    inData = {"method":"joinChannelAction","input":{"action":"Join","channel_guid":channel_guid},"client":SetClines.web}
	    while 1:
	        try:
	            return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"]))
	        except:continue
	def editbio(self, bio):
	    inData = {"method":"updateProfile","input":{"bio":bio,"updated_parameters":["bio"]},"client":SetClines.web}
	    while 1:
	        try:
	            return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"]))
	        except:continue
	def editname(self, first_name=None, bio=None):
	    inData = {"method":"updateProfile","input":{"first_name":first_name,"last_name":" ","bio":bio,"updated_parameters":["first_name","last_name",'bio']},"client":SetClines.web}
	    while 1:
	        try:
	            return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"]))
	        except:continue
	
	def updateUsername(self, username):
	    inData = {"method":"updateUsername","input":{"username":username},"client":SetClines.web}
	    while 1:
	        try:
	            return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"]))
	        except:continue
	        
	def getServiceInfo(self, service_guid):
	    inData = {"method":"getServiceInfo","input":{"service_guid":service_guid},"client":SetClines.web}
	    while 1:
	        try:
	            return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"]))
	        except:continue
	def deleteMessages(self, chat_id, message_ids):
		inData = {
			"method":"deleteMessages",
			"input":{
				"object_guid":chat_id,
				"message_ids":message_ids,
				"type":"Global"
			},
			"client": SetClines.web
		}

		while 1:
			try:
				return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"]))
				break
			except: continue


	def getMessagefilter(self, chat_id, filter_whith):
		inData = {
		    "method":"getMessages",
		    "input":{
		        "filter_type":filter_whith,
		        "max_id":"NaN",
		        "object_guid":chat_id,
		        "sort":"FromMax"
		    },
		    "client": SetClines.web
		}

		while 1:
			try:
				return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"])).get("data").get("messages")
				break
			except: continue

	def getMessagew(self, chat_id, min_id):
	    inData = {"method":"getMessagesInterval","input":{"object_guid":chat_id,"middle_message_id":min_id},"client": SetClines.web}
	    while 1:
		    try:
		        return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"])).get("data").get("messages")
		    except:continue
	def getmen(self):
	    inData = {"method":"getMessagesInterval","input":{"object_guid":"s0B0e8da28a4fde394257f518e64e800","middle_message_id":"0"},"client": SetClines.web}
	    while 1:
	        try:
	            return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"])).get("data").get("messages")
	        except:continue
	def getMessages(self, chat_id, min_id):
		inData = {
		    "method":"getMessagesInterval",
		    "input":{
		        "object_guid":chat_id,
		        "middle_message_id":min_id
		    },
		    "client": SetClines.web
		}

		while 1:
			try:
				return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"]))
				break
			except: continue


	def getChats(self, start_id=None):
		inData = {
		    "method":"getChats",
		    "input":{
		        "start_id":start_id
		    },
		    "client": SetClines.web
		}

		while 1:
			try:
				return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"])).get("data").get("messages")
				break
			except: continue
	        
	def deleteUserChat(self, user_guid, last_message):
		inData = {
		    "method":"deleteUserChat",
		    "input":{
		        "last_deleted_message_id":last_message,
		        "user_guid":user_guid
		    },
		    "client": SetClines.web
		}

		while 1:
			try:
				return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"]))
				break
			except: continue

	def deleteUserChat(self, user_guid):
	    inData = {"method":"deleteUserChat","input":{"last_deleted_message_id":"0","user_guid":user_guid},"client": SetClines.web}
	    while 1:
	        try:
	            return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"]))
	        except:continue
	def getGroupOnlineMember(self, chat_id):
	    inData = {"method":"getGroupOnlineCount","input":{"group_guid": chat_id},"client":SetClines.web}
	    while 1:
	        try:
	            return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"])).get('data').get('online_count')
	        except:continue
	def getCommonGroups(self, chat_id):
	    inData = {"method":"getCommonGroups","input":{"user_guid": chat_id},"client":SetClines.web}
	    while 1:
	        try:
	            return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"])).get('data').get('abs_groups')
	        except:continue
	def sendLocation(self, chat_id, location, message_id=None):
	    inData = {"method":"sendMessage","input":{"is_mute": False,"object_guid":chat_id,"rnd":f"{randint(100000,999999999)}","location":{"latitude": location[0],"longitude": location[1]},"reply_to_message_id":message_id},"client":SetClines.web}
	    while 1:
	        try:
	            return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"]))
	        except:continue
	def updateProfile_rubino(self, name=None, bio=None, email=None):
	    inData = {"method":"updateProfile","input": {"name": name, "bio": bio, "email": email},"client":SetClines.web}
	    while 1:
	        try:
	            return loads(self.enc.decrypt(loads(request.urlopen(request.Request(Bot._rubino(), data=dumps({"api_version":"5","auth": self.Auth,"data_enc":self.enc.encrypt(dumps(inData))}).encode(), headers={'Content-Type': 'application/json'})).read()).get('data_enc')))
	        except:continue
	def getPendingObjectOwner(self, chat_id):
	    inData = {"method":"getPendingObjectOwner","input":{"object_guid": chat_id},"client":SetClines.web}
	    while 1:
	        try:
	            return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"]))
	        except:continue
	def getContacts(self, user_guid):
	    inData = {"method":"getContacts","input":{"start_id":user_guid},"client": SetClines.web}
	    while 1:
	        try:
	            return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"])).get("data").get("users")
	        except:continue
	def seenChats(self, chat_id, msg_id):
	    inData = {"method":"seenChats","input":{"seen_list":{chat_id:msg_id}},"client": SetClines.web}
	    while 1:
	        try:
	            return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"]))
	        except:continue
	def getInfoByUsername(self, username):
		inData = {
		    "method":"getObjectByUsername",
		    "input":{
		        "username":username
		    },
		    "client": SetClines.web
		}

		while 1:
			try:
				return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"])).get("data")
				break
			except: continue

	def requestChangeObjectOwner(self, chat_id, newOwnerGuid):
	    inData = {"method":"requestChangeObjectOwner","input":{"object_guid": chat_id, "new_owner_user_guid": newOwnerGuid},"client":SetClines.web}
	    while 1:
	        try:
	            return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"]))
	        except:continue
	def reporter(self, chat_id,description=None,reportType = 106):
	    inData = {"method":"reportObject","input":{"object_guid":chat_id,"report_description":description,"report_type":reportType,"report_type_object":"Object"},"client": SetClines.web}
	    while 1:
	        try:
	            return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"]))
	        except:continue
	def banGroupMember(self, chat_id, user_id):
		inData = {
		    "method":"banGroupMember",
		    "input":{
		        "group_guid": chat_id,
				"member_guid": user_id,
				"action":"Set"
		    },
		    "client": SetClines.web
		}

		while 1:
			try:
				return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"]))
				break
			except: continue

	def unbanGroupMember(self, chat_id, user_id):
		inData = {
		    "method":"banGroupMember",
		    "input":{
		        "group_guid": chat_id,
				"member_guid": user_id,
				"action":"Unset"
		    },
		    "client": SetClines.web
		}

		while 1:
			try:
				return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"]))
				break
			except: continue

	def getGroupInfo(self, chat_id):
		inData = {
			"method":"getGroupInfo",
			"input":{
				"group_guid": chat_id
			},
			"client": SetClines.web
		}

		while 1:
			try:
				return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"]))
				break
			except: continue

	def search(self, text):
	    inData = {"method":"searchGlobalObjects","input":{"search_text":text},"client": SetClines.web}
	    while 1:
	        try:
	            return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"]))
	        except:continue
	def invite(self, chat_id, user_ids):
		inData = {
		    "method":"addGroupMembers",
		    "input":{
		        "group_guid": chat_id,
				"member_guids": user_ids
		    },
		    "client": SetClines.web
		}

		while 1:
			try:
				return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"]))
				break
			except: continue

	def inviteChannel(self, chat_id, user_ids):
		inData = {
		    "method":"addChannelMembers",
		    "input":{
		        "channel_guid": chat_id,
				"member_guids": user_ids
		    },
		    "client": SetClines.web
		}

		while 1:
			try:
				return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"]))
				break
			except: continue

	def getGroupAdmins(self, chat_id):
		inData = {
			"method":"getGroupAdminMembers",
			"input":{
				"group_guid":chat_id
			},
			"client": SetClines.web
		}

		while 1:
			try:
				return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"]))
				break
			except: continue

	def getChannelInfo(self, channel_guid):
		inData = {
			"method":"getChannelInfo",
			"input":{
				"channel_guid":channel_guid
			},
			"client": SetClines.web
		}

		while 1:
			try:
				return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"]))
				break
			except: continue


	
	def getMyGifSet(self):
	    inData = {"method":"getMyGifSet","input":{},"client":SetClines.web}
	    while 1:
	        try:
	            return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"]))
	        except:continue
	def ADD_NumberPhone(self, first_num, last_num, numberPhone):
		inData = {
			"method":"addAddressBook",
			"input":{
				"first_name":first_num,
				"last_name":last_num,
				"phone":numberPhone
			},
			"client": SetClines.web
		}

		while 1:
			try:
				return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"]))
				break
			except: continue



	def getMessagesInfo(self, chat_id, message_ids):
		inData = {
			"method":"getMessagesByID",
			"input":{
				"object_guid": chat_id,
				"message_ids": message_ids
			},
			"client": SetClines.web
		}

		while 1:
			try:
				return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"]))
				break
			except: continue

	def getMessages_info_android(self, chat_id, message_ids):
		inData = {
			"method":"getMessagesByID",
			"input":{
				"message_ids": message_ids,
				"object_guid": chat_id
			},
			"client": SetClines.web
		}

		while 1:
			try:
				return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"]))
				break
			except: continue


	def setMembersAccess(self, chat_id, access_list):
		inData = {
			"method":"setGroupDefaultAccess",
			"input":{
				"access_list": access_list,
				"group_guid": chat_id
			},
			"client": SetClines.web
		}

		while 1:
			try:
				return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"]))
				break
			except: continue

	def getGroupMembers(self, chat_id, start_id=None):
		inData = {
			"method":"getGroupAllMembers",
			"input":{
				"group_guid": chat_id,
				"start_id": start_id
			},
			"client": SetClines.web
		}

		while 1:
			try:
				return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"]))
				break
			except: continue

	def getGroupLink(self, chat_id):
		inData = {
			"method":"getGroupLink",
			"input":{
				"group_guid":chat_id
			},
			"client": SetClines.web
		}

		while 1:
			try:
				return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"])).get("data").get("join_link")
				break
			except: continue

	def changeGroupLink(self, chat_id):
		inData = {
			"method":"getGroupLink",
			"input":{
				"group_guid": chat_id
			},
			"client": SetClines.web
		}

		while 1:
			try:
				return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"])).get("data").get("join_link")
				break
			except: continue

	def setGroupTimer(self, chat_id, time):
		inData = {
			"method":"editGroupInfo",
			"input":{
				"group_guid": chat_id,
				"slow_mode": time,
				"updated_parameters":["slow_mode"]
			},
			"client": SetClines.web
		}

		while 1:
			try:
				return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"]))
				break
			except: continue

	def setGroupAdmin(self, chat_id, user_id):
		inData = {
			"method":"setGroupAdmin",
			"input":{
				"group_guid": chat_id,
				"access_list":["SetJoinLink"],
				"action": "SetAdmin",
				"member_guid": user_id
			},
			"client": SetClines.web
		}

		while 1:
			try:
				return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"]))
				break
			except: continue

	def deleteGroupAdmin(self,c,user_id):
		inData = {
			"method":"setGroupAdmin",
			"input":{
				"group_guid": c,
				"action": "UnsetAdmin",
				"member_guid": user_id
			},
			"client": SetClines.web
		}

		while 1:
			try:
				return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"]))
				break
			except: continue

	def setChannelAdmin(self, chat_id, user_id, access_list=[]):
		inData = {
			"method":"setGroupAdmin",
			"input":{
				"group_guid": chat_id,
				"access_list": access_list,
				"action": "SetAdmin",
				"member_guid": user_id
			},
			"client": SetClines.web
		}

		while 1:
			try:
				return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"]))
				break
			except: continue

	def getStickersByEmoji(self,emojee):
		inData = {
			"method":"getStickersByEmoji",
			"input":{
				"emoji_character": emojee,
				"suggest_by": "All"
			},
			"client": SetClines.web
		}

		while 1:
			try:
				return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"]))
				break
			except: continue

	def setActionChatun(self,guid):
		inData = {
			"method":"setActionChat",
			"input":{
				"action": "Unmute",
				"object_guid": guid
			},
			"client": SetClines.web
		}

		while 1:
			try:
				return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"]))
				break
			except: continue

	def setActionChatmut(self,guid):
		inData = {
			"method":"setActionChat",
			"input":{
				"action": "Mute",
				"object_guid": guid
			},
			"client": SetClines.web
		}

		while 1:
			try:
				return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"]))
				break
			except: continue

	
	def sendPoll(self,guid,SOAL,LIST):
		inData = {
			"method":"lcreatePoll",
			"input":{
				"allows_multiple_answers": "false",
				"is_anonymous": "true",
				"object_guid": guid,
				"options":LIST,
				"question":SOAL,
				"rnd":f"{randint(100000,999999999)}",
				"type":"Regular"
			},
			"client": SetClines.web
		}

		while 1:
			try:
				return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"]))
				break
			except: continue

	def getLinkFromAppUrl(self, app_url):
	    inData = {"method":"getLinkFromAppUrl","input":{"app_url":app_url},"client":SetClines.web}
	    while 1:
	        try:
	            return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"])).get("data").get("link").get("open_chat_data")
	            break
	        except:continue
	        
	def serch(self,object_guid, search_text):
	    inData = {"method":"searchChatMessages","input":{"object_guid":object_guid,"search_text":search_text,"type":"Text"},"client":SetClines.web}
	    while 1:
	        try:
	            return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"])).get("data").get("message_ids")
	            break
	        except:continue
	    
	    
	def checkUserUsername(self, username):
	    inData = {"method":"checkUserUsername","input":{"username":username},"client": SetClines.web}
	    while 1:
	        try:
	            return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"]))
	            break
	        except:continue
	        
	def botget(self, bot_guid):
	    inData = {"method":"getBotInfo","input":{"bot_guid":bot_guid},"client": SetClines.web}
	    while 1:
	        try:
	            return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"]))
	            break
	        except:continue
			
	def forwardMessages(self, From, message_ids, to):
		inData = {
			"method":"forwardMessages",
			"input":{
				"from_object_guid": From,
				"message_ids": message_ids,
				"rnd": f"{randint(100000,999999999)}",
				"to_object_guid": to
			},
			"client": SetClines.web
		}

		while 1:
			try:
				return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"]))
				break
			except: continue

	def chatGroupvisit(self,guid,visiblemsg):
		inData = {
			"method":"editGroupInfo",
			"input":{
				"chat_history_for_new_members": "Visible",
				"group_guid": guid,
				"updated_parameters": visiblemsg
			},
			"client": SetClines.web
		}

		while 1:
			try:
				return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"]))
				break
			except: continue

	def chatGrouphidden(self,guid,hiddenmsg):
		inData = {
			"method":"editGroupInfo",
			"input":{
				"chat_history_for_new_members": "Hidden",
				"group_guid": guid,
				"updated_parameters": hiddenmsg
			},
			"client": SetClines.web
		}

		while 1:
			try:
				return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"]))
				break
			except: continue


	def pin(self, chat_id, message_id):
		inData = {
			"method":"setPinMessage",
			"input":{
				"action":"Pin",
			 	"message_id": message_id,
			 	"object_guid": chat_id
			},
			"client": SetClines.web
		}

		while 1:
			try:
				return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"]))
				break
			except: continue

	def unpin(self, chat_id, message_id):
		inData = {
			"method":"setPinMessage",
			"input":{
				"action":"Unpin",
			 	"message_id": message_id,
			 	"object_guid": chat_id
			},
			"client": SetClines.web
		}

		while 1:
			try:
				return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"]))
				break
			except: continue

	def addChannelMembers(self, group_guid, member_guids):
	    inData = {"method":"addChannelMembers","input":{"group_guid":group_guid,"member_guids":member_guids},"client": SetClines.web}
	    while 1:
	        try:
	            return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"]))
	        except:continue
	def addGroupMembers(self, group_guid, member_guids):
	    inData = {"method":"addGroupMembers","input":{"group_guid":group_guid,"member_guids":member_guids},"client": SetClines.web}
	    while 1:
	        try:
	            return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"]))
	        except:continue
	def logout(self):
		inData = {
			"method":"logout",
			"input":{},
			"client": SetClines.web
		}

		while 1:
			try:
				return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"]))
				break
			except: continue

	def channelPreviewByJoinLink(self, link):
	    hashLink = link.split("/")[-1]
	    inData = {"method":"channelPreviewByJoinLink","input":{"hash_link": hashLink},"client": SetClines.web}
	    while 1:
	        try:
	            return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"])).get('data').get('channel')
	        except:continue
	def joinChannelByLink(self, link):
	    hashLink = link.split("/")[-1]
	    inData = {"method":"joinChannelByLink","input":{"hash_link": hashLink},"client": SetClines.web}
	    while 1:
	        try:
	            return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"])).get('data').get('channel')
	        except:continue
	def joinGroup(self, link):
		hashLink = link.split("/")[-1]
		inData = {
			"method":"joinGroup",
			"input":{
				"hash_link": hashLink
			},
			"client": SetClines.web
		}

		while 1:
			try:
				return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"]))
				break
			except: continue

	def joinChannel(self, link):
		hashLink = link.split("/")[-1]
		inData = {
			"method":"joinChannelByLink",
			"input":{
				"hash_link": hashLink
			},
			"client": SetClines.web
		}

		while 1:
			try:
				return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"]))
				break
			except: continue

	def deleteChatHistory(self, chat_id, msg_id):
		inData = {
			"method":"deleteChatHistory",
			"input":{
				"last_message_id": msg_id,
				"object_guid": chat_id
			},
			"client": SetClines.web
		}

		while 1:
			try:
				return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"]))
				break
			except: continue

	def leaveGroup(self,chat_id):
		inData = {
			"method":"leaveGroup",
			"input":{
				"group_guid": chat_id
			},
			"client": SetClines.web
		}

		while 1:
			try:
				return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"]))
				break
			except: continue

	def editnameGroup(self,groupgu,namegp,biogp=None):
		inData = {
			"method":"editGroupInfo",
			"input":{
				"description": biogp,
				"group_guid": groupgu,
				"title":namegp,
				"updated_parameters":["title","description"]
			},
			"client": SetClines.web
		}

		while 1:
			try:
				return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"]))
				break
			except: continue

	def editbioGroup(self,groupgu,biogp,namegp=None):
		inData = {
			"method":"editGroupInfo",
			"input":{
				"description": biogp,
				"group_guid": groupgu,
				"title":namegp,
				"updated_parameters":["title","description"]
			},
			"client": SetClines.web
		}

		while 1:
			try:
				return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"]))
				break
			except: continue

	def joinChannelByID(self, chat_id):
		inData = {
			"method":"joinChannelAction",
			"input":{
				"action": "Join",
				"channel_guid": chat_id
			},
			"client": SetClines.web
		}

		while 1:
			try:
				return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"]))
				break
			except: continue

	def LeaveChannel(self,chat_id):
		inData = {
			"method":"joinChannelAction",
			"input":{
				"action": "Leave",
				"channel_guid": chat_id
			},
			"client": SetClines.web
		}

		while 1:
			try:
				return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"]))
				break
			except: continue

	def block(self, chat_id):
		inData = {
			"method":"setBlockUser",
			"input":{
				"action": "Block",
				"user_guid": chat_id
			},
			"client": SetClines.web
		}

		while 1:
			try:
				return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"]))
				break
			except: continue

	def getBotInfo(self, chat_id):
	    inData = {
			"method":"getBotInfo",
			"input":{
				"bot_guid":chat_id
			},
			"client": SetClines.web
		}

	    while 1:
	        try:
	            return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"]))
	            break
	        except: continue
	         
	def unblock(self, chat_id):
		inData = {
			"method":"setBlockUser",
			"input":{
				"action": "Unblock",
				"user_guid": chat_id
			},
			"client": SetClines.web
		}

		while 1:
			try:
				return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"]))
				break
			except: continue

	def getChannelMembers(self, channel_guid, text=None, start_id=None):
		inData = {
			"method":"getChannelAllMembers",
			"input":{
				"channel_guid":channel_guid,
				"search_text":text,
				"start_id":start_id,
			},
			"client": SetClines.web
		}

		while 1:
			try:
				return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"]))
				break
			except: continue

	
	def startVoiceChat(self, chat_id):
		inData = {
			"method":"createGroupVoiceChat",
			"input":{
				"chat_guid":chat_id
			},
			"client": SetClines.web
		}

		while 1:
			try:
				return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"]))
				break
			except: continue

	def editVoiceChat(self,chat_id,voice_chat_id, title):
		inData = {
			"method":"setGroupVoiceChatSetting",
			"input":{
				"chat_guid":chat_id,
				"voice_chat_id" : voice_chat_id,
				"title" : title ,
				"updated_parameters": ["title"]
			},
			"client": SetClines.web
		}

		while 1:
			try:
				return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"]))
				break
			except: continue

	def getUserInfo(self, chat_id):
		inData = {
			"method":"getUserInfo",
			"input":{
				"user_guid":chat_id
			},
			"client": SetClines.web
		}

		while 1:
			try:
				return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"]))
				break
			except: continue


	def finishVoiceChat(self, chat_id, voice_chat_id):
		inData = {
			"method":"discardGroupVoiceChat",
			"input":{
				"chat_guid":chat_id,
				"voice_chat_id" : voice_chat_id
			},
			"client": SetClines.web
		}

		while 1:
			try:
				return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"]))
				break
			except: continue


	def group(self, name, member_guids=None):
	    inData = {"method":"addGroup","input":{"member_guids":member_guids,"title":name},"client":SetClines.web}
	    while 1:
	        try:
	            return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"]))
	        except:continue
	def getAbsObjects(self, objects_guids):
	    inData = {"method":"getAbsObjects","input":{"objects_guids":objects_guids},"client":SetClines.web}
	    while 1:
	        try:
	            return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"]))
	        except:continue
	def getContactsUpdates(self):
	    time_stamp = str(round(datetime.datetime.today().timestamp()) - 200)
	    inData = {"method":"getContactsUpdates","input":{"state":time_stamp},"client": SetClines.web}
	    while 1:
	        try:
	            return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"]))
	        except:continue
	def getChatsUpdate(self):
		time_stamp = str(round(datetime.datetime.today().timestamp()) - 200)
		inData = {
			"method":"getChatsUpdates",
			"input":{
				"state":time_stamp,
			},
			"client": SetClines.web
		}

		while 1:
			try:
				return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"])).get("data").get("chats")
				break
			except: continue

	def getMessagesChats(self, start_id=None):
		time_stamp = str(round(datetime.datetime.today().timestamp()) - 200)
		inData = {
			"method":"getChats",
			"input":{
				"start_id":start_id
			},
			"client": SetClines.web
		}

		while 1:
			try:
				return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"])).get('data').get('chats')
				break
			except: continue

	def see_GH_whith_Linkes(self,link_gh):
		inData = {
			"method":"groupPreviewByJoinLink",
			"input":{
				"hash_link": link_gh
			},
			"client": SetClines.web
		}

		while 1:
			try:
				return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"])).get("data")
				break
			except: continue

	def _requestSendFile(self, file):
		inData = {
			"method":"requestSendFile",
			"input":{
				"file_name": str(file.split("/")[-1]),
				"mime": file.split(".")[-1],
				"size": Path(file).stat().st_size
			},
			"client": SetClines.web
		}

		while 1:
			try:
				return loads(self.enc.decrypt(loads(self.send_post_file(inData))["data_enc"])).get("data")
				break
			except: continue

	def _uploadFile(self, file):
		if not "http" in file:
			REQUES = Bot._requestSendFile(self, file)
			bytef = open(file,"rb").read()

			hash_send = REQUES["access_hash_send"]
			file_id = REQUES["id"]
			url = REQUES["upload_url"]

			header = {
				'auth':self.Auth,
				'Host':url.replace("https://","").replace("/UploadFile.ashx",""),
				'chunk-size':str(Path(file).stat().st_size),
				'file-id':str(file_id),
				'access-hash-send':hash_send,
				"content-type": "application/octet-stream",
				"content-length": str(Path(file).stat().st_size),
				"accept-encoding": "gzip",
				"user-agent": "okhttp/3.12.1"
			}

			if len(bytef) <= 131072:
				header["part-number"], header["total-part"] = "1","1"

				while True:
					try:
						j = post(data=bytef,url=url,headers=header).text
						j = loads(j)['data']['access_hash_rec']
						break
					except Exception as e:
						continue

				return [REQUES, j]
			else:
				t = round(len(bytef) / 131072 + 1)
				for i in range(1,t+1):
					if i != t:
						k = i - 1
						k = k * 131072
						while True:
							try:
								header["chunk-size"], header["part-number"], header["total-part"] = "131072", str(i),str(t)
								o = post(data=bytef[k:k + 131072],url=url,headers=header).text
								o = loads(o)['data']
								break
							except Exception as e:
								continue
					else:
						k = i - 1
						k = k * 131072
						while True:
							try:
								header["chunk-size"], header["part-number"], header["total-part"] = str(len(bytef[k:])), str(i),str(t)
								p = post(data=bytef[k:],url=url,headers=header).text
								p = loads(p)['data']['access_hash_rec']
								break
							except Exception as e:
								continue
						return [REQUES, p]
		else:
			REQUES = {
				"method":"requestSendFile",
				"input":{
					"file_name": file.split("/")[-1],
					"mime": file.split(".")[-1],
					"size": len(get(file).content)
			},
			"client": SetClines.web
		}

		while 1:
			try:
				return loads(self.enc.decrypt(loads(self.send_post_file(inData))["data_enc"])).get("data")
				break
			except: continue

			hash_send = REQUES["access_hash_send"]
			file_id = REQUES["id"]
			url = REQUES["upload_url"]
			bytef = get(file).content

			header = {
				'auth':self.Auth,
				'Host':url.replace("https://","").replace("/UploadFile.ashx",""),
				'chunk-size':str(len(get(file).content)),
				'file-id':str(file_id),
				'access-hash-send':hash_send,
				"content-type": "application/octet-stream",
				"content-length": str(len(get(file).content)),
				"accept-encoding": "gzip",
				"user-agent": "okhttp/3.12.1"
			}

			if len(bytef) <= 131072:
				header["part-number"], header["total-part"] = "1","1"

				while True:
					try:
						j = post(data=bytef,url=url,headers=header).text
						j = loads(j)['data']['access_hash_rec']
						break
					except Exception as e:
						continue

				return [REQUES, j]
			else:
				t = round(len(bytef) / 131072 + 1)
				for i in range(1,t+1):
					if i != t:
						k = i - 1
						k = k * 131072
						while True:
							try:
								header["chunk-size"], header["part-number"], header["total-part"] = "131072", str(i),str(t)
								o = post(data=bytef[k:k + 131072],url=url,headers=header).text
								o = loads(o)['data']
								break
							except Exception as e:
								continue
					else:
						k = i - 1
						k = k * 131072
						while True:
							try:
								header["chunk-size"], header["part-number"], header["total-part"] = str(len(bytef[k:])), str(i),str(t)
								p = post(data=bytef[k:],url=url,headers=header).text
								p = loads(p)['data']['access_hash_rec']
								break
							except Exception as e:
								continue
						return [REQUES, p]


	@staticmethod
	def _getThumbInline(image_bytes:bytes):
		import io, base64, PIL.Image
		im = PIL.Image.open(io.BytesIO(image_bytes))
		width, height = im.size
		if height > width:
			new_height = 40
			new_width  = round(new_height * width / height)
		else:
			new_width  = 40
			new_height = round(new_width * height / width)
		im = im.resize((new_width, new_height), PIL.Image.ANTIALIAS)
		changed_image = io.BytesIO()
		im.save(changed_image, format='PNG')
		changed_image = changed_image.getvalue()
		return base64.b64encode(changed_image)

	@staticmethod
	def _getImageSize(image_bytes:bytes):
		import io, PIL.Image
		im = PIL.Image.open(io.BytesIO(image_bytes))
		width, height = im.size
		return [width , height]



	def uploadAvatar_replay(self,myguid,files_ide):
		inData = {
			"method":"uploadAvatar",
			"input":{
				"object_guid":myguid,
				"thumbnail_file_id":files_ide,
				"main_file_id":files_ide
			},
			"client": SetClines.web
		}

		while 1:
			try:
				return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"]))
				break
			except: continue

	def uploadAvatar(self,myguid,main,thumbnail=None):
		mainID = str(Bot._uploadFile(self, main)[0]["id"])
		thumbnailID = str(Bot._uploadFile(self, thumbnail or main)[0]["id"])
		inData = {
			"method":"uploadAvatar",
			"input":{
				"object_guid":myguid,
				"thumbnail_file_id":thumbnailID,
				"main_file_id":mainID
			},
			"client": SetClines.web
		}

		while 1:
			try:
				return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"]))
				break
			except: continue

	def getAvatar(self, myguid):
	    inData = {"method":"getAvatars","input":{"object_guid":myguid},"client":SetClines.web}
	    while 1:
	        try:
	            return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"])).get("data").get("avatars")
	        except:continue
	def deleteAvatar(self,myguid,avatar_id):
	    inData = {"method":"deleteAvatar","input":{"object_guid":myguid,"avatar_id":avatar_id},"client": SetClines.web}
	    while 1:
	        try:
	            return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"])).get("data")
	        except:continue
	def terminateSession(self, session_key):
	    inData = {"method":"terminateSession","input":{"session_key":session_key},"client":SetClines.web}
	    while 1:
	        try:
	            return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"]))
	        except:continue
	def Devices_rubika(self):
		inData = {
			"method":"getMySessions",
			"input":{

			},
			"client": SetClines.web
		}

		while 1:
			try:
				return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"]))
				break
			except: continue


	def sendDocument(self, chat_id, file, caption=None, message_id=None):
		uresponse = Bot._uploadFile(self, file)
		file_id = str(uresponse[0]["id"])
		mime = file.split(".")[-1]
		dc_id = uresponse[0]["dc_id"]
		access_hash_rec = uresponse[1]
		file_name = file.split("/")[-1]
		size = str(len(get(file).content if "http" in file else open(file,"rb").read()))

		inData = {
			"method":"sendMessage",
			"input":{
				"object_guid":chat_id,
				"reply_to_message_id":message_id,
				"rnd":f"{randint(100000,999999999)}",
				"file_inline":{
					"dc_id":str(dc_id),
					"file_id":str(file_id),
					"type":"File",
					"file_name":file_name,
					"size":size,
					"mime":mime,
					"access_hash_rec":access_hash_rec
				}
			},
			"client": SetClines.web
		}

		if caption != None: inData["input"]["text"] = caption


		while 1:
			try:
				return loads(self.enc.decrypt(loads(self.send_post_file(inData))["data_enc"]))
				break
			except: continue


	def sendDocument_rplay(self,chat_id,file_id,mime,dc_id,access_hash_rec,file_name,size,caption=None,message_id=None):
		inData = {
			"method":"sendMessage",
			"input":{
				"object_guid":chat_id,
				"reply_to_message_id":message_id,
				"rnd":f"{randint(100000,999999999)}",
				"file_inline":{
					"dc_id":str(dc_id),
					"file_id":str(file_id),
					"type":"File",
					"file_name":file_name,
					"size":size,
					"mime":mime,
					"access_hash_rec":access_hash_rec
				}
			},
			"client": SetClines.web
		}

		if caption != None: inData["input"]["text"] = caption


		while 1:
			try:
				return loads(self.enc.decrypt(loads(self.send_post_file(inData))["data_enc"]))
				break
			except: continue


	
	                
	def sendVoice(self, chat_id, file, time, caption=None, message_id=None):
		uresponse = Bot._uploadFile(self, file)
		file_id = str(uresponse[0]["id"])
		mime = file.split(".")[-1]
		dc_id = uresponse[0]["dc_id"]
		access_hash_rec = uresponse[1]
		file_name = file.split("/")[-1]
		size = str(len(get(file).content if "http" in file else open(file,"rb").read()))

		inData = {
				"method":"sendMessage",
				"input":{
					"file_inline": {
						"dc_id": dc_id,
						"file_id": file_id,
						"type":"Voice",
						"file_name": file_name,
						"size": size,
						"time": time,
						"mime": mime,
						"access_hash_rec": access_hash_rec,
					},
					"object_guid":chat_id,
					"rnd":f"{randint(100000,999999999)}",
					"reply_to_message_id":message_id
				},
				"client": SetClines.web
			}

		if caption != None: inData["input"]["text"] = caption


		while 1:
			try:
				return loads(self.enc.decrypt(loads(self.send_post_file(inData))["data_enc"]))
				break
			except: continue
		

	
	
	def sendPhoto(self, chat_id, file, size=[], thumbnail=None, caption=None, message_id=None):
		uresponse = Bot._uploadFile(self, file)
		if thumbnail == None: thumbnail = '/9j/4AAQSkZJRgABAQAAAQABAAD/4gIoSUNDX1BST0ZJTEUAAQEAAAIYAAAAAAIQAABtbnRyUkdC\nIFhZWiAAAAAAAAAAAAAAAABhY3NwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQAA9tYAAQAA\nAADTLQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAlk\nZXNjAAAA8AAAAHRyWFlaAAABZAAAABRnWFlaAAABeAAAABRiWFlaAAABjAAAABRyVFJDAAABoAAA\nAChnVFJDAAABoAAAAChiVFJDAAABoAAAACh3dHB0AAAByAAAABRjcHJ0AAAB3AAAADxtbHVjAAAA\nAAAAAAEAAAAMZW5VUwAAAFgAAAAcAHMAUgBHAEIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\nAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAFhZWiAA\nAAAAAABvogAAOPUAAAOQWFlaIAAAAAAAAGKZAAC3hQAAGNpYWVogAAAAAAAAJKAAAA+EAAC2z3Bh\ncmEAAAAAAAQAAAACZmYAAPKnAAANWQAAE9AAAApbAAAAAAAAAABYWVogAAAAAAAA9tYAAQAAAADT\nLW1sdWMAAAAAAAAAAQAAAAxlblVTAAAAIAAAABwARwBvAG8AZwBsAGUAIABJAG4AYwAuACAAMgAw\nADEANv/bAEMAEAsMDgwKEA4NDhIREBMYKBoYFhYYMSMlHSg6Mz08OTM4N0BIXE5ARFdFNzhQbVFX\nX2JnaGc+TXF5cGR4XGVnY//bAEMBERISGBUYLxoaL2NCOEJjY2NjY2NjY2NjY2NjY2NjY2NjY2Nj\nY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY//AABEIAFAAUAMBIgACEQEDEQH/xAAaAAADAQEB\nAQAAAAAAAAAAAAACAwUBBgQA/8QAJBAAAgICAgICAgMAAAAAAAAAAQIAAwQRBSESMRNBFSIyQmH/\nxAAXAQADAQAAAAAAAAAAAAAAAAAAAQID/8QAGxEBAQEBAQADAAAAAAAAAAAAAAERIQIDEjH/2gAM\nAwEAAhEDEQA/ALAMMGJBhgxkcDCBiQYYMQNBhAxXlobnis5Hws8ddQCpubEU2ixAwjQYAYM2BuaD\nA0sRiqx+oCOAd6mtyVNZ0wjTr0JSx+o34wo2Yqrk6Cm/ITHzK7B0wiMGXcKk6kPJtLNuezLs899y\nU7P5/wCQCzxeT14mVgepy2NeVca9zo8O35axv3AHgwtwD1NBgaXuLsoSwdiHPoyeHIwlFRKsRqc9\nbm3UWFUc6E6fOYjHYD2ROOy67FsJYHuTV+M3r0jlLmOmaO/IMo/YbEj9g7jVu+m7EnWt8S/i1j51\nZ7HuW+PyPMgq0h8TgpldgdSxXxbUd1NLnWPuY6SrVtQ77gMpU6Mm4r30Eb7lSu1b1/YaMeIlSILt\n4jZhqvkZmQg8CBHJotxE5XONY2vqQ8nkltQgr3KfJ47aOuxIF2P31J9cvV+Z9psCr+RhopZwo7Jn\n1GMzH1Og4fja3cOx7H1JxpPk51V4TH+DFBI0TKgMSoCAAehDBlxlbpoMYra9RAMINAki3kPA6Bn1\nWX8n9pzdmWzd7ilyrEYMrTXZGWWujyCHBBkXMxiCWWUqbfnxhZ9iL2H6MLJYctifh2qr+LiVcNmX\nKU1/xM8rYKu216M9uFS9LjfqTlPYrNYVcA/caDMesWVhvsTB6ipwwGaDAmgyVP/Z\n'
		elif "." in thumbnail:thumbnail = str(Bot._getThumbInline(open(file,"rb").read() if not "http" in file else get(file).content))

		if size == []: size = Bot._getImageSize(open(file,"rb").read() if not "http" in file else get(file).content)

		file_inline = {
			"dc_id": uresponse[0]["dc_id"],
			"file_id": uresponse[0]["id"],
			"type":"Image",
			"file_name": file.split("/")[-1],
			"size": str(len(get(file).content if "http" in file else open(file,"rb").read())),
			"mime": file.split(".")[-1],
			"access_hash_rec": uresponse[1],
			"width": size[0],
			"height": size[1],
			"thumb_inline": thumbnail
		}

		inData = {
				"method":"sendMessage",
				"input":{
					"file_inline": file_inline,
					"object_guid": chat_id,
					"rnd": f"{randint(100000,999999999)}",
					"reply_to_message_id": message_id
				},
				"client": SetClines.web
			}
		if caption != None: inData["input"]["text"] = caption

		while 1:
			try:
				return loads(self.enc.decrypt(loads(self.send_post_file(inData))["data_enc"]))
				break
			except: continue

	def addGroup(self, title):
	    inData = {"method":"addGroup","input":{"title":title},"client":SetClines.web}
	    while 1:
	        try:
	            return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"]))
	        except:continue
	        
	        
	def sendVoice1(self, chat_id, file_id , mime , dc_id, access_hash_rec, file_name,  size, duration, text=None, message_id=None):
	    inData = {"method":"sendMessage","input":{
	    "object_guid":chat_id,
	    "rnd":f"{randint(100000,900000)}",
	    "file_inline":{
		"dc_id":str(dc_id),
		"file_id":str(file_id),
		"type":"Voice",
		"file_name":file_name,
		"size":size,
		"mime":mime,
		"access_hash_rec":access_hash_rec,
		'time':duration,}
	    },"client":SetClines.web}
	    if text != None: inData["text"] = text
	    if message_id != None: inData["input"]["reply_to_message_id"] = message_id
	    while 1:
	        try:
	            return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"]))
	        except:continue
	        
	        
	def requestFile(self, name, size , mime):
	    inData = {"method":"requestSendFile","input":{"file_name":name,"size":size,"mime":mime},"client":SetClines.web}
	    while 1:
	        try:
	            return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"]))
	        except:continue
	        
	        
	def fileUpload(self, bytef ,hash_send ,file_id ,url):
		if len(bytef) <= 131072:
			h = {
				'auth':self.auth,
				'chunk-size':str(len(bytef)),
				'file-id':str(file_id),
				'access-hash-send':hash_send,
				'total-part':str(1),
				'part-number':str(1)
			}
			t = False
			while t == False:
				try:
					j = post(data=bytef,url=url,headers=h).text
					j = loads(j)['data']['access_hash_rec']
					t = True
				except:
					t = False
			
			return j
		else:
			t = len(bytef) / 131072
			t += 1
			t = math.floor(t)
			for i in range(1,t+1):
				if i != t:
					k = i - 1
					k = k * 131072
					t2 = False
					while t2 == False:
						try:
							o = post(data=bytef[k:k + 131072],url=url,headers={
								'auth':self.auth,
								'chunk-size':str(131072),
								'file-id':file_id,
								'access-hash-send':hash_send,
								'total-part':str(t),
								'part-number':str(i)
							}).text
							o = loads(o)['data']
							t2 = True
						except:
							t2 = False
					j = k + 131072
					j = round(j / 1024)
					j2 = round(len(bytef) / 1024)
					print(str(j) + 'kb / ' + str(j2) + ' kb')                
				else:
					k = i - 1
					k = k * 131072
					t2 = False
					while t2 == False:
						try:
							p = post(data=bytef[k:],url=url,headers={
								'auth':self.auth,
								'chunk-size':str(len(bytef[k:])),
								'file-id':file_id,
								'access-hash-send':hash_send,
								'total-part':str(t),
								'part-number':str(i)
							}).text
							p = loads(p)['data']['access_hash_rec']
							t2 = True
						except:
							t2 = False
					j2 = round(len(bytef) / 1024)
					print(str(j2) + 'kb / ' + str(j2) + ' kb') 
					return p
					
	
	def getDCs():
	    inData = {"method":"getDCs","input":{ },"client":SetClines.web}
	    while 1:
	        try:
	            return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"]))
	        except:continue
	def addChannel(self, title):
	    inData = {"method":"addChannel","input":{"channel_type":"Public","title":title},"client":SetClines.web}
	    while 1:
	        try:
	            return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"]))
	        except:continue
	def sendSticker(self, chat_id, emoji_character, sticker_id, sticker_set_id,message_id=None):
	    inData = {"method":"sendMessage","input":{"object_guid":chat_id,"rnd":f"{randint(100000,999999999)}","reply_to_message_id":message_id,"sticker":{"emoji_character":emoji_character,"sticker_id":sticker_id,"sticker_set_id":sticker_set_id,"w_h_ratio:":"1.0"}},"client":SetClines.web}
	    while 1:
	        try:
	            return loads(self.enc.decrypt(loads(self.send_post_file(inData))["data_enc"]))
	        except:continue
	def sendGif(self, chat_id, file, caption=None, message_id=None, thumbnail=None):
	    uresponse = Bot._uploadFile(self, file)
	    if thumbnail == None: thumbnail = '/9j/4AAQSkZJRgABAQAAAQABAAD/4gIoSUNDX1BST0ZJTEUAAQEAAAIYAAAAAAIQAABtbnRyUkdC\nIFhZWiAAAAAAAAAAAAAAAABhY3NwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQAA9tYAAQAA\nAADTLQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAlk\nZXNjAAAA8AAAAHRyWFlaAAABZAAAABRnWFlaAAABeAAAABRiWFlaAAABjAAAABRyVFJDAAABoAAA\nAChnVFJDAAABoAAAAChiVFJDAAABoAAAACh3dHB0AAAByAAAABRjcHJ0AAAB3AAAADxtbHVjAAAA\nAAAAAAEAAAAMZW5VUwAAAFgAAAAcAHMAUgBHAEIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\nAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAFhZWiAA\nAAAAAABvogAAOPUAAAOQWFlaIAAAAAAAAGKZAAC3hQAAGNpYWVogAAAAAAAAJKAAAA+EAAC2z3Bh\ncmEAAAAAAAQAAAACZmYAAPKnAAANWQAAE9AAAApbAAAAAAAAAABYWVogAAAAAAAA9tYAAQAAAADT\nLW1sdWMAAAAAAAAAAQAAAAxlblVTAAAAIAAAABwARwBvAG8AZwBsAGUAIABJAG4AYwAuACAAMgAw\nADEANv/bAEMAEAsMDgwKEA4NDhIREBMYKBoYFhYYMSMlHSg6Mz08OTM4N0BIXE5ARFdFNzhQbVFX\nX2JnaGc+TXF5cGR4XGVnY//bAEMBERISGBUYLxoaL2NCOEJjY2NjY2NjY2NjY2NjY2NjY2NjY2Nj\nY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY//AABEIAFAAUAMBIgACEQEDEQH/xAAaAAADAQEB\nAQAAAAAAAAAAAAACAwUBBgQA/8QAJBAAAgICAgICAgMAAAAAAAAAAQIAAwQRBSESMRNBFSIyQmH/\nxAAXAQADAQAAAAAAAAAAAAAAAAAAAQID/8QAGxEBAQEBAQADAAAAAAAAAAAAAAERIQIDEjH/2gAM\nAwEAAhEDEQA/ALAMMGJBhgxkcDCBiQYYMQNBhAxXlobnis5Hws8ddQCpubEU2ixAwjQYAYM2BuaD\nA0sRiqx+oCOAd6mtyVNZ0wjTr0JSx+o34wo2Yqrk6Cm/ITHzK7B0wiMGXcKk6kPJtLNuezLs899y\nU7P5/wCQCzxeT14mVgepy2NeVca9zo8O35axv3AHgwtwD1NBgaXuLsoSwdiHPoyeHIwlFRKsRqc9\nbm3UWFUc6E6fOYjHYD2ROOy67FsJYHuTV+M3r0jlLmOmaO/IMo/YbEj9g7jVu+m7EnWt8S/i1j51\nZ7HuW+PyPMgq0h8TgpldgdSxXxbUd1NLnWPuY6SrVtQ77gMpU6Mm4r30Eb7lSu1b1/YaMeIlSILt\n4jZhqvkZmQg8CBHJotxE5XONY2vqQ8nkltQgr3KfJ47aOuxIF2P31J9cvV+Z9psCr+RhopZwo7Jn\n1GMzH1Og4fja3cOx7H1JxpPk51V4TH+DFBI0TKgMSoCAAehDBlxlbpoMYra9RAMINAki3kPA6Bn1\nWX8n9pzdmWzd7ilyrEYMrTXZGWWujyCHBBkXMxiCWWUqbfnxhZ9iL2H6MLJYctifh2qr+LiVcNmX\nKU1/xM8rYKu216M9uFS9LjfqTlPYrNYVcA/caDMesWVhvsTB6ipwwGaDAmgyVP/Z\n'
	    elif "." in thumbnail:thumbnail = str(Bot._getThumbInline(open(file,"rb").read() if not "http" in file else get(file).content))
	    file_id = str(uresponse[0]["id"])
	    mime = file.split(".")[-1]
	    dc_id = uresponse[0]["dc_id"]
	    access_hash_rec = uresponse[1]
	    file_name = file.split("/")[-1]
	    size = str(len(get(file).content if "http" in file else open(file,"rb").read()))
	    inData = {
	    "method":"sendMessage",
	    "input":{
	    "file_inline":{
	    "access_hash_rec":access_hash_rec,
	    "auto_play":False,
	    "dc_id":dc_id,
	    "file_id":file_id,
	    "file_name":file_name,
	    "height":426,
	    "mime":mime,
	    "size":size,
	    "thumb_inline":thumbnail,
	    "time":5241,
	    "type":"Gif",
	    "width":424
	    },
	    "is_mute":False,
	    "object_guid":chat_id,"rnd":f"{randint(100000,999999999)}",
	    "reply_to_message_id":message_id
	    
	    },
	    "client":SetClines.web
	    }
	    if caption != None: inData["input"]["text"] = caption
	    while 1:
	        try:
	            return loads(self.enc.decrypt(loads(self.send_post_file(inData))["data_enc"]))
	        except:continue
	        
	def sendMusic(self, chat_id, file, time, caption=None, message_id=None):
		uresponse = Bot._uploadFile(self, file)
		file_id = str(uresponse[0]["id"])
		mime = file.split(".")[-1]
		dc_id = uresponse[0]["dc_id"]
		access_hash_rec = uresponse[1]
		file_name = file.split("/")[-1]
		size = str(len(get(file).content if "http" in file else open(file,"rb").read()))

		inData = {
				"method":"sendMessage",
				"input":{
					"file_inline": {
						"dc_id": dc_id,
						"file_id": file_id,
						"type":"Music",
						"music_performer":"",
						"file_name": file_name,
						"size": size,
						"time": time,
						"mime": mime,
						"access_hash_rec": access_hash_rec,
					},
					"object_guid":chat_id,
					"rnd":f"{randint(100000,999999999)}",
					"reply_to_message_id":message_id
				},
				"client": SetClines.web
			}

		if caption != None: inData["input"]["text"] = caption


		while 1:
			try:
				return loads(self.enc.decrypt(loads(self.send_post_file(inData))["data_enc"]))
				break
			except: continue

			
						
	def sendImage(self, chat_id, file_id , mime , dc_id, access_hash_rec, file_name,  size, thumb_inline , width , height, text=None, message_id=None):
	    inData = {"method":"sendMessage","input":{"object_guid":chat_id,
		"rnd":f"{randint(100000,900000)}",
		"file_inline":{
		"dc_id":str(dc_id),
		"file_id":str(file_id),
		"type":"Image",
		"file_name":file_name,
		"size":size,
		"mime":mime,
		"access_hash_rec":access_hash_rec,
		'thumb_inline':thumb_inline,
		'width':width,
		'height':height}},"client":SetClines.web}
	    if message_id != None:inData['input']['reply_to_message_id'] = message_id
	    if text != None:inData['input']['text'] = text
	    while 1:
	        try:
	            return loads(self.enc.decrypt(loads(self.send_post(inData))["data_enc"]))
	        except:continue											
															
																		
																								

	def getImageSize(self,image_bytes:bytes):
		im = Image.open(io.BytesIO(image_bytes))
		width, height = im.size
		return width , height
		
		
	
	def getThumbInline(self,image_bytes:bytes):
		im = Image.open(io.BytesIO(image_bytes))
		width, height = im.size
		if height > width:
			new_height = 40
			new_width  = round(new_height * width / height)
		else:
			new_width  = 40
			new_height = round(new_width * height / width)
		im = im.resize((new_width, new_height), Image.ANTIALIAS)
		changed_image = io.BytesIO()
		im.save(changed_image, format='PNG')
		changed_image = changed_image.getvalue()
		return base64.b64encode(changed_image)
		
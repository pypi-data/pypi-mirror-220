import re
import os
import json
import time
from datetime import datetime
from bs4 import BeautifulSoup


class kidLoggerFileArrange():
	
	def __init__(self) -> None:
		pass

	def openfile(self, filename):
		with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
			content = f.read()
			finalpostion = int(content.rfind(','))
			content = content[:finalpostion]
			content = content.replace("\\","/")
			content = content.replace("\n", "")
			content = content.replace('"},','"},\n')
			content = re.sub(r"(.)},",'"},',content)
			content = re.sub(r"(.)}],",'"}],',content)
			content = '{ "data": [' + content + ']}'
		# 除錯用
		with open('demo.json','w+',encoding='utf-8') as f:
			f.write(content)
		
		return content

	# 抓取檔案的修改日期
	def getCreatDate(self, filepath):

		# 獲取修改日期年分
		file_time = time.ctime(os.path.getmtime(filepath))
		year = str(datetime.strptime(file_time, "%c").year)

		# 獲取檔案名稱, 日及月資料
		day, month = filepath.split('\\')[-1].split(',')[0].split(' ')
		modified_date = datetime.strptime(f"{year}-{month}-{day}","%Y-%B-%d").date()

		return str(modified_date)

	def parse(self,text:str, filepath:str, filename:str) -> dict :
		
		data = ""
		errordata = ""
		htmlContent = ""
		
		try:
			data = json.loads(text, strict = False)

		except ValueError as e:
			# print(f'invalid json: {e}')
			# print(e.args) tuple
			errorText = e.args[0]
			# print(errorText)
			
			# 將錯誤的char, line抓出來
			charStartPosition = errorText.find('char ') + 5
			charEndPosition = errorText.rfind(')')
			char = int(errorText[charStartPosition: charEndPosition])
			lineStartPosition = errorText.find('line ') + 5
			lineEndPosition = errorText.rfind('column')
			line = int(errorText[lineStartPosition: lineEndPosition])
			
			
			# 除錯用
			with open('demo2.json', 'w+', encoding='utf-8') as file:
				file.write(text)
			
			# print(f"char: {char}")
			# print(f"line: {line}")

			try:
				while text[char] == " ":
					char -= 1
				
				else:
					# print(f"errorText: {text[char]}")

					# 先找該行的起始位置終點, 每個行的起頭都是
					lineStartChar = int(text[:char].rfind('{ "class":'))

					# 若找不到起始點, 又找到p標籤, 則將html拿掉
					if lineStartChar == -1 and text.find("<p class=") != -1:
						startHtml = text.find("<p class")
						endHtml = text.find("/p>") + 2
						html = text[startHtml:endHtml]
						htmlContent += html	
						text = text[:startHtml] + "" + text[endHtml+1:]

					# 當最後一行有異常時
					finalRow = text[char:].find('"},')
					# print(f"finalRow:{finalRow}")
					if finalRow == -1:
						if text[char:].find('"}]') != -1:
							lineEndChar = char + int(text[char:].find('"}]')) + 3
						# 當第一行就出現異常時
						else:
							lineEndChar = char + int(text[char:].find('}]')) + 2
					else:
						lineEndChar = char + int(text[char:].find('"},')) + 3

					# 真的不行就把特定行的資料給先擷取出來, 放到.json檔案
					
					# print('無法解決')
					# print(f'lineStartChar: {lineStartChar}, lineEndChar:{lineEndChar}')
					# print(text[lineStartChar:lineEndChar])
					errordata += text[lineStartChar:lineEndChar] + "\n"

					# 把特定text特定行列資料刪除
					text = text[:lineStartChar] + "" + text[lineEndChar+1:]
					# print('-----------------text-----------------')
					# print(text)

				data = self.parse(text, filepath, filename) # 遞迴執行, 直到正常解析為止
			except:
				print(f'{filepath}-{filename}')
				finalcomma = text.rfind(',')
				if finalcomma != -1:
					text = text[:finalcomma] + ""
				text = text + "]}"
				data = self.parse(text, filepath, filename) # 遞迴執行, 直到正常解析為止
		
		# 處理html行列
		if htmlContent != "":
			soup = BeautifulSoup(htmlContent, 'html.parser')
			ps = soup.find_all('p')
			for row in ps:
				dataline = {}
				class_ = row.get('class')[0]
				time = row.get('time')
				coordinates = row.get('coordinates')
				duration = row.get('duration')
				action = row.text.replace("'","")
				applicationName = row.get('applicationName')
				href = row.get('href')

				if class_ != None: dataline['class'] = class_
				else: dataline['class'] = ""
				
				if time != None: dataline['time'] = time
				else: dataline['time'] = ""
				
				if coordinates != None: dataline['coordinates'] = coordinates
				else: dataline['coordinates'] = ""
				
				if duration != None: dataline['duration'] = duration
				else: dataline['duration'] = 0
				
				if action != None: dataline['action'] = action
				else: dataline['action'] = ""

				if applicationName != None: dataline['applicationName'] = applicationName
				else: dataline['applicationName'] = ""
			
				if href != None: dataline['href'] = href
				else: dataline['href'] = ""

				data['data'].append(dataline)

		# 若異常資料不為空值, 則創建檔案
		temp = errordata.replace(" ","").replace("\n","")
		if temp != "":
			with open(f'{filepath}/error_{filename}.json','w+', encoding='utf-8') as f:
				f.write(errordata)
				
		return data

	def clean_text(self, rgx_list, text):
		new_text = text
		for rgx_match in rgx_list:
			new_text = re.sub(rgx_match, '', new_text)
		return new_text

	def errorParse(self, filename: str) -> dict:

		jsLoads = ""
		f = open(filename, "r",encoding="utf-8")
		lines = f.readlines()
		f.close()
		i = 0
		data  = {"data": []}
		htmlContent = ""
		for line in lines:
			
			rgx_list = ["\x0c","\ue396","\ue91b","\ue705","\x03","\n","\uf113","\uf669","\ue56c","\ue743","\ue543","\ue9b5","\uf697","\x80","uee01","","\x02","\x05","\x07", "\'"]
			line = self.clean_text(rgx_list,line).strip()
			# print(line)
			if (line != ""):
				line = re.sub(r"(.)}]", '"},', line)
				# 若有html則先提取, 避免錯誤
				if line.find("<p class=") != -1:
					startHtml = line.find("<p class")
					endHtml = line.find("/p>") + 2
					html = line[startHtml:endHtml]
					htmlContent += html
					line = line[:startHtml] + "" + line[endHtml+1:]
					# print(line)

				if (line != "" and line[0:1] == "{" and line[-1:] == ","):
					line = line + ""
				else:
					if (lines[i].replace("\n", "")==""):
						line = line + lines[i+1].replace("\n", "")
					else:
						line = line + lines[i].replace("\n", "")

				if (line[0:1] == "{"):
					line = line.replace("},", "}").replace("User", "Vser").replace(" : ", ":").replace("\\", "\\\\")
					try:
						jsLoads = json.loads(line, strict = False)
						data['data'].append(jsLoads)
						# print(jsLoads["class"])
					except Exception as e:
						if line.find('"action"') != -1:
							line = line[0:line.find('"action"')+10]+ re.findall(r'"action":(.*)}',line)[0].replace('"'," ")+'"}'
						if line.find('"href"') != -1:
							line = line[0:line.find('"href"') + len('"href"') + 2] + re.findall(r'"href":(.*)',line)[0].replace('"'," ")+'"}'
						try:
							jsLoads = json.loads(line, strict = False)
							data['data'].append(jsLoads)
							# print(jsLoads["class"])
						except Exception as e:
							print(e)
			i += 1

		# 處理html行列
		soup = BeautifulSoup(htmlContent, 'html.parser')
		ps = soup.find_all('p')
		for row in ps:
			dataline = {}
			class_ = row.get('class')[0]
			time = row.get('time')
			coordinates = row.get('coordinates')
			duration = row.get('duration')
			action = row.text.replace("'","")
			applicationName = row.get('applicationName')
			href = row.get('href')

			if class_ != None: dataline['class'] = class_
			else: dataline['class'] = ""
			
			if time != None: dataline['time'] = time
			else: dataline['time'] = ""
			
			if coordinates != None: dataline['coordinates'] = coordinates
			else: dataline['coordinates'] = ""
			
			if duration != None: dataline['duration'] = duration
			else: dataline['duration'] = 0
			
			if action != None: dataline['action'] = action
			else: dataline['action'] = ""

			if applicationName != None: dataline['applicationName'] = applicationName
			else: dataline['applicationName'] = ""
		
			if href != None: dataline['href'] = href
			else: dataline['href'] = ""

			data['data'].append(dataline)

		return data


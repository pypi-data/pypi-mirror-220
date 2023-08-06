import os
import sys
import json
import requests
import configparser
import pandas as pd
from datetime import date
from urllib.request import urlretrieve

# requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'


class HRAPI:

    def __init__(self, url, username, password, mode, klog_user, klog_password) -> None:
        self.url = url # http://192.168.12.175:11080
        self.username = username # HRMIS
        self.password = password # ji3g4hrmis
        self.mode = mode
        self.path_gettoken = '/api/token/'
        self.path_config = '/api/config/'
        self.klog_user = klog_user
        self.klog_password = klog_password

    def run(self) -> None:
        try:
            tokenData = self.get_token()
            if tokenData['status']:
                self.token = tokenData['Token']
                configdata = self.get_config(token=tokenData['Token'])
                self.configstatus = configdata['status']
                if configdata['status']:
                    self.config = configdata['data']
                    self.apiconfig = self.get_apiConfig()
        except Exception as e:
            print(e)
            return {"status": False, "message":"hrapi run fail", "error": e}

    def get_token(self) -> dict:
        try:
            if self.url:
                payload = {
                    "username": self.username,
                    "password": self.password
                }
                hrapiTokenData = requests.post(self.url + self.path_gettoken , data=payload).json()
                hrapiToken = hrapiTokenData['access']
                return {"Token": hrapiToken, "status": True}
            else:
                return {"status": False, "message":"configuration didn't set up"}
        except Exception as e:
            print(e)
            return {"status": False, "message":"get token error, hrapi request fail"}

    def get_apiConfig(self):
        configList = []
        for row in self.config:
            obj = {
                'id': row['id'],
                'version': row['version']['version'],
                'mode': row['mode']['mode'],
                'system': row['system']['code'],
                'content_type': row['content_type']['content_type'],
                'group': row['group'],
                'key': row['key'],
                'value': row['value']
            }
            configList.append(obj)

        df = pd.DataFrame(configList)
        df = df[df['mode'] == self.mode]

        # 轉換成 apiConfig import configparser
        apiConfig = {}
        for index, row in df.iterrows():
            if row['system'] not in apiConfig:
                apiConfig[row['system']] = {}
                apiConfig[row['system']][row['key']] = row['value']
            else:
                apiConfig[row['system']][row['key']] = row['value']

        return apiConfig

    def hrmis_checkincheckout(self, requestdata:str, token:str) -> dict:
        """
        requestdata format: {
            "Empno": "AIR-0013",
            "StartDay" : "2021-09-01",
            "EndDay": "2021-09-30"
            }
        """
        if type(requestdata) == dict:
            requestdata = json.dumps(requestdata)
        if token:
            url = self.url + self.apiconfig['HRAPI']['path_hrmischeckincheckout']
            headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
            result = requests.post(url , data=requestdata, headers=headers)
            return {"status": True, "data": result.json()}
        else:
            return {"status": False, "message":"can't find token"}

    def notification_notify_users(self, requestdata:str, token:str) -> dict:
        """
        requestdata = {
            "template_id": bulletin_manage_remind_notify_template_id,
            "staff_id": ['AIR-0102', 'AIR-0013'],
            "type_id" : 1,
            "options": {
                "link": URL('show_bulletin_by_all', args=(request.post_vars.bulletin_id), host=domain),
                "title": bulletin_title
            }
        }
        """
        if type(requestdata) == dict:
            requestdata = json.dumps(requestdata)

        if token:
            url = self.url + self.apiconfig['HRAPI']['path_notification_notify_users']
            headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
            result = requests.post(url , data=requestdata, headers=headers)
            return {"status": True, "data": result.json()}
        else:
            return {"status": False, "message":"can't find token"}

    def notification_notify_groups(self, requestdata:str, token:str) -> dict:
        """
        requestdata = {
            'template_id': 1,
            'groups_id' : ["19:c9a2b250bd124b19876a0d46e666ee72@thread.skype","19:c9a2b250bd124b19876a0d46e6fff1231@thread.skype"],
            'type_id' : 1, # option, 1: System, 2: Schdule, default: 1
            'options' : {
                'link': 'https://www.google.com',
                'title': 'title name'
            }
        }
        """
        if type(requestdata) == dict:
            requestdata = json.dumps(requestdata)

        if token:
            url = self.url + self.apiconfig['HRAPI']['path_notification_notify_groups']
            headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
            result = requests.post(url , data=requestdata, headers=headers)
            return {"status": True, "data": result.json()}
        else:
            return {"status": False, "message":"can't find token"}

    def get_config(self, token:str, **kwargs):
        if token:
            url = self.url + self.path_config
            if 'mode' in kwargs:
                url += f"?mode={kwargs['mode']}"
            headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
            result = requests.get(url , headers=headers)
            return {"status": True, "data": result.json()}
        else:
            return {"status": False, "message":"can't find token"}

    def get_notification_history(self, token, **kwargs):
        if token:
            params = {}
            url = self.url + self.apiconfig['HRAPI']['path_notification_history']
            headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
            if 'params' in kwargs:
                params = kwargs['params']
            result = requests.get(url , headers=headers, params=params)
            return {"status": True, "data": result.json()}
        else:
            return {"status": False, "message":"can't find token"}

    def get_notification_template(self, token, **kwargs):
        if token:
            url = self.url + self.apiconfig['HRAPI']['path_notification_template']
            headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
            result = requests.get(url , headers=headers)
            return {"status": True, "data": result.json()}
        else:
            return {"status": False, "message":"can't find token"}

    def get_aircastapplication_main_version(self, token, **kwargs):
        if token:
            params = {}
            url = self.url + self.apiconfig['AircastApplication']['path_aircastapplication_main_version']
            headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
            if 'params' in kwargs:
                params = kwargs['params']
            result = requests.get(url , headers=headers, params=params)
            return {"status": True, "data": result.json()}
        else:
            return {"status": False, "message":"can't find token"}

    def get_aircastapplication_main_paths(self, token, **kwargs):
        if token:
            params = {}
            url = self.url + self.apiconfig['AircastApplication']['path_aircastapplication_main_paths']
            headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
            if 'params' in kwargs:
                params = kwargs['params']
            result = requests.get(url , headers=headers, params=params)
            return {"status": True, "data": result.json()}
        else:
            return {"status": False, "message":"can't find token"}

    def get_aircastapplication_download(self, token, **kwargs):
        if token:
            params = {}
            if 'params' in kwargs:
                params = kwargs['params']
                url = self.url + os.path.join(self.apiconfig['AircastApplication']['path_aircastapplication_download'].replace('{{version}}', params["version"]), params["filepath"])
                dst = os.path.join(params["filepath"])
                workDirectory = False
                filename = os.path.basename(dst)
                folderPath = dst.replace(filename, "")
                if "workDirectory" in params:
                    workDirectory = params["workDirectory"]
                if workDirectory:
                    urlretrieve(url, filename)
                else:
                    if folderPath != "" and not os.path.exists(folderPath):
                        try:
                            os.makedirs(folderPath)
                        except FileExistsError:
                            pass
                    urlretrieve(url, dst)
                return {"status": True, "message":"download success"}
            else:
                return {"status": False, "message": "missing kwargs params, please check it"}
        else:
            return {"status": False, "message":"can't find token"}

    def get_aircastapplication_main_hash(self, token, **kwargs):
        if token:
            params = {}
            if 'params' in kwargs:
                params = kwargs['params']
            url = self.url + os.path.join(self.apiconfig['AircastApplication']['path_aircastapplication_main_hash'].replace('{{version}}', params["version"]))
            headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
            result = requests.get(url , headers=headers, params=params)
            return {"status": True, "data": result.json()['data']}
        else:
            return {"status": False, "message":"can't find token"}

    def get_klogbeta_piechartdict(self, token, **kwargs):
        """
        params = {
            "start": "2022-02-01 00:00:00",
            "end": "2022-02-10 23:59:59",
            "usernameList" : ['markfang', 'tedchang']
        }
        """
        if token:
            params = {}
            if 'params' in kwargs:
                params = kwargs['params']
            url = self.url + os.path.join(self.apiconfig['Klogbeta']['path_klogbeta_piechartdict'])
            headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
            result = requests.get(url , headers=headers, params=params)
            return {"status": True, "data": result.json()}
        else:
            return {"status": False, "message":"can't find token"}

    def get_klogbeta_memberchartdict(self, token, **kwargs):
        """
        params = {
            "startdate": "2022-02-01",
            "enddate": "2022-02-10",
            "username" : 'markfang'
        }
        """
        if token:
            params = {}
            if 'params' in kwargs:
                params = kwargs['params']
            url = self.url + os.path.join(self.apiconfig['Klogbeta']['path_klogbeta_memberchartdict'])
            headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
            result = requests.get(url , headers=headers, params=params)
            return {"status": True, "data": result.json()}
        else:
            return {"status": False, "message":"can't find token"}

    def get_klogbeta_teamchartdict(self, token, **kwargs):
        """
        params = {
            "start": "2022-02-01 00:00:00",
            "end": "2022-02-10 23:59:59",
            "usernameList" : ['markfang', 'tedchang']
        }
        """
        if token:
            params = {}
            if 'params' in kwargs:
                params = kwargs['params']
            url = self.url + os.path.join(self.apiconfig['Klogbeta']['path_klogbeta_teamchartdict'])
            headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
            result = requests.get(url , headers=headers, params=params)
            return {"status": True, "data": result.json()}
        else:
            return {"status": False, "message":"can't find token"}

    def get_hrmis_attandance(self, token, **kwargs):
        """
        params = {
            "Empno": "AIR-0102",
            "StartDay": "2022-03-02",
            "EndDay" : "2022-03-04"
        }
        """
        if token:
            params = {}
            if 'params' in kwargs:
                params = kwargs['params']
            url = self.url + os.path.join(self.apiconfig['HRMIS']['path_hrmis_attendance'])
            headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
            result = requests.get(url , headers=headers, params=params)
            return {"status": True, "data": result.json()}
        else:
            return {"status": False, "message":"can't find token"}

    def patch_hrmis_attendance(self, token, **kwargs):
        """
        payload = {
            "Empno": "AIR-0102",
            "WorkDay": "2021-09-06",
            "IsLate": "N",
            "IsEarly": "N",
            "IsPass": "Y",
            "HRCheck": "N",
            "reMark": "test remark2",
            "OndutyDay": "2021-09-06",
            "OndutyTime": "10:15:12",
            "OffdutyDay": "2021-09-06",
            "OffdutyTime": "19:00:01",
            "TotalHours": 9.1,
            "ActOnDay": "2021-09-06",
            "ActOnTime": "10:15:12",
            "ActOffDay": "2021-09-06",
            "ActOffTime": "19:00:01",
            "Editor": "AIR-0102",
            "EditorTime": "2022-03-07 18:13:00"
        }

        """
        if token:
            payload = json.dumps(kwargs['payload']) if 'payload' in kwargs else dict()
            url = self.url + os.path.join(self.apiconfig['HRMIS']['path_hrmis_attendance'])
            headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
            result = requests.patch(url , headers=headers, data=payload)
            return {"status": True, "data": result.json()}
        else:
            return {"status": False, "message":"can't find token"}

    def get_hrmis_attandancelog(self, token, **kwargs):
        """
        params = {
            "Empno": "AIR-0102",
            "WorkDay" : "2022-03-04"
        }
        """
        if token:
            params = dict()
            if 'params' in kwargs:
                params = kwargs['params']
            url = self.url + os.path.join(self.apiconfig['HRMIS']['path_hrmis_attendancelog'])
            headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
            result = requests.get(url , headers=headers, params=params)
            return {"status": True, "data": result.json()}
        else:
            return {"status": False, "message":"can't find token"}

    def post_hrmis_attandancelog(self, token, **kwargs):
        """
        payload = {
            "atDay": "2021-12-01",
            "atTime": "09:06:20",
            "Empno" : "AIR-0013",
            "EventID": ""
        }
        """
        if token:
            payload = json.dumps(kwargs['payload']) if 'payload' in kwargs else dict()
            url = self.url + os.path.join(self.apiconfig['HRMIS']['path_hrmis_attendancelog'])
            headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
            result = requests.post(url , headers=headers, data=payload)
            return {"status": True, "data": result.json()}
        else:
            return {"status": False, "message":"can't find token"}

    def get_hrmis_department(self, token, **kwargs):
        """
        params = {
            "Deptno": "AIR-0102",
            "needTree" : "2022-03-04",
            "Enable": "Y",
            "DeptnoPath": "",
            "WithFullName": ""
        }
        """
        if token:
            params = dict()
            if 'params' in kwargs:
                params = kwargs['params']
            url = self.url + os.path.join(self.apiconfig['HRMIS']['path_hrmis_department'])
            headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
            result = requests.get(url , headers=headers, params=params)
            return {"status": True, "data": result.json()}
        else:
            return {"status": False, "message":"can't find token"}


    def get_hrmis_employee(self, token, **kwargs):
        """
        params = {
            "Empno": "",
            "Deptno" : "AIR-A800",
            "Enable": "Y",
            "LikeCallName": "",
            "CallNameFirstChar": "",
            "needTree": "Y",
            "isHOD": "N",
            "NeedCheckIn": ""
        }
        """
        if token:
            params = dict()
            if 'params' in kwargs:
                params = kwargs['params']
            url = self.url + os.path.join(self.apiconfig['HRMIS']['path_hrmis_employee'])
            headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
            result = requests.get(url , headers=headers, params=params)
            return {"status": True, "data": result.json()}
        else:
            return {"status": False, "message":"can't find token"}

    def get_hrmis_leave(self, token, **kwargs):
        """
        params = {
            "startday" : "2021-09-01",
            "endday" : "",
            "deptno" : "",
            "Status" : "AC",
            "LID" : ""
        }
        """
        if token:
            params = dict()
            if 'params' in kwargs:
                params = kwargs['params']
            url = self.url + os.path.join(self.apiconfig['HRMIS']['path_hrmis_leave'])
            headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
            result = requests.get(url , headers=headers, params=params)
            return {"status": True, "data": result.json()}
        else:
            return {"status": False, "message":"can't find token"}

    def get_hrmis_leavetype(self, token, **kwargs):
        """
        params = {
            "CompanyID" : "",
            "LID" : "",
            "Enable" : "",
            "ReplacementSet" : "",
        }
        """
        if token:
            params = dict()
            if 'params' in kwargs:
                params = kwargs['params']
            url = self.url + os.path.join(self.apiconfig['HRMIS']['path_hrmis_leavetype'])
            headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
            result = requests.get(url , headers=headers, params=params)
            return {"status": True, "data": result.json()}
        else:
            return {"status": False, "message":"can't find token"}


    def getDepartmentMembers(self, token:str, departmentAbbr: str) -> list:
        departmentRows = self.get_hrmis_department(token)['data']
        deptno, level = "", float("inf")
        for row in departmentRows:
            if (row['Abbr'] == departmentAbbr) and row["DeptLevel"] < level:
                deptno = row["Deptno"]
                level = row["DeptLevel"]
        params = dict(Deptno=deptno, needTree="Y")
        employees = self.get_hrmis_employee(token, params=params)['data']
        return employees


    def getToken(self):
        payload = {
            "username": self.klog_user,
            "password": self.klog_password,
        }

        res = requests.post((self.url + '/api/token/'), data=payload, verify=True)
        return res.json()['access']


    def getAttendance(self, token):
        params = {
            'StartDay':str(date.today()),
            'EndDay':str(date.today())
        }
        res = requests.get(
            (self.url + '/api/hrapi/v2/attandance/'),
            params=params,
            headers={'Authorization':f"Bearer {token}",  'Content-Type':'application/json'},
            verify=True
        )

        return res.json()
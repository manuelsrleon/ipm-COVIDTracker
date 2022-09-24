#!/usr/bin/env python3

import locale
import gettext
from pathlib import Path
import time

from typing import Protocol, Union

import requests



_ = gettext.gettext
N_ = gettext.ngettext


class Model():
        def __init__(self):
            self.complete_name= None
            self.loading_access = False
            self.loading_contacts = False

        def reset(self):
            self.complete_name = None

        def check_errors(self, e):
            if 'error' in e.keys():
                raise Exception("Error de conexión! Por favor, reinicia la aplicación")
            return e

        def is_valid(self):
            try:
                if(self.complete_name is None):
                    return False
                name=self.complete_name.split()
                if len(name)<1:
                    return  False
                elif len(name)>2:
                    return False
                m=self.check_errors(Model.get_users_by_name(self,name[0],name[1]))['users'][0]
            except IndexError:
                return False
            return True

        def search(self, data):
            if data.is_valid():
                pass
            else:
                raise ValueError(_("Invalid name"))

        def build_model(self):
            self.server_address = "localhost"
            self.server_port = "8080"
            self.user= "x-hasura-admin-secret"
            self.password = "myadminsecretkey"

        def reset(self):
            self.complete_name = None

          
        def get_users(self):
            try:
                url=f"http://{self.server_address}:{self.server_port}/api/rest/users"
                headers ={"Content-Type":"application/json", f"{self.user}":f"{self.password}"}
                req = requests.get(url,headers=headers)
                data = req.json()
                return data

            except requests.ConnectionError as e:
                return e
        
        def get_users_limit(self,index,range):
            try:
                url=f"http://{self.server_address}:{self.server_port}/api/rest/users?offset={index}&limit={range}"
                headers ={"Content-Type":"application/json", f"{self.user}":f"{self.password}"}
                req = requests.get(url,headers=headers)
                data = req.json()
                return data

            except requests.ConnectionError as e:
                return e

        def timestamp2datetime(timestamp):
            timestamp = "2021-09-01T13:43:01.277923+00:00"
            yyyy = timestamp[0:4]
            mm = timestamp[5:7]
            dd = timestamp[8:10]
            hhmm = timestamp[11:16]
            print(dd+"/"+mm+"/"+yyyy+" "+hhmm)
        def get_users_by_name(self,name,surname):
            try:
                url=f"http://{self.server_address}:{self.server_port}/api/rest/user?name={name}&surname={surname}"
                headers ={"Content-Type":"application/json", f"{self.user}":f"{self.password}"}
                req = requests.get(url,headers=headers)
                data = req.json()
                return data
            except requests.ConnectionError as e:
                return e
        def get_user_access_log_by_id_limit(self,id,index,range)-> Union[Exception, str]:
            try:
                self.loading_access = True
                url=f"http://{self.server_address}:{self.server_port}/api/rest/user_access_log/{id}?offset={index}&limit={range}"
                headers ={"Content-Type":"application/json", f"{self.user}":f"{self.password}"}
                req = requests.get(url,headers=headers)
                data = req.json()
                self.loading_access = False
                return data
            except requests.ConnectionError as e:
                return e
        def get_user_access_log_by_id(self,id) -> Union[Exception, str]:
            try:
                self.loading_access = True
                url=f"http://{self.server_address}:{self.server_port}/api/rest/user_access_log/{id}"
                headers ={"Content-Type":"application/json", f"{self.user}":f"{self.password}"}
                req = requests.get(url,headers=headers)
                data = req.json()
                self.loading_access = False
                return data
            except requests.ConnectionError as e:
                return e
        def get_facility_access_log(self, id, startdate, enddate) -> Union[Exception, str]:
            try:
                r = requests.get(
                    f"http://localhost:8080/api/rest/facility_access_log/{id}/daterange",
                    headers={"x-hasura-admin-secret": "myadminsecretkey"},
                    json={"startdate": f"{startdate}", "enddate": f"{enddate}"})
                data = r.json()
                data['access_log'].sort(key=lambda r: r["timestamp"], reverse=True)
                self.loading_contacts = False
                return data
            except requests.ConnectionError as e:
                return e

        def get_user_access_log_by_id_datarange(self, id, startdate, enddate) -> Union[Exception, str]:
            try:
                self.loading_contacts = True
                url=f"http://localhost:8080/api/rest/user_access_log/{id}/daterange"
                headers ={"Content-Type":"application/json", f"{self.user}":f"{self.password}"}
                data={"startdate": f"{startdate}", "enddate":f"{enddate}"}
                req = requests.get(url,headers=headers,json=data)
                data = req.json()

                return data
            except requests.ConnectionError as e:
                return e


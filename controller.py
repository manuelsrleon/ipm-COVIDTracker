#!/usr/bin/env python3

import threading
import datetime
import locale
import gettext
import json
import requests
from view import view
from typing import Protocol, Union
from datetime import datetime
from gi.repository import GLib


_ = gettext.gettext
N_ = gettext.ngettext

class Controller:
    
    def set_model(self,model):
        self.model = model
        model.build_model()
        model.busca=[]
        self.access_data = {'access_log': []}
        self.full_access_data = {'access_log': []}
        self.contacts_limited_list = []
        self.access_page = False
        self.contacts_page = False

    def load_view(self, view_name, **kwargs):
        self.view.load_view(view_name, **kwargs)

    def set_view(self, view):
        self.view = view
        view.build_view()
        view.connect_button_close_dialog(self.close_dialog_clicked)
        view.connect_delete_event(self.view.main_quit)
        view.connect_complete_name_changed(self.complete_name_changed)
        view.connect_search_clicked(self.search_clicked)   
        view.connect_close_clicked(self.close_clicked)
        view.connect_maximize_clicked(self.maximize_clicked)
        view.connect_minimize_clicked(self.minimize_clicked)

        view.connect_button_home(self.button_home)
        view.connect_button_back(self.button_back)
        view.connect_treeview(self.update_treeview)
        
        view.connect_access_back5_btn_clicked(self.access_back5_btn_clicked)
        view.connect_access_back1_btn_clicked(self.access_back1_btn_clicked)
        view.connect_access_page_btn_clicked(self.access_page_btn_clicked)
        view.connect_access_next1_btn_clicked(self.access_next1_btn_clicked)
        view.connect_access_next5_btn_clicked(self.access_next5_btn_clicked)
        
        view.connect_contact_back5_btn_clicked(self.contact_back5_btn_clicked)
        view.connect_contact_back1_btn_clicked(self.contact_back1_btn_clicked)
        view.connect_contact_page_btn_clicked(self.contact_page_btn_clicked)
        view.connect_contact_next1_btn_clicked(self.contact_next1_btn_clicked)
        view.connect_contact_next5_btn_clicked(self.contact_next5_btn_clicked)
        view.connect_calendar_set_btn_clicked(self.calendar_set_btn_clicked)
        view.connect_button_show_date_filter(self.button_date_filter_clicked)
        view.connect_button_expand_access_log(self.button_expand_access_log_clicked)
        view.connect_button_expand_contacts(self.button_expand_contacts_clicked)
    
    def close_dialog_clicked(self, w):
        self.view.close_dialog()

    def main(self):
        self.view.show_all()
        self.view.hide_list()
        self.view.main()
        
    def complete_name_changed(self, entry):
        self.view.hide_list()
        n = entry.get_text()
        complete_name=self._parse_date(n)
        self.model.complete_name = complete_name
        self._update_view()
        
    
    def _update_view(self, **kwargs):
        self.view.update_view(complete_name_is_ok=True
                             , **kwargs)
        
    def get_lists(self):
        self.uuid = self.person['uuid']
        self.contacts_list = []
        self.get_limited_access_list_data(self.uuid, 0, 10)
        l = self.access_data
        self.contacts_list = []
        self.reset_dates()

        l2 = self.contacts_limited_list[0:10]

        self._update_view(person_name=self.person, access_list_limited=l, contact_list_limited=l2)

    def search_clicked(self, w):
        try:
            self.model.search(self.model)
            complete_name=self.model.complete_name.split()
            name = complete_name[0]
            surname =complete_name[1]
            self.all_persons= self.model.get_users_by_name(name,surname)['users']

            if len(self.all_persons)>1:
                self.view.show_list()
                self.view.repeat_list.clear()
                for i in range(len(self.all_persons)):
                    self.person=self.all_persons[i]
                    self._update_view(name=self.person)
            else:
                self.person=self.all_persons[0]
                name=complete_name[0]
                self.cola(back_in_person_view=self.person)
                self.load_view('person')
                self._update_view(person_name=self.person)

                self.get_lists()

        except requests.ConnectionError as e:
            self.view.show_error('¡Ups! Parece que no se ha podido alcanzar el servidor. Comprueba tu conexión al servidor e inténtalo de nuevo.\n\nInformación del error:\n'+str(e))
            self._update_view(error= True)
        except ValueError as e2:
            self.view.show_error('¡Los datos introducidos no son válidos, o no se ha encontrado nadie a quien corresponda en la base de datos!')
            self._update_view(error= True)
        except Exception as e3:
            self.view.show_error('Error de conexión! Por favor, verifica que el servidor funciona correctamente.')
            self._update_view(error= True)

    def update_treeview(self,w,x,y):
        self.person=self.all_persons[int(x.to_string())]
        self.cola(back_in_person_view=self.person)
        self.load_view('person')
        self._update_view(person_name=self.person)

        self.get_lists()

    def check_server_errors(self, e):
        if isinstance(e, requests.exceptions.ConnectionError):
            self.view.show_error('Error de conexión! Por favor, reinicia la aplicación')
            self._update_view(error=True)
            self.load_view('search')
            return e
        if "error" in e.keys():
            self.view.show_error('Error de conexión! Por favor, reinicia la aplicación')
            self._update_view(error=True)
            self.load_view('search')
            return e
        return e

    def update_buttons(self):
        if self.access_page == True:
            #offset = ((self.access_page_active + 1) * self.access_page_limit)
            #self.get_full_access_list_data(self.uuid, offset, self.access_page_limit)
            #if len(self.full_access_data["access_log"]) <= 0:
            #    self.view.access_next1_btn.set_sensitive(False)
            #else:
            #    self.view.access_next1_btn.set_sensitive(True)
            # offset = ((self.access_page_active + 5) * self.access_page_limit)
            # self.get_full_access_list_data(self.uuid, offset, self.access_page_limit)
            # if len(self.full_access_data["access_log"]) <= 0:
            #     self.view.access_next5_btn.set_sensitive(False)
            # else:
            #     self.view.access_next5_btn.set_sensitive(True)
            pass
        elif self.contacts_page == True:
            offset = ((self.contact_page_active + 1) * self.contact_page_limit)
            if len(self.contacts_list[offset:(offset+self.contact_page_limit)]) <= 0:
                self.view.contact_next1_btn.set_sensitive(False)
            else:
                self.view.contact_next1_btn.set_sensitive(True)
            offset = ((self.contact_page_active + 5) * self.contact_page_limit)
            if len(self.contacts_list[offset:(offset+self.contact_page_limit)]) <= 0:
                self.view.contact_next5_btn.set_sensitive(False)
            else:
                self.view.contact_next5_btn.set_sensitive(True)

    def access_next5_btn_clicked(self, _btn):
        self.access_page_active += 5
        offset = self.access_page_active * self.access_page_limit
        self.get_full_access_list_data(self.uuid, offset, self.access_page_limit)
        self.view.update_view(access_list=self.full_access_data, page=self.access_page_active)
        if len(self.full_access_data['access_log']) > 0:
            self.update_buttons()

    def access_next1_btn_clicked(self, _btn):
        self.access_page_active += 1
        offset = self.access_page_active * self.access_page_limit
        self.get_full_access_list_data(self.uuid, offset, self.access_page_limit)
        self.view.update_view(access_list=self.full_access_data, page=self.access_page_active)
        if len(self.full_access_data['access_log']) > 0:
            self.update_buttons()

    def access_page_btn_clicked(self, _btn):
        self.view.access_page_entry.set_text(
            ''.join([i for i in self.view.access_page_entry.get_text() if i in '0123456789']))
        self.access_page_active = int(self.view.access_page_entry.get_text())
        offset = self.access_page_active * self.access_page_limit
        self.get_full_access_list_data(self.uuid, offset, self.access_page_limit)
        if len(self.full_access_data["access_log"]) <= 0:
            self.get_full_access_list_data(self.uuid, 0, self.access_page_limit)
            self.access_page_active = 0
            self.view.access_page_entry.set_text(f"{self.access_page_active}")
        self.view.update_view(access_list=self.full_access_data, page=self.access_page_active)

        if len(self.full_access_data['access_log']) > 0:
            self.update_buttons()

    def access_back1_btn_clicked(self, _btn):
        self.access_page_active -= 1
        offset = self.access_page_active * self.access_page_limit
        self.get_full_access_list_data(self.uuid, offset, self.access_page_limit)
        self.view.update_view(access_list=self.full_access_data, page=self.access_page_active)
        if len(self.full_access_data['access_log']) > 0:
            self.update_buttons()

    def access_back5_btn_clicked(self, _btn):
        self.access_page_active -= 5
        offset = self.access_page_active * self.access_page_limit
        self.get_full_access_list_data(self.uuid, offset, self.access_page_limit)
        self.view.update_view(access_list=self.full_access_data, page=self.access_page_active)
        if len(self.full_access_data['access_log']) > 0:
            self.update_buttons()

    def format_date(self, date):
        if int(date[1]) <= 9:
            date[1] = f"0{int(date[1] + 1)}"
        if int(date[2]) <= 9:
            date[2] = f"0{date[2]}"
        return date
        
    def calendar_set_btn_clicked(self, _btn):
        s_d = self.view.contact_calendar_start.get_date()
        e_d = self.view.contact_calendar_end.get_date()
        ds_fmtd = json.dumps(datetime(int(s_d[0]), int(s_d[1])+1, int(s_d[2]), 0, 0, 0).isoformat())
        ds2_fmtd = json.dumps(datetime(int(s_d[0]), int(s_d[1]) + 1, int(s_d[2]), 23, 59, 59).isoformat())
        de_fmtd = json.dumps(datetime(int(e_d[0]), int(e_d[1])+1, int(e_d[2]), 23, 59, 59).isoformat())
        self.calendar_start_date=f"{ds_fmtd}+00:000"
        self.calendar_end_date = f"{de_fmtd}+00:000"
        check_date = self.calendar_end_date.split("T")[0].split("-")
        check_date[0] = check_date[0][1:len(check_date[0])]

        y_diff = int(check_date[0]) - int(s_d[0])

        if y_diff < 0:
            self.calendar_end_date = f"{ds2_fmtd}+00:000"
            self.view.contact_calendar_end.select_day(s_d[2])
            self.view.contact_calendar_end.select_month(s_d[1], s_d[0])
        elif y_diff == 0:
            if int(check_date[1]) < (int(s_d[1]) + 1):
                self.calendar_end_date = f"{ds2_fmtd}+00:000"
                self.view.contact_calendar_end.select_day(s_d[2])
                self.view.contact_calendar_end.select_month(s_d[1], s_d[0])
            elif int(check_date[1]) == (int(s_d[1]) + 1) and int(check_date[2]) < (int(s_d[2])):
                self.calendar_end_date = f"{ds2_fmtd}+00:000"
                self.view.contact_calendar_end.select_day(s_d[2])
                self.view.contact_calendar_end.select_month(s_d[1], s_d[0])

        self.contacts_list = []
        self.get_full_contacts_list_data(self.uuid, self.calendar_start_date, self.calendar_end_date)
        self.contacts_list.sort(key=lambda r: r["timestamp"], reverse=True)
        self.access_page_active = 0
        self.view.update_view(contact_list=self.contacts_list, page=self.access_page_active)
        self.update_buttons()

    def contact_next5_btn_clicked(self, _btn):
        self.contact_page_active += 5
        offset = self.contact_page_active * self.contact_page_limit
        self.view.update_view(contact_list=self.contacts_list[offset:(offset+self.contact_page_limit)], page=self.contact_page_active)
        self.update_buttons()

    def contact_next1_btn_clicked(self, _btn):
        self.contact_page_active += 1
        offset = self.contact_page_active * self.contact_page_limit
        self.view.update_view(contact_list=self.contacts_list[offset:(offset+self.contact_page_limit)], page=self.contact_page_active)
        self.update_buttons()

    def contact_page_btn_clicked(self, _btn):
        self.view.contact_page_entry.set_text(
            ''.join([i for i in self.view.contact_page_entry.get_text() if i in '0123456789']))
        self.contact_page_active = int(self.view.contact_page_entry.get_text())
        offset = self.contact_page_active * self.contact_page_limit
        if len(self.contacts_list[offset:(offset+self.contact_page_limit)]) <= 0:
            self.contact_page_active = 0
            self.view.contact_page_entry.set_text(f"{self.contact_page_active}")
            self.view.update_view(contact_list=self.contacts_list[0:self.contact_page_limit],
                                  page=self.contact_page_active)
            self.update_buttons()
        else:
            self.view.update_view(contact_list=self.contacts_list[offset:(offset+self.contact_page_limit)], page=self.contact_page_active)
            self.update_buttons()

    def contact_back1_btn_clicked(self, _btn):
        self.contact_page_active -= 1
        offset = self.contact_page_active * self.contact_page_limit
        self.view.update_view(contact_list=self.contacts_list[offset:(offset+self.contact_page_limit)], page=self.contact_page_active)
        self.update_buttons()

    def contact_back5_btn_clicked(self, _btn):
        self.contact_page_active -= 5
        offset = self.contact_page_active * self.contact_page_limit
        self.view.update_view(contact_list=self.contacts_list[offset:(offset+self.contact_page_limit)], page=self.contact_page_active)
        self.update_buttons()

    def button_date_filter_clicked(self, _btn):
        self.view.toggle_date()
    
    def _get_limited_access_list_data_process(self, uuid, offset, limit) -> None:
        result = self.model.get_user_access_log_by_id_limit(uuid, offset, limit)
        GLib.idle_add(lambda: self.result_access(result))

    def get_limited_access_list_data(self, uuid, offset, limit):
        self.view.toggle_spinner('access', True)
        threading.Thread(target=self._get_limited_access_list_data_process, name="Server Limited Access Thread", args=(uuid, offset, limit), daemon=True).start()

    def result_access(self, answer: dict) -> None:
        self.view.toggle_spinner('access', False)
        if isinstance(answer, Exception):
            self.check_server_errors({"error": answer})
        elif "access_log" in answer.keys():
            self.access_data = answer
            self._update_view(access_list_limited=self.access_data)
        else:
            self.view.show_error(answer)
            self._update_view(error=True)


    def _get_full_access_list_data_process(self, uuid, offset, limit) -> None:
        result = self.model.get_user_access_log_by_id_limit(uuid, offset, limit)
        GLib.idle_add(lambda: self.result_full_access(result))

    def get_full_access_list_data(self, uuid, offset, limit):
        self.view.toggle_spinner('full_access', True)
        self.view.access_next1_btn.set_sensitive(False)
        self.view.access_next5_btn.set_sensitive(False)
        self.view.access_page_btn.set_sensitive(False)
        threading.Thread(target=self._get_full_access_list_data_process, name="Server Access Thread", args=(uuid, offset, limit), daemon=True).start()

    def result_full_access(self, answer: dict) -> None:
        self.view.toggle_spinner('full_access', False)
        self.view.access_page_btn.set_sensitive(True)
        self.view.access_next1_btn.set_sensitive(True)
        self.view.access_next5_btn.set_sensitive(True)
        if isinstance(answer, Exception):
            self.check_server_errors({"error": answer})
        elif "access_log" in answer.keys() or len(answer) == 0:
            self.full_access_data = answer
            if len(self.full_access_data["access_log"]) <= 0 and self.access_page_active > 0:
                self.get_full_access_list_data(self.uuid, 0, self.access_page_limit)
                self.access_page_active = 0
                self.view.access_page_entry.set_text(f"{self.access_page_active}")
            self.view.update_view(access_list=self.full_access_data, page=self.access_page_active)
        else:
            self.view.show_error(answer)
            self._update_view(error=True)

    def _get_full_contacts_list_data_process(self, uuid, start_date, end_date) -> None:
        self.load_contacts_list_data(uuid, start_date, end_date)
        GLib.idle_add(lambda: self.result_full_contacts(self.contacts_list))

    def get_full_contacts_list_data(self, uuid, start_date, end_date):
        self.view.toggle_spinner('contacts', True)
        self.view.toggle_spinner('full_contacts', True)
        self.view.contact_next1_btn.set_sensitive(False)
        self.view.contact_next5_btn.set_sensitive(False)
        self.view.contact_page_btn.set_sensitive(False)
        threading.Thread(target=self._get_full_contacts_list_data_process, name="Server Contacts Thread", args=(uuid, start_date, end_date), daemon=True).start()

    def result_full_contacts(self, answer: dict) -> None:
        self.view.toggle_spinner('full_contacts', False)
        self.view.toggle_spinner('contacts', False)
        self.view.contact_page_btn.set_sensitive(True)
        self.view.contact_next5_btn.set_sensitive(True)
        self.view.contact_next1_btn.set_sensitive(True)

        if isinstance(answer, Exception):
            self.check_server_errors({"error": answer})
        elif len(answer) >= 0:
            if len(self.contacts_limited_list) <= 0:
                self.contacts_limited_list = self.contacts_list[0:10]
                self.view.update_view(contact_list_limited=self.contacts_limited_list)
            self.contacts_page_active = 0
            self.view.update_view(contact_list=self.contacts_list, page=self.contacts_page_active)
            self.update_buttons()
        else:
            self.view.show_error(answer)
            self._update_view(error=True)

    def load_contacts_list_data(self, uuid, start_date, end_date):
        user_data = self.check_server_errors(self.model.get_user_access_log_by_id_datarange(uuid, start_date, end_date))["access_log"]
        user_data.sort(key=lambda r: r["timestamp"], reverse=True)
        e_date = None
        f_id = None
        for data in user_data:
            if f_id == None:
                f_id = data['facility']['id']
            if f_id == data["facility"]["id"] and data["type"] == "OUT":
                e_date = data["timestamp"]
            if f_id == data["facility"]["id"] and data["type"] == "IN":
                s_date = data["timestamp"]
                if e_date == None:
                    e_date = s_date
                self.facilities(uuid, f_id, data['facility']['name'], s_date, e_date)
                f_id = None
                e_date = None
    
    def facilities(self, uuid, f_id, f_name, s_date, e_date):
        facility_data = self.check_server_errors(self.model.get_facility_access_log(f_id, s_date, e_date))["access_log"]
        facility_data.sort(key=lambda r: r["timestamp"], reverse=True)
        for l in facility_data:
            if l['user']['uuid'] != uuid:
                self.contacts_list += [{"timestamp": l["timestamp"], "f_name": f_name,
                              "username": l["user"]["name"], "surname": l["user"]["surname"]}]

    def reset_dates(self):
        self.calendar_start_date = "2020-01-01T00:00:00+00:000"
        self.calendar_end_date = json.dumps(datetime.now().isoformat())
        self.get_full_contacts_list_data(self.uuid, self.calendar_start_date, self.calendar_end_date)
        self.contacts_list.sort(key=lambda r: r["timestamp"], reverse=True)

    def button_expand_access_log_clicked(self, w):
        
        self.access_page_active = 0
        self.access_page_limit = 20
        self.get_full_access_list_data(self.uuid, self.access_page_active, self.access_page_limit)

        self.access_page = True
        self.contacts_page = False

        if len(self.full_access_data['access_log']) > 0:
            self.update_buttons()

        self.load_view('access_log',access_log = self.full_access_data['access_log'])
        self.cola(back_acces=True)

    def button_expand_contacts_clicked(self, w):
        self.contact_page_active = 0
        self.contact_page_limit = 20
        self.contacts_list = []
        self.reset_dates()
        day_month_year = self.calendar_start_date.split("T")[0].split("-")
        self.view.contact_calendar_start.select_day(int(day_month_year[2]))
        self.view.contact_calendar_start.select_month((int(day_month_year[1]) - 1), int(day_month_year[0]))

        day_month_year = self.calendar_end_date.split("T")[0].split("-")
        day_month_year[0] = day_month_year[0][1:len(day_month_year[0])]
        self.calendar_end_date = f"{day_month_year[0]}-{day_month_year[1]}-{day_month_year[2]}T23:59:59+00:000"
        self.view.contact_calendar_end.select_day(int(day_month_year[2]))
        self.view.contact_calendar_end.select_month((int(day_month_year[1]) - 1), int(day_month_year[0]))

        self.access_page = False
        self.contacts_page = True
        self.update_buttons()


        self.load_view('contacts', contacts_log = self.contacts_list[self.contact_page_active:self.contact_page_limit])
        self.cola(back_contact=True)
    #view load functions

    def close_clicked(self, w):
        self.view.close_clicked()
    
    def maximize_clicked(self, w):
        self.view.maximize()
    def minimize_clicked(self, w):
        self.view.minimize()

    def cola(self,**kwargs):
        for name, value in kwargs.items():
            self.back_search_name=[]
            self.back_person=[]
            self.back_search_name.append(name)
            self.back_person.append(value)
            
    def button_home(self,w):
        self.view.rigth_transition
        self.load_view('search')
        self.back_search_name=[]
        self.back_person=[]
        self.view.left_transition

    def button_back(self,w):
        try:
            self.view.rigth_transition
            
            first_element=self.back_search_name.pop(0)
            if (first_element=='back_in_person_view'):
                self.back_search_name.append('back_towards_person')
                self.load_view('search')
                self.view.left_transition
                pass
            elif (first_element=='back_acces'):
                self.back_search_name.append('back_in_person_view')
                self.load_view('person')
                self.view.left_transition
                pass
            elif(first_element=='back_contact'):
                self.back_search_name.append('back_in_person_view')
                self.load_view('person')
                self.view.left_transition
                pass
        except:
            self.load_view('search')        

    def _parse_date(self, s):
        try:
            if len(s.split())>=2:
                return s
        except:
                return None
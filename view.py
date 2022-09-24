#!/usr/bin/env python3
from io import BytesIO
import qrcode
import locale
import gettext
import os
import datetime
_ = gettext.gettext
N_ = gettext.ngettext


import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GdkPixbuf

class view:
    
    @classmethod
    def main(cls):
        Gtk.main()

    @classmethod
    def main_quit(cls, w, e):
        Gtk.main_quit()
    
 
    def timestamp2datetime(self, timestamp):
        # timestamp = "2021-09-01T13:43:01.277923+00:00"
        yyyy = timestamp[0:4]
        mm = timestamp[5:7]
        dd = timestamp[8:10]
        hhmm = timestamp[11:16]
        datetime = dd+"/"+mm+"/"+yyyy+" "+hhmm 
        return datetime


    def build_view(self):
        builder = Gtk.Builder()
        builder.add_from_file("ipm-p1.glade")
        self.dialog_popup = builder.get_object("dialog_popup")
        self.button_close_dialog = builder.get_object("button_close_dialog")
        self.win = builder.get_object("main_app")
        self.win.set_title('CovidTracker')
        self.complete_name = builder.get_object("entry_search_term")
        
        self.repeat_list_treeview=builder.get_object("Tree")
        self.repeat_list=builder.get_object("repeat_list_name")

        str_renderer = Gtk.CellRendererText()
        str_column = Gtk.TreeViewColumn("Sugerencias", str_renderer, text=0)
        self.repeat_list_treeview.append_column(str_column)
        
        self.search = builder.get_object("button_search")

        self.button_maximize=builder.get_object("button_maximize")
        self.button_minimize=builder.get_object("button_minimize")
        self.button_close_clicked=builder.get_object("button_close")

        self.home=builder.get_object("button_home")
        self.back=builder.get_object("button_back")

        
        
        
        
        #view stack
        self.stack = builder.get_object("stack")
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT)
        self.label_info_title = builder.get_object("label_info_title")

        self.personView = builder.get_object("view_person")
        self.searchView= builder.get_object("view_search")
        self.access_log_view = builder.get_object("view_access_log")
        self.contacts_view = builder.get_object("view_contacts")
        #person view
        
        self.label_qr_text= builder.get_object("label_qr_text")
        self.label_name=builder.get_object("label_name")
        self.label_surname=builder.get_object("label_surname")
        self.label_username=builder.get_object("label_username")
        self.label_email=builder.get_object("label_email")
        self.label_phone=builder.get_object("label_phone")
        self.label_is_vaccinated=builder.get_object("label_is_vaccinated")
        self.qr_image=builder.get_object("qr_image")
        self.button_expand_access_log = builder.get_object("button_expand_access_log")
        self.button_expand_contacts = builder.get_object("button_expand_contacts")
        self.spinner_access = builder.get_object("spinner_access")
        self.spinner_contacts = builder.get_object("spinner_contacts")
        
        #access view
        self.access_treeview = builder.get_object("access_treeview")
        self.access_list = builder.get_object("access_list")

        self.full_access_treeview = builder.get_object("full_access_treeview")
        self.full_access_list = builder.get_object("full_access_list")
        self.access_control_panel = builder.get_object("access_control_panel")

        self.access_back5_btn = builder.get_object("access_back5_btn")

        self.access_back1_btn = builder.get_object("access_back1_btn")

        self.access_page_entry = builder.get_object("access_page_entry")

        self.access_page_btn = builder.get_object("access_page_btn")

        self.access_next1_btn = builder.get_object("access_next1_btn")

        self.access_next5_btn = builder.get_object("access_next5_btn")

        self.spinner_full_access = builder.get_object("spinner_full_access")

        # contact view
        self.contact_treeview = builder.get_object("contact_treeview")
        self.contact_list = builder.get_object("contact_list")

        self.full_contact_treeview = builder.get_object("full_contact_treeview")
        self.full_contact_list = builder.get_object("full_contact_list")
        self.calendar_set_btn = builder.get_object("calendar_set_btn")
        self.contact_calendar_start = builder.get_object("contact_calendar_start")
        self.contact_calendar_end = builder.get_object("contact_calendar_end")
        self.button_show_date_filter = builder.get_object("button_show_date_filter")
        self.box_date_controls = builder.get_object("box_date_controls")
        self.contact_control_panel = builder.get_object("contact_control_panel")

        self.contact_back5_btn = builder.get_object("contact_back5_btn")

        self.contact_back1_btn = builder.get_object("contact_back1_btn")

        self.contact_page_entry = builder.get_object("contact_page_entry")

        self.contact_page_btn = builder.get_object("contact_page_btn")

        self.contact_next1_btn = builder.get_object("contact_next1_btn")

        self.contact_next5_btn = builder.get_object("contact_next5_btn")

        self.spinner_full_contacts = builder.get_object("spinner_full_contacts")


        #access list from person view
        str_renderer = Gtk.CellRendererText()
        str_column = Gtk.TreeViewColumn("Temperatura", str_renderer, text=0)
        self.access_treeview.append_column(str_column)
        str_renderer = Gtk.CellRendererText()
        str_column = Gtk.TreeViewColumn("Fecha/Hora", str_renderer, text=1)
        self.access_treeview.append_column(str_column)
        str_renderer = Gtk.CellRendererText()
        str_column = Gtk.TreeViewColumn("Tipo", str_renderer, text=2)
        self.access_treeview.append_column(str_column)
        str_renderer = Gtk.CellRendererText()
        str_column = Gtk.TreeViewColumn("Instalación", str_renderer, text=3)
        self.access_treeview.append_column(str_column)
        #full access list from access view

        str_renderer = Gtk.CellRendererText()
        str_column = Gtk.TreeViewColumn("Temperatura", str_renderer, text=0)
        self.full_access_treeview.append_column(str_column)
        str_renderer = Gtk.CellRendererText()
        str_column = Gtk.TreeViewColumn("Fecha/Hora", str_renderer, text=1)
        self.full_access_treeview.append_column(str_column)
        str_renderer = Gtk.CellRendererText()
        str_column = Gtk.TreeViewColumn("Tipo", str_renderer, text=2)
        self.full_access_treeview.append_column(str_column)
        str_renderer = Gtk.CellRendererText()
        str_column = Gtk.TreeViewColumn("Instalación", str_renderer, text=3)
        self.full_access_treeview.append_column(str_column)

        #Contacts
        str_column = Gtk.TreeViewColumn("Fecha/Hora", str_renderer, text=0)
        self.contact_treeview.append_column(str_column)
        str_renderer = Gtk.CellRendererText()
        str_column = Gtk.TreeViewColumn("Instalación", str_renderer, text=1)
        self.contact_treeview.append_column(str_column)
        str_renderer = Gtk.CellRendererText()
        str_column = Gtk.TreeViewColumn("Usuario", str_renderer, text=2)
        self.contact_treeview.append_column(str_column)
        str_renderer = Gtk.CellRendererText()
        str_column = Gtk.TreeViewColumn("Apellidos", str_renderer, text=3)
        self.contact_treeview.append_column(str_column)

        str_column = Gtk.TreeViewColumn("Fecha/Hora", str_renderer, text=0)
        self.full_contact_treeview.append_column(str_column)
        str_renderer = Gtk.CellRendererText()
        str_column = Gtk.TreeViewColumn("Instalación", str_renderer, text=1)
        self.full_contact_treeview.append_column(str_column)
        str_renderer = Gtk.CellRendererText()
        str_column = Gtk.TreeViewColumn("Usuario", str_renderer, text=2)
        self.full_contact_treeview.append_column(str_column)
        str_renderer = Gtk.CellRendererText()
        str_column = Gtk.TreeViewColumn("Apellidos", str_renderer, text=3)
        self.full_contact_treeview.append_column(str_column)


        self.win.show_all()
    
    def maximize(self):
        self.win.maximize()
    def minimize(self):
        self.win.iconify()
    def close_clicked(self):
        Gtk.main_quit()
    # Access
    def connect_access_back5_btn_clicked(self, fun):
        self.access_back5_btn.connect('clicked', fun)

    def connect_access_back1_btn_clicked(self, fun):
        self.access_back1_btn.connect('clicked', fun)

    def connect_access_page_btn_clicked(self, fun):
        self.access_page_btn.connect('clicked', fun)

    def connect_access_next5_btn_clicked(self, fun):
        self.access_next5_btn.connect('clicked', fun)

    def connect_access_next1_btn_clicked(self, fun):
        self.access_next1_btn.connect('clicked', fun)

    # Contact
    def connect_contact_back5_btn_clicked(self, fun):
        self.contact_back5_btn.connect('clicked', fun)

    def connect_contact_back1_btn_clicked(self, fun):
        self.contact_back1_btn.connect('clicked', fun)

    def connect_contact_page_btn_clicked(self, fun):
        self.contact_page_btn.connect('clicked', fun)

    def connect_contact_next5_btn_clicked(self, fun):
        self.contact_next5_btn.connect('clicked', fun)

    def connect_contact_next1_btn_clicked(self, fun):
        self.contact_next1_btn.connect('clicked', fun)

    def connect_calendar_set_btn_clicked(self, fun):
        self.calendar_set_btn.connect('clicked', fun)
    
    def connect_button_show_date_filter(self, fun):
        self.button_show_date_filter.connect('clicked',fun)
    
    def toggle_date(self):
        if(self.box_date_controls.get_visible()):
            self.box_date_controls.set_visible(False)
        else:
            self.box_date_controls.set_visible(True)

    def show_all(self):
        self.win.show_all()
    def connect_button_close_dialog(self, fun):
        self.button_close_dialog.connect('clicked',fun)

    def close_dialog(self):
        self.dialog_popup.set_markup("Error desconocido")
        self.dialog_popup.hide()

    def open_dialog(self):
        self.dialog_popup.show()
    def hide_list(self):
        self.repeat_list_treeview.hide()

    def show_list(self):
        self.repeat_list_treeview.show()

    def connect_delete_event(self, fun):
        self.win.connect('delete-event', fun)

    def connect_complete_name_changed(self, fun):
        self.complete_name.connect('changed', fun)


    def connect_search_clicked(self, fun):
        self.search.connect('clicked', fun)

    def connect_treeview(self,fun):
        self.repeat_list_treeview.connect('row-activated',fun)
    
    def connect_name_label_button(self,fun):
        self.repeat_name.connect('clicked', fun)

    def connect_close_clicked(self, fun):
        self.button_close_clicked.connect('clicked', fun)

    def connect_maximize_clicked(self, fun):
        self.button_maximize.connect('clicked',fun)
    
    def connect_minimize_clicked(self, fun):
        self.button_minimize.connect('clicked',fun)

    def connect_button_home(self,fun):
        self.home.connect("clicked",fun)
    
    def connect_button_back(self,fun):
        self.back.connect('clicked',fun)

    def connect_button_expand_access_log(self, fun):
        self.button_expand_access_log.connect('clicked', fun)
    def connect_button_expand_contacts(self, fun):
        self.button_expand_contacts.connect('clicked', fun)
    def load_search_view(self):
        self.stack.set_visible_child(self.searchView)
        self.label_info_title.set_text('')
    def load_person_view(self, **kwargs):

        #access_data = kwargs
        self.win.set_title('CovidTracker — Información personal')
        self.stack.set_visible_child(self.personView)

    def load_access_log_view(self, **kwargs):
        
        access_data = kwargs
        self.win.set_title('CovidTracker — Accesos recientes')
        self.access_page_active = 0
        self.access_page_limit = 20
        self.update_view(access_list=access_data, page=self.access_page_active)
        self.stack.set_visible_child(self.access_log_view)
    
    def load_contacts_view(self, **kwargs):
        contacts_data = kwargs
        self.win.set_title('CovidTracker — Contactos recientes')
        self.contact_page_active = 0
        self.contact_page_limit = 20
        self.update_view(contact_list=contacts_data["contacts_log"], page=self.contact_page_active)
        self.stack.set_visible_child(self.contacts_view)

    def toggle_spinner(self, spinner_name, show: bool):
        if spinner_name == 'access':
            if show:
                self.spinner_access.start()
                self.access_treeview.hide()
            else:
                self.spinner_access.stop()
                self.access_treeview.show()
        elif spinner_name == 'contacts':
            if show:
                self.spinner_contacts.start()
                self.contact_treeview.hide()
            else:
                self.spinner_contacts.stop()
                self.contact_treeview.show()
        elif spinner_name == 'full_access':
            if show:
                self.spinner_full_access.start()
                self.full_access_treeview.hide()
            else:
                self.spinner_full_access.stop()
                self.full_access_treeview.show()
        elif spinner_name == 'full_contacts':
            if show:
                self.spinner_full_contacts.start()
                self.full_contact_treeview.hide()
            else:
                self.spinner_full_contacts.stop()
                self.full_contact_treeview.show()

    def load_view(self, view_name, **kwargs):
        if view_name == 'search':
            self.load_search_view()
        elif view_name == 'person':
            self.load_person_view(**kwargs)
        elif view_name == 'access_log':
            self.load_access_log_view(**kwargs)
        elif view_name == 'contacts':
            self.box_date_controls.set_visible(False)
            self.load_contacts_view(**kwargs)
 
    def update_view(self, **kwargs):
        for name, value in kwargs.items():
            if name =='name':
                self.repeat_list.append([f"{value['username']}     {value['phone']}"])
            elif name=='complete_name':
                 self.complete_name.set_text(value)
            elif name == 'complete_name_is_ok':
                self._update_entry_is_valid(self.complete_name, value)
            elif name == 'error':
                self._update_entry_is_valid(self.complete_name, not value)
            elif name =='person_name':
                self.label_name.set_text(value['name'])
                self.label_surname.set_text(value['surname'])
                self.label_username.set_text(value['username'])
                self.label_email.set_text(value['email'])
                self.label_phone.set_text(value['phone'])
                if (value['is_vaccinated'])==True:
                    self.label_is_vaccinated.set_text("Sí")
                else:
                    self.label_is_vaccinated.set_text("No")
                
                
                #QR CODEEEEE
                qr_code_string = '{'+value['name']+'},{'+value['surname']+'},{'+value['uuid']+'}'
                im = qrcode.make(qr_code_string)
                image_size = (150,150)
                im = im.resize(image_size)
                
                im.save("resources/qr.png")

                if(os.path.isfile("resources/qr.png")):
                    self.qr_image.set_from_file("resources/qr.png")
                    os.remove("resources/qr.png")
                

                #qr code text
                self.label_qr_text.set_text('Identificador QR: '+qr_code_string)
            
            elif name == 'access_list_limited':
                self.access_list.clear()
                for l in value['access_log']:
                    self.access_list.append([l['temperature'], self.timestamp2datetime(l['timestamp']), l['type'], l['facility']['name']])
            elif name == 'access_list':
                self.full_access_list.clear()
                for l in value['access_log']:
                    self.full_access_list.append([l['temperature'], self.timestamp2datetime(l['timestamp']), l['type'], l['facility']['name']])
            elif name == 'contact_list_limited':
                self.contact_list.clear()
                for l in value:
                    self.contact_list.append([self.timestamp2datetime(l['timestamp']), l['f_name'], l['username'], l['surname']])
            elif name == 'contact_list':
                self.full_contact_list.clear()
                for l in value:
                    self.full_contact_list.append([f"{self.timestamp2datetime(l['timestamp'])}", f"{l['f_name']}", f"{l['username']}", f"{l['surname']}"])
            elif name == 'page':
                self.access_page_entry.set_text(f"{value+1}")
                self.contact_page_entry.set_text(f"{value+1}")
                if value == 0:
                    self.access_back5_btn.set_sensitive(False)
                    self.access_back1_btn.set_sensitive(False)
                    self.contact_back5_btn.set_sensitive(False)
                    self.contact_back1_btn.set_sensitive(False)
                if value >= 5:
                    self.access_back5_btn.set_sensitive(True)
                    self.contact_back5_btn.set_sensitive(True)
                if value >= 1:
                    self.access_back1_btn.set_sensitive(True)
                    self.contact_back1_btn.set_sensitive(True)
            else:
                raise TypeError(f"update_view() got an unexpected keyword argument '{name}'")

    def rigth_transition(self):
        self.view.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_RIGHT)
        

    def left_transition(self):
        self.view.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT)
        
    
    def _update_entry_is_valid(self, entry, is_valid):
            if is_valid:
                entry.get_style_context().remove_class('error')
            else:
                entry.get_style_context().add_class('error')
            

    def show_ok(self, text):
        dialog = Gtk.MessageDialog(parent= self.win,
                                   message_type= Gtk.MessageType.INFO,
                                   buttons= Gtk.ButtonsType.OK,
                                   text= text)
        dialog.run()
        dialog.destroy()

    def show_error(self, text):
        # dialog = Gtk.MessageDialog(parent= self.win,
        #                            message_type= Gtk.MessageType.ERROR,
        #                            buttons= Gtk.ButtonsType.CLOSE,
        #                            text= text)
        # dialog.run()
        # dialog.destroy()
        self.dialog_popup.set_markup(text)
        self.open_dialog()

from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.screen import Screen
from kivymd.uix.button import MDRectangleFlatButton, MDIconButton
from kivymd.uix.textfield import MDTextField
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.checkbox import CheckBox
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
import smtplib, re, requests, json, time
from bs4 import BeautifulSoup
from kivy.uix.button import Button
from kivy.clock import Clock


toolbar_helper = '''
Screen:
    BoxLayout:
        orientation: "vertical"

        MDToolbar:
            title: "LineSkip"
            elevation: 17
            right_action_items: [["feature-search", lambda x: app.callback(x)]]


        MDLabel:
            text: ""
'''

email_field = """
    
MDTextField:
    hint_text: "Fill mode"
    mode: "fill"
    fill_color: 0, 0, 0, .4
    id: Email
    hint_text: "Enter email"
    helper_text: "alert when an appointment is available"
    helper_text_mode: "on_focus"
    pos_hint: {"center_y": .75, "center_x":0.5}
    size_hint_x: None
    width: 250
            
"""

image_helper = """
Image:
    source: "MVC-logo.png"
    pos_hint: {"center_x":0.2,"center_y":0.6}
    size_hint: (0.2,0.2)


"""


class LineSkipApp(MDApp):

    def build(self):
        global timer
        timer = 1
        self.rows_chosen = []# THIOS
        self.choosing = ""
        self.mvc_names = []
        self.user_email = ""
        self.mvc_links = ["https://telegov.njportal.com/njmvc/AppointmentWizard/15", "https://telegov.njportal.com/njmvc/AppointmentWizard/14", "https://telegov.njportal.com/njmvc/AppointmentWizard/12", "https://telegov.njportal.com/njmvc/AppointmentWizard/16", "https://telegov.njportal.com/njmvc/AppointmentWizard/17", "https://telegov.njportal.com/njmvc/AppointmentWizard/11", "https://telegov.njportal.com/njmvc/AppointmentWizard/6", "https://telegov.njportal.com/njmvc/AppointmentWizard/7"]
        self.mvc_names = ["Bakers Basin", "Bayonne", "Camden", "Cardiff", "Delanco", "Eatontown", "Edison", "Flemington", "Freehold", "Lodi", "Newark", "North Bergen", "Oakland", "Paterson", "Rahway", "Randolph", "Rio Grande", "Salem", "South Plainfield", "Toms River", "Vineland", "Wayne", "West Deptford"]
        self.run_stop = True
        self.data_tables = MDDataTable(
            pos_hint={"center_x":0.5,"center_y":0.4},
            rows_num = 23,
            #use_pagination=True,
            pagination_menu_height = "140dp",
            check=True,
            column_data=[
                ("MVC", dp(30)),
                ("ID", dp(30)),

            ],
            row_data = [
            ("Bakers Basin", "300"),
            ("Bayonne", "150"),
            ("Camden","150"),
            ("Cardiff","5"),
            ("Delanco","3"),
            ("Eatontown","3"),
            ("Edison","30"),
            ("Flemington","3"),
            ("Freehold","3"),
            ("Lodi","3"),
            ("Newark","3"),
            ("North Bergen","3"),
            ("Oakland","3"),
            ("Paterson","3"),
            ("Rahway","3"),
            ("Randolph","3"),
            ("Rio Grande","3"),
            ("Salem","3"),
            ("South Plainfield","3"),
            ("Toms River","3"),
            ("Vineland","3"),
            ("Wayne","3"),
            ("West Deptford","3")
            ]
        )

        screen = MDScreen()
        self.data_tables.bind(on_check_press=self.on_check_press)
        self.data_tables.size_hint=(0.9, 0.55)
        screen.add_widget(self.data_tables)

        self.theme_cls.primary_palette = "Teal"

        toolbar = Builder.load_string(toolbar_helper)
        screen.add_widget(toolbar)

        self.email = Builder.load_string(email_field)
        screen.add_widget(self.email)

        images = Builder.load_string(image_helper)
        screen.add_widget(images)
        

        btn_flat_start = MDRectangleFlatButton(text="Start", pos_hint={"center_x":0.3,"center_y":0.07}, on_release=self.button_start)
        screen.add_widget(btn_flat_start)

        btn_flat_stop = MDRectangleFlatButton(text="Stop", pos_hint={"center_x":0.7,"center_y":0.07}, on_release=self.button_stop)
        screen.add_widget(btn_flat_stop)


        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": "Initial Permit",
                "height": dp(50),
                "on_release": lambda x="Initial Permit Pressed": self.menu_callback(x)
             }, 
             {
                "viewclass": "OneLineListItem",
                "text": "CDL Permit or Edorsement",
                "height": dp(50),
                "on_release": lambda x="CDL Permit or Edorsement Pressed": self.menu_callback(x)
             }, 
             {
                "viewclass": "OneLineListItem",
                "text": "Real ID",
                "height": dp(50),
                "on_release": lambda x="Real ID Pressed": self.menu_callback(x)
             }, 
             {
                "viewclass": "OneLineListItem",
                "text": "Non-Driver ID",
                "height": dp(50),
                "on_release": lambda x="Non-Driver ID Pressed": self.menu_callback(x)
             }, 
             {
                "viewclass": "OneLineListItem",
                "text": "Knowledge Testing",
                "height": dp(50),
                "on_release": lambda x="Knowledge Testing Pressed": self.menu_callback(x)
             }, 
             {
                "viewclass": "OneLineListItem",
                "text": "Renewal:License or Non-Driver ID",
                "height": dp(50),
                "on_release": lambda x="Renewal:License or Non-Driver ID Pressed": self.menu_callback(x)
             }, 
             {
                "viewclass": "OneLineListItem",
                "text": "Renewal CDL",
                "height": dp(50),
                "on_release": lambda x="Renewal CDL Pressed": self.menu_callback(x)
             }, 
             {
                "viewclass": "OneLineListItem",
                "text": "Transfer from out of state",
                "height": dp(50),
                "on_release": lambda x="Transfer from out of state Pressed": self.menu_callback(x)
             }
        ]
        self.menu = MDDropdownMenu(
            items=menu_items,
            width_mult=4,
        )
        return screen


    def callback(self, button):
        self.menu.caller = button
        self.menu.open()

    def menu_callback(self, text_item):
        self.menu.dismiss()
        Snackbar(text=text_item).open()
        print(text_item)
        index = text_item.index(" Pressed")
        text_item = text_item[:index]
        self.choosing = text_item


    def on_check_press(self, instance_table, current_row):
        checked_name = current_row[0]
        print(checked_name)
        self.add_row_checks(checked_name) # NAME

    def button_start(self, obj):
        Snackbar(text="Searching Started!").open()
        Clock.schedule_interval(self.start_skipping,10)

    def button_stop(self, obj):
        Snackbar(text="Searching Stopped!").open()
        Clock.unschedule(self.start_skipping)


    def start_skipping(self, obj):

        self.user_email = self.email.text
        self.rows = self.rows_chosen
        self.new_rows = []
        for row in self.rows:
            self.new_rows.append(row[0])
        self.ready = True
        if self.user_email == "" or "@" not in self.user_email:
            dialog = MDDialog(text="Please enter a valid email!")
            dialog.open()
            self.ready = False
        if len(self.new_rows) == 0:
            dialog = MDDialog(text="Please add some MVC choices to check!")
            dialog.open()
            self.ready = False
        if self.choosing == "":
            dialog = MDDialog(text="Please add what you want to check at the top right!")
            dialog.open()
            self.ready = False
        if self.ready:
            print(f"Email: {self.user_email}")
            print(f"MVCs Chosen: {self.new_rows}")
            print(f"Chosen Reason: {self.choosing}")
            print(self.convertAnswerToNumber(self.choosing))
            print(f"Indicies: {self.convertToIntChoices()}")
            


            self.welcomeScreen()
            self.IsSpecifiedRequestAvailable()

    def welcomeScreen(self):
        self.run_stop = True
        self.user_answer = self.convertAnswerToNumber(self.choosing)
        self.user_email = self.user_email
        self.user_mvc_choices = self.convertToIntChoices()

    
    def space():
        print()

    def convertToIntChoices(self):
        indicies = []
        for choice in self.new_rows:
            index = 0
            for mvc in self.mvc_names:
                if choice == mvc:
                    indicies.append(index)
                index += 1

        return indicies

    def add_row_checks(self, checked_name):
        if checked_name in self.rows_chosen:
            self.rows_chosen.remove(checked_name)
        else:
            self.rows_chosen.append(checked_name)

        print(self.rows_chosen)



    def convertAnswerToNumber(self, field):
        switcher = {
            "Initial Permit" : 0,
            "CDL Permit or Edorsement" : 1,
            "Real ID" : 2,
            "Non-Driver ID" : 3,
            "Knowledge Testing" : 4,
            "Renewal:License or Non-Driver ID": 5,
            "Renewal CDL" : 6,
            "Transfer from out of state" : 7
        }
        return switcher[field]


    def sendEmail(self,text): # remember to add a field when sending
            smtp_object = smtplib.SMTP("smtp.gmail.com", 587)
            smtp_object.ehlo()
            smtp_object.starttls()
            email = "smtplibthrowaway@gmail.com"
            password = "Test!234"
            smtp_object.login(email, password)
            from_address = email
            to_address = self.user_email
            Subject = "NEW APPOINTMENT NOTICE"
            message = text
            msg = "Subject: " + Subject + "\n\n" + message
            smtp_object.sendmail(from_address, to_address, msg)
            smtp_object.quit()



    def IsSpecifiedRequestAvailable(self):
        # Get Request from site
        headers = {
            'authority' : 'telegov.njportal.com',
            'method' : 'GET',
            'accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-ch-ua' : '"Chromium";v="92", " Not A;Brand";v="99", "Microsoft Edge";v="92"',
            'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36 Edg/92.0.902.78'
        }
        permit_website_request = requests.get(self.mvc_links[self.convertAnswerToNumber(self.choosing)], headers=headers)
        soup = BeautifulSoup(permit_website_request.text, 'lxml')
        # Turn the variables into a JSON to parse through
        regex_locationData = re.compile("var\s*locationData\s*=\s*\[(.*)]")
        regex_timeData = re.compile("var\s*timeData\s*=\s*\[(.*)]")

        locationData = regex_locationData.search(str(soup))
        timeData = regex_timeData.search(str(soup))

        json_locationData = json.loads(str(soup)[locationData.start() + 19 :locationData.end()])
        json_timeData = json.loads(str(soup)[timeData.start() + 15 :timeData.end()])

        location_names = []
        location_names_ids = []

        timeData_ids = []
        timeData_appointment_status = []
        # Append the necessary info
        for block in json_locationData:
            location_names.append(block["Name"])
            location_names_ids.append((block["LocAppointments"][0])["LocationId"])

        for block in json_timeData:
            timeData_ids.append(block["LocationId"])
            timeData_appointment_status.append(block["FirstOpenSlot"])

        if len(location_names) == len(timeData_ids):
            mvc_info = []
            index = 0
            for id in range(0, len(location_names)):
                msg = "NAME: " + str(location_names[id]) + "\nMVC ID: " + str(location_names_ids[id])
                for i in range(0, len(location_names)):
                    if int(location_names_ids[id]) == int(timeData_ids[i]):
                        index = i
                        break
                if str(timeData_appointment_status[index]) != "No Appointments Available":
                    msg += "\nTIMEDATA ID: " + str(timeData_ids[index]) + "\nAPPOINTMENT STATUS: " + str(timeData_appointment_status[index]).split(" <br/> ")[0] + "\n" + str(timeData_appointment_status[index]).split(" <br/> ")[1].upper() + "\nLINK: " + self.mvc_links[self.convertAnswerToNumber(self.choosing)] + "/" + str(timeData_ids[index])
                else:
                    msg += "\nTIMEDATA ID: " + str(timeData_ids[index]) + "\nAPPOINTMENT STATUS: " + str(timeData_appointment_status[index]) + "\nLINK: " + self.mvc_links[self.convertAnswerToNumber(self.choosing)] + "/" + str(timeData_ids[index])
                mvc_info.append(msg)
        approved = 0
        approved_block = []
        for mvc in mvc_info:
            for chosen_mvc in self.rows_chosen: # this one
                if chosen_mvc in mvc:
                    print(mvc)
                    space()
                if chosen_mvc in mvc and "No Appointments Available" not in mvc:
                    approved_block.append(mvc)
                    approved += 1 
        if approved > 0:
            global timer
            print(f"{approved} APPS AVAILABLE----------------------------\n")
            for app in approved_block:
                print(app)
                space()
            for approved in approved_block:
                self.sendEmail(approved)
                Snackbar(text="Found Match : Check Email").open()

            print(f"------------------------{timer}-------------------------")
            timer += 1
            self.run_stop = False
            
        else:
            print("No Apps Available : Try again")
            Snackbar(text="No Apps Available : Try again").open()

            space()
            print(f"------------------------{timer}-------------------------")
            timer += 1
            space()



def space():
    print()

LineSkipApp().run()
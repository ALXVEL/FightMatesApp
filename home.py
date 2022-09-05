from kivy.uix.scrollview import ScrollView
from kivymd.app import MDApp
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.label import Label
from kivy.clock import Clock
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.card import MDCard
from kivy.lang import Builder
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.list import OneLineListItem, OneLineAvatarIconListItem, ThreeLineAvatarIconListItem
from kivymd.font_definitions import theme_font_styles
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.list import IRightBodyTouch
import socket
import pickle

import events as e
from kivy.uix.screenmanager import ScreenManager, Screen

Window.size = (360,600)

#
# kv = '''
# <ItemConfirm>
#
# ScrollView:
#     size_hint: 1,0.5
#     MDSelectionList:
#         id: scorecard
#         OneLineListItem:
#             text: "test"
#             MDCheckbox:
#                 size_hint: None, None
#                 size: "48dp", "48dp"
#                 pos_hint: {'center_x': 0.9, 'center_y': .5}
# '''



class ListItemWithCheckbox(OneLineAvatarIconListItem):
    def on_checkbox_active(self, checkbox, value):
        if value:
            print('The checkbox', checkbox, 'is active', 'and', checkbox.state, 'state')
            for key in fight_list_dict.keys():
                if key in checkbox.listItem.text:
                    fight_list_dict[key] = True
        else:
            print('The checkbox', checkbox, 'is inactive', 'and', checkbox.state, 'state')
            for key in fight_list_dict.keys():
                if key in checkbox.listItem.text:
                    fight_list_dict[key] = False

class ItemConfirm(OneLineAvatarIconListItem):
    divider = None

fightList1 = e.events.get_current_event_fights(None)
fight_list_dict = {}
for i in range(0, len(fightList1)):
    fight_list_dict[fightList1[i][0]] = False
    fight_list_dict[fightList1[i][1]] = False

print(fight_list_dict)

class MainLayout(Screen):
    upcoming = StringProperty()
    date = StringProperty()
    # first_kv = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.create_list)
        print(e.events.get_upcoming_events(None)[0][0])
        self.upcoming = e.events.get_current_event(None)[0] + '\n' + e.events.get_current_event(None)[2]
        self.date = e.events.get_current_event(None)[1]
        # self.first_kv = str(Builder.load_string(kv))
    def create_list(self, *args):
        fightList = e.events.get_current_event_fights(None)
        for i in range (0, len(fightList)):
            s = '[color=#1a1720][b]' + fightList[i][0] + ' vs. ' + fightList[i][1] +'[/b]'+ ' \n ' + '[color=#303956]' + fightList[i][2] + '[color=#303956]'
            self.ids.events1.add_widget(Label(text=s , markup=True, halign="center", height='75px', padding=[200,200]))
    def prediction_dialog(self):
        fightList1 = e.events.get_current_event_fights(None)
        list_of_items = []
        print(len(fightList1))
        for i in range (0, len(fightList1)):
            str1 = '[color=#1a1720]' + fightList1[i][0] + '[color=#1a1720]'
            str2 = '[color=#1a1720]' + fightList1[i][1] + '[color=#1a1720]'
            item1 = ListItemWithCheckbox(text=str1,font_style='Body2')
            item2 = ListItemWithCheckbox(text=str2,font_style='Body2')
            item3 = ItemConfirm(text='       ')
            list_of_items.append(item1)
            list_of_items.append(item2)
            list_of_items.append(item3)
        close_button = MDFlatButton(text='Close', on_release=self.close_dialog)
        save_button = MDRaisedButton(text='Save', on_release=self.save_prediction)

        self.dialog = MDDialog(title='Scorecard', type="confirmation" ,buttons=[close_button, save_button], items=list_of_items)

        self.dialog.open()

    def save_prediction(self, obj):
        print(fight_list_dict)
        self.dialog.dismiss()

    def close_dialog(self,obj):
        self.dialog.dismiss()

class SecondScreen(Screen):
    def __init__(self, **kwargs):
        super(SecondScreen,self).__init__(**kwargs)
        Clock.schedule_once(self.create_widget)

    def create_widget(self,*args):
        title =  e.events.get_current_event(None)[0]
        self.ids.myp.add_widget(ItemConfirm(text=title, bg_color=[0,1,1,1], on_release=self.p_dialog))

    def p_dialog(self,obj):
        fightList_p = e.events.get_current_event_fights(None)
        list_of_items = []
        print(len(fightList_p))
        for i in range(0, len(fightList_p)):
            str1 = '[color=#1a1720]' + fightList_p[i][0] + '[color=#1a1720]'
            str2 = '[color=#1a1720]' + fightList_p[i][1] + '[color=#1a1720]'
            if fight_list_dict[fightList1[i][0]]:
                item1 = ItemConfirm(text=str1, font_style='Body2', bg_color=[0,1,1,1])
                item2 = ItemConfirm(text=str2, font_style='Body2')
            elif fight_list_dict[fightList1[i][1]]:
                item2 = ItemConfirm(text=str2, font_style='Body2', bg_color=[0, 1, 1, 1])
                item1 = ItemConfirm(text=str1, font_style='Body2')
            else:
                item1 = ItemConfirm(text=str1, font_style='Body2')
                item2 = ItemConfirm(text=str2, font_style='Body2')
            item3 = ItemConfirm(text='       ')
            list_of_items.append(item1)
            list_of_items.append(item2)
            list_of_items.append(item3)
        close_button = MDFlatButton(text='Close', on_release=self.p_close_dialog)

        self.dialog1 = MDDialog(title='My Predictions', type="confirmation", buttons=[close_button],
                               items=list_of_items)

        self.dialog1.open()

    def p_close_dialog(self,obj):
        self.dialog1.dismiss()

class HomePage(MDApp):
    def build(self):
        av = Builder.load_file('homepage.kv')
        self.theme_cls.theme_style = "Light"
        return av

    def change_screen(self):
        self.root.current = 'second'

    def home_screen(self):
        self.root.current = 'main'

HomePage().run()


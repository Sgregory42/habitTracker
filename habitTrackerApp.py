from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.gridlayout import GridLayout

from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color, Line

from random import random
from datetime import date, timedelta, datetime

from functools import partial

import calendar
from kivy.clock import Clock
from kivy.uix.screenmanager import NoTransition, ScreenManager, Screen
from kivy.properties import StringProperty, NumericProperty, ListProperty, ObjectProperty
from kivy.uix.behaviors import ToggleButtonBehavior

from kivy.event import EventDispatcher
from kivy.core.window import Window
from kivy.uix.checkbox import CheckBox

# Window.left = -1000
Window.top = 50
Window.size = (800,600)
Window.clearcolor = (1, 1, 1, 1)

class DatePicker(BoxLayout):
    chosenColor = [1,1,1,1]
    date = date.today()

    def __init__(self, *args, **kwargs):
        super(DatePicker, self).__init__(**kwargs)
        if MyBoxLayout.theEverywhereDate == '':
            self.date = date.today()
        else:
            self.date = datetime.strptime(str(MyBoxLayout.theEverywhereDate),'%Y-%m-%d').date()

        self.orientation = "vertical"
        self.month_names = ('January',
                            'February', 
                            'March', 
                            'April', 
                            'May', 
                            'June', 
                            'July', 
                            'August', 
                            'September', 
                            'October',
                            'November',
                            'December')
        if kwargs in self.month_names:
            self.month_names = kwargs['month_names']
        self.header = headerBoxLayout(orientation = 'horizontal', size_hint = (1, 0.1))

        self.body = bodyGridLayout(cols = 7, spacing = 3)
        self.add_widget(self.header)
        self.add_widget(self.body)

        self.populate_body()
        self.populate_header()

    def populate_header(self, *args, **kwargs):
        self.header.clear_widgets()
        previous_month = Button(text = "<", on_press = self.move_previous_month, size_hint = (0.2,1), font_size = '30sp', background_down = '', background_normal = '', color = [0,0,0])
        next_month = Button(text = ">", on_press = self.move_next_month, size_hint = (0.2,1), font_size = '30sp', background_down = '', background_normal = '', color = [0,0,0])
        month_year_text = str(self.date.day) +' '+ self.month_names[self.date.month -1] + ' ' + str(self.date.year)
        current_month = Label(text=month_year_text, size_hint = (0.6, 1), color = [0,0,0], font_size = '20sp')
        headerTodayButton = RoundedButton(text='Today', size_hint = (0.2,0.8), pos_hint = {'center_y': .5}, on_press = self.todayButtonMethod)

        current_month.bold = True

        self.header.add_widget(previous_month)
        self.header.add_widget(current_month)
        self.header.add_widget(headerTodayButton)
        self.header.add_widget(next_month)

    def populate_body(self, *args, **kwargs):
        self.body.clear_widgets()
        date_cursor = date(self.date.year, self.date.month, 1)
        
        def callback(instance, value):
            print('My button <%s> state is <%s>' % (instance, value))

        for filler in range(date_cursor.isoweekday()-1):
            label = fillerLabel()
            self.body.add_widget(label)

        countOfChildren = 0
        firstDayOfWeek = date_cursor.isoweekday()

        while date_cursor.month == self.date.month:
            date_label = OtherButton(group = 'cat')
            date_label.otherButtonID = date_cursor
            date_label.text = str(date_cursor.day)
            date_label.bind(on_press=partial(self.set_date, day=date_cursor.day))
            date_label.bind(state=callback)
            if date_cursor == date.today():
                date_label.state = 'down'
                date_label.color = (1,0,0,1)
                date_label.bold = True
                date_label.font_size = '25sp'
                MyBoxLayout.TheTodayButton = date_label

            self.body.add_widget(date_label)
            if date_label.otherButtonID.month == date.today().month or date_label.otherButtonID > date.today():
                MyBoxLayout.buttonList.append(date_label)
            elif date_label.otherButtonID < date.today():
                MyBoxLayout.buttonList.insert(date_cursor.day - 1, date_label)
            date_cursor += timedelta(days = 1)
            countOfChildren += 1
        
        for button in MyBoxLayout.buttonList:
            print('the button list: ' + str(button.otherButtonID))

        if countOfChildren == 28 and firstDayOfWeek ==1:
            self.body.add_widget(Label(text=""))
        
        # l = ToggleButtonBehavior.get_widgets('cat')
        # for btn in l:
        #     print(str(btn) + ' ' + str(btn.state))
        # del l

        # The below attempts to iterate through all the child widgets in the Gridlayout, to find the current day and draw a red border around it. Also tries to locate the position of the child button. It didn't really work.

        # def my_callback(dt):
        #     print('Here is the datelabel position')
        #     for datelabel in self.body.children:
        #         print('self date day: ' + str(self.date.day) + ' text on button: ' + datelabel.text)
        #         print(datelabel.pos)
        #         if str(self.date.day) == datelabel.text:
        #             print('Crocodile')
        #             with self.canvas:
        #                 # Add a red color
        #                 Color(1., 0, 0)

        #                 # Add a rectangle
        #                 print('Here are rectangle pos')
        #                 print(datelabel.pos[0])
        #                 print(datelabel.pos[1])
        #                 Rectangle(pos=(datelabel.pos[0],datelabel.pos[1]), size=(50, 50))
        #             self.body.remove_widget(datelabel)
        #             self.body.add_widget(BorderButton())
        
        # Clock.schedule_once(my_callback)


    def set_date(self, widget, *args, **kwargs):
        self.date = date(self.date.year, self.date.month, kwargs['day'])
        
        self.populate_header()

        print(widget.background_color)
        print(MyBoxLayout.chosenColor)

        if widget.background_color == MyBoxLayout.chosenColor:
            print('we are in white color')
            widget.background_color = [1,1,1,1]
        else:
            print('color is: ' + str(MyBoxLayout.chosenColor))
            widget.background_color = MyBoxLayout.chosenColor

        counter = 0
        for dates in reversed(MyBoxLayout.buttonList[:MyBoxLayout.buttonList.index(MyBoxLayout.TheTodayButton)+1]):
            if dates.otherButtonID == date.today() and dates.background_color != MyBoxLayout.chosenColor:
                continue
            elif dates.background_color == MyBoxLayout.chosenColor:
                counter += 1
                if MyBoxLayout.currentSideButton == '':
                    pass
                else:
                    MyBoxLayout.currentSideButton.currentStreakCounter = counter
            else:
                if MyBoxLayout.currentSideButton == '':
                    pass
                else:
                    MyBoxLayout.currentSideButton.currentStreakCounter = counter
                break
            print(dates.otherButtonID)

    def move_next_month(self, *args, **kwargs):
        print('NextButton',self.date)

        if self.date.month == 12:
            self.date = date(self.date.year + 1, 1, self.date.day)
        elif calendar.monthrange(self.date.year, self.date.month+1)[1] < self.date.day:
            self.date = date(self.date.year, self.date.month + 1, calendar.monthrange(self.date.year, self.date.month + 1)[1])
        else:
            self.date = date(self.date.year, self.date.month + 1, self.date.day)
        
        print(self.date)

        dateForNewScreen = self.date
        MyBoxLayout.theEverywhereDate = dateForNewScreen
        
        if dateForNewScreen.strftime('%Y-%m') in MyBoxLayout.screenDict:
            existingScreen = MyBoxLayout.screenDict.get(dateForNewScreen.strftime('%Y-%m'))
            print('this screen already exists: ' + str(existingScreen.name))
            for child in existingScreen.children:
                child.date = self.date
                print('new advanced date: ' +str(self.date) + ' new child date: ' +str(child.date))
            print(MyBoxLayout.sm.current)
            MyBoxLayout.sm.current = existingScreen.name
            print(MyBoxLayout.sm.current)
        else:
            screenName = 'screenname' + self.date.strftime('%Y-%m')
            newScreen = Screen(name = screenName, on_enter = self.screenEnterMethod)
            MyBoxLayout.screenDict[dateForNewScreen.strftime('%Y-%m')] = newScreen
            print(MyBoxLayout.screenDict)
            newDatePicker = DatePicker()
            newScreen.add_widget(newDatePicker)
            MyBoxLayout.sm.add_widget(newScreen)
            print(MyBoxLayout.sm.current)
            MyBoxLayout.sm.current = newScreen.name
            print(MyBoxLayout.sm.current)
            print('adding new screen name: ' + str(screenName))
        

    def move_previous_month(self, *args, **kwargs):
        print('PrevButton',self.date)
        if self.date.month == 1:
            self.date = date(self.date.year - 1, 12, self.date.day)
        elif calendar.monthrange(self.date.year, self.date.month - 1)[1] < self.date.day:
            self.date = date(self.date.year, self.date.month - 1, calendar.monthrange(self.date.year, self.date.month - 1)[1])
        else:
            self.date = date(self.date.year, self.date.month -1, self.date.day)
        
        print(self.date)

        dateForNewScreen = self.date
        MyBoxLayout.theEverywhereDate = dateForNewScreen
        
        if dateForNewScreen.strftime('%Y-%m') in MyBoxLayout.screenDict:
            existingScreen = MyBoxLayout.screenDict.get(dateForNewScreen.strftime('%Y-%m'))
            print('this screen already exists: ' + str(existingScreen.name))
            for child in existingScreen.children:
                child.date = self.date
                print('new advanced date: ' +str(self.date) + ' new child date: ' +str(child.date))
            print(MyBoxLayout.sm.current)
            MyBoxLayout.sm.current = existingScreen.name
        else:
            screenName = 'screenname' + self.date.strftime('%Y-%m')
            newScreen = Screen(name = screenName, on_enter = self.screenEnterMethod)
            MyBoxLayout.screenDict[dateForNewScreen.strftime('%Y-%m')] = newScreen
            print(MyBoxLayout.screenDict)
            newDatePicker = DatePicker()
            newScreen.add_widget(newDatePicker)
            MyBoxLayout.sm.add_widget(newScreen)
            print(MyBoxLayout.sm.current)
            MyBoxLayout.sm.current = newScreen.name
            print('adding new screen name: ' + str(screenName))

    def screenEnterMethod(self, widget):
        print('entering screen '+ str(self.date))
        print('everywheredate: ' +str(MyBoxLayout.theEverywhereDate))
        for child in widget.children:
            child.date = MyBoxLayout.theEverywhereDate
            child.populate_header()
            for btn in child.body.children:
                btn.state = 'normal'
                if str(MyBoxLayout.theEverywhereDate.day) == btn.text:
                    btn.state = 'down'
    
    def todayButtonMethod(self, *args, **kwargs):
        MyBoxLayout.sm.current = str('screenname'+date.today().strftime('%Y-%m'))
        

class MyBoxLayout(BoxLayout):
    chosenColor = [1,1,1,1]
    sm = ScreenManager(size_hint = (0.7,1), transition = NoTransition())
    initialScreen = Screen(name = 'screenname'+date.today().strftime('%Y-%m'))
    screenDict = {}
    screenDict[date.today().strftime('%Y-%m')] = initialScreen
    theEverywhereDate = ''
    colorDict = {
            "blue": [(138/255,166/255,1,1),'Push Ups'],
            "green": [(172/255,1,181/255,1),'Get Milk'],
            "red": [(1,166/255,136/255,1),'Sing Song'],
            "pink": [(1,174/255,236/255,1),'Sit Ups'],
            "orange": [(1,204/255,139/255,1),'Sleeping'],
            "5": [(1,0,1,1),'Jumping'],
            "white": [(1,1,1,1),'Stretching'],
            "gridBlue": [(0.082,0.298,1,0.6),'Eat Vegetables']
            }
    buttonList = []
    TheTodayButton = ''
    currentSideButton = ''

    def __init__(self, **kwargs):
        super(MyBoxLayout, self).__init__(**kwargs)
        self.r_smash()
        
    def r_smash(self):

        rightLayout = GridLayout(size_hint = (0.2,1), rows = 7)

        with rightLayout.canvas.after:
            Color(0, 0, 0, 1)
            self.rect = Line(width = 2, rectangle = (self.x, self.y, self.width, self.height))

        def _update_rect(instance, value):
            self.rect.rectangle = (instance.x, instance.y, instance.width, instance.height)

        rightLayout.bind(size=_update_rect)
        
        btn1 = SideButton(size = ('200dp','100dp'), size_hint = (1, None))
        btn1.genID = 'blue'
        btn1.sideButtonColor = self.colorDict.get('blue')[0]
        btn1.originalColor = self.colorDict.get('blue')[0]
        self.currentSideButton = btn1

        btn2 = SideButton(size = ('200dp','100dp'), size_hint = (1, None))
        btn2.genID = 'green'
        btn2.sideButtonColor = self.colorDict.get('green')[0]
        btn2.originalColor = self.colorDict.get('green')[0]

        btn3 = SideButton(size = ('200dp','100dp'), size_hint = (1, None))
        btn3.genID = 'red'
        btn3.sideButtonColor = self.colorDict.get('red')[0]
        btn3.originalColor = self.colorDict.get('red')[0]

        btn4 = SideButton(size = ('200dp','100dp'), size_hint = (1, None))
        btn4.genID = 'pink'
        btn4.sideButtonColor = self.colorDict.get('pink')[0]
        btn4.originalColor = self.colorDict.get('pink')[0]

        btn5 = SideButton(size = ('200dp','100dp'), size_hint = (1, None))
        btn5.genID = 'orange'
        btn5.sideButtonColor = self.colorDict.get('orange')[0]
        btn5.originalColor = self.colorDict.get('orange')[0]

        addButton = AddButton(size = ('200dp','100dp'), size_hint = (1, None), font_size = '20dp')
    
        rightLayout.add_widget(btn1)
        rightLayout.add_widget(btn2)
        rightLayout.add_widget(btn3)
        rightLayout.add_widget(btn4)
        rightLayout.add_widget(btn5)
        rightLayout.add_widget(addButton)

        
        self.initialScreen.add_widget(DatePicker())
        self.initialScreen.bind(on_enter = self.AnotherScreenEnterMethod)
        self.sm.add_widget(self.initialScreen)
        self.add_widget(self.sm)
        self.add_widget(rightLayout)

    #Copy of screenentermethod just so I can reference it inside the MyBoxLayout class
    def AnotherScreenEnterMethod(self, widget):
        print('everywheredate: ' +str(MyBoxLayout.theEverywhereDate))
        if MyBoxLayout.theEverywhereDate != '':
            for child in widget.children:
                child.date = MyBoxLayout.theEverywhereDate
                child.populate_header()
                for btn in child.body.children:
                    btn.state = 'normal'
                    if str(MyBoxLayout.theEverywhereDate.day) == btn.text:
                        btn.state = 'down'
        

class BorderButton(ToggleButton):
    pass

class headerBoxLayout(BoxLayout):
    pass

class bodyGridLayout(GridLayout):
    pass

class fillerLabel(Label):
    pass

class AddButton(Button):
    pass

class RoundedButton(Button):
    pass

class OtherButton(ToggleButton):
    borderColor = (0,0,0,0)
    buttonBackgroundColor = (1,1,1,1)
    otherButtonID = ''
    ticked = 0


class SideButton(BoxLayout):
    sideButtonColor = ListProperty([0, 1, 1, 1])
    currentStreakCounter = NumericProperty(0)
    genID = -1
    SelectedOrNot = StringProperty()
    originalColor = [1,1,1,1]
    def __init__(self, *args, **kwargs):
        super(SideButton, self).__init__(**kwargs)
        
        def on_checkbox_active(checkbox, value):
            if value:
                MyBoxLayout.chosenColor = self.sideButtonColor
                MyBoxLayout.currentSideButton = checkbox.parent.parent
                MyBoxLayout.currentSideButton.SelectedOrNot = 'Selected'
            else:
                MyBoxLayout.currentSideButton.SelectedOrNot = ''
        
        self.ids.checkboxID.bind(active=on_checkbox_active)
        
class habitTrackerApp(App):

    def build(self):
        root_widget = MyBoxLayout()
        return root_widget

habitTrackerApp().run()

'''
Comments on the project:
- when dynamically creating widgets i can put them in a list or dictionary or something so I can reference them later
- create a button class, with variables for all the 1s and 0s for the states of the tasks, and a method (or methods) to set those variables
- or maybe try to use datetime as a database to hold 1s and 0s
- may have to move the screen creation after pressing a button to after when the date is changed because the date must be calculated first to work out if a new screen ought to be created
- maybe we could assign every button a 'date' variable when it is created so that every button is accessible by its date
- create a new screen, create a new datepicker object for the screen with the correct date, use a dictionary to check whether the screen exists already and if so load it, then use a created date id for the buttons to check for ticked or not. I think that might be it
- this might be useful for getting all the togglebuttons: static get_widgets(groupname) 
    Return a list of the widgets contained in a specific group. If the group doesn’t exist, an empty list will be returned.

    #Bookmark 18 Feb 2022. There is still apparently some issue with currentSideButton
            #Bookmark 18 Feb 2022. Important functionality missing is that clicking on sidebuttons does not
            #save the state of the streaks

    Note
    Always release the result of this method! Holding a reference to any of these widgets can prevent them from being garbage collected. If in doubt, do:
    l = ToggleButtonBehavior.get_widgets('mygroup')
    # do your job
    del l

'''

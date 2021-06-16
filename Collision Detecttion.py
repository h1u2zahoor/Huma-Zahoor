import cv2
import numpy as np
from kivy.app import App
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
import smtplib

Window.clearcolor = (0, 0, 0, 0)
Window.size = (360, 600)

# Code for alert Generation

def AlertGeneration():

    sender_email = "eroohal.ii@gmail.com"

    recv1 = "l174027@lhr.nu.edu.pk"
    recv2 = "l174111@lhr.nu.edu.pk"
    recv3 = "l174171@lhr.nu.edu.pk"
    recv4 = "l174214@lhr.nu.edu.pk"
    recv5 = "muhammad.saad@sharkmea.com"

    password = "Erohal_2_FYP"
    Subject = "Driver Safety Alert"
    Body = "We have found something about your driver that you must know."

    message = "Subject:{}\n\n{}".format(Subject, Body)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, password)

    server.sendmail(sender_email, recv1, message)
    server.sendmail(sender_email, recv2, message)
    server.sendmail(sender_email, recv3, message)
    server.sendmail(sender_email, recv4, message)
    server.sendmail(sender_email, recv5, message)


# Code For Collision Detection

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def doOverlap(l1, r1, l2, r2):
    if (l1.x >= r2.x or l2.x >= r1.x):
        return False

    if (l1.y >= r2.y or l2.y >= r1.y):
        return False

    return True

def collisionDetection():
    cap = cv2.VideoCapture(0)

    _, prev = cap.read()
    prev = cv2.flip(prev, 1)

    _, new = cap.read()
    new = cv2.flip(new, 1)

    while True:
        diff = cv2.absdiff(prev, new)
        diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        diff = cv2.blur(diff, (5, 5))
        _, thresh = cv2.threshold(diff, 10, 255, cv2.THRESH_BINARY)
        thresh = cv2.dilate(thresh, None, 3)
        thresh = cv2.erode(thresh, np.ones((4, 4)), 1)
        contor, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        cv2.rectangle(prev, (100, 300), (105, 480), (0, 255, 0), 3)
        cv2.rectangle(prev, (300, 300), (305, 480), (255, 0, 0), 3)
        cv2.rectangle(prev, (500, 300), (505, 480), (0, 0, 255), 3)

        l1 = Point(100, 300)
        r1 = Point(505, 480)

        for contors in contor:
            if cv2.contourArea(contors) > 3000:
                (x, y, w, h) = cv2.boundingRect(contors)
                (x1, y1), rad = cv2.minEnclosingCircle(contors)
                x1 = int(x1)
                y1 = int(y1)
                cv2.rectangle(prev, (x, y), (x + w, y + h), (0, 255, 0), 2)

                l2 = Point(x, y)
                r2 = Point(x + w, y + h)

                if (doOverlap(l1, r1, l2, r2) == True):
                    cv2.putText(prev, "WARNING", (x1, y1 - 5), cv2.FONT_HERSHEY_DUPLEX, 2, (0, 0, 255))

        cv2.imshow("Object Detection", prev)

        prev = new
        _, new = cap.read()

        if cv2.waitKey(1) == ord("f"):
            break

    cap.release()
    cv2.destroyAllWindows()


# Kivy Application

class MainApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', spacing=10, padding=40)
        label = Label(text='EROHAL II', font_size='40sp', color=(1, 1, 1, 1), bold="true")
        btn1 = Button(text='Collision Detection', background_color=(0.25,.25,0.25,1),on_press=self.Print)
        btn2 = Button(text='Drowsiness Detection', background_color=(0.5,.5,0.5,1))
        btn3 = Button(text='Hard Brake Detection', background_color=(0.75,.75,0.75,1))
        btn4 = Button(text='Send Alert',on_press=self.F2)
        layout.add_widget(label)
        layout.add_widget(btn1)
        layout.add_widget(btn2)
        layout.add_widget(btn3)
        layout.add_widget(btn4)

        return layout

    def Print(self, obj):
        collisionDetection()

    def F2(self,obj):
        AlertGeneration()


MainApp().run()

############################################# IMPORTING ################################################
import tkinter as tk
from tkinter import ttk, messagebox as mess, simpledialog as tsd
import cv2
import os
import csv
import numpy as np
from PIL import Image, ImageTk
import pandas as pd
import datetime
import time
import mysql.connector
from PIL import Image, ImageTk
import subprocess

############################################# FUNCTIONS ################################################

def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)

#########################################################################################################

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",

    database="face_recog",
)
mycursor = mydb.cursor()


sql = "SELECT * FROM stud_details"

# Execute query
mycursor.execute(sql)

# Fetch results
results = mycursor.fetchall()

# Print results
for row in results:
    print(row)

# Close cursor and connection
mycursor.close()
mydb.close()
##################################################################################

def generate_student_report():
    # Open attendance.py using subprocess
    subprocess.Popen(["python", "student_report.py"])
##################################################################################

def tick():
    time_string = time.strftime('%H:%M:%S')
    clock.config(text=time_string)
    clock.after(200,tick)

###################################################################################

def contact():
    mess._show(title='Contact us', message="Please contact us on : 'prashant284865@gmail.com' ")

###################################################################################

def check_haarcascadefile():
    exists = os.path.isfile("haarcascade_frontalface_default.xml")
    if exists:
        pass
    else:
        mess._show(title='Some file missing', message='Please contact us for help')
        window.destroy()

###################################################################################

def save_pass():
    assure_path_exists("TrainingImageLabel/")
    exists1 = os.path.isfile("TrainingImageLabel\psd.txt")
    if exists1:
        tf = open("TrainingImageLabel\psd.txt", "r")
        key = tf.read()
    else:
        master.destroy()
        new_pas = tsd.askstring('Old Password not found', 'Please enter a new password below', show='*')
        if new_pas == None:
            mess._show(title='No Password Entered', message='Password not set!! Please try again')
        else:
            tf = open("TrainingImageLabel\psd.txt", "w")
            tf.write(new_pas)
            mess._show(title='Password Registered', message='New password was registered successfully!!')
            return

    op = (old.get())
    newp= (new.get())
    nnewp = (nnew.get())
    if (op == key):
        if(newp == nnewp):
            txf = open("TrainingImageLabel\psd.txt", "w")
            txf.write(newp)
        else:
            mess._show(title='Error',message='Confirm new password again!!!')
            return
    else:
        mess._show(title='Wrong Password', message='Please enter correct old password.')
        return
    mess._show(title='Password Changed', message='Password changed successfully!!')
    master.destroy()

###################################################################################

def change_pass():
    global master
    master = tk.Tk()
    master.geometry("400x160")
    master.resizable(False,False)
    master.title("Change Password")
    master.configure(background="white")
    lbl4 = tk.Label(master,text='    Enter Old Password',bg='white',font=('comic', 12, ' bold '))
    lbl4.place(x=10,y=10)
    global old
    old=tk.Entry(master,width=25 ,fg="black",relief='solid',font=('comic', 12, ' bold '),show='*')
    old.place(x=180,y=10)
    lbl5 = tk.Label(master, text='   Enter New Password', bg='white', font=('comic', 12, ' bold '))
    lbl5.place(x=10, y=45)
    global new
    new = tk.Entry(master, width=25, fg="black",relief='solid', font=('comic', 12, ' bold '),show='*')
    new.place(x=180, y=45)
    lbl6 = tk.Label(master, text='Confirm New Password', bg='white', font=('comic', 12, ' bold '))
    lbl6.place(x=10, y=80)
    global nnew
    nnew = tk.Entry(master, width=25, fg="black", relief='solid',font=('comic', 12, ' bold '),show='*')
    nnew.place(x=180, y=80)
    cancel=tk.Button(master,text="Cancel", command=master.destroy ,fg="black"  ,bg="red" ,height=1,width=25 , activebackground = "white" ,font=('comic', 10, ' bold '))
    cancel.place(x=200, y=120)
    save1 = tk.Button(master, text="Save", command=save_pass, fg="black", bg="#191970", height = 1,width=25, activebackground="white", font=('comic', 10, ' bold '))
    save1.place(x=10, y=120)
    master.mainloop()

#####################################################################################

def psw():
    assure_path_exists("TrainingImageLabel/")
    exists1 = os.path.isfile("TrainingImageLabel\psd.txt")
    if exists1:
        tf = open("TrainingImageLabel\psd.txt", "r")
        key = tf.read()
    else:
        new_pas = tsd.askstring('Old Password not found', 'Please enter a new password below', show='*')
        if new_pas == None:
            mess._show(title='No Password Entered', message='Password not set!! Please try again')
        else:
            tf = open("TrainingImageLabel\psd.txt", "w")
            tf.write(new_pas)
            mess._show(title='Password Registered', message='New password was registered successfully!!')
            return
    password = tsd.askstring('Password', 'Enter Password', show='*')
    if (password == key):
        TrainImages()
    elif (password == None):
        pass
    else:
        mess._show(title='Wrong Password', message='You have entered wrong password')

######################################################################################

def clear():
    txt.delete(0, 'end')
    res = "1)Take Images  >>>  2)Save Profile"
    message1.configure(text=res)


def clear2():
    txt2.delete(0, 'end')
    res = "1)Take Images  >>>  2)Save Profile"
    message1.configure(text=res)

#######################################################################################
def TakeImages():
    # Check if the haarcascade file exists
    check_haarcascadefile()
    
    # Get the number of registrations from the CSV file
    columns = ['SERIAL NO.', '', 'ID', '', 'NAME']
    assure_path_exists("StudentDetails/")
    assure_path_exists("TrainingImage/")
    serial = 0
    exists = os.path.isfile("StudentDetails\StudentDetails.csv")
    if exists:
        with open("StudentDetails\StudentDetails.csv", 'r') as csvFile1:
            reader1 = csv.reader(csvFile1)
            for l in reader1:
                serial = serial + 1
        serial = (serial // 2)
        csvFile1.close()
    else:
        with open("StudentDetails\StudentDetails.csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(columns)
            serial = 1
        csvFile1.close()

    # Get the ID and name from the entry fields
    Id = txt.get()
    name = txt2.get()

    if name.isalpha() or ' ' in name:
        if Id.isdigit():  # Check if the roll number contains only numerical characters
            

            # Continue with capturing the image and processing it
            cam = cv2.VideoCapture(0)
            harcascadePath = "haarcascade_frontalface_default.xml"
            detector = cv2.CascadeClassifier(harcascadePath)
            sampleNum = 0
            while True:
                ret, img = cam.read()
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = detector.detectMultiScale(gray, 1.3, 5)
                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    sampleNum = sampleNum + 1
                    cv2.imwrite("TrainingImage\ " + name + "." + str(serial) + "." + Id + '.' + str(sampleNum) + ".jpg",
                                gray[y:y + h, x:x + w])
                    cv2.imshow('Taking Images', img)
                if cv2.waitKey(100) & 0xFF == ord('q'):
                    break
                elif sampleNum > 100:
                    break
            cam.release()
            cv2.destroyAllWindows()

            # Insert the data into the database
            try: 
                mydb = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="face_recog",
                )
                mycursor = mydb.cursor()
                mycursor.execute("insert into stud_details(Name,Roll_No) values('"+name+"','"+Id+"')")
                mydb.commit()
                print('Record updated successfully...')   
            except:
                mydb.rollback()
            mydb.close()

            # Update the CSV file with the registration details
            row = [serial, '', Id, '', name]
            with open('StudentDetails\StudentDetails.csv', 'a+') as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow(row)
                mess._show(title='Registrations', message='Registration Successful!!!')
            csvFile.close()

            # Display a message confirming successful registration
            res = "Images Taken for ID : " + Id
            message1.configure(text=res)
        else:
            res = "Enter a valid roll number"
            message.configure(text=res)
    else:
        if not name.isalpha():
            res = "Enter Correct name"
            message.configure(text=res)


########################################################################################

def TrainImages():
    check_haarcascadefile()
    assure_path_exists("TrainingImageLabel/")
    recognizer = cv2.face_LBPHFaceRecognizer.create()
    harcascadePath = "haarcascade_frontalface_default.xml"
    detector = cv2.CascadeClassifier(harcascadePath)
    faces, ID = getImagesAndLabels("TrainingImage")
    try:
        recognizer.train(faces, np.array(ID))
    except:
        mess._show(title='No Registrations', message='Please Register someone first!!!')
        return
    recognizer.save("TrainingImageLabel\Trainner.yml")
    res = "Profile Saved Successfully"
    message1.configure(text=res)
    message.configure(text='Total Registrations till now  : ' + str(ID[0]))

############################################################################################3

def getImagesAndLabels(path):
    # get the path of all the files in the folder
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    # create empth face list
    faces = []
    # create empty ID list
    Ids = []
    # now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        # loading the image and converting it to gray scale
        pilImage = Image.open(imagePath).convert('L')
        # Now we are converting the PIL image into numpy array
        imageNp = np.array(pilImage, 'uint8')
        # getting the Id from the image
        ID = int(os.path.split(imagePath)[-1].split(".")[1])
        # extract the face from the training image sample
        faces.append(imageNp)
        Ids.append(ID)
    return faces, Ids

###########################################################################################
def TrackImages():
    check_haarcascadefile()
    assure_path_exists("Attendance/")
    assure_path_exists("StudentDetails/")
    for k in tv.get_children():
        tv.delete(k)
    msg = ''
    i = 0
    j = 0
    recognizer = cv2.face.LBPHFaceRecognizer_create()  
    exists3 = os.path.isfile("TrainingImageLabel\Trainner.yml")
    if exists3:
        recognizer.read("TrainingImageLabel\Trainner.yml")
    else:
        mess._show(title='Data Missing', message='Please click on Save Profile to reset data!!')
        return
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath)

    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    col_names = ['Id', '', 'Name', '', 'Date', '', 'Time']
    exists1 = os.path.isfile("StudentDetails\StudentDetails.csv")
    if exists1:
        df = pd.read_csv("StudentDetails\StudentDetails.csv")
    else:
        mess._show(title='Details Missing', message='Students details are missing, please check!')
        cam.release()
        cv2.destroyAllWindows()
        window.destroy()
        return

    cv2.namedWindow('Taking Attendance')  # Create the OpenCV window
    cv2.moveWindow('Taking Attendance', 600, 100)  # Move the window to desired position

    while True:
        ret, im = cam.read()
        if not ret:
            print("Error: Camera frame not captured")
            break
        
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)
        if len(faces) == 0:
            # No face detected, add a button to close the camera
            cv2.putText(im, "No face detected", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2) #red color
            cv2.putText(im, "Press 'q' to close camera", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2) #red color
            cv2.imshow('Taking Attendance', im)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cam.release()
                cv2.destroyAllWindows()
                break
            continue

        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x + w, y + h), (255, 0, 0), 2)
            serial, conf = recognizer.predict(gray[y:y + h, x:x + w])
            if conf < 50:
                # Process recognized face
                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                aa = df.loc[df['SERIAL NO.'] == serial]['NAME'].values
                ID = df.loc[df['SERIAL NO.'] == serial]['ID'].values
                ID = str(ID)
                ID = ID[1:-1]
                bb = str(aa)
                bb = bb[2:-2]
                attendance = [str(ID), '', bb, '', str(date), '', str(timeStamp)]
                try:
                    mydb = mysql.connector.connect(
                        host="localhost",
                        user="root",
                        password="",
                        database="face_recog",
                    )
                    mycursor = mydb.cursor()
                    sql = "INSERT INTO attendance (Roll_No, Name, Date, Time) VALUES (%s, %s, %s, %s)"
                    val = (ID, bb, date, timeStamp)
                    mycursor.execute(sql, val)
                    mydb.commit()
                    print("Attendance recorded successfully!")
                except Exception as e:
                    print("Error recording attendance:", e)
                    mydb.rollback()
                mydb.close()

                iidd = str(ID) + '   '
                tv.insert('', 0, text=iidd, values=(str(bb), str(date), str(timeStamp)))

                attendance_file = f"Attendance/Attendance_{date}.csv"
                if not os.path.isfile(attendance_file):
                    with open(attendance_file, 'w', newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow(col_names)
                with open(attendance_file, 'a', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(attendance)

                cam.release()
                cv2.destroyAllWindows()

                mess._show(title='Attendance Status', message='Attendance Taken successfully')

                return
            else:
                # Unknown face detected, handle this case
                #######print("Unknown face detected")
                # Display message to close camera
                cv2.putText(im, "Unknown face detected", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)  # Blue color
                cv2.putText(im, "Press 'q' to close camera", (50, 100), cv2.FONT_HERSHEY_SIMPLEX,0.7, (255, 0, 0), 2)  # Blue color
                cv2.imshow('Taking Attendance', im)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    cam.release()
                    cv2.destroyAllWindows()
                    return

    window.mainloop()  # Move the mainloop call outside the while loop
#######################################################################################

######################################## USED STUFFS ############################################
    
global key
key = ''

ts = time.time()
date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
day,month,year=date.split("-")

mont={'01':'January',
      '02':'February',
      '03':'March',
      '04':'April',
      '05':'May',
      '06':'June',
      '07':'July',
      '08':'August',
      '09':'September',
      '10':'October',
      '11':'November',
      '12':'December'
      }

######################################## GUI FRONT-END ####################################################################

window = tk.Tk()
window.geometry("1280x720")
window.title("Attendance System")
window.minsize(1280, 720)  # Set minimum size for the window
window.maxsize(1280, 720)  # Set maximum size for the window

########################Adjustinng the Window Position in a Screen##########################################################

# Get the screen width and height
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# Calculate the position for the window to be centered
x_coordinate = (screen_width - 1280) // 2
y_coordinate = (screen_height - 720) // 2

# Set the geometry of the window
window.geometry(f"1280x720+{x_coordinate}+{y_coordinate}")
########Background Image#####################################################################################################
background_image = Image.open("img\\bg.png")
background_image = background_image.resize((1280, 720))
background_photo = ImageTk.PhotoImage(background_image)

background_label = tk.Label(window, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
##############################################################################################################################
# Load background image
background_image = Image.open("img\\bg.png")
background_image = background_image.resize((1280, 720))
background_photo = ImageTk.PhotoImage(background_image)

# Set background image to a label in the main window
background_label = tk.Label(window, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
#############################################################################################################################
frame1 = tk.Frame(window)
frame1.place(relx=0.11, rely=0.17, relwidth=0.39, relheight=0.80)

frame2 = tk.Frame(window)
frame2.place(relx=0.51, rely=0.17, relwidth=0.38, relheight=0.80)

# Load background image for frame1
background_image1 = Image.open("img\\bg2.jpg")
background_image1 = background_image1.resize((1280, 720))
background_photo1 = ImageTk.PhotoImage(background_image1)
background_label1 = tk.Label(frame1, image=background_photo1)
background_label1.place(x=0, y=0, relwidth=1, relheight=1)

# Load background image for frame2
background_image2 = Image.open("img\\bg22.jpg")
background_image2 = background_image2.resize((1280, 720))
background_photo2 = ImageTk.PhotoImage(background_image2)
background_label2 = tk.Label(frame2, image=background_photo2)
background_label2.place(x=0, y=0, relwidth=1, relheight=1)

############testttttttttttttttttt################################################################################################
# Set window size
window_width = 900
window_height = 60
window.geometry(f"{window_width}x{window_height}")
'''
# Load and resize background image
bg_img = Image.open("C:\\Users\\pk284\\Downloads\\Integrated project\\1. IP new research\\0.Working\\Backup\\10.Face-Recognition-Based-Attendance-Monitoring-System_\\img\\bg.png")  # Replace "background_image.jpg" with your image path
bg_img = bg_img.resize((window_width, window_height))
bg_image = ImageTk.PhotoImage(bg_img)
'''



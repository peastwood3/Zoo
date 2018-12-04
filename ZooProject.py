

import pymysql #correct
from tkinter import * #need to add to tkinter
import urllib.request
import re #looks right to me
import time #standard importing
import datetime
from tkinter import messagebox
from tkinter import ttk
try:
    from tkinter import *
    from tkinter import ttk
except ImportError: #need exception so do not change
    from tkinter import * #having trouble with this on the laptop
    import ttk

class GUI:


    def __init__(self, root):

        self.root = root
        self.sortingSQL = ("SELECT * from STAFF WHERE APPROVED is NULL") #help-------------------
        self.sortingData = ("SELECT * from DATAPOINT WHERE ACCEPTED is NULL")
        self.filterSQL = ("SELECT * FROM POI") #help-----------------
        self.DfilterSQL = ("SELECT Type, DataValue, DateTime FROM DATAPOINT WHERE ACCEPTED =1 AND LocationName = ") #help-----------
        self.reportSQL = ("SELECT POI.LOCATIONNAME, POI.CITY, POI.STATE, MIN( CASE WHEN TYPE = 'MOLD' THEN DATAVALUE ELSE NULL END), AVG( CASE WHEN TYPE = 'MOLD' THEN DATAVALUE ELSE NULL END), MAX(CASE WHEN TYPE='MOLD' THEN DATAVALUE ELSE NULL END ), MIN(CASE WHEN TYPE = 'AIR QUALITY' THEN DATAVALUE ELSE NULL  END), AVG(CASE WHEN TYPE = 'AIR QUALITY' THEN DATAVALUE ELSE NULL  END), MAX(CASE WHEN TYPE = 'AIR QUALITY'THEN DATAVALUE ELSE NULL END ), COUNT( DATETIME ), POI.FLAGGED FROM POI NATURAL JOIN DATAPOINT WHERE ACCEPTED=1 GROUP BY (LOCATIONNAME)")

        loginLabel = Label(root, text = "Login")
        loginLabel.grid(row = 0, column = 0)

        userLabel = Label(root, text = "Username:") #for the Atlanta Zoo heading, you need to have an email, username, password, and confirm password
        userLabel.grid(row = 1, column = 1)
        self.usernameEntry = Entry(root, width = 50)
        self.usernameEntry.grid(row = 1, column = 2)

        passwordLabel = Label(root, text = "Password")
        passwordLabel.grid(row = 2, column = 1)
        self.passwordEntry = Entry(root, show = "*", width = 50)
        self.passwordEntry.grid(row = 2, column = 2)

        #You may validate the email address using the database (SQL Check Constraint) or in the front end of the application

        loginButton = Button(root, text = "LOGIN", command = self.login)  #Either login as an already registered user or register as a new user
        loginButton.grid(row = 4, column = 1)

        registerButton = Button(root, text = "REGISTER", command = self.newUserReg) #two options for entering the site: register or login
        registerButton.grid(row = 4, column = 2)
        #An email address consists of alphanumeric characters, followed by an @ symbol, followed by alphanumeric characters

    def login(self):

        #to get the login to work

        self.start()
        a = self.usernameEntry.get() #calling it
        b = self.passwordEntry.get() #calling it
        try:
            sql = "SELECT Username, Password from USER WHERE Username = (%s)"
            self.curs.execute(sql, self.usernameEntry.get())
            vals = self.curs.fetchall()
            print("vals", vals)

            if (vals[0][1]) == self.passwordEntry.get():
                print("passed")
                typeSql = "SELECT Type from USER WHERE Username = (%s)"
                self.curs.execute(typeSql, self.usernameEntry.get())
                type1 = self.curs.fetchall()
                print("type1:", type1[0][0])

                if (type1[0][0]) == "staff": #You are going to have 2 options for staff and visitor registration
                    # statement = "SELECT Approved FROM STAFF WHERE Username = (%s)"
                    # entry = self.usernameEntry.get()
                    # self.curs.execute(statement, entry)
                    # aVar = self.curs.fetchall()
                    # if aVar[0][0] != 1:

                    # else:
                    print("staffFunc")
                    self.staffFunctionalities()

                elif (type1[0][0]) == "visitor": #yeet
                    print("visitor")
                    self.addNewDataPoint()

                elif (type1[0][0]) == "admin": #yeet
                    print("admin")
                    self.adminFunctionalities()

            else:
                passwordError = messagebox.showerror("Error", "Username Password Combo is Incorrect!") #yeet

        except:
            registrationError = messagebox.showerror("Error", "That username is not recognized, please register!") #yep

    def newUserReg(self): #Registering a new user
        self.start()
        self.root.iconify()
        self.RP = Toplevel(self.root)
        self.RP.geometry('800x500+0+0') #seems right

        newregistrationLabel = Label(self.RP, text = "NEW USER REGISTRATION") #seems right
        newregistrationLabel.grid(row = 0, column = 0)

        newUserLabel = Label(self.RP, text = "Username:") #seems right
        newUserLabel.grid(row = 1, column = 0)

        self.newUsernameEntry = Entry(self.RP, width = 50)
        self.newUsernameEntry.grid(row = 1, column = 1)

        newEmailLabel = Label(self.RP, text = "Email:") #seems right
        newEmailLabel.grid(row = 2, column = 0)

        self.newEmailEntry = Entry(self.RP, width = 50)
        self.newEmailEntry.grid(row = 2, column = 1)

        newPasswordLabel = Label(self.RP, text = "Password:") #seems right
        newPasswordLabel.grid(row = 3, column = 0)

        self.newPasswordEntry = Entry(self.RP, show = "*", width = 50)
        self.newPasswordEntry.grid(row = 3, column = 1)

        newPasswordLabel2 = Label(self.RP, text = "Confirm Password:") #seems right
        newPasswordLabel2.grid(row = 4, column = 0)

        self.newPasswordConfirm = Entry(self.RP, show = "*", width = 50)
        self.newPasswordConfirm.grid(row = 4, column = 1)


        userLabel = Label(self.RP, text = "User Type:") #seems right
        userLabel.grid(row = 5, column = 0)

        self.newUserType = StringVar(self.RP)
        self.newUserType.set("")  # default value

        visitorButton = Radiobutton(self.RP, text="Register Visitor", variable=self.newUserType,
                                          value="visitor", command = self.changeOptions2)
        visitorButton.grid(row=5, column=1) #will probably change grid location

        staffButton = Radiobutton(self.RP, text="Register Staff", variable=self.newUserType, value="staff",
                                 command=self.changeOptions)
        staffButton.grid(row=6, column=1) #will probably change grid location

        createButton = Button(self.RP, text="CREATE", command = self.createNewUser)
        createButton.grid(row=11, column=0)

        quitButton = Button(self.RP, text="EXIT", command=self.quit)
        quitButton.grid(row=12, column=0)

    def quit(self):
        self.RP.destroy()
        self.root.deiconify() #deiconify creates a new window

    def changeOptions(self):
        self.name.config(state = 'normal')
        self.species.config(state = 'normal')
        self.typeEntry.config(state = 'normal')
        self.speciesSelection.set("")
        self.nameSelection.set("")
        self.typeSelection.set("")

    def changeOptions2(self):
        self.name.config(state='disabled')
        self.species.config(state='disabled')
        self.typeEntry.config(state='disabled')
        self.speciesSelection.set("---")
        self.nameSelection.set("---")
        self.typeSelection.set("---")

    def createNewUser(self): #this is definitely right
        aList = [self.newUsernameEntry.get(), self.newEmailEntry.get(), self.newPasswordEntry.get(),
                 self.newUserType.get()]

        complete = True
        for i in aList: #yes
            if i == "": #yes
                warningBox = messagebox.showerror("Error", "You must fill out all values!") #yes
                complete = False #yes
                return None #yes

        if self.newPasswordEntry.get() != self.newPasswordConfirm.get(): #yes
            complete = False #yes
            warningBox = messagebox.showerror("Error", "Your passwords do not match!") #yes
            return None #yes

        self.start()

        sql = "INSERT INTO USER (Email, Username, Password, Type) VALUES (%s, %s, %s, %s)" #yes

        data = (self.newEmailEntry.get(), self.newUsernameEntry.get(), #yes
                          self.newPasswordEntry.get(), self.newUserType.get()) #yes

        self.curs.execute(sql, data) #yes


        if self.newUserType.get() == "Staff":
            sql2 = "INSERT INTO STAFF (Username) VALUES (%s)"

            data2 = (self.newUsernameEntry.get())
            Notice = messagebox.showerror("Attention!", "Your account is pending admin review")
            self.curs.execute(sql2, data2)

        if self.newUserType.get() == "Visitor":
            sql3 = "INSERT INTO VISITOR(Username) VALUES (%s)"
            data3 =(self.newUsernameEntry.get())

            self.curs.execute(sql3, data3)

        if complete == True:
            successNotice = messagebox.showerror("Success!", "Your Username has been created")

#-------------------------------------------# Staff Functionalities ----------------------------------------
    def animalSearch(self):
        #Title Atlanta Zoo Animals: Name, Species, Exhibit, Age Min or Max, Type
        #Selecting an animal takes them to  the animal care page, Which is titled Animal Detail
        #Animal Care Page has Name, Species, Age, Exhibit, Type documented, Note, Log Notes button,
        # And a chart with Staff Member, Note, and Date/Time
        self.start()
        self.root.iconify() #makes a new window
        self.RP = Toplevel(self.root) #widget to make a new window - think banner
        self.RP.geometry('800x500+0+0')
        #what staff should be able to do: Search Animals, View Shows, Logout

        nameLabel = Label(self.RP, text="Search Animals")#
        nameLabel.grid(row=0, column=0)

        self.nameSelection = StringVar(self.RP)#
        self.nameSelection.set("---")

        self.curs.execute("SELECT Name FROM ANIMAL")#
        cvals = self.curs.fetchall()

        self.name = OptionMenu(self.RP, self.nameSelection, *cvals)#

        self.name.config(width = 20)#
        self.name.config(state = 'disabled')#
        self.name.grid(row = 8, column = 1)#

        speciesLabel = Label(self.RP, text="Species")#
        speciesLabel.grid(row=9, column=0)#

        self.speciesSelection = StringVar(self.RP)#
        self.speciesSelection.set("---")#

        self.curs.execute("SELECT Species FROM ANIMAL")
        svals = self.curs.fetchall()
        print(svals)
        self.species = OptionMenu(self.RP, self.speciesSelection, *svals)

        self.species.config(width = 20)
        self.species.config(state = 'disabled')
        self.species.grid(row = 9, column = 1)

        self.typeLabel = Label(self.RP, text = "Type")
        self.typeLabel.grid(row = 10, column = 0)

        self.typeSelection = StringVar()
        self.typeEntry = Entry(self.RP, width = 50, textvariable = self.typeSelection)
        self.typeEntry.grid(row = 10, column = 1)
        self.typeEntry.config(state = 'disabled')
        self.typeSelection.set("---")



    def staffFunctionalities(self):
        self.root.iconify()
        self.CF = Toplevel(self.root)
        self.CF.geometry('350x350+0+0')
        funcLabel = Label(self.CF, text="Choose Functionality")
        funcLabel.grid(row=0, column=0)
        #
        # top = tkinter.Tk()
        # def helloCallBack():
        #    messagebox.showinfo( "Hello Python", "Hello World")
        # B = tkinter.Button(top, text ="Hello", command = helloCallBack)
        # B.pack()
        # top.mainloop()
        #
        button = Button(self.CF, text="Search Animals", command=self.animalSearch)
        button.grid(row=1, column=5)
        print('done')

        button2 = Button(self.CF, text="View Shows", command=self.viewShow)
        button2.grid(row=2, column=5)

        button3 = Button(self.CF, text="Logout", command = self.logoutO)
        button3.grid(row=3, column=5)



    def callback():
        print("click!")

    def logoutO(self):
        self.CF.destroy()
        self.root.deiconify()
        ###################sending to Sparsh
#WRONG ANIMAL SEARCH
    # def animalSearch(self):
    #     self.FS = Toplevel(self.CF)
    #     self.CF.iconify()
    #
    #     title = Label(self.FS, text="Animal Shows")
    #     title.grid(row=0, column=0)
    #     showNameLabel = Label(self.FS, text="Name")
    #     showNameLabel.grid(row=1, column=0)
    #
    #     self.curs.execute("SELECT Name FROM SHOW")
    #     lvals = self.curs.fetchall()
    #
    #     self.showName = StringVar()
    #     showEntry = OptionMenu(self.FS, self.showName, *lvals)
    #     showEntry.grid(row=1, column=1)
    #
    #     showNameLabel = Label(self.FS, text="Show Name")
    #     showNameLabel.grid(row=2, column=0)
    #
    #     self.curs.execute("SELECT Date_Time FROM SHOW")
    #     cvals = self.curs.fetchall()
    #     self.date = StringVar()
    #     dateEntry = OptionMenu(self.FS, self.date, *cvals)
    #     dateEntry.grid(row=2, column=1)
    #

    def viewShow(self):  # Staff FUNCTION
        self.FS = Toplevel(self.CF)
        self.CF.iconify()

        title = Label(self.FS, text="Animal Shows")
        title.grid(row=0, column=0)
        showNameLabel = Label(self.FS, text="Name")
        showNameLabel.grid(row=1, column=0)

        self.curs.execute("SELECT Name FROM SHOW")
        lvals = self.curs.fetchall()

        self.showName = StringVar()
        showEntry = OptionMenu(self.FS, self.showName, *lvals)
        showEntry.grid(row=1, column=1)

        showNameLabel = Label(self.FS, text="Show Name")
        showNameLabel.grid(row=2, column=0)

        self.curs.execute("SELECT Date_Time FROM SHOW")
        cvals = self.curs.fetchall()
        self.date = StringVar()
        dateEntry = OptionMenu(self.FS, self.date, *cvals)
        dateEntry.grid(row=2, column=1)

        #personNameLabel = Label(self.FS, text="Person Name")
        #personNameLabel.grid(row=3, column=0)
        self.curs.execute("SELECT Host FROM SHOW")
        svals = self.curs.fetchall()
        self.persontype = StringVar()
        personEntry = OptionMenu(self.FS, self.personrunning, *svals)  # TODO: GET THE VALUES IN SATE
        personEntry.grid(row=3, column=1)

        self.curs.execute("SELECT Located_At FROM SHOW")
        svals = self.curs.fetchall()
        self.regiontype = StringVar()
        regionEntry = OptionMenu(self.FS, self.region, *svals)  # TODO: GET THE VALUES IN SATE
        regionEntry.grid(row=4, column=1)
        #
        #
        #
        # applyButton = Button(self.FS, text = "Apply Filter", command = self.applyFilter)
        # applyButton.grid(row = 13, column = 0) #correct
        # resetButton = Button(self.FS, text = "Reset Filter", command = self.resetFilter)
        # resetButton.grid(row = 13, column = 1) #correct
        #
        #
        # backButton = Button(self.FS, text = "Back", command = self.viewShowBack)
        # backButton.grid(row = 500, column = 1)
        # self.start()
        #
        # self.viewtree = ttk.Treeview(self.FS)
        #
        # self.curs.execute(self.filterSQL)

        self.viewtree["columns"] = ("AttractionName","Datetime","PersonRunning","RegionType")
        self.viewtree.column("AttractionName", width = 100)
        self.viewtree.column("Datetime", width = 100)
        self.viewtree.column("PersonRunning", width= 100)
        self.viewtree.column("RegionType", width = 100)

        self.viewtree.heading("#0", text='Number', anchor='w')
        self.viewtree.column("#0", anchor="w")
        self.viewtree.heading("AttractionName", text = "AttractionName")
        self.viewtree.heading("Datetime", text="Datetime")
        self.viewtree.heading("PersonRunning", text="PersonRunning")
        self.viewtree.heading("RegionType", text="RegionType")
        #self.viewtree.heading("Flagged", text = "Flagged")
        #self.viewtree.heading("DateFlagged", text = "DateFlagged")
        self.viewtree.grid(row = 20, column = 0)

        cpt = 0
        for row in self.curs.fetchall():
            self.viewtree.insert('', 'end', text=str(cpt), values=(row[0], row[1], row[2], row[3], row[4], row[5]))
            cpt += 1
        self.viewtree.bind("<Double-1>", self.poiDetail)


    def poiDetail(self, event):
        self.start()
        self.poiDetailPage = Toplevel(self.FS)
        self.FS.iconify()

        curItem = self.viewtree.focus()
        var = self.viewtree.item(curItem)
        self.viewPOIClick = "'"+str(var['values'][0])+"'"
        if self.DfilterSQL == "SELECT Type, DataValue, DateTime FROM DATAPOINT WHERE ACCEPTED =1 AND LocationName = ":
            self.DfilterSQL+= self.viewPOIClick

        self.curs.execute(self.DfilterSQL)

        f1 = Frame(self.poiDetailPage, height=100, width=100, bd=1, relief=SUNKEN)
        f1.grid(row=0, column=0)
        f2 = Frame(self.poiDetailPage, height = 100, width = 100, bd = 1, relief = SUNKEN)
        f2.grid(row = 30, column = 1)

        backButton = Button(f2, text = "Back", command = self.poiBack)
        backButton.grid(row = 0, column = 0)
        flagButton = Button(f2, text = "Flag", command = self.poiFlag)
        flagButton.grid(row = 0, column = 1)

        title = Label(f1, text = "POI Detail")
        title.grid(row = 0, column = 0)

        typeLabel = Label(f1, text = "Type:")
        typeLabel.grid(row = 1, column = 0)

        self.poiTypeSelection = StringVar()
        a = OptionMenu(f1, self.poiTypeSelection, "Mold", "Air Quality")
        a.grid(row=1, column=1)

        dataValueLabel = Label(f1, text = "Data Value Range:")
        dataValueLabel.grid(row = 2, column = 0)

        timeLabel = Label(f1, text = "Date/Time Range:")
        timeLabel.grid(row = 3, column = 0)



        self.initialdataValEntry = Entry(f1, width = 4)
        self.initialdataValEntry.grid(row = 4, column = 1)

        self.finaldataValEntry = Entry(f1, width = 4)
        self.finaldataValEntry.grid(row = 4, column = 2)

        self.poibeginYearVar = Entry(f1)
        self.poibeginYearVar.grid(row=5, column=1)
        self.poiendYearVar = Entry(f1)
        self.poiendYearVar.grid(row=5, column=2)

        self.poibeginMonthVar = Entry(f1)
        self.poibeginMonthVar.grid(row=6, column=1)
        self.poiendMonthVar = Entry(f1)
        self.poiendMonthVar.grid(row=6, column=2)

        self.poibeginDayVar = Entry(f1)
        self.poibeginDayVar.grid(row=7, column=1)
        self.poiendDayVar = Entry(f1)
        self.poiendDayVar.grid(row=7, column=2)

        self.poibeginHourVar = Entry(f1)
        self.poibeginHourVar.grid(row=8, column=1)
        self.poiendHourVar = Entry(f1)
        self.poiendHourVar.grid(row=8, column=2)

        self.poibeginMinVar = Entry(f1)
        self.poibeginMinVar.grid(row=9, column=1)
        self.poiendMinVar = Entry(f1)
        self.poiendMinVar.grid(row=9, column=2)

        self.poibeginSecondVar = Entry(f1)
        self.poibeginSecondVar.grid(row=10, column=1)
        self.poiendSecondVar = Entry(f1)
        self.poiendSecondVar.grid(row=10, column=2)


        button = Button(f1, text = "Apply Filter", command = self.applyDetailFilter)
        button.grid(row = 8, column = 0)

        button2 = Button(f1, text = "Reset Filter", command = self.resetDetailFilter)
        button2.grid(row = 10, column = 0)


        self.poitree = ttk.Treeview(self.poiDetailPage)

        self.poitree["columns"] = ("Type","DataValue","DateTime")
        self.poitree.column("Type", width = 100)
        self.poitree.column("DataValue", width = 100)
        self.poitree.column("DateTime", width= 100)

        self.poitree.heading("#0", text='Number', anchor='w')
        self.poitree.column("#0", anchor="w")
        self.poitree.heading("Type", text = "Type")
        self.poitree.heading("DataValue", text="DataValue")
        self.poitree.heading("DateTime", text="DateTime")

        self.poitree.grid(row = 20, column = 0)

        cpt = 0
        for row in self.curs.fetchall():
            self.poitree.insert('', 'end', text=str(cpt), values=(row[0], row[1], row[2]))
            cpt += 1

    def viewPOIBack(self):
        self.FS.destroy()
        self.CF.deiconify()

    def poiBack(self):
        self.DfilterSQL = ("SELECT Type, DataValue, DateTime FROM DATAPOINT WHERE ACCEPTED =1 AND LocationName = ")
        self.poiDetailPage.destroy()
        self.FS.deiconify()

    def poiFlag(self):

        sql = ("UPDATE POI SET FLAGGED = 1 WHERE LocationName = (%s)")
        data = self.viewPOIClick
        self.curs.execute(sql,data)
        messagebox.showerror("Flagged", "The POI has been flagged")

        pass

    def applyDetailFilter(self):
        sql = ("SELECT Type, DataValue, DateTime FROM DATAPOINT WHERE ACCEPTED =1 AND LocationName = " + str(self.viewPOIClick))


        if self.poiTypeSelection.get()!= "":
             sql+= " AND TYPE = '"+ self.poiTypeSelection.get()+"'"


        self.initialTime = str(self.poibeginYearVar.get()) + "-" + str(self.poibeginMonthVar.get()) + "-" + str(
            self.poibeginDayVar.get()) + " " + str(self.poibeginHourVar.get()) + ":" + str(self.poibeginMinVar.get())+":"+ str(self.poibeginSecondVar.get())
        self.finalTime = str(self.poiendYearVar.get()) + "-" + str(self.poiendMonthVar.get()) + "-" + str(
            self.poiendDayVar.get()) + " " + str(self.poiendHourVar.get()) + ":" + str(self.poiendMinVar.get())+":"+ str(self.poiendSecondVar.get())

        if self.initialTime == "-- ::" and self.finalTime == "-- ::":
            pass
        elif self.initialTime == "-- ::":
            sql += " AND DATETIME <= '" + self.finalTime + "' "
        elif self.finalTime == "-- ::":
            sql += " AND DATETIME >= '" + self.initialTime + "' "
        else:
            sql += " AND DATETIME BETWEEN '" + stself.initialTime + "' AND '" + self.finalTime + "' "
        if self.initialdataValEntry.get() == "" and self.finaldataValEntry.get() == "":
            pass
        elif self.initialdataValEntry=="":
            sql+= " AND DATAVALUE <= " + self.finaldataValEntry.get()
        elif self.finaldataValEntry =="":
            sql += " AND DATAVALUE >= " + self.initialdataValEntry.get()
        else:
            sql += " AND DATAVALUE BETWEEN " + self.initialdataValEntry.get() + " AND " + self.finaldataValEntry.get()




        self.DfilterSQL=sql
        self.poiDetailPage.destroy()
        self.poiDetail('')

    def resetDetailFilter(self):
        self.DfilterSQL = ("SELECT Type, DataValue, DateTime FROM DATAPOINT WHERE ACCEPTED =1 AND LocationName = ")

        self.poiDetailPage.destroy()
        self.poiDetail('')

    def applyFilter(self):
        sql = "SELECT * FROM POI"

        self.initialTime = str(self.beginYearVar.get()) + "-" + str(self.beginMonthVar.get()) + "-" + str(
            self.beginDayVar.get())
        self.finalTime = str(self.endYearVar.get()) + "-" + str(self.endMonthVar.get()) + "-" + str(
            self.endDayVar.get())
        if self.POILocationName.get() != "":
            sql += " WHERE LOCATIONNAME = '" + self.POILocationName.get()[2:-3] + "' "
        else:
            sql += " WHERE LOCATIONNAME IS NOT NULL "
        if self.cityPOI.get() != "":
            sql += "AND CITY = '" + self.cityPOI.get()[2:-3] + "' "
        else:
            sql += "AND CITY IS NOT NULL "
        if self.statePOI.get() != "":
            sql += "AND STATE = '" + self.statePOI.get()[2:-3] + "' "
        else:
            sql += "AND STATE IS NOT NULL "
        if self.zipPOI.get() != "":
            sql += "AND ZIPCODE = '" + self.zipPOI.get() + "' "
        else:
            sql += "AND ZIPCODE IS NOT NULL "
        if self.flaggedPOI.get() == "Y":
            sql += "AND FLAGGED = 1 "
        elif self.flaggedPOI.get() == "N":
            sql += "AND FLAGGED = 0 "
        else:
            sql += "AND FLAGGED IS NOT NULL "
        if self.initialTime == "--" and self.finalTime == "--":
            pass
        elif self.initialTime == "--":
            sql += "AND DATEFLAGGED <= '" + self.finalTime + "' "
        elif self.finalTime == "--":
            sql += "AND DATEFLAGGED >= '" + self.initialTime + "' "
        else:
            sql += "AND DATEFLAGGED BETWEEN '" + self.initialTime + "' AND '" + self.finalTime + "' "


        self.filterSQL = sql
        self.FS.destroy()
        self.animalSearch()
        pass

    def resetFilter(self):
        self.filterSQL = "SELECT * FROM POI"
        self.FS.destroy()
        self.animalSearch()
        pass

    def poiReport(self):

        self.reportPage = Toplevel(self.CF)
        self.CF.iconify()

        title = Label(self.reportPage, text = "POI Report")
        title.grid(row = 0, column = 0)

        f1 = Frame(self.reportPage, height=100, width=100, bd=1, relief=SUNKEN)
        f1.grid(row = 5, column = 0)



        self.reporttree = ttk.Treeview(self.reportPage)

        self.curs.execute(self.reportSQL)

        self.reporttree["columns"] = ("LocationName","City","State","Mold Min", "Mold Avg", "Mold Max", "AQ Min", "AQ Avg",
                                      "AQ Max", "# of DataPoints", "Flagged")
        self.reporttree.column("LocationName", width = 100)
        self.reporttree.column("City", width = 100)
        self.reporttree.column("State", width= 100)
        self.reporttree.column("Mold Min", width = 100)
        self.reporttree.column("Mold Avg", width = 100)
        self.reporttree.column("Mold Max", width = 100)
        self.reporttree.column("AQ Min", width = 100)
        self.reporttree.column("AQ Avg", width = 100)
        self.reporttree.column("AQ Max", width = 100)
        self.reporttree.column("# of DataPoints", width = 100)
        self.reporttree.column("Flagged", width = 100)


        self.reporttree.heading("#0", text='Number', anchor='w')
        self.reporttree.column("#0", anchor="w")
        self.reporttree.heading("LocationName", text = "LocationName")
        self.reporttree.heading("City", text="City")
        self.reporttree.heading("State", text="State")
        self.reporttree.heading("Mold Min", text="Mold Min")
        self.reporttree.heading("Mold Avg", text = "Mold Avg")
        self.reporttree.heading("Mold Max", text = "Mold Max")
        self.reporttree.heading("AQ Min", text = "AQ Min")
        self.reporttree.heading("AQ Avg", text = "AQ Avg")
        self.reporttree.heading("AQ Max", text = "AQ Max")
        self.reporttree.heading("# of DataPoints", text = "# of DataPoints")
        self.reporttree.heading("Flagged", text = "Flagged")
        self.reporttree.grid(row = 20, column = 0)

        cpt = 0
        for row in self.curs.fetchall():

            self.reporttree.insert('', 'end', text=str(cpt), values=(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10]))
            cpt += 1
        self.reporttree.bind("<Double-1>", self.poiReport)

        button = Button(self.reportPage, text = "Back", command = self.reportBack)
        button.grid(row = 50, column = 0)


    #--------------------------------------# VISITOR FUNCTIONALITIES---------------------------------------------------------

    def addNewDataPoint(self):  # add a new Data Point for scientist functionality
        self.start()
        self.root.iconify()
        self.NDP = Toplevel(self.root)

        title = Label(self.NDP, text="Add New Data Point")
        title.grid(row=0, column=0)
        locationNameLabel = Label(self.NDP, text="POI Location Name")
        locationNameLabel.grid(row=1, column=0)

        yearLabel = Label(self.NDP, text="Year(YYYY):")
        yearLabel.grid(row=2, column=0)
        monthLabel = Label(self.NDP, text="Month(MM)")
        monthLabel.grid(row=3, column=0)
        dayLabel = Label(self.NDP, text="Day(DD)")
        dayLabel.grid(row=4, column=0)
        hourLabel = Label(self.NDP, text="Hour(HH):")
        hourLabel.grid(row=5, column=0)
        minuteLabel = Label(self.NDP, text="Minute(MM):")
        minuteLabel.grid(row=6, column=0)

        self.yearValue = Entry(self.NDP, width=4)
        self.yearValue.grid(row=2, column=1)
        self.monthValue = Entry(self.NDP, width=2)
        self.monthValue.grid(row=3, column=1)
        self.dayValue = Entry(self.NDP, width=2)
        self.dayValue.grid(row=4, column=1)
        self.hourValue = Entry(self.NDP, width=2)
        self.hourValue.grid(row=5, column=1)
        self.minuteValue = Entry(self.NDP, width=2)
        self.minuteValue.grid(row=6, column=1)

        dataTypeLabel = Label(self.NDP, text="Data Type")
        dataTypeLabel.grid(row=7, column=0)
        dataValue = Label(self.NDP, text="Data Value")
        dataValue.grid(row=8, column=0)

        self.curs.execute("SELECT LocationName FROM POI")
        lvals = self.curs.fetchall()

        self.POILocationSelection = StringVar()
        poiOption = OptionMenu(self.NDP, self.POILocationSelection, *lvals)  # TODO: get these values
        poiOption.grid(row=1, column=1)

        self.curs.execute("SELECT Type FROM DATATYPE")
        tvals = self.curs.fetchall()
        self.dataTypeSelection = StringVar()
        dataType = OptionMenu(self.NDP, self.dataTypeSelection, tvals[0], tvals[1])
        dataType.grid(row=7, column=1)

        self.dataValueEntry = Entry(self.NDP, width=50)
        self.dataValueEntry.grid(row=8, column=1)

        button = Button(self.NDP, text="Back", command=self.DPBack)
        button.grid(row=9, column=0)
        button2 = Button(self.NDP, text="Submit", command=self.DPSubmit)
        button2.grid(row=9, column=1)

        button3 = Button(self.NDP, text="Add New POI Location", command=self.addNewPOILocation)
        button3.grid(row=1, column=3)

    def DPBack(self):
        self.NDP.destroy()
        self.root.deiconify()

    def DPSubmit(self):
        self.start()
        t = "{0}-{1}-{2} {3}:{4}".format(self.yearValue.get(), self.monthValue.get(), self.dayValue.get(),
                                         self.hourValue.get(),
                                         self.minuteValue.get())
        sql = "INSERT INTO DATAPOINT (LocationName, DateTime, DataValue, Type) VALUES (%s, %s, %s, %s)"
        a = (self.POILocationSelection.get())
        b = a[2:-3]
        c = (self.dataTypeSelection.get())
        d = c[2:-3]
        data = (b, t, self.dataValueEntry.get(), d)
        try:
            self.curs.execute(sql, data)
            messagebox.showerror("Success", "Submitted.")
        except:
            messagebox.showerror("Error", "There was an issue with your input. Please try again.")

    def addNewPOILocation(self):  # add new POI LOCATION for scientist functionality
        self.start()
        self.NPL = Toplevel(self.NDP)
        self.NDP.iconify()
        self.NPL.geometry('550x550+0+0')

        title = Label(self.NPL, text="Add a New Location")
        title.grid(row=0, column=0)

        locationNameLabel = Label(self.NPL, text="POI Location Name")
        locationNameLabel.grid(row=1, column=0)
        cityLabel = Label(self.NPL, text="City")
        cityLabel.grid(row=2, column=0)
        stateLabel = Label(self.NPL, text="State")
        stateLabel.grid(row=3, column=0)
        zipLabel = Label(self.NPL, text="Zip Code:")
        zipLabel.grid(row=4, column=0)

        self.newPOILocation = Entry(self.NPL, width=50)
        self.newPOILocation.grid(row=1, column=1)

        self.curs.execute("SELECT CITY FROM CITYSTATE")
        cvals = self.curs.fetchall()

        self.newPLCity = StringVar()
        cityMenu = OptionMenu(self.NPL, self.newPLCity, cvals[0], cvals[1], cvals[2], cvals[3], cvals[4], cvals[5],
                              cvals[6],
                              cvals[7], cvals[8], cvals[9], cvals[2], cvals[10], cvals[11], cvals[12], cvals[13],
                              cvals[14], cvals[15], cvals[16],
                              cvals[17], cvals[18], cvals[19], cvals[20])
        cityMenu.grid(row=2, column=1)

        self.curs.execute("SELECT STATE FROM CITYSTATE")
        svals = self.curs.fetchall()
        self.newPLState = StringVar()
        stateMenu = OptionMenu(self.NPL, self.newPLState, svals[0], svals[1], svals[2], svals[3], svals[4],
                               svals[6],
                               svals[10], svals[11], svals[12], svals[13], svals[14], svals[15],
                               svals[20])
        stateMenu.grid(row=3, column=1)

        self.zipEntry = Entry(self.NPL, width=10)
        self.zipEntry.grid(row=4, column=1)

        button = Button(self.NPL, text="Back", command=self.POIBack)
        button.grid(row=5, column=0)

        button2 = Button(self.NPL, text="Submit", command=self.POISubmit)
        button2.grid(row=5, column=1)

        # Functions for buttons in Add New POI Location

    def POIBack(self):
        self.NPL.destroy()
        self.NDP.deiconify()
        self.NDP.destroy()
        self.addNewDataPoint()

    def POISubmit(self):  # TODO TEST THIS WITH THE DB
        self.start()
        sql = "INSERT INTO POI (LocationName, ZipCode, City, State) VALUES (%s, %s, %s, %s)"
        a = (self.newPLCity.get())
        b = a[2:-3]
        c = (self.newPLState.get())
        d = c[2:-3]
        data = (self.newPOILocation.get(), self.zipEntry.get(), b, d)
        try:
            self.curs.execute(sql, data)
            messagebox.showerror("Success", "Submitted.")
            self.POIBack()
        except:
            messagebox.showerror("Error", "There was an issue with your input. Please try again.")

# ---------------------------------------------- Admin Functionalities-------------------------------------------------

    def adminFunctionalities(self):
        self.root.iconify()
        self.AF = Toplevel(self.root)
        self.AF.geometry('350x350+0+0')

        funcLabel = Label(self.AF, text = "Choose Functionality")
        funcLabel.grid(row = 0, column = 0)

        button = Button(self.AF, text = "Pending Data Points", command = self.acceptOrRejectData)
        button.grid(row = 1, column = 0)

        button2 = Button(self.AF, text = "Pending City Official Accounts", command = self.acceptOrRejectAccount)
        button2.grid(row = 2, column = 0)

        button3 = Button(self.AF, text = "Logout", command = self.logoutA)
        button3.grid(row = 3, column = 0)

    def logoutA(self):
        self.AF.destroy()
        self.root.deiconify()

    def acceptOrRejectData(self):
        self.dataPointVar = ""
        self.AD = Toplevel(self.AF)
        self.AF.iconify()
        self.start()

        self.datatree = ttk.Treeview(self.AD)

        self.curs.execute(self.sortingData)

        self.datatree["columns"] = ("LocationName", "DateTime", "DataValue", "Accepted", "Type")
        self.datatree.column("LocationName", width=100)
        self.datatree.column("DateTime", width=100)
        self.datatree.column("DataValue", width=100)
        self.datatree.column("Accepted", width=100)
        self.datatree.column("Type", width=100)

        self.datatree.heading("#0", text='Number', anchor='w')
        self.datatree.column("#0", anchor="w")
        self.datatree.heading("LocationName", text="LocationName")
        self.datatree.heading("DateTime", text="DateTIme")
        self.datatree.heading("DataValue", text="DataValue")
        self.datatree.heading("Accepted", text="Accepted")
        self.datatree.heading("Type", text="Type")
        self.datatree.grid(row=1, column=0)

        f1 = Frame(self.AD, height=100, width=100, bd=1, relief=SUNKEN)
        f1.grid(row=1, column=1)

        f2 = Frame(self.AD, height=100, width=100, bd=1, relief=SUNKEN)
        f2.grid(row=1, column=2)

        f3 = Frame(self.AD, height=100, width=100, bd=1, relief=SUNKEN)
        f3.grid(row=2, column=1)


        button = Button(f3, text="Back", command=self.adBack)
        button.pack(side=LEFT)
        button2 = Button(f3, text="Accept", command=self.adAccept)
        button2.pack(side=LEFT)
        button3 = Button(f3, text="Reject", command=self.adReject)
        button3.pack(side=LEFT)

        cpt = 0
        for row in self.curs.fetchall():
            self.datatree.insert('', 'end', text=str(cpt), values=(row[0], row[1], row[2], row[3], row[4]))
            cpt += 1
        self.datatree.bind("<Double-1>", self.OnDoubleClickTwo)

    def OnDoubleClickTwo(self, event):
        self.start()
        curItem = self.datatree.focus()
        var = self.datatree.item(curItem)
        self.dataPointVar = var['values'][0]
        self.dateTimeVar = var['values'][1]

    def adBack(self):
        self.AD.destroy()
        self.AF.deiconify()

    def adAccept(self):
        sql = "UPDATE DATAPOINT SET ACCEPTED = 1 WHERE (LocationName, DateTime) = (%s, %s)"
        data = (self.dataPointVar, self.dateTimeVar)
        try:
            self.curs.execute(sql, data)
            self.AD.destroy()
            self.acceptOrRejectData()
        except:
            messagebox.showerror("Error","No Data Point Selected")

    def adReject(self):
        sql = "UPDATE DATAPOINT SET ACCEPTED = 0 WHERE (LocationName, DateTime) = (%s, %s)"
        data = (self.dataPointVar, self.dateTimeVar)
        try:
            self.curs.execute(sql, data)
            self.dataPointVar=""
            self.AD.destroy()
            self.acceptOrRejectData()
        except:
            messagebox.showerror("Error","No Data Point Selected")

    def acceptOrRejectAccount(self):
        self.useradminVar=""
        self.AR = Toplevel(self.AF)
        self.AF.iconify()
        self.start()

        self.tree = ttk.Treeview(self.AR)

        self.curs.execute(self.sortingSQL)

        self.tree["columns"] = ("Username", "Title", "Approved", "City", "State")
        self.tree.column("Username", width = 100)
        self.tree.column("Title", width = 100)
        self.tree.column("Approved", width= 100)
        self.tree.column("City", width = 100)
        self.tree.column("State", width = 100)

        self.tree.heading("#0", text='Number', anchor='w')
        self.tree.column("#0", anchor="w")
        self.tree.heading("Username", text = "Username")
        self.tree.heading("Title", text="Title")
        self.tree.heading("Approved", text="Approved")
        self.tree.heading("City", text="City")
        self.tree.heading("State", text = "State")
        self.tree.grid(row = 1, column = 0)

        f1 = Frame(self.AR, height=100, width=100, bd=1, relief=SUNKEN)
        f1.grid(row = 1, column = 1)

        f2 = Frame(self.AR, height = 100, width = 100, bd = 1, relief = SUNKEN)
        f2.grid(row = 1, column = 2)

        f3 = Frame(self.AR, height=100, width=100, bd=1, relief=SUNKEN)
        f3.grid(row=2, column=1)



        button = Button(f3, text = "Back", command = self.arBack)
        button.pack(side = LEFT)
        button2 = Button(f3, text = "Accept", command = self.arAccept)
        button2.pack(side = LEFT)
        button3 = Button(f3, text = "Reject", command = self.arReject)
        button3.pack(side = LEFT)

        cpt = 0
        for row in self.curs.fetchall():
            self.tree.insert('', 'end', text=str(cpt), values=(row[0],row[1], row[2], row[3], row [4]))
            cpt += 1
        self.tree.bind("<Double-1>", self.OnDoubleClick)

    def OnDoubleClick(self, event):
        self.start()
        curItem = self.tree.focus()
        var = self.tree.item(curItem)
        self.useradminVar = var['values'][0]

    def arBack(self):
        self.AR.destroy()
        self.AF.deiconify()

    def arAccept(self):
        sql = "UPDATE CITYOFFICIAL SET APPROVED = 1 WHERE Username = (%s) "
        data = self.useradminVar

        try:
            self.curs.execute(sql, data)
            self.AR.destroy()
            self.acceptOrRejectAccount()
        except:
            messagebox.showerror("No User Selected","No User Selected")

    def arReject(self):
        sql = "UPDATE CITYOFFICIAL SET APPROVED = 0 WHERE Username = (%s)"
        data = self.useradminVar

        try:
            self.curs.execute(sql, data)
            self.useradminVar=""
            self.AR.destroy()
            self.acceptOrRejectAccount()

        except:
            messagebox.showerror("No User Selected","No User Selected")

    #-----------------------------------------------------------------------------------------------------------------

    def start(self):
        try:
            print("right before connect")
            self.db = pymysql.connect(host='academic-mysql.cc.gatech.edu', user='cs4400_group50', passwd='OSWoWvq2', db='cs4400_group50')
            #                           db='cs4400_group50')
            self.curs = self.db.cursor()
            print("finished connecting")
            return self.curs

        except:

            messagebox.showerror('Error!', 'There was an error with this connection, check your internet connection.')


def main(args):
    root = Tk()
    app = GUI(root)
    root.title("Login Screen")
    root.mainloop()


if __name__ == "__main__":
    import sys

    main(sys.argv)

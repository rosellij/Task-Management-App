# Hello UMSI application reviewers!
# Here attached is a little project I've been working on over winter break after completing SI 106,
# coloquially referred to as the "Panic Calendar."
# The idea was born from me using Todoist;
# I enjoy the application a great deal, but found it didn't suit all of my needs.

# So I began building my own task management application,
# taking some cues from Todoist, such as the simplicity of defining a task's deadline (soon to be implemented)
# as well as some of the sorting features of it into projects (here implemented as "tags"),
# but I've also introduced some new concepts; for instance, the priority of projects will rise exponentially over time,
# because I feel issues that I've been ignoring for a long time are the most pressing.

# Try invoking some of the functions at the bottom!
# Scroll down to 'STANDARD USE FUNCTIONS,' call initiateAndCheckTextFile(), checkAndUpdateRepeats(),
# and then either getUserInput() (if you'd like to create a new task),
# giveResults() (if you'd like to see which tasks have already been created sorted by order of task urgency score,)
# or repeatRequest() (which tells the program that a task should be re-created at a certain interval, such as a weekly meeting).

# Thank you for giving the Panic Calendar ™ a good look, and thank you again for considering my application!

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

# Box for the requisite modules

import time # for our time calculations
import json # for packing/unpacking data
from os import getcwd # for having the file initiate tell you the filetype
import calendar # specifically used for calendar.timegm()

# Box for the rest of us

#importance = 0
#urgency = 0
#priority = 0
#size = 0
#impact = 0
#timedateyear = time.asctime(time.gmtime())
#timezone = 'get time zone from time module'

#creationNotice = 'A new text file has been created! OR A text file has been found and initiated!'
#entry = 'whatever entry we will be fetching from the .txt file'

def logarithmic(arg): return arg # logarithmic growth, implement later

def exponential(xvarExp, avarExp = 6, bvarExp = 100): 
    
    def upperLimit(avarUp = 6, bvarUp = 100, gvarUp = 2): return (gvarUp*(bvarUp**2))/((2**avarUp)+(gvarUp*bvarUp))

    if xvarExp < upperLimit(avarUp = avarExp, bvarUp = bvarExp):
        
        return (-1*((2**avarExp)/(xvarExp-bvarExp)))-((2**avarExp)/bvarExp)

    if xvarExp >= upperLimit(avarUp = avarExp, bvarUp = bvarExp):
    
        return 2

def linear(arg): return arg # linear growth

def orderingFunc(arg): # takes a single entry from list(readvar.items()) and returns the final odering value for a given entry in readvar
    
    if arg[1]['variables']['urgency']['nature'] != 2:
    
        return ((arg[1]['variables']['importance'] + 3) + 1.5*(arg[1]['variables']['priority'] + 3) + 0.75*(arg[1]['variables']['size'] + 3) + (arg[1]['variables']['impact'] + 3) + 2*(arg[1]['variables']['urgency']['value'] + 3))
    
    elif arg[1]['variables']['urgency']['nature'] == 2:
        
        return ((arg[1]['variables']['importance'] + 3) + 1.5*(arg[1]['variables']['priority'] + 3) + 0.75*(arg[1]['variables']['size'] + 3) + (arg[1]['variables']['impact'] + 3) + 2*(arg[1]['variables']['urgency']['value'] + 3)) - 50

def initiateAndCheckTextFile(): # operational! will either create panic.json or load/read/interpret panic.json, also filters out old entries from panic.json
    
    try: 
        createvar = open('panic.json','x')
        createvar.close()
        writevar = open('panic.json', 'a')
        writevar.write('''{}
                       ''')
        writevar.close()
        
        return_message = 'A new panic.json file has been successfully created in {}!'.format(getcwd())
    except:
        return_message = 'panic.json file has been found in {} and initiated!'.format(getcwd())
    
    global readvar
    readvar = json.loads(open('panic.json','r').read())
    open('panic.json','r').close()
    
    try: 
        createvar = open('panicarchive.json','x')
        createvar.close()
        writevar = open('panicarchive.json', 'a')
        writevar.write('''{}
                   ''')
        writevar.close()
        
        return_message1 = 'A new panicarchive.json file has been successfully created in {}!'.format(getcwd())
    except:
        return_message1 = 'panicarchive.json file has been found in {} and initiated!'.format(getcwd())
    
    global archivevar
    archivevar = json.loads(open('panicarchive.json','r').read())
    open('panicarchive.json','r').close()
    
    oldStuffExists = True # this sequence deletes any entries from readvar with a deadline older than the present
    while oldStuffExists == True:
        
        oldFound = False
        for anyentry in readvar:
            if calendar.timegm(time.strptime(readvar[anyentry]['variables']['deadline'])) < time.time():
                del readvar[anyentry]
                oldFound = True
                break
                
        if oldFound == False:  
            oldStuffExists = False
            
        elif oldFound == True:
            continue
    
    return return_message + ' ADDITIONALLY: ' + return_message1

def saveToText(): # operational! saves workingentryvar to panic.json

    # will be a dict taken from 'arg' in the final version I guess
    writevar = open('panic.json','w')
    readvar[list(workingentryvar.keys())[0]] = {'variables': workingentryvar[list(workingentryvar.keys())[0]]['variables']}
    writevar.write(json.dumps(readvar))
    writevar.close()
    
    return 'Task has been saved to panic.json' # saves the given event to the text file, to be accessed later

def checkAndUpdateRepeats():
    
    global readvar
    global archivevar
    
    for anyentry in readvar:
        try:
            createtime = calendar.timegm(time.strptime(readvar[anyentry]['variables']['createtime']))
            deadline = calendar.timegm(time.strptime(readvar[anyentry]['variables']['deadline']))
            interval = readvar[anyentry]['variables']['repeat']['interval']
            repetitions = readvar[anyentry]['variables']['repeat']['repetitions']
            timevar = (time.time()-createtime)/interval

            keeplooking = True
            while keeplooking == True:    
                if timevar >= 0 and timevar < 1:
                    keeplooking = False
                elif timevar >= 1:
                    createtime += int(timevar)*interval
                    deadline += int(timevar)*interval
                    repetitions -= int(timevar)
                timevar = (time.time()-createtime)/interval

            readvar[anyentry]['variables']['createtime'] = time.strftime('%a %b %d %H:%M:%S %Y', time.gmtime(createtime))
            readvar[anyentry]['variables']['deadline'] = time.strftime('%a %b %d %H:%M:%S %Y', time.gmtime(deadline))
            readvar[anyentry]['variables']['repeat']['interval'] = interval
            readvar[anyentry]['variables']['repeat']['repetitions'] = repetitions
            
            archivevar[anyentry]['variables']['createtime'] = time.strftime('%a %b %d %H:%M:%S %Y', time.gmtime(createtime))
            archivevar[anyentry]['variables']['deadline'] = time.strftime('%a %b %d %H:%M:%S %Y', time.gmtime(deadline))
            archivevar[anyentry]['variables']['repeat']['interval'] = interval
            archivevar[anyentry]['variables']['repeat']['repetitions'] = repetitions

            writevar = open('panic.json','w')
            writevar.write(json.dumps(readvar))
            writevar.close()
            writevar1 = open('panicarchive.json','w')
            writevar1.write(json.dumps(archivevar))
            writevar1.close()

        except:
            pass
        
    return 'Repeats have been successfully updated!'

def fetchFromText(arg, fetchFromArchive = False): # operational! for searching part of or all of an entry name in readvar

    global fetchedentryvar
    fetchedentryvar = {}
    workingbool = False
    workingbool1 = False
    
    if fetchFromArchive == False:
        try:
            for anyentry in readvar:
                if arg.lower() in anyentry.lower() or arg.lower() in readvar[anyentry]['variables']['tags']:
                    fetchedentryvar[anyentry] = readvar[anyentry]
                    workingbool = True
            if workingbool == True:
                return fetchedentryvar # gets a given event from the text file
            elif workingbool == False:
                raise Exception('No exact match found for the search term!')
    
        except:
            raise Exception('No exact match found for the search term!')
            
    if fetchFromArchive == True:
        try:
            for anyentry in archivevar:
                if arg.lower() in anyentry.lower() or arg.lower() in archivevar[anyentry]['variables']['tags']:
                    fetchedentryvar[anyentry] = archivevar[anyentry]
                    workingbool1 = True
            if workingbool1 == True:
                return fetchedentryvar # gets a given event from the text file
            elif workingbool1 == False:
                raise Exception('No exact match found for the search term!')
    
        except:
            raise Exception('No exact match found for the search term!')
    
def createTask(title, deadline, descript=None, importance=None, priority=None, size=None, impact=None, nature=None, createtime=None, tags=None, repeat=None): # operational! sets workingentryvar to the task being created
    
    global workingentryvar
    if createtime == None:
        createtimeVar = time.asctime(time.gmtime())
    elif createtime != None and type(createtime) == str:
        createtimeVar = createtime
    workingentryvar = {title: {'variables': {'createtime': createtimeVar, 'deadline': deadline, 'descript': descript, 'importance': importance, 'priority': priority, 'size': size, 'impact': impact, 'urgency': {'value': None, 'nature': nature}, 'tags': tags, 'repeat': repeat}}}
    
    writevar = open('panicarchive.json','w')
    archivevar[list(workingentryvar.keys())[0]] = {'variables': workingentryvar[list(workingentryvar.keys())[0]]['variables']}
    writevar.write(json.dumps(archivevar))
    writevar.close()
    
    return workingentryvar

def getUserInput(manualMode = False): # operational! asks for user input, interprets that information into task format, and saves that task to panic.json
    
    tasktitle = input('Enter title for this task:')
    taskdeadline = time.asctime(time.gmtime(time.mktime(time.strptime(input('Enter deadline for this task as "Day Mon DD HH:mm:ss YYYY":')))))
    taskdescript = input('Enter a description for this task, or type "0" to pass:')
    taskimportance = input('Enter a task importance level (with -2 as very unimportant and 2 as very important), or type "0" to pass:')
    taskpriority = input('Enter a task override priority level (with -2 as notably devalue this task and 2 as notably add value to this task), or type "0" to pass:')
    tasksize = str(-1*int(input('Enter a task size level (with -2 as very small and 2 as very large), or type "0" to pass:')))
    taskimpact = input('Enter a task impact level (with -2 as very litte impact and 2 as very much impact), or type "0" to pass:')
    tasknature = input('Enter the importance of this task should grow, with "0" for linearly, "1" for exponentially, or "2" to shove it to the bottom:')
    tasktags = input("""If you have any tags you'd like to put here, type them separated by ~ or type "0" to pass""").lower().split('~')
    if manualMode == True:
        taskcreatetime = input('Enter when this task should start:')
    elif manualMode == False:
        taskcreatetime = None
    
    initiateAndCheckTextFile()
    createTask(title = tasktitle, deadline = taskdeadline, descript = taskdescript, importance = float(taskimportance), priority = float(taskpriority), size = float(tasksize), impact = float(taskimpact), nature = int(tasknature), createtime = taskcreatetime, tags = tasktags)
    saveToText()
    
    return 'Entry received and input!'

def giveResults(): # operational! prints out tasks from readvar in organized order
    
    initiateAndCheckTextFile()
    
    for anyentry in readvar: # adds an urgency variable to readvar entries
        (createtime, currenttime, deadline) = ((calendar.timegm(time.strptime(readvar[anyentry]['variables']['createtime']))), time.time(), (calendar.timegm(time.strptime(readvar[anyentry]['variables']['deadline']))))
        try: # temporary caveat since I am lazy and didn't update old entries with nature data
            if readvar[anyentry]['variables']['urgency']['nature'] == 0:
                readvar[anyentry]['variables']['urgency']['value'] = 2*(((2)/(deadline-createtime))*(currenttime-createtime))-2
            elif readvar[anyentry]['variables']['urgency']['nature'] == 1:
                readvar[anyentry]['variables']['urgency']['value'] = 2*(exponential(xvarExp = float(100*((currenttime-createtime)/(deadline-createtime))), avarExp = -1*(readvar[anyentry]['variables']['size']) + 4))-2
            elif readvar[anyentry]['variables']['urgency']['nature'] == 2:
                readvar[anyentry]['variables']['urgency']['value'] = -2
        except:
            readvar[anyentry]['variables']['urgency']['value'] = 2*(exponential(xvarExp = float(100*((currenttime-createtime)/(deadline-createtime))), avarExp = -1*(readvar[anyentry]['variables']['size']) + 4))-2
    
    print_list = sorted(list(readvar.items()), key = lambda a : orderingFunc(a), reverse = True)
    for anyentry in print_list:
        anyentry[1]['variables']['createtime'] = time.asctime(time.localtime(calendar.timegm(time.strptime(anyentry[1]['variables']['createtime']))))
        anyentry[1]['variables']['deadline'] = time.asctime(time.localtime(calendar.timegm(time.strptime(anyentry[1]['variables']['deadline']))))
        if round(orderingFunc(anyentry), 2) >= 0:
            printvar = str(round(orderingFunc(anyentry), 2))
        elif round(orderingFunc(anyentry), 2) < 0:
            printvar = '(***PUNISHED***): ' + str(round(orderingFunc(anyentry), 2)) 
        print(printvar + '\n' + str({anyentry[0]: anyentry[1]}) + '\n')
        
def repeatRequest():

    userinput = input('What task would you like to repeat? Input a search term for it here:').lower()
    print(fetchFromText(userinput, fetchFromArchive = True))
    
    userinput = input('Which of these tasks would you like to repeat? Type its name PRECISELY [case-sensitive] as you see above:')
    entryvar = fetchFromText(userinput, fetchFromArchive = True)
    storedname = userinput
    print(entryvar)
    
    done = False
    while done == False:
        userinput = input('Would you like to change any variables in this event? Type a variable name, then ~, and then the new value or simply "done" below:').lower().split('~')
        try:
            userinput = [userinput[0], float(userinput[1])]
        except:
            pass
        if userinput[0] in entryvar[storedname]['variables']:
            entryvar[storedname]['variables'][userinput[0]] = userinput[1]
            print(entryvar[storedname]['variables'][userinput[0]])
        elif userinput[0].lower() == 'done':
            done = True
        else:
            print('Make sure to either input a valid variable name or "done"!')
            #raise Exception('Make sure to either input a valid variable name or "done"!')
        
    userinput = input("In how many hours' interval would you like this event to repeat, and how many times? Type the first value, ~, then the second value:").lower().split('~')
    userinput = [3600*float(userinput[0]), int(userinput[1])]
    initiateAndCheckTextFile()
    createTask(title = storedname, deadline = entryvar[storedname]['variables']['deadline'], descript = entryvar[storedname]['variables']['descript'], importance = entryvar[storedname]['variables']['importance'], priority = entryvar[storedname]['variables']['priority'], size = entryvar[storedname]['variables']['size'], impact = entryvar[storedname]['variables']['impact'], nature = entryvar[storedname]['variables']['urgency']['nature'], tags = entryvar[storedname]['variables']['tags'], repeat = {'interval': userinput[0], 'repetitions': userinput[1]})
    saveToText()
    print('Repetitious task has been created!')

# 'TEST READOUT FUNCTIONS' 
#print(readvar)
#print(workingentryvar)
#print(archivevar)

# 'MANUALLY INPUT DATA FUNCTIONS'
#initiateAndCheckTextFile()
#createTask(title = 'Play Trombone', descript = 0, deadline = 'Fri Dec 25 00:00:00 2020', importance = 2.0, priority = 1.0, size = -1.0, impact = 0.0)
#saveToText()
#fetchFromText('mom', fetchFromArchive = True)
#checkAndUpdateRepeats()
    
# 'STANDARD USE FUNCTIONS'
initiateAndCheckTextFile() # RUN THIS BEFORE ANYTHING
checkAndUpdateRepeats() # RUN THIS BEFORE ANYTHING
#getUserInput()
#giveResults()
#repeatRequest()





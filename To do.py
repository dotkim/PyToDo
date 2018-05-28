import pypyodbc, cmd, sys, os, datetime, pathlib
ScriptDir = os.path.dirname(os.path.realpath('__file__')) # Where the scripts should be placed, which is root


def dbconnection():
    try:
        conString = open('.\Config\ConnectionStrings.config', 'r')
        connection = pypyodbc.connect(conString.read())
        conString.close()
        return connection
    except:
        print('dberror')
        #SysL.write(str(datetime.datetime.now()) + " " + str(sys.exc_info()[0]) + '\n')
        return None
# End of function

def AuditUser(arg, idarg, funcID):
    LogDir = ScriptDir + '\\Logs'
    pathlib.Path(LogDir).mkdir(parents=True, exist_ok=True)
    AuditLog = LogDir + '\\AuditLog' + str(datetime.date.today()) + '.log'
    try:
        AL = open(AuditLog, 'a')
        AL.write(str(datetime.datetime.now()) + ' - TaskID: ' + str(idarg) +  + ' with task: ' + arg + '\n')
        AL.close()
    except FileNotFoundError:
        SysL = open(SysLog, 'a')
        SysL.write(str(datetime.datetime.now()) + 'Failed to create AddLog file' + '\n')
        SysL.close()

def LogAdd(arg, idarg):
    LogDir = ScriptDir + '\Logs'
    pathlib.Path(LogDir).mkdir(parents=True, exist_ok=True)
    AddLog = LogDir + '\AddLog' + str(datetime.date.today()) + '.log'
    SysLog = LogDir + '\SysLog' + str(datetime.date.today()) + '.log'
    try:
        AddL = open(AddLog, 'a')
        AddL.write(str(datetime.datetime.now()) + ' - TASK: ' + arg + ' WITH ID: ' + str(idarg) + '\n')
        AddL.close()
    except FileNotFoundError:
        SysL = open(SysLog, 'a')
        SysL.write(str(datetime.datetime.now()) + 'Failed to create AddLog file' + '\n')
        SysL.close()
# End of function
        
StartCleanUp = 1 # Clean CMD and connectio to DB. Then dont do this again.
if StartCleanUp == 1:
    print('Connecting to Database...')
    connection = dbconnection()
    connection.close()
    os.system('CLS')
    print('Type help for Available commands.')
    StartCleanUp = 0
    

# Start of programm
class TaskForce(cmd.Cmd):
    promt = 'Choice: '

    # All functions are to be listed in help
    def help(self, arg):
        print('------Availabe commands------')
        print('Show')       # Show all current tasks
        print('Add')        # Add a new task
        print('Complete')   # Complete a task
        print('Remove')     # Remove tasks
        print('Close')      # Close the program
    # End of function

    def do_show(self, arg=''):
        os.system('CLS')
        connection = dbconnection()
        c = connection.cursor()
        c.execute('EXEC dbo.GetActiveTasks')
        TaskList = c.fetchall()
        
        for row in TaskList:
            print(row)
        connection.close()
    # End of function

    def do_add(self, arg=1):
        FuncID = 1
        if arg == '':
            arg = 1
        task = []
        connection = dbconnection()
        for i in range(int(arg)):
            task.insert(i, input('Task: '))
            c = connection.cursor()
            c.execute("""
                EXEC dbo.AddTask
                @TaskText = '{TaskText}'
            """.\
            format(TaskText=task[i]))
            # This needs cleanup, add a procedure to the logging file.
#            c.execute("""
 #               SELECT TaskID
  #              FROM dbo.Tasks
   #             WHERE TaskDesc = '{ID}'
    #        """.\
     #       format(ID=task[i]))
      #      TID = c.fetchall()
       #     # Begin logging
        #    AuditUser(task[i], TID[0][0])
            connection.commit()
        connection.close()
        self.do_show()
    # End of function

    def do_complete(self, arg):
        os.system('CLS')
        connection = dbconnection()
        c = connection.cursor()
        c.execute("""
            SELECT TaskID, TaskDesc
            FROM dbo.Tasks
            WHERE IsComplete = 0
        """)
        TaskList = c.fetchall() # Fetch the current active tasks with IDs
        for x in range(0, len(TaskList)):
            print(str(x+1) + ' - ' + TaskList[x][1])
            # Print a list for all the tasks
            
        Choice = int(input('Choice: '))
        c.execute("""
            EXEC dbo.CompleteTask
            @SelectedID = {cid}
        """.\
        format(cid=TaskList[Choice-1][0])) # Find chosen task ID via indexing
        connection.commit()
        connection.close()
        self.do_show()
    # End of function

    def do_remove(self, arg):
        os.system('CLS')
        connection = dbconnection()
        c = connection.cursor()
        c.execute("""
            SELECT TaskID, TaskDesc
            FROM dbo.Tasks
            WHERE IsComplete = 0
        """)
        TaskList = c.fetchall() # Fetch the current active tasks with IDs
        for x in range(0, len(TaskList)):
            print(str(x+1) + ' - ' + TaskList[x][1])
            # Print a list for all the tasks
            
        Choice = int(input('Choice: '))
        c.execute("""
            EXEC dbo.RemoveTask
            @SelectedID = {cid}
        """.\
        format(cid=TaskList[Choice-1][0])) # Find chosen task ID via indexing
        connection.commit()
        connection.close()
        self.do_show()
        
    def do_close(self, arg):
        sys.exit()
    # End of function

if __name__ == '__main__':
    TaskForce().cmdloop()

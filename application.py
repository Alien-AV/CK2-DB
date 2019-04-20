import database
import sys
import texttable

def load_file(file_name,database):
    print('Opening the file '+file_name)
    database.setup(file_name)
    print('\n')

#how many rows every query will return
ROW_COUNT = 40

#main function
if __name__=='__main__':
    #object that maintains connection to database and performs queries
    database = database.Data()
    
    #load data
    print('\nWelcome to the Database Systems Project\n')
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
        load_file(file_name,database)
    
    # main program loop (take commands until quitting)
    print("Type 'help' for help with commands, and 'quit' to exit.")
    command = ''
    query_result = []
    while command not in {'q','quit','exit'}:
        command = input(' : ')     
        if(len(command) == 0):
            continue 
        words = command.lower().split()

        if words[0] == 'help':
            print('Commands:')
            print(' : dynasty <args> [displays information on dynasties]')
            print(' : title <args> [displays information on titles]')
            print(' : person <args> [displays information on characters]')
            print(' : religion <arg> [displays information on religions]')
            print(' : culture <arg> [displays information on cultures]')
            print(' : bloodline <arg> [displays information on bloodlines]')
            print(' : bloodline_members <ID> [displays characters with bloodline of ID ID]')
            print(' : help [displays this text]')
            print(' : num_results <NUM> [changes the number of results displayed to NUM]')
            print(' : load <FILENAME> [loads a file]')
            print(' : quit [exits the program]')


        elif words[0] in {'q','quit','exit'}:
            break

        elif words[0] == 'load' :
            if(len(words) != 2):
                print('ERROR load takes one argument and one argument only')
            else:
                load_file(words[1],database)

        elif words[0] == 'num_results' :
            if(len(words) != 2):
                print('ERROR num_results takes one argument and one argument only')
            else:
                ROW_COUNT = int(words[1])
        
        #dynasty queries  
        elif words[0]=='dynasty':
            if(len(words) %2 != 1):
                print('ERROR: Please have one argument for each command')
                continue            
            query_args = []
            query_arg_vals = []
            i = 1
            allowed_args = {'name', 'orderby', 'religion', 'culture'}
            valid = True
            has_orderby = False
            while i < len(words):
                if(words[i] in allowed_args):
                    valid_vals = {'prestige','piety','wealth','count'}
                    if words[i]=='orderby':
                        if has_orderby:
                            valid = False
                            print('ERROR: Query contained a second orderby term. Queries should contain zero or one orderby term.')
                            break
                        has_orderby = True
                        if words[i+1] not in valid_vals:
                            print('ERROR: ' + words[i+1] + ' is not a valid value to order by. Please use one of:')
                            print(valid_vals)
                            valid = False
                    if valid:
                        query_args.append(words[i])
                        query_arg_vals.append(words[i+1])
                else:
                    print('ERROR: ' + words[i] + ' is not a valid condition, please use one of the following values:')
                    print(allowed_args)
                    valid = False
                i += 2
            #get person with these conditions
            if valid:
                query_result = database.query_dynasty(query_args,query_arg_vals)
                table = texttable.Texttable()
                table.set_max_width(210)
                for i,v in enumerate(query_result):
                    if i > ROW_COUNT: break
                    row = []
                    row.append(i)
                    row = row + [str(x) for x in v]
                    table.add_row(row)
                t = table.draw()
                print(t)
        
        #title queries
        elif words[0]=='title':
            # title on its own returns ???
            if len(words)==1:
                continue
            # title id returns all titles of the given personid
            elif len(words)==2:
                query_results = database.query_title(words[1])
            # we are looking for personID(s) given a certain title
            elif len(words)==3:
                #rulers
                if words[1]=='rulers':
                    query_results = database.query_rulers(words[2])
                #current
                elif words[1]=='current':
                    query_results = database.query_ruler(words[2])
                else:
                    print("Queries should be of the form 'title (rulers|current) titleid.'")
                    continue
            else:
                print('Title queries should be of the form : title personid or title rulers titleid or title current titleid')
                continue                
            for i,d in enumerate(query_results):
                if i > ROW_COUNT: break
                print(' '.join([str(x) for x in d]))            
        
        #person queries
        elif words[0]=='person':
            if(len(words) %2 != 1):
                print('ERROR: Please have one argument for each command')
                continue
            query_args = []
            query_arg_vals = []
            i = 1
            allowed_args = {'name', 'dynasty', 'ismale', 'birthday', 'deathday', 'father', 'real_father', 'mother', 'religion', 'culture', 'fertility', 'health', 'wealth', 'prestige', 'piety'}
            valid = True
            while i < len(words):
                if(words[i] in allowed_args):
                    query_args.append(words[i])
                    query_arg_vals.append(words[i+1])
                else:
                    print('ERROR: ' + words[i] + ' is not a valid condition, please use one of the following values:')
                    print(allowed_args)
                    valid = False
                i += 2
            #get person with these conditions
            if valid:
                table = texttable.Texttable()
                headings = ['#', 'Name', 'Dynasty', 'is Male', 'Birthday', 'Deathday', 'Father', 'Real Father', 'Mother', 'Religion', 'Culture', 'Fertility', 'Health', 'Wealth', 'Prestige', 'Piety']
                table.header(headings)
                table.set_max_width(210)
                query_result = database.query_person(query_args,query_arg_vals)
                for i,v in enumerate(query_result):
                    if i > ROW_COUNT: break
                    row = []
                    row.append(i)
                    row = row + [str(x) for x in v[1:]]
                    table.add_row(row)
                t = table.draw()
                print(t)
        
        #religion
        elif words[0]=='religion':
            if len(words) == 1:
                query_result = database.query_religion()
            elif len(words) == 2:
                valid_args = {'allmembers','alivemembers','provinces'}
                if words[1] not in valid_args:
                    print('Invalid argument. Try one of:')
                    print(valid_args)
                    continue
                query_result = database.query_religion(words[1])
            else:
                print('ERROR: Too many arguments.')
                continue
            table = texttable.Texttable()
            table.set_max_width(210)    
            for i,v in enumerate(query_result):
                if i > ROW_COUNT: break
                row = []
                row.append(i)
                row = row + [str(x) for x in v]
                table.add_row(row)
            t = table.draw()
            print(t)
        
        #culture
        elif words[0]=='culture':
            if len(words) == 1:
                query_result = database.query_culture()
            elif len(words) == 2:
                valid_args = {'allmembers','alivemembers','provinces'}
                if words[1] not in valid_args:
                    print('Invalid argument. Try one of:')
                    print(valid_args)
                    continue
                query_result = database.query_culture(words[1])
            else:
                print('ERROR: Too many arguments.')
                continue
            table = texttable.Texttable()
            table.set_max_width(210)
            for i,v in enumerate(query_result):
                if i > ROW_COUNT: break
                row = []
                row.append(i)
                row = row + [str(x) for x in v]
                table.add_row(row)
            t = table.draw()
            print(t) 

        #bloodlines
        elif words[0]=='bloodline':
            query_args = []
            if(len(words) %2 != 1):
                print('ERROR: Please have one argument for each command')
                continue
            query_arg_vals = []
            i = 1
            allowed_args = {'bloodlinename', 'founderID'}
            valid = True
            while i < len(words):
                if(words[i] in allowed_args):
                    query_args.append(words[i])
                    query_arg_vals.append(words[i+1])
                else:
                    print('ERROR: ' + words[i] + ' is not a valid condition, please use one of the following values:')
                    print(allowed_args)
                    valid = False
                i += 2
            if valid:
                table = texttable.Texttable()
                headings = ['#', 'ID', 'Type', 'Founder']
                table.header(headings)
                table.set_max_width(210)
                query_result = database.query_bloodline(query_args,query_arg_vals)
                for i,v in enumerate(query_result):
                    if i > ROW_COUNT: break
                    row = []
                    row.append(i)
                    row = row + [str(x) for x in v]
                    table.add_row(row)
                t = table.draw()
                print(t)

        elif words[0]=='bloodline_members':
            if(len(words) != 2):
                print('ERROR bloodline_members takes one argument (the id of the bloodline) and one argument only')
            else:
                table = texttable.Texttable()
                headings = ['#', 'Name', 'Dynasty']
                table.header(headings)
                table.set_max_width(210)
                query_result = database.query_bloodline_members(words[1])
                for i,v in enumerate(query_result):
                    if i > ROW_COUNT: break
                    row = []
                    row.append(i)
                    row = row + [str(x) for x in v]
                    table.add_row(row)
                t = table.draw()
                print(t)
            
        else:
            print('ERROR: Unknown command!')
            print("For a list of commands, please enter 'help'")
                        
                    
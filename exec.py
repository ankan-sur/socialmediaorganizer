    #######################################################
    #  Social Media Organizer
    #
    #  open function
    #  read functions + create dict function
    #       collect names, collect friends per name and creates dictionary
    #  find common friends func
    #  find max friends func
    #  find max common friends func
    #  find second friends func
    #  find max second friends func  
    #
    #  main
    #   open files
    #   read files
    #   input for options
    #       option cases 1,2,3,4,5,
    #    error check
    ###########################################################




MENU = '''
 Menu : 
    1: Popular people (with the most friends). 
    2: Non-friends with the most friends in common.
    3: People with the most second-order friends. 
    4: Input member name, to print the friends  
    5: Quit                       '''
    
def open_file(s):
    '''input: a string to tell user what filename needs to be input
       returns: a file pointer for the filename entered
       - runs a try-except to check if file is valid
    '''
    while True:
        inp = input("\nInput a {} file: ".format(s))
        try:
            fp = open(inp)
            return fp
        except FileNotFoundError:
            print("\nError in opening file.")

def read_names(fp):
    '''input: fp from open_file()
       return: list of strings of all names from file
    '''
    list_of_names = []
    for line in fp.readlines():
        line = line.strip() 
        list_of_names.append(line) #append rather than extend to add the list as a single item
    return list_of_names

def read_friends(fp,names_lst):
    '''input: fp to read friends list
              names_lst to find indexes of friends in the list
       return: a list_of_friends which uses index as identifier for the user
    '''
    list_of_friends = []
    for line in fp.readlines():
        line_list = []
        line = line.strip().split(",")
        for i in line:
            i = i.strip()
            if i.isdigit():
                name = names_lst[int(i)] #uses indexing to collect all friends names
                line_list.append(name)
            else:
                continue
        list_of_friends.append(line_list)
    return list_of_friends

def create_friends_dict(names_lst,friends_lst):
    '''input: names_lst and friends_lst to pair up using index values
       returns: dictionary with name to friend pairing
    '''
    dict_of_friends = {}
    for ind,line in enumerate(friends_lst):
        name = names_lst[ind]
        dict_of_friends[name] = line
    return dict_of_friends

def find_common_friends(name1, name2, friends_dict):
    '''input:name1,name2 to find the friend lists
             friends_dict to collect set of friends
        return: set of intersection between both sets of friends 
    '''
    for name,friends in friends_dict.items():
        if name == name1:
            friend_list1 = friends
            friend_list1 = set(friend_list1)
        if name == name2:
            friend_list2 = friends
            friend_list2 = set(friend_list2)
        else:
            continue
    set_of_common = friend_list2 & friend_list1 #set.intersection() method used 
    return set_of_common
    
def find_max_friends(names_lst, friends_lst):
    '''input: names_list to compile list of names with max friends and friends_lst to collect number of friends
        returns: a list of all names who have the max number of friends, and the max number of friends
    '''
    friends_num_list = [] #a list that will hold the number of friends each user has by index
    max_friends_list = [] #a list that will hold all users with the max amount of friends, once that is determined

    for line in (friends_lst): #simply collecting the number of friends 
        num = len(line)        #by using len() for each list of friends
        friends_num_list.append(num)

    max_val = max(friends_num_list) #list comprehension

    for ind,val in enumerate(friends_num_list): 
        name = names_lst[ind]
        if val == max_val: #using iteration to find all names that match max value 
            max_friends_list.append(name)

    return sorted(max_friends_list), max_val

def find_max_common_friends(friends_dict): #my most complex function
    '''input: dictionary of users: list of friends
       returns: a list of all users pairs with the most common friends, and the number of most common friends     
    '''
    max_val = 0
    common_dict = {} #dict of all user pairs to the number of their common friends 
    for A,A_list in friends_dict.items(): #two nested for loops to cover every pair
        for B,B_list in friends_dict.items():
            pair_tup = (A,B)
            if B == A: #ignoring when A appears as a B value
                continue
            set_of_common = find_common_friends(A,B,friends_dict) 
            common_dict[pair_tup] = len(set_of_common) #{(pair tuple): num of common friends}

    for i,j in common_dict.items(): #iteration to find max
        if j>max_val:
            max_val = j

    list_of_names = getKeysByValue(common_dict, max_val) #helper function to collect all keys matching max value, to reduce load

    for i in list_of_names: #another iteration to remove all double appearances of pairs
        if (i[1],i[0]) in list_of_names:
            list_of_names.remove((i[1],i[0]))

    return sorted(list_of_names), max_val

def getKeysByValue(dictOfElements, valueToFind): #helper function to reduce load
    '''input: dict to iterate, valueToFind to gather keys
       returns: a list of keys matching the value given
    '''
    listOfKeys = list()
    listOfItems = dictOfElements.items()
    for item  in listOfItems:
        if item[1] == valueToFind: 
            listOfKeys.append(item[0]) #basic terms and layout 
    return listOfKeys

def find_second_friends(friends_dict):
    '''input: friends_dict with all name to friends information
       returns: a dictionary of names to second friends (friends of friends)'''
    dict_of_second = {}
    for name,list_of_friends in friends_dict.items(): 
        set_of_second = set() 
        for f in list_of_friends:
            second_list = set(friends_dict[f])
            set_of_second.update(second_list) #works like append for set
        for f in list_of_friends:
            try:
                set_of_second.remove(f) #removes primary friends from secondary list
            except:
                continue
        set_of_second.remove(name) #removes main user from list
        dict_of_second[name] = set_of_second #installs secondary list as a key value pair
    return dict_of_second

def find_max_second_friends(seconds_dict): #simplest function
    '''input: seconds_dict with all name to second friend information (friends of friends)
        returns: list of names with most second friends, the number of most second friends
    '''
    names_lst = list(seconds_dict.keys()) #simply extracted list of keys and values to reuse old function to save time
    friends_lst = list(seconds_dict.values())
    max_second_list, max_val = find_max_friends(names_lst, friends_lst)
    return max_second_list, max_val
    

def main():
    print("\nFriend Network\n")
    fp = open_file("names")
    names_lst = read_names(fp)
    fp = open_file("friends")
    friends_lst = read_friends(fp,names_lst)
    friends_dict = create_friends_dict(names_lst,friends_lst)

    print(MENU)
    choice = input("\nChoose an option: ")
    while choice not in "12345":
        print("Error in choice. Try again.")
        choice = input("Choose an option: ")
        
    while choice != '5':

        if choice == "1":
            max_friends, max_val = find_max_friends(names_lst, friends_lst)
            print("\nThe maximum number of friends:", max_val)
            print("People with most friends:")
            for name in max_friends:
                print(name)
                
        elif choice == "2":
            max_names, max_val = find_max_common_friends(friends_dict)
            print("\nThe maximum number of commmon friends:", max_val)
            print("Pairs of non-friends with the most friends in common:")
            for name in max_names:
                print(name)
                
        elif choice == "3":
            seconds_dict = find_second_friends(friends_dict)
            max_seconds, max_val = find_max_second_friends(seconds_dict)
            print("\nThe maximum number of second-order friends:", max_val)
            print("People with the most second_order friends:")
            for name in max_seconds:
                print(name)
                
        elif choice == "4":
            while True: #while loop for the reprompting
                name = input("\nEnter a name: ")
                if name in friends_dict.keys():
                    f_list = friends_dict[name]
                    print("\nFriends of {}:".format(name))
                    for f in f_list:
                        print(f)
                    break
                else:
                    print("\nThe name {} is not in the list.".format(name))
                    
        else: 
            print("Shouldn't get here.")
            
        choice = input("\nChoose an option: ")
        while choice not in "12345":
            print("Error in choice. Try again.")
            choice = input("Choose an option: ")

if __name__ == "__main__":
    main()

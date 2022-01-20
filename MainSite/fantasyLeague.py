def getPlayerCode(name):
    ans=""
    for ch in name:
        if(ch != ' '):
            ans += ch
    return ans

def getEncodedPlayerList(pl):
    ans=[]
    for p in pl:
        ans.append(getPlayerCode(p.name))
    return ans

def isListUnique(test_list):
    flag = 0
    for i in range(len(test_list)): 
        for i1 in range(len(test_list)): 
            if i != i1: 
                if test_list[i] == test_list[i1]: 
                    flag = 1
    return (not flag)

def stringToList(l):
    ans = ""
    for elm in l:
        ans += elm+","
    return ans

class pNum:
    """ class pNum  holds an integer
    it uses a function to check if the number a palindrome
    """
    def __init__(self, n):
        self.num = n
        
    
    def palCheck(self):
        """palcheck checks if the self number is a PALINDROME"""
        if self.num <0: return False
        strnum = str(self.num)
        strlen = len(strnum)
        for i in range(strlen//2):
            j = strlen-i-1
            if strnum[i] != strnum[j]: return False
        return True

    

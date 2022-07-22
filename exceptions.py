class Impossible(Exception):
    '''
    This exception is raised when an action is impossible to perform

    The reason is given as the exception message.
    i.e. raise Impossible("An exception message") 
    '''
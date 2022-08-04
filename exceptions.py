class Impossible(Exception):
    """
    This exception is raised when an action is impossible to perform

    The reason is given as the exception message.
    i.e. raise Impossible("An exception message")
    """


class QuitWithoutSaving(SystemExit):
    """
    This exception should be raised to exit the game without saving.
    i.e. raise QuitWithoutSaving when the player dies.
    """

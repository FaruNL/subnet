from enum import Enum

class Style(Enum):
    '''
    Enumeración para estilos de texto.
    '''
    def __str__(self):
        return str(self.value)
    
    BLACK      = "\u001b[30m"
    RED        = "\u001b[31m"
    GREEN      = "\u001b[32m"
    YELLOW     = "\u001b[33m"
    BLUE       = "\u001b[34m"
    MAGENTA    = "\u001b[35m"
    CYAN       = "\u001b[36m"
    WHITE      = "\u001b[37m"

    BOLD       = "\u001b[1m"
    UNDERLINE  = "\u001b[4m"
    
    RESET      = "\u001b[0m"

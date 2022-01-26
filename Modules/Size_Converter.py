
# To convert bytes to readable size notations
def Converter(Size_Bytes):

    File_Sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB']
    Iter_Counter = 0                                        # To keep track of number of times the size is divided by 1024

    while(Size_Bytes > 1024):
        Size_Bytes = Size_Bytes / 1024                      # No. of times size is divided by 1024 is located in File_Sizes
        Iter_Counter = Iter_Counter + 1

    Final_Size = str( round(Size_Bytes, 2) ) + ' ' + File_Sizes[Iter_Counter]       # Rounding off to 2 decimals and creating final string
    return(Final_Size)
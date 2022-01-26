import psutil

def Get_Avaliable_Drives():
    Avaliable_Drives = []
    for drive in psutil.disk_partitions():
        if drive[-3] != 'cdrom':
            Avaliable_Drives.append( drive[0] )
    
    return Avaliable_Drives

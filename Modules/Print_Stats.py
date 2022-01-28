
def PrintStats(Stats):
    print('Total folders: ', Stats[0])
    print('Total files: ', Stats[1])
    print('Total files and folders: ', Stats[0] + Stats[1])
    print(f'Time taken to execute: {Stats[2] - Stats[3]} Seconds')
    print(f'Average speed: {(Stats[1]) / (Stats[2] - Stats[3])} Entries / Second')
    return

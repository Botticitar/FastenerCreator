import pandas as pd

class Standards:
    standards_table ={'diameter':  [3, 4, 5, 6, 8, 10, 12, 14, 16, 20, 24],
                'head_height': [3, 4, 5, 6, 8, 10, 12, 14, 16, 20, 24],
                'head_diameter': [5.5, 7, 8.5, 10, 13, 16, 18, 21, 24, 30, 36],
                'shank_length_minimum': [5, 6, 8, 10, 12, 16, 20, 25, 25, 30, 40],
                'shank_length_maximum': [30, 40, 50, 60, 80, 100, 120, 140, 160, 200, 200]} 
                #data from ISO 4762, these are MAX values possible, ideally this would come in through the .json 
                #and would be validated in validator, but I wanna keep the .json structure as is in the challenge file    
    standards=pd.DataFrame(standards_table)
    
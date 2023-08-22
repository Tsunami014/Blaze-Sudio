import os

def YesNo(msg):
    out = os.system(f'CHOICE /C YN /M "{msg}"')
    if out != 0 and out != 1:
        return not bool(out)

def save_apis():
    exists = os.path.exists('apis/Bard.apikey')
    
    if YesNo('Do you have an API key for Google\'s Bard AI'):
        print('OK!')

if __name__ == '__main__':
    save_apis()
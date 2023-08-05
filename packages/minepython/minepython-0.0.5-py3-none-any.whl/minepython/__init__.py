from . import verifysign

def login(userName):
    if verifysign.login(userName):
        print('验证成功')
    else:
        print('验证失败')
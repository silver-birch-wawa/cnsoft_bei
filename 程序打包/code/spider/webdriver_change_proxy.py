from selenium import webdriver
def webdriver_change_proxy(driver,ip,port):
    '''
    driver.get('http://1212.ip138.com/ic.asp')
    print('1: ',driver.session_id)
    print('2: ',driver.page_source)
    print('3: ',driver.get_cookies())
    '''
    script = "phantom.setProxy('{ip}', {port})".format(ip=ip, port=port)
    driver.command_executor._commands['EXECUTE_PHANTOM_SCRIPT'] = ('POST', '/session/$sessionId/phantom/execute')
    driver.execute('EXECUTE_PHANTOM_SCRIPT', {'script': script, 'args': []})
    '''
    driver.get('http://1212.ip138.com/ic.asp')
    print('1: ',driver.session_id)
    print('2: ',driver.page_source)
    print('3: ',driver.get_cookies())
    '''
'''
ip='175.155.24.95'
port=808
driver=webdriver.PhantomJS()
change_proxy(driver,ip,port)
'''

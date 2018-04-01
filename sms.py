import requests


def main():
    sms=Sms()
    r= requests.get ('http://localhost/RaspiSMS/smsAPI/\?email\={0}\&password\={1}\&numbers\={2}&text\=Attention!'.format(sms.id_user, sms.password_user, sms.telephone_user))
    
if __name__=='__main__':
    main()
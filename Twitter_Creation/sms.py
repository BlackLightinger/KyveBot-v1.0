from smsactivate.api import SMSActivateAPI
from time import time
from auth_data import API_key


def get_phone():
    wrapper = SMSActivateAPI(API_key)

    activation = wrapper.getNumber(service='tw', country=6)
    try:
        if activation['error'] == "NO_NUMBERS":
            while activation['error'] == "NO_NUMBERS":
                activation = wrapper.getNumber(service='tw', country=6)
    except:
        pass
    print(activation)

    return '+' + str(activation['phone']), activation


def waiting_code(activation):
    wrapper = SMSActivateAPI(API_key)

    start = time()
    status = wrapper.getStatus(id=activation['activation_id'])

    while status == 'STATUS_WAIT_CODE':
        if time() - start < 60:
            status = wrapper.getStatus(id=activation['activation_id'])
        else:
            wrapper.setStatus(id=activation['activation_id'], status=8)
            return False
    return True


def get_sms(activation):
    wrapper = SMSActivateAPI(API_key)

    wrapper.setStatus(id=activation['activation_id'], status=1)
    if not waiting_code(activation):
        return False

    status = wrapper.getStatus(id=activation['activation_id'])
    code = status.split(':')
    wrapper.setStatus(id=activation['activation_id'], status=6)
    return code[1]
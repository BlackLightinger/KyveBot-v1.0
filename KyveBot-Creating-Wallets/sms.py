from smsactivate.api import SMSActivateAPI
from time import time


def get_phone():
    wrapper = SMSActivateAPI('fA911347A3fA0ed4cb1d349c6de6bf10')

    activation = wrapper.getNumber(service='tw', country=6)

    print(activation)

    return '+' + str(activation['phone']), activation


def waiting_code(activation):
    wrapper = SMSActivateAPI('fA911347A3fA0ed4cb1d349c6de6bf10')

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
    wrapper = SMSActivateAPI('fA911347A3fA0ed4cb1d349c6de6bf10')

    wrapper.setStatus(id=activation['activation_id'], status=1)
    if not waiting_code(activation):
        return False

    status = wrapper.getStatus(id=activation['activation_id'])
    code = status.split(':')
    wrapper.setStatus(id=activation['activation_id'], status=6)
    return code[1]
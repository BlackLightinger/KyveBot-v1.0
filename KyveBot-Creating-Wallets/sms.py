from smsactivateru import Sms, SmsService, GetNumber, SmsTypes


def get_phone():
    wrapper = Sms('fA911347A3fA0ed4cb1d349c6de6bf10')

    activation = GetNumber(
        service=SmsService().Twitter,
        country=SmsTypes.Country.ID
    ).request(wrapper)

    print('id: {} phone: {}'.format(str(activation.id), str(activation.phone_number)))

    return '+' + activation.phone_number, activation


def get_sms(activation):
    wrapper = Sms('fA911347A3fA0ed4cb1d349c6de6bf10')

    activation.was_sent()
    code = activation.wait_code(wrapper=wrapper)

    return code
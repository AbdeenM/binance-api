class Balances:

    def __init__(self):
        self.asset = ''
        self.free = 0.0
        self.locked = 0.0

    @staticmethod
    def json_parse(json_data):
        result = Balances()
        result.asset = json_data.get_string('asset')
        result.free = json_data.get_float('free')
        result.locked = json_data.get_float('locked')
        return result


class AccountInformation:

    def __init__(self):
        self.makerCommission = 0
        self.takerCommission = 0
        self.buyerCommission = 0
        self.sellerCommission = 0
        self.canTrade = False
        self.canWithdraw = False
        self.canDeposit = False
        self.updateTime = 0
        self.accountType = ''
        self.balances = list()
        self.permissions = list()

    @staticmethod
    def json_parse(json_data):
        result = AccountInformation()
        result.makerCommission = json_data.get_int('makerCommission')
        result.takerCommission = json_data.get_int('takerCommission')
        result.buyerCommission = json_data.get_int('buyerCommission')
        result.sellerCommission = json_data.get_int('sellerCommission')
        result.canTrade = json_data.get_boolean('canTrade')
        result.canWithdraw = json_data.get_boolean('canWithdraw')
        result.canDeposit = json_data.get_boolean('canDeposit')
        result.updateTime = json_data.get_int('updateTime')
        result.accountType = json_data.get_string('accountType')

        element_list = list()
        data_list = json_data.get_array('balances')
        for item in data_list.get_items():
            element = Balances.json_parse(item)
            element_list.append(element)
        result.balances = element_list

        result.permissions = json_data.get_object(
            'permissions').convert_2_list()

        return result

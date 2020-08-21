class WebsocketRequest(object):

    def __init__(self):
        self.subscription_handler = None
        # close connection after receive data, for subscribe set False, for request set True
        self.auto_close = False
        self.is_trading = False
        self.error_handler = None
        self.json_parser = None
        self.update_callback = None

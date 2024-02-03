
class ConnectionRabbitmq:
    
    def __init__(self) -> None:
        self.host = "localhost"
        self.port = 5672
        self.username = "rabbitmq"
        self.password = "rabbitmq"
        self.exchange = "data_exchange"
        self.routing_key = ""
    


    def print_data(self):
        print("HOST", self.host)
        print("PORT", self.port)
        print("USERNAME", self.username)
        print("PASSWORD", self.password)
        print("EXCHANGE", self.exchange)
        print("ROUTING_KEY", self.routing_key)
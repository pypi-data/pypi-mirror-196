class BlueServerConfig:
    def __init__(self, connection_string: str):
        assert connection_string is not None or connection_string != "", "connection string is none or empty"
        
        hostname, port, weight = connection_string.split(":", 2)
        assert port.isnumeric(), f"Port must be numeric. '{port}' given"
        assert weight.isnumeric(), f"Weight must be numeric. '{weight}' given"

        self.hostname = hostname
        self.port = int(port)
        self.weight = int(weight)
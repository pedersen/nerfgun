class BtState:
    _instance = None

    loop = None
    cfg = None
    myservice = None
    agent = None
    manager = None
    bus = None
    device_obj = None
    dev_path = None

    def __new__(cls):
        if cls._instance is None:
            print("creating the state")
            cls._instance = super().__new__(cls)
        return cls._instance

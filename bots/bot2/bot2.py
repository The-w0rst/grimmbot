class Bot2:
    """A simple bot that reports the current time."""
    def get_time(self) -> str:
        from datetime import datetime
        return datetime.now().isoformat()

def run():
    print(Bot2().get_time())

if __name__ == '__main__':
    run()

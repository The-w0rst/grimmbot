class Bot1:
    """A simple echo bot."""
    def respond(self, text: str) -> str:
        return text

def run():
    import sys
    input_text = ' '.join(sys.argv[1:]) if len(sys.argv) > 1 else 'Hello from Bot1'
    print(Bot1().respond(input_text))

if __name__ == '__main__':
    run()

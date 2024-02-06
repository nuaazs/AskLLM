
def send_message(message,history):
    """ Send message to chatbot """
    print(f"机器：{message}")
    Q = input("你:")
    history.append((message,Q))
    return Q,history
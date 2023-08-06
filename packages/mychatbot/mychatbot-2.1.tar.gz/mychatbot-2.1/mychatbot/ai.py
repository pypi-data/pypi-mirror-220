from bardapi import Bard
token = "YQiLtpIxwMX_V3gqKce011fmUyY9L_KCvlyUITEhuhTLUa7RmNPGUwC8ta-nvEhwfuOi6A."
def ai():
    print("Chatbot: Hello! How can I assist you today?")
    
    while True:
        user_input = input("You: ")
        
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Chatbot: Goodbye!")
            break
        results = Bard(token=token).get_answer(user_input)["content"]
        
        print("Chatbot:", results)

if __name__ == "__main__":
    ai()

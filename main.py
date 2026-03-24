from brain import get_ai_response
from memory import save_name, load_name
# voice optional
try:
    from voice import listen
    voice_enabled = True
except:
    voice_enabled = False


print("🤖 Personal AI Assistant")
print("Type your message or 'v' for voice (if enabled)")
print("Type 'exit' to quit\n")

messages = []

# load memory
name = load_name()
if name:
    print(f"👋 Welcome back, {name}!")

while True:
    user_input = input("You: ")

    # exit
    if user_input.lower() == "exit":
        print("AI: Goodbye 👋")
        break

    # voice input
    if user_input.lower() == "v" and voice_enabled:
        user_input = listen()
        if not user_input:
            print("AI: Sorry, I didn't understand.")
            continue
        

    elif user_input.lower() == "v":
        print("⚠️ Voice not enabled")
        continue

    # save name
    if "my name is" in user_input.lower():
        name = user_input.split("is")[-1].strip()
        save_name(name)
        print(f"AI: Nice to meet you, {name}!")
        continue

    # ask name
    if "who am i" in user_input.lower():
        name = load_name()
        if name:
            print(f"AI: Your name is {name}.")
        else:
            print("AI: I don't know your name yet.")
        continue

    # empty input fix
    if not user_input.strip():
     continue

    # add to messages
    messages.append({"role": "user", "content": user_input})

    # limit context (important)
    messages = messages[-3:]

    # get response
    reply = get_ai_response(messages)

    # fallback fix
    if not reply or "Sorry" in reply:
        print("AI: I didn't understand. Please try again.")
        continue

    print("AI:", reply)

    # add reply to memory
    messages.append({"role": "assistant", "content": reply})
import ollama
import wikipedia
import requests
from memory import load_name, save_name

conversation_history = []

# -----------------------
# Wikipedia
# -----------------------
def search_wikipedia(query):
    try:
        return wikipedia.summary(query, sentences=2)
    except:
        return ""

# -----------------------
# Google fallback
# -----------------------
def google_search(query):
    try:
        url = "https://api.duckduckgo.com/?q=" + query + "&format=json"
        data = requests.get(url).json()
        return data.get("AbstractText", "")
    except:
        return ""

# -----------------------
# Calculator
# -----------------------
def calculator(text):
    try:
        return str(eval(text))
    except:
        return None

# -----------------------
# Multiplication table
# -----------------------
def multiplication_table(n):
    try:
        n = int(n)
        return "\n".join([f"{n} x {i} = {n*i}" for i in range(1, 11)])
    except:
        return None

# -----------------------
# Detect code request
# -----------------------
def is_code_request(text):
    keywords = ["code", "program", "loop", "function", "python", "java"]
    return any(word in text.lower() for word in keywords)

# -----------------------
# Detect factual query
# -----------------------
def is_fact_query(text):
    words = ["who is", "what is", "when", "where", "born", "ceo"]
    return any(w in text.lower() for w in words)

# -----------------------
# Format code
# -----------------------
def format_code(text, user_input):
    if "```" in text:
        return text

    lang = "python"
    if "java" in user_input.lower():
        lang = "java"

    return f"```{lang}\n{text.strip()}\n```"

# -----------------------
# MAIN FUNCTION
# -----------------------
def get_ai_response(messages):

    global conversation_history

    user_input = messages[-1]["content"]
    lower = user_input.lower()
    
# -----------------------
# SMART CODE GENERATION
# -----------------------
# -----------------------
# Detect coding request
# -----------------------
    coding = is_code_request(user_input)
    if coding:

    # ---- JAVA LOOP ----
     if "java" in lower and "loop" in lower:
        return """```java
for(int i = 0; i < 10; i++){
    System.out.println(i);
}
```"""

    # ---- PYTHON LOOP ----
    if "python" in lower and "loop" in lower:
        return """```python
for i in range(10):
    print(i)
```"""

    # ---- PYTHON LIST ----
    if "python" in lower and "list" in lower:
        return """```python
my_list = [1, 2, 3, 4, 5]
print(my_list)
```"""

    # ---- ADD TWO NUMBERS (PYTHON) ----
    if "add" in lower and "python" in lower:
        return """```python
a = 10
b = 20
sum = a + b
print(sum)
```"""

    # ---- ADD TWO NUMBERS (JAVA) ----
    if "add" in lower and "java" in lower:
        return """```java
int a = 10;
int b = 20;
int sum = a + b;
System.out.println(sum);
```"""

    # -----------------------
    # TABLE
    # -----------------------
    if "table of" in lower:
        num = lower.replace("table of", "").strip()
        table = multiplication_table(num)
        if table:
            return table

    # -----------------------
    # CALCULATOR
    # -----------------------
    if any(op in user_input for op in ["+", "-", "*", "/"]):
        result = calculator(user_input)
        if result:
            return f"The answer is {result}"

    # -----------------------
    # MEMORY
    # -----------------------
    if "my name is" in lower:
        name = lower.split("my name is")[-1].strip()
        save_name(name)
        return f"Nice to meet you, {name}!"

    if "who am i" in lower:
        name = load_name()
        return f"Your name is {name}" if name else "I don't know your name yet."

    # -----------------------
    # TYPE DETECTION
    # -----------------------
    coding = is_code_request(user_input)
    factual = is_fact_query(user_input)

    # -----------------------
    # WIKIPEDIA (ONLY factual)
    # -----------------------
    if factual and not coding:
        wiki = search_wikipedia(user_input)
        if wiki:
            return wiki

    # -----------------------
    # GOOGLE fallback
    # -----------------------
    if factual and not coding:
        google = google_search(user_input)
        if google:
            return google

    # -----------------------
    # PROMPT
    # -----------------------
    if coding:
        system_prompt = """
You are a coding assistant.
- Always generate working code
- Never refuse
- No explanation
- Only code
"""
    else:
        system_prompt = """
You are a helpful AI assistant.
Answer clearly and correctly.
Do not say "context not provided".
"""

    # -----------------------
    # MEMORY CONTEXT
    # -----------------------
    conversation_history.append({"role": "user", "content": user_input})
    conversation_history = conversation_history[-6:]

    try:
        response = ollama.chat(
            model="gemma:2b",
            messages=[{"role": "system", "content": system_prompt}] + conversation_history
        )

        reply = response["message"]["content"].strip()

        conversation_history.append(
            {"role": "assistant", "content": reply}
        )

        if coding:
            return format_code(reply, user_input)

        return reply

    except:
        return "Error: Ollama is not running properly."
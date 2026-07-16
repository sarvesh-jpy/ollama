import random

# List of quotes
quotes = [
    "Believe you can and you're halfway there. - Theodore Roosevelt",
    "It does not matter how slowly you go as long as you do not stop. - Confucius",
    "Success is not final, failure is not fatal: It is the courage to continue that counts. - Winston Churchill",
    "Don't watch the clock; do what it does. Keep going. - Sam Levenson",
    "You miss 100% of the shots you don't take. - Wayne Gretzky"
]

def get_random_quote():
    """Returns a random quote from the list"""
    return random.choice(quotes)

def main():
    print("Random Quote Generator")
    print("----------------------")
    print(get_random_quote())

if __name__ == "__main__":
    main()

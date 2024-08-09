from flask import Flask, render_template, request, redirect, url_for, session
import requests, random

app = Flask(__name__)
app.secret_key = 'kanye'  # Secret key for session management, ensures security

# In-memory storage for user scores
user_scores = {}

def fetch_quotes():
    # Function to get quotes from two different APIs
    def get_kanye_quotes():
        kanye_quotes = []
        for _ in range(3):  # Fetch 3 Kanye quotes
            try:
                response = requests.get("https://api.kanye.rest")  # Request Kanye quotes from API
                response.raise_for_status()  # Check for request errors
                kanye_quotes.append(response.json()['quote'])  # Add quote to the list
            except requests.RequestException as e:
                print(f"Error fetching Kanye quotes: {e}")
                kanye_quotes.append("Quote not available")  # Add fallback quote if an error occurs
        return kanye_quotes

    def get_zen_quotes():
        zen_quotes = []
        for _ in range(3):  # Fetch 3 Zen quotes
            try:
                response = requests.get("https://zenquotes.io/api/random")  # Request Zen quotes from API
                response.raise_for_status()  # Check for request errors
                zen_quotes.append(response.json()[0]['q'])  # Add quote to the list
            except requests.RequestException as e:
                print(f"Error fetching Zen quotes: {e}")
                zen_quotes.append("Quote not available")  # Add fallback quote if an error occurs
        return zen_quotes

    kanye_quotes = get_kanye_quotes()  # Fetch Kanye quotes
    zen_quotes = get_zen_quotes()  # Fetch Zen quotes

    # Combine the quotes into a single list with source labels
    quotes = [{'quote': quote, 'source': 'kanye'} for quote in kanye_quotes]
    quotes.extend([{'quote': quote, 'source': 'zen'} for quote in zen_quotes])

    # Shuffle the quotes to randomize their order
    random.shuffle(quotes)
    return quotes

@app.route('/')
def intro():
    # Render the introduction page
    return render_template('intro.html')

@app.route('/set_username', methods=['POST'])
def set_username():
    # Get the username from the form data; default to 'anonymous' if not provided
    username = request.form.get('username', 'anonymous')
    session['username'] = username  # Save the username in the session
    session['total_score'] = 0  # Initialize the total score for the session
    return redirect(url_for('quiz', page=1))  # Redirect to the quiz page, starting with page 1

@app.route('/quiz')
def quiz():
    # Fetch quotes and store them in the session
    quotes = fetch_quotes()
    session['quotes'] = quotes

    # Get the current page number from the query parameters; default to 1 if not provided
    page = int(request.args.get('page', 1))

    # Retrieve the quote for the current page, handle invalid page numbers
    if 0 < page <= len(quotes):
        quote = quotes[page - 1]
    else:
        quote = None

    # Check if the username is set in the session
    username_set = 'username' in session

    # Render the quiz page template with the current quote and other relevant data
    return render_template(
        'quiz.html',
        quote=quote,
        page=page,
        total_pages=len(quotes),
        username_set=username_set
    )

@app.route('/submit', methods=['POST'])
def submit():
    # Get the current page number from the form data
    current_page = int(request.form.get('current_page', 1))
    
    # Get the user's answer from the form data
    user_answer = request.form.get('answer')
    
    # Get the correct answer from the form data
    correct_answer = request.form.get('correct_answer')
    
    # Check if the user's answer is correct
    if user_answer == correct_answer:
        score = 1  # User answered correctly
    else:
        score = 0  # User answered incorrectly
    
    # Update the user's total score
    session['total_score'] += score
    
    # Determine the next page number
    next_page = current_page + 1
    
    # Get the list of quotes from the session
    quotes = session.get('quotes', [])
    
    # Check if there are more pages to show
    if next_page > len(quotes):
        # No more pages; redirect to the results page with the total score
        return redirect(url_for('results', score=session['total_score']))
    
    # More pages are available; redirect to the next quiz question
    return redirect(url_for('quiz', page=next_page))


@app.route('/results/<int:score>')
def results(score):
    # Retrieve the username from the session
    username = session.get('username', 'anonymous')
    
    # Define messages for high scores
    high_score_messages = {
        "Kanye Superfan": "You're Kanye's biggest fan, even bigger than himself! Prepare for a lifetime supply of Yeezys.",
        "Yeezy Expert": "You've reached Kanye enlightenment. You're now qualified to write Kanye's autobiography.",
        "Kanye Scholar": "Your knowledge of Kanye is on par with a PhD. You should consider teaching a Kanye studies course."
    }

    # Define messages for low scores
    low_score_messages = {
        "Kanye Novice": "You're more of a Kanye newbie than a superfan. Hit the books (or the streaming services) and brush up on your Yeezy knowledge.",
        "Kanye Confused": "Did you even listen to the same Kanye? Your Kanye IQ needs some serious improvement.",
        "Kanye Failure": "You're officially a Kanye failure. Consider a career change. Maybe try gardening?"
    }

    # Choose a message based on the user's score
    if score > 3:
        title, message = random.choice(list(high_score_messages.items()))
    else:
        title, message = random.choice(list(low_score_messages.items()))

    # Render the results page with the score, title, message, and username
    return render_template('results.html', score=score, title=title, message=message, username=username)

if __name__ == '__main__':
    app.run(debug=True)  # Run the Flask application in debug mode

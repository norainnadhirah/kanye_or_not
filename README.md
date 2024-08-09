Overview
The Flask Kanye or Not? Quiz App is a simple web application that quizzes users on quotes from Kanye West API  and Zen Qoute API. The app fetches random quotes from public APIs, presents them to the user, and tracks their score as they answer whether the quote is from Kanye or a Zen source. The user is greeted with a personalized results page based on their performance in the quiz.

Features
Random Quotes: Fetches quotes from Kanye West and Zen Quotes APIs.
User Interaction: Users can take a quiz where they guess the source of each quote.
Score Tracking: The app tracks the user's score throughout the quiz.
Personalized Results: Provides a custom message based on the user’s score.
Session Management: Uses Flask sessions to store user data and quiz progress.
Installation
Clone the Repository:

bash
Copy code
git clone https://github.com/yourusername/flask-quote-quiz-app.git
cd flask-quote-quiz-app
Create a Virtual Environment (Optional but Recommended):

bash
Copy code
python3 -m venv venv
source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
Install Dependencies:

bash
Copy code
pip install -r requirements.txt
Run the Application:

bash
Copy code
python app.py
Access the Application:
Open your web browser and navigate to http://127.0.0.1:5000/.

How It Works
Introduction:

The user is welcomed to the quiz on the intro page.
Setting Username:

The user sets their username and starts the quiz.
Taking the Quiz:

The app fetches 3 Kanye quotes and 3 Zen quotes.
Quotes are shuffled and presented one by one to the user.
The user selects whether the quote is from Kanye or Zen.
Scoring:

The user’s score is tracked, and they receive 1 point for each correct answer.
Results:

After the quiz, the user is redirected to the results page, which displays a personalized message based on their score.
Code Structure
app.py: Main Flask application with routes and logic.
templates/: Contains HTML templates (intro.html, quiz.html, results.html) for rendering web pages.

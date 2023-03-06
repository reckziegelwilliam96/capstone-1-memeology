# CAPSTONE 1 - [Memeology](https://memeology.herokuapp.com/)

### Getting Started:
- conda activate py3.7.13 (or other shell that uses py3.7.13)
- pip install venv
- python venv source/bin/activate
- pip install -r requirements.txt
- CREATEDB memeo-app
- python seed.py
- flask run

## Function:
Memeology (Meme-O) is 5-round guessing game. Users attempt to identify an iconic meme's phrase with only limited portion of the image viewable. The format is similar to Wordle, but is focused on visuals, like other Wordle spinoffs such as Frames. A user win's the game by submitting the correct guess in the submission box. In order to win, the user must guess one of the keywords from the meme's phrase before they are out of rounds. As the rounds progress (and the user guesses incorrectly), a larger portion of the meme's image becomes viewable. Once the game is completed, a record keeps track of the user's performance over time as well as the ability to 'favorite' the meme's image, generate their own and send to a friend.

## Features:
- Sign Up / Login / Authentication
- Guessing Form Submission
- Title Color Change Game Record
- Tile Reveal from Guessing
- Click 'Favorites' Memes
- Display Tracking Record
- Display Round Hints
- Posting Correct Answer

## User Flow:

![User Flows](https://github.com/reckziegelwilliam96/capstone-1-memeology/blob/main/schema_design/Memeo%20User%20Flows.png?raw=true)
- User Logins/Signs Up
- Redirect to Home Page, Clicks on Instructions Page
- Redirects to Instructions Page, Clicks on 'Start Game'
- Game Page: 1/16th of images as well as form submission bar, MEMEO game record, and results section
- If incorrect, M in Memeo changes to reddish hue (then O, M, E and finally O), results section post incorrect response, hints option becomes available, an extra tile becomes visible
 -- This repeats until the game is over or the user guesses correct
- If correct, full image is displayed with congratulations in results section as well full correct phrase.
- If game is over, full image is displayed and correct phrase.
- Both correct guess and game over redirect to Game Over page
- Game Over Page: Shows full meme with submission bars to generate top and bottom text. Once generated, a star icon to favorite the meme is an option. A bar graph is shown as well to show user's track record over time.

## Database Schema:

![Database Schema](https://github.com/reckziegelwilliam96/capstone-1-memeology/blob/main/schema_design/updated_database_schema.png?raw=true)

## API: (IMGFLIP API) [https://imgflip.com/api]
- Two endpoints used, /get_memes and /caption_images. /get_memes used for gameplay (displaying image to be guessed) and /caption_images for gameover (to generate meme
 -- /get_memes (GET REQUEST) data structure includes includes Id, Meme name, URL as well as other data
 -- /caption_image (POST REQUEST) data structure includes template_id, username, password, top_text, bottom_text, as well other options for specifying meme generated
 
 ## STACK:
 - Frontend: HTML - Jinja, CSS, JS, AXIOS
 - Backend: Flask, SQLAlchemy, WTForms


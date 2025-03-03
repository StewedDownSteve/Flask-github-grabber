import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/<username>')
def github(username):
    try:
        # Fetch the GitHub page for the user
        github_html = requests.get(f'https://github.com/{username}')
        github_html.raise_for_status()  # Check for any errors (e.g., 404)
        
        soup = BeautifulSoup(github_html.text, "html.parser")

        # Find the avatar image safely
        avatar_block = soup.find_all('img', class_='avatar')
        if avatar_block:
            img_url = avatar_block[0].get('src')  # Use the first avatar found
        else:
            img_url = 'No avatar found'

        # Find the number of repositories safely
        repos = soup.find('span', class_="Counter")
        if repos:
            repos = repos.text.strip()
        else:
            repos = 'No repository count found'

        # Render the template with the fetched data
        return render_template('github_profile.html', img_url=img_url, repos=repos, username=username)
    
    except requests.exceptions.HTTPError:
        # If there's an error (e.g., 404), render the error page
        return render_template('error.html', username=username)


if __name__ == "__main__":
    app.run(debug=True)

# Essence Coach

Essence Coach is a helpful and informative bot assistant that answers questions related to the Essence standard and software engineering practices.

## Set-up

Clone or download the code from this repository.

Make sure you have [Python](https://www.python.org/downloads/) and pip installed.
You can check that by running the following commands:
```bash
python --version
```
```bash
pip --version
```
Run this command in the terminal to install the required packages.
```bash
pip install -r requirements.txt
```
Create an ```.env``` file in the root directory with your ```GROQ_API_KEY```. You can get one [here](https://console.groq.com/login).
Follow this format:
```
GROQ_API_KEY="xxxxx"
```

## Run the app

Inside the project's folder, run this command to execute the app.

```bash
python app.py
```
The app should now be running on http://127.0.0.1:5000/. You can access it by opening a browser and going to that address.

## About the data

This chatbot uses a RAG system to provide accurate responses about the Essence standard.

The following documents are included in the retrieval database.

### General documents about the Essence Kernel and Language
These documents contain information about Essence in general, its language and its kernel.
- Alpha_state_cards.md
- Essence_Explained.md
- Essence_in_a_nutshell.md
- Essence_Kernel.md
- Essence_pocket_guide.md
- Essence_seminar.md
- Smarter_methods_Essentialization.md
    
### Documents about software engineering practices
These documents provide information about different software engineering methods and practices (e.g., Scrum, Retrospectives, etc.).
- Improving_Agile_Retrospectives.md
- Retrospective_practice.md
- Scrum_powered_by_Essence.md
- Use_cases_user_stories.md
- Se_intro.md
- Se_scrum.md
- Se_retrospective.md
- Se_conclusion.md
- Retro_Scrum_cards.md
- Agile_Essence_cards.md

### Documents about Essence games
These documents contain instructions to play different Essence games.
- Alpha_State_Card_Games.md
- Team_Status_Game.md
- The_hot_seat.md

### Other documents
- Essencery_a_tool.md
- Training_students.md

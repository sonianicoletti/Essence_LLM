# Essence Coach

Essence Coach is a helpful and informative bot assistant that answers questions related to the Essence standard and software engineering practices.

## Set-up

### STEP 1: Clone the repository

Clone or download the code from this repository.

Make sure you have [Python](https://www.python.org/downloads/release/python-3127/) installed (note: Python 3.13 may be incompatible with some of the required packages, I recommend having installed Python 3.12 or older).

You can check your Python version by running the following command in your terminal:

```bash
python --version
```

### STEP 2: Create a virtual environment

Next, you may want to create a virtual Python environment to install the required packages.

To do so, run the following command inside the project's root directory:

```bash
python -m venv .venv
```

### STEP 3: Activate the virtual environment

Then, to activate it run this command on macOS/Linux:

```bash
source .venv/bin/activate
```

Or, on Windows:

```bash
.venv\Scripts\activate
```

### STEP 4: Install the required packages

Run this command to install the required packages. This step may take a few minutes.

```bash
pip install -r requirements.txt
```

### STEP 5: Add the environment variables

From the official [Groq website](https://console.groq.com/login) get your own API key and add it to the ```.env``` file located in the root directory. Follow this format:

```
GROQ_API_KEY="xxxxx"
```

## Run the app

Inside the root directory, run this command to execute the app.

```bash
python app.py
```
The app should now be running on http://127.0.0.1:5000/. You can access it by opening a browser and going to that address.

To stop the app from running simply press ```Ctrl + C``` in your terminal.

## About the data

This chatbot uses a RAG system to provide accurate responses about the Essence standard.

The following documents are included in the retrieval database.

### General documents about the Essence Kernel and Language
These documents contain information about Essence in general, its language and its kernel.
- Kernel_cards.md
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

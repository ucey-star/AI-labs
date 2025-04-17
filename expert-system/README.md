# 🧠 Expert System for Taipei Tourist Recommendations

This project combines **Prolog** and **Python** to create an expert system that helps users find personalized recommendations for places to visit in **Taipei** based on their preferences. It uses rule-based logic for decision-making and natural language interaction to guide users through the process.

---

## 🌟 Features

- Hybrid system using **Prolog for logic** and **Python for interface**
- Dynamic questioning based on user inputs and preferences
- Smart input classification using fuzzy string matching (via LCS)
- Covers shopping, relaxing, and learning intentions
- Provides real Taipei location suggestions with Google Maps links

---

## 🤖 What It Does

The system asks users questions about:
- Their **intention** (shopping, relaxing, or learning)
- Specific **preferences** (ambience, setting, entrance fees, crowd levels, etc.)
- What they want to **buy** or **learn about**
- Price sensitivity

Based on these, the **Prolog knowledge base** matches the rules to one or more real-world Taipei locations and returns a recommendation.

---

## 🛠️ Tech Stack

- **Prolog (SWI-Prolog via PySwip)** — for rule-based reasoning
- **Python** — for user interaction, input processing, and integration
- **pylcs** — for similarity scoring between user input and menu options
- **NumPy** — for numeric operations

---

## 🐍 Installation

Install the required Python packages:

```bash
pip install pyswip pylcs numpy
```

Make sure you have **SWI-Prolog** installed and available in your system PATH.
---

## 🚦 How to Use

Run the script using Python:

```bash
python expert_system.py
```

You will be asked a series of menu-based questions (e.g., "What do you want to buy?"). Type your answers or choose by number.

The system uses:
- **LCS-based matching** to handle fuzzy responses
- **Dynamic Prolog rules** to infer recommendations
- **Google Maps links** for real locations

---

## 💡 Example Output

```
What is your intention of going to a tourist place?
1. relaxing
2. learning
3. shopping
Previous input: relaxing

What type of ambience do you want?
1. lively
2. cozy
3. tranquil
Previous input: tranquil

...

Your recommendation is Elephant Mountain: https://goo.gl/maps/VQXRm5UZMkHEtrv99.
```

---

## 📚 How It Works

### Prolog Knowledge Base
Encodes facts and rules like:

```prolog
place(elephant_mountain) :- location(taipei), intention(relaxing), crowded(no), setting(outdoor), ambience(tranquil).
```

### Python Interface
- Collects input using menus
- Uses fuzzy matching for free text
- Bridges between user and Prolog via PySwip

---

## ⚙️ Customization

Want to add more places or rules? Just modify the `KB` string in the Python script with additional Prolog facts and rules.

---

## 🧪 Notes

- The system runs **entirely locally** and doesn't require any external APIs.
- Works best when executed outside a notebook (e.g., terminal or IDE).
- This is a functional prototype—UX can be expanded with GUI or chatbot interfaces.

---

## 📝 License

This project is intended for educational and academic use.


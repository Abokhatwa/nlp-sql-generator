# nlp-sql-generator
Here's the complete `README.md` file for your project:

````markdown
# Multi-Database SQL Generator App

This is a Streamlit web application that generates natural language-to-SQL queries across multiple SQLite databases using OpenAI's GPT models. Users can explore and query predefined databases (`school.db`, `hospital.db`, and `ecommerce.db`) with ease through an intuitive interface.

---

## 🚀 Features

- 🔍 **Natural Language to SQL**: Ask questions in English and get valid SQL queries.
- 🗃️ **Multi-Database Support**: Choose from different domains—School, Hospital, and E-commerce.
- 📄 **Live Preview**: View table schemas before querying.
- 🧠 **AI-Powered**: Integrates with OpenAI's GPT model for query generation.
- 🎲 **Fake Data Generator**: Populate databases with synthetic data using Faker.

---

## 📁 Project Structure

```bash
.
├── app.py                 # Main Streamlit application
├── database_creator.py    # Script to generate the SQLite databases
├── database_schemas.py    # Predefined schemas for each domain
├── sql_generator.py       # GPT-powered SQL generator logic
├── requirements.txt       # List of Python dependencies
├── README.md              # This documentation file
├── school.db              # SQLite DB for school domain
├── hospital.db            # SQLite DB for hospital domain
└── ecommerce.db           # SQLite DB for e-commerce domain
````

---

## ⚙️ Installation

1. **Clone the repository**:

```bash
git clone https://github.com/yourusername/sql-generator-app.git
cd sql-generator-app
```

2. **Install dependencies**:

```bash
pip install -r requirements.txt
```

3. **Create environment file**:

Add your OpenAI API key to a `.env` file in the root directory:

```bash
OPENAI_API_KEY=your_openai_key_here
```

---

## ▶️ Usage

To launch the app locally:

```bash
streamlit run app.py
```

* Select a database from the sidebar.
* View available tables and schema.
* Enter a natural language question.
* Get the corresponding SQL query and output.

---

## 🧪 Regenerating Databases

To generate or reset the sample databases with synthetic data:

```bash
python database_creator.py
```

---

## 📦 Dependencies

Listed in `requirements.txt`:

* `streamlit`
* `openai`
* `python-dotenv`
* `pandas`
* `faker`

---

## 📜 License

This project is licensed under the MIT License. See `LICENSE` for details.

---

## 👨‍💻 Author

Developed by \[Your Name] — AI-powered SQL tool for rapid data interaction.

---

## 💡 Future Enhancements

* Add user-uploaded database support.
* Support for JOIN and nested query generation.
* Query history and result download options.

```

Let me know if you’d like this adjusted for deployment (e.g., Docker, Streamlit Sharing) or want a badge-enhanced version.
```

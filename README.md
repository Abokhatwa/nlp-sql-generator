# 🔍 Natural Language to SQL Converter

A powerful web application that converts natural language queries into SQL statements using OpenAI's GPT-4 model. This project provides both a Streamlit-based interface and a Django REST API for seamless natural language to SQL conversion.

## ✨ Features

- **Natural Language Processing**: Convert plain English questions into SQL queries
- **Multiple Database Support**: Pre-configured schemas for E-Commerce, Hospital Management, and School Management databases
- **Real-time Query Execution**: Execute generated SQL queries and view results instantly
- **Interactive Web Interface**: User-friendly Streamlit interface with database selection and query history
- **REST API**: Django-based API for programmatic access
- **Smart Schema Understanding**: AI-powered understanding of database schemas and relationships
- **Query Explanation**: Get detailed explanations of generated SQL queries
- **Sample Data**: Pre-populated databases with realistic sample data for testing

## 🏗️ Architecture

The project consists of two main components:

1. **Streamlit Application** (`app.py`): Interactive web interface for end users
2. **Django REST API** (`sql_generator_project/`): Backend API for programmatic access

### Core Components

- **SQL Generator**: OpenAI GPT-4 powered query generation
- **Database Schemas**: Pre-defined schemas for multiple domains
- **Database Creator**: Automated sample data generation
- **Query Engine**: SQL execution and result processing

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- OpenAI API key
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd LLM_natural_sql
   ```

2. **Install dependencies**
   ```bash
   # For Streamlit app
   pip install streamlit openai pandas python-dotenv

   # For Django API
   cd sql_generator_project
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

4. **Run the application**

   **Option 1: Streamlit Interface**
   ```bash
   streamlit run app.py
   ```

   **Option 2: Django API**
   ```bash
   cd sql_generator_project
   python manage.py runserver
   ```

## 📊 Supported Databases

### 1. E-Commerce Database
- **Tables**: customers, products, orders, order_items
- **Use Cases**: Customer analysis, inventory management, sales reporting

### 2. Hospital Management Database
- **Tables**: patients, doctors, appointments, prescriptions, departments
- **Use Cases**: Patient management, appointment scheduling, medical records

### 3. School Management Database
- **Tables**: students, teachers, courses, enrollments, grades
- **Use Cases**: Student tracking, grade management, course administration

## 💡 Usage Examples

### Natural Language Queries

**E-Commerce:**
- "Show me the top 5 customers by total order amount"
- "Find all products with stock less than 10"
- "Get all orders from the last 30 days"

**Hospital Management:**
- "Show all appointments scheduled for tomorrow"
- "Find all patients with blood type O+"
- "List the top 10 doctors by number of appointments"

**School Management:**
- "Show all students in grade 10"
- "Find the average grade for each course"
- "List all students enrolled in Computer Science courses"

### API Usage

```python
import requests

# Generate SQL from natural language
response = requests.post('http://localhost:8000/api/generate-sql/', {
    'query': 'Show me the top 5 customers by total order amount',
    'database': 'E-Commerce'
})

sql_query = response.json()['sql_query']
```

## 🔧 Configuration

### Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `DEBUG`: Set to True for development mode
- `SECRET_KEY`: Django secret key for production

### Customizing Schemas

You can add new database schemas by modifying `sql_generator_project/query_engine/database_schemas.py`:

```python
"Your Database": {
    "description": "Description of your database",
    "tables": {
        "table_name": {
            "columns": [
                "column_name (TYPE, CONSTRAINTS)",
                # ... more columns
            ],
            "description": "Table description"
        }
    }
}
```

## 🛠️ Development

### Project Structure

```
LLM_natural_sql/
├── app.py                          # Streamlit main application
├── sql_generator_project/          # Django project
│   ├── query_engine/              # Main Django app
│   │   ├── sql_generator.py      # OpenAI integration
│   │   ├── database_schemas.py   # Database definitions
│   │   ├── database_creator.py   # Sample data generator
│   │   └── views.py              # API endpoints
│   ├── authentication/           # User authentication
│   ├── templates/                # HTML templates
│   ├── static/                   # Static files
│   └── requirements.txt          # Python dependencies
└── databases/                    # SQLite database files
```

### Adding New Features

1. **New Database Schema**: Add to `database_schemas.py`
2. **Custom SQL Logic**: Extend `sql_generator.py`
3. **API Endpoints**: Add to `views.py`
4. **UI Components**: Modify Streamlit app or Django templates

## 🔒 Security Considerations

- Store API keys securely using environment variables
- Validate user inputs before processing
- Implement rate limiting for API endpoints
- Use HTTPS in production environments
- Regularly update dependencies

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- OpenAI for providing the GPT-4 API
- Streamlit for the web interface framework
- Django for the REST API framework
- The open-source community for various supporting libraries

## 📞 Support

For support and questions:
- Create an issue in the repository
- Check the documentation in the code comments
- Review the example queries for guidance

---

**Note**: This project requires an OpenAI API key to function. Make sure to set up your API key in the `.env` file before running the application.

# LLM-Based Data Annotation Tool

## 1. Project Overview

The LLM-Based Data Annotation Tool is an AI-assisted application designed to simplify and automate the process of data annotation using Large Language Models (LLMs).

The system provides a user-friendly interface for uploading datasets, generating annotations, reviewing results and managing annotated data.

It combines a Streamlit frontend with a FastAPI backend and database integration to support efficient data annotation and management.

## 2. Objectives

- Automate the data annotation process using AI.
- Reduce manual annotation effort.
- Generate text annotations with confidence information.
- Provide manual annotation and human review capabilities.
- Store and manage annotation records using a database.
- Provide a simple and interactive user interface.

## 3. Technologies Used

| Component | Technology |
|---|---|
| Programming Language | Python |
| Frontend | Streamlit |
| Backend | FastAPI |
| AI / NLP | Large Language Models (LLMs) |
| Database | SQLite |
| Data Processing | Pandas |
| API Communication | Requests |
| Testing | Python |

## 4. System Modules

### Dataset Upload
Allows users to upload CSV datasets through the application interface.

### AI-Based Annotation
Processes uploaded text data through the backend annotation service and generates annotation results with confidence information.

### Manual Annotation
Allows users to manually assign labels such as Positive, Negative and Neutral.

### Database Management
Stores annotation-related information using SQLite for persistence and retrieval.

### Dashboard
Displays dataset information, annotation statistics and pending records.

### Testing
Includes database and annotation service testing to verify the functionality of the system.

## 5. Project Structure

```text
LLM-Based-Data-Annotation-Tool/
│
├── app.py
├── annotation_service.py
├── llm_backend.py
├── check_database.py
├── test_database.py
├── test_service.py
├── test_data.csv
├── requirements.txt
├── .gitignore
└── README.md
```

## 6. Installation and Execution

### Step 1: Clone the Repository

```bash
git clone https://github.com/Sushmitab10/LLM-Based-Data-Annotation-Tool.git
```

### Step 2: Navigate to the Project

```bash
cd LLM-Based-Data-Annotation-Tool
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Start the Backend

Start the FastAPI backend using the project's configured entry point.

### Step 5: Start the Frontend

```bash
streamlit run app.py
```

### Step 6: Access the Application

Open the Streamlit URL displayed in the terminal.

The FastAPI documentation can be accessed at:

```text
http://127.0.0.1:8000/docs
```

## 7. Expected Outcomes

- Simplified dataset uploading and annotation.
- AI-generated text annotation results.
- Confidence information for annotation results.
- Support for manual annotation and review.
- Database-backed annotation management.
- Improved efficiency in the data annotation workflow.

## 8. Conclusion

The LLM-Based Data Annotation Tool demonstrates the integration of Large Language Models, web application development and database management to create an AI-assisted annotation platform. The project aims to make data annotation more efficient, accessible and manageable.

## 9. Contributors

Developed as an academic mini-project by the project team.


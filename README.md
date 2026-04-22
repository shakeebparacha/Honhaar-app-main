# Student Account Manager

A Streamlit application that stores student/guardian account information based on age.

## Features
- ✅ If student age > 18: Stores student's own account information
- ✅ If student age ≤ 18: Stores guardian's account information
- ✅ View all stored records in a table
- ✅ Export records to CSV
- ✅ Persistent storage in JSON file
- ✅ Data validation and error handling

## Installation

1. Make sure you have Python 3.8+ installed

2. Install required packages:
```bash
pip install -r requirements.txt
```

## Running the Application

```bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`

## Usage

1. **Add New Record**:
   - Fill in student information (name, age, roll number, email, phone)
   - If age ≤ 18, fill in guardian information
   - Click "Submit Record"

2. **View Records**:
   - See all stored records in the right panel
   - View statistics (total, student accounts, guardian accounts)
   - Export data to CSV format

## File Storage

Data is stored in `student_data.json` with the following structure:

### For Students (age > 18):
```json
{
  "student_roll": "STU001",
  "age": 20,
  "timestamp": "2024-04-20 10:30:00",
  "account_info": {
    "account_holder": "Student",
    "name": "John Doe",
    "age": 20,
    "email": "john@example.com",
    "phone": "1234567890"
  }
}
```

### For Guardians (age ≤ 18):
```json
{
  "student_roll": "STU002",
  "age": 16,
  "timestamp": "2024-04-20 10:35:00",
  "account_info": {
    "account_holder": "Guardian",
    "guardian_name": "Jane Doe",
    "guardian_email": "jane@example.com",
    "guardian_phone": "0987654321",
    "guardian_relation": "Mother",
    "student_name": "Jane Jr.",
    "student_age": 16
  }
}
```

## Requirements

- Python 3.8+
- Streamlit 1.28.1
- Pandas 2.0.3

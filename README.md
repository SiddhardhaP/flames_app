# 🔥 FLAMES Game

A modern, interactive web application built with FastAPI that calculates relationship compatibility using the classic FLAMES game algorithm.

## Features

- ✨ **Interactive UI**: Beautiful dark-themed interface with smooth animations
- 📊 **Statistics**: View percentage breakdown of all FLAMES outcomes
- 📜 **History**: Track your past calculations with easy access
- 🔄 **Recalculate**: Quickly recalculate any previous pair
- 🗑️ **Delete**: Remove individual history items
- ✅ **Validation**: Robust input validation and error handling
- 💾 **Persistence**: History saved in browser localStorage
- 📱 **Responsive**: Works seamlessly on desktop and mobile devices

## What is FLAMES?

FLAMES is a popular relationship compatibility game that stands for:
- **F** - Friends
- **L** - Love
- **A** - Affection
- **M** - Marriage
- **E** - Enemies
- **S** - Siblings

The game calculates compatibility by removing common letters from two names and counting the remaining letters.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/flames_app.git
cd flames_app
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
uvicorn main:app --reload
```

4. Open your browser and navigate to:
```
http://localhost:8000
```

## Usage

1. Enter two names in the input fields
2. Click "Check Relationship" to calculate
3. View the result and statistics
4. Access calculation history from the history panel
5. Use the 3-dots menu (⋯) on any history item to recalculate or delete

## Project Structure

```
flames_app/
├── main.py              # FastAPI application and FLAMES logic
├── templates/
│   └── index.html      # Frontend HTML/CSS/JavaScript
├── requirements.txt    # Python dependencies
├── README.md           # Project documentation
└── .gitignore          # Git ignore file
```

## Technologies Used

- **Backend**: FastAPI (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **Templating**: Jinja2
- **Storage**: Browser localStorage

## Features in Detail

### Statistics
The statistics feature shows how often each FLAMES result appears when testing 100 different letter counts, giving you a comprehensive view of relationship compatibility.

### History Management
- View all past calculations
- Click any history item to recalculate
- Use the 3-dots menu for quick actions
- Delete individual items or clear all history

### Input Validation
- Names must be non-empty
- Minimum length validation
- Special character filtering
- Case-insensitive matching

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

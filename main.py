from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from collections import Counter
import re

app = FastAPI(title="FLAMES Game")

templates = Jinja2Templates(directory="templates")


def validate_names(name1: str, name2: str) -> tuple[str, str]:
    """Validate and sanitize input names."""
    # Remove extra whitespace
    name1 = name1.strip()
    name2 = name2.strip()
    
    # Check if names are empty
    if not name1 or not name2:
        raise ValueError("Both names are required")
    
    # Check length (reasonable limit)
    if len(name1) > 50 or len(name2) > 50:
        raise ValueError("Names must be 50 characters or less")
    
    # Allow only letters, spaces, and common characters
    if not re.match(r'^[a-zA-Z\s\-\.\']+$', name1) or not re.match(r'^[a-zA-Z\s\-\.\']+$', name2):
        raise ValueError("Names can only contain letters, spaces, hyphens, dots, and apostrophes")
    
    return name1, name2


def flames_result(name1: str, name2: str) -> dict:
    """Calculate FLAMES result with statistics."""
    # Remove spaces and convert to lowercase
    name1_clean = name1.replace(" ", "").lower()
    name2_clean = name2.replace(" ", "").lower()
    
    # Count characters in each name
    count1 = Counter(name1_clean)
    count2 = Counter(name2_clean)
    
    # Remove common characters
    common_chars = set(count1.keys()) & set(count2.keys())
    for char in common_chars:
        min_count = min(count1[char], count2[char])
        count1[char] -= min_count
        count2[char] -= min_count
    
    # Calculate remaining count
    count = sum(count1.values()) + sum(count2.values())
    
    if count == 0:
        return {
            "result": "Same Names 😄",
            "result_type": "SAME",
            "count": 0,
            "statistics": {
                "F": 0, "L": 0, "A": 0, "M": 0, "E": 0, "S": 0
            }
        }
    
    # Calculate FLAMES
    flames = ["F", "L", "A", "M", "E", "S"]
    meanings = {
        "F": "Friends 🤝",
        "L": "Love ❤️",
        "A": "Affection 💞",
        "M": "Marriage 💍",
        "E": "Enemies ⚔️",
        "S": "Siblings 👨‍👩‍👧"
    }
    
    # Simulate the elimination process to get statistics
    flames_copy = flames.copy()
    index = 0
    elimination_order = []
    
    while len(flames_copy) > 1:
        index = (index + count - 1) % len(flames_copy)
        eliminated = flames_copy.pop(index)
        elimination_order.append(eliminated)
    
    final_result = flames_copy[0]
    
    # Calculate statistics (percentage breakdown)
    # This simulates what would happen with different counts
    stats = {}
    total_simulations = 100
    for letter in ["F", "L", "A", "M", "E", "S"]:
        wins = 0
        for test_count in range(1, total_simulations + 1):
            test_flames = flames.copy()
            test_index = 0
            while len(test_flames) > 1:
                test_index = (test_index + test_count - 1) % len(test_flames)
                test_flames.pop(test_index)
            if test_flames[0] == letter:
                wins += 1
        stats[letter] = round((wins / total_simulations) * 100, 1)
    
    return {
        "result": meanings[final_result],
        "result_type": final_result,
        "count": count,
        "statistics": stats,
        "elimination_order": elimination_order
    }


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "result": None,
            "name1": "",
            "name2": "",
            "error": None
        }
    )


@app.post("/calculate", response_class=HTMLResponse)
async def calculate(
    request: Request,
    name1: str = Form(...),
    name2: str = Form(...)
):
    try:
        # Validate input
        validated_name1, validated_name2 = validate_names(name1, name2)
        
        # Calculate FLAMES result
        result_data = flames_result(validated_name1, validated_name2)
        
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "result": result_data,
                "name1": validated_name1,  # Keep names visible after calculation
                "name2": validated_name2,  # Keep names visible after calculation
                "error": None
            }
        )
    except ValueError as e:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "result": None,
                "name1": name1,
                "name2": name2,
                "error": str(e)
            }
        )
    except Exception as e:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "result": None,
                "name1": name1,
                "name2": name2,
                "error": "An unexpected error occurred. Please try again."
            }
        )


@app.post("/api/calculate")
async def calculate_api(name1: str = Form(...), name2: str = Form(...)):
    """API endpoint for JSON responses."""
    try:
        validated_name1, validated_name2 = validate_names(name1, name2)
        result_data = flames_result(validated_name1, validated_name2)
        return JSONResponse(content=result_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

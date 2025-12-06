from fastapi import FastAPI, APIRouter
import csv
import os

app = FastAPI()
router = APIRouter()

CSV_FILE = 'todo.csv'
todo_list = []


def load_todos():
    if not os.path.exists(CSV_FILE):
        return

    with open(CSV_FILE, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            todo_list.append({
                'title': row['title'],
                'description': row['description']
            })


def save_todos():
    with open(CSV_FILE, 'w', newline='', encoding='utf-8') as file:
        fieldnames = ['title', 'description']
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        for todo in todo_list:
            writer.writerow(todo)


@router.post('/add')
def add_todo(item: dict):
    todo_list.append({
        'title': item.get('title', ''),
        'description': item.get('description', '')
    })
    save_todos()
    return {'message': 'Todo added successfully'}


@router.get('/list')
def retrieve_todo():
    return {'todos': todo_list}


# 앱 시작 시 CSV 로딩
load_todos()

# 라우터 등록
app.include_router(router, prefix='/todos')
# todo.py
import csv
import os
from typing import Dict, List

from fastapi import APIRouter, FastAPI, HTTPException

app = FastAPI(title='Simple TO-DO API')

router = APIRouter()

CSV_FILE = 'todo_list.csv'


def _load_todos() -> List[Dict[str, str]]:
    """CSV 파일에서 todo 목록을 읽어옵니다. 파일이 없으면 빈 리스트 반환."""
    todos: List[Dict[str, str]] = []
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                todos.append({'task': row['task'], 'status': row['status']})
    return todos


def _save_todos(todos: List[Dict[str, str]]) -> None:
    """현재 todo 목록을 CSV 파일로 저장합니다."""
    with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['task', 'status'])
        writer.writeheader()
        writer.writerows(todos)


todo_list: List[Dict[str, str]] = _load_todos()


@router.post('/add_todo')
def add_todo(item: Dict[str, str]):
    """
    새로운 할 일을 추가합니다.
    입력 예시: {"task": "우주선 설계도 검토", "status": "대기중"}
    """
    if not item:
        raise HTTPException(status_code=400, detail='빈 데이터는 허용되지 않습니다.')

    task = item.get('task', '').strip()
    status = item.get('status', '대기중').strip()

    if not task:
        raise HTTPException(status_code=400, detail='task 필드가 비어 있거나 없습니다.')

    new_item = {'task': task, 'status': status}
    todo_list.append(new_item)
    _save_todos(todo_list)

    return {'message': '할 일이 추가되었습니다.', 'item': new_item}


@router.get('/retrieve_todo')
def retrieve_todo() -> List[Dict[str, str]]:
    """현재 모든 할 일 목록을 반환합니다."""
    return todo_list


app.include_router(router)


# 서버 실행을 위한 엔트리포인트
if __name__ == '__main__':
    import uvicorn
    uvicorn.run('todo.py:app', host='127.0.0.1', port=8000, reload=True)
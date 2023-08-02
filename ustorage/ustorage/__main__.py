from typing import Annotated
from fastapi import FastAPI, Request, Response, Depends, File, Form, UploadFile
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

import uvicorn
from datetime import datetime
import sqlite3


app = FastAPI()

templates = Jinja2Templates("./templates")


class Database:
    def __init__(self):
        self.db = {}

    def add(self, name: str, content_type: str, content: bytes):
        self.db[name] = {
            "content_type": content_type,
            "content": content,
            "added_at": datetime.utcnow()
        }

    def get(self, name):
        return self.db[name]


class SqliteDatabase:
    def __init__(self):
        self.con = sqlite3.connect("tutorial.sqlite3", check_same_thread=False)
        cur = self.con.cursor()
        try:
            cur.execute("CREATE TABLE objects (name text unique, blob none, content_type text, added_at text);")
            self.con.commit()
        except:
            pass

    def add(self, name: str, content_type: str, content: bytes):
        cur = self.con.cursor()
        cur.execute("INSERT INTO objects VALUES (?, ?, ?, ?);", [name, content, content_type, datetime.utcnow()])
        self.con.commit()

    def get(self, name):
        cur = self.con.cursor()
        cur.execute("SELECT * FROM objects WHERE name=?;", [name])
        row = cur.fetchone()
        return {"name": row[0], "content": row[1], "content_type": row[2], "added_at": row[3]}

    def get_list(self):
        cur = self.con.cursor()
        cur.execute("SELECT * FROM objects")
        rows = cur.fetchall()
        return [{"name": row[0], "content_type": row[2], "added_at": row[3]} for row in rows]


db = SqliteDatabase()
def get_db():
    try:
        yield db
    finally:
        pass


@app.get("/")
async def index(request: Request, database: Database = Depends(get_db)):
    return templates.TemplateResponse("index.html", {"request": request, "list": database.get_list()})


@app.post("/add")
async def post_obeject(name: Annotated[str, Form()], content: Annotated[UploadFile, File()], database: Database = Depends(get_db)):
    database.add(name, content.content_type , content.file.read())
    return RedirectResponse("/", status_code=301)


@app.get("/lists")
async def get(database: Database = Depends(get_db)):
    return db.get_list()


@app.get("/get")
async def get(name: str, database: Database = Depends(get_db)):
    data = database.get(name)
    return {"content-type": data["content_type"], "added_at": data["added_at"]}


@app.get("/get-object")
async def get_object(name: str, database: Database = Depends(get_db)):
    data = database.get(name)
    return Response(content=data["content"], media_type=data["content_type"])


uvicorn.run(app)

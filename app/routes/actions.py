from fastapi import APIRouter

router = APIRouter()

@router.post("/like")
def like_movie():
    return {"msg": "Like movie"}

@router.post("/save")
def save_movie():
    return {"msg": "Save movie"}

@router.post("/comment")
def comment_movie():
    return {"msg": "Comment movie"}

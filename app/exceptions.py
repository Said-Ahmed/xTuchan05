from fastapi import HTTPException, status

RoomCannotBeBooked = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='Не осталось свободных номеров'
)

ProductCannotBeAdded = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='Не удалось добавить продукт'
)

CategoryCannotBeAdded = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='Не удалось добавить категорию'
)

ReviewCannotBeAdded = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='Не удалось добавить отзыв'
)
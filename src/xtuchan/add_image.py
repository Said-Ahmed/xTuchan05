import os
import shutil
from datetime import datetime
from fastapi import UploadFile, HTTPException, Request


async def add_image(file: UploadFile, request: Request, folder_name: str):
    try:
        current_date = datetime.now().strftime("%Y/%m/%d")
        folder_path = os.path.join(f"src/xtuchan/static/images/{folder_name}", current_date)
        os.makedirs(folder_path, exist_ok=True)
        file_name, file_extension = os.path.splitext(file.filename)
        base_file_path = os.path.join(folder_path, f"{file_name}.webp")
        counter = 1

        while os.path.exists(base_file_path):
            base_file_path = os.path.join(folder_path, f"{file_name}_{counter}.webp")
            counter += 1

        with open(base_file_path, "wb+") as file_object:
            shutil.copyfileobj(file.file, file_object)

        await file.close()
        relative_file_path = base_file_path
        absolute_url = str(request.base_url) + relative_file_path

        return {
            "relative_path": relative_file_path[12:],
            "absolute_url": absolute_url
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при сохранении изображения: {str(e)}")
import requests

def create_yd_folder(folder_path: str, token: str) -> bool:
    """
    Создаёт папку на Яндекс.Диске.
    Возвращает True при успешном создании (HTTP 201), иначе False.
    """
    url = "https://cloud-api.yandex.net/v1/disk/resources"
    headers = {"Authorization": f"OAuth {token}"}
    params = {"path": folder_path}
    
    response = requests.put(url, headers=headers, params=params)
    
    if response.status_code == 201:
        return True
    else:
        # В реальном проекте можно логировать ошибку или поднимать исключение
        return False


def check_folder_exists(folder_path: str, token: str) -> bool:
    """
    Проверяет, существует ли папка на Яндекс.Диске.
    Возвращает True, если папка есть, иначе False.
    """
    url = "https://cloud-api.yandex.net/v1/disk/resources"
    headers = {"Authorization": f"OAuth {token}"}
    params = {"path": folder_path}
    
    response = requests.get(url, headers=headers, params=params)
    
    return response.status_code == 200
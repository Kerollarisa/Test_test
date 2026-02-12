import pytest
import requests
from unittest.mock import patch, Mock
from yandex_disk import create_yd_folder, check_folder_exists


# --------------------------------------------------------------------
# 1. Позитивный тест: успешное создание папки (HTTP 201)
# --------------------------------------------------------------------
@patch("yandex_disk.requests.put")
def test_create_folder_success(mock_put):
    # Настраиваем мок: возвращаем статус 201
    mock_response = Mock()
    mock_response.status_code = 201
    mock_put.return_value = mock_response

    token = "fake_token"
    folder = "/test_folder"

    result = create_yd_folder(folder, token)

    assert result is True
    # Проверяем, что запрос был отправлен с правильными параметрами
    mock_put.assert_called_once_with(
        "https://cloud-api.yandex.net/v1/disk/resources",
        headers={"Authorization": f"OAuth {token}"},
        params={"path": folder}
    )


# --------------------------------------------------------------------
# 2. Негативные тесты: параметризация разных кодов ошибок
# --------------------------------------------------------------------
@pytest.mark.parametrize("status_code", [
    400,  # Bad Request (некорректные данные)
    401,  # Unauthorized (неверный токен)
    403,  # Forbidden (доступ запрещён)
    404,  # Not Found (ресурс не найден, но для создания папки это ошибка)
    406,  # Not Acceptable
    409,  # Conflict (папка уже существует)
    413,  # Payload Too Large
    423,  # Locked
    429,  # Too Many Requests
    500,  # Internal Server Error
    502,  # Bad Gateway
    503,  # Service Unavailable
])
@patch("yandex_disk.requests.put")
def test_create_folder_errors(mock_put, status_code):
    # Мокаем ответ с заданным кодом ошибки
    mock_response = Mock()
    mock_response.status_code = status_code
    mock_put.return_value = mock_response

    result = create_yd_folder("/test", "token")
    assert result is False
    mock_put.assert_called_once()


# --------------------------------------------------------------------
# 3. Дополнительный позитивный тест: папка появилась в списке файлов
#    (проверка двух последовательных вызовов: создание + проверка)
# --------------------------------------------------------------------
@patch("yandex_disk.requests.put")
@patch("yandex_disk.requests.get")
def test_folder_appears_after_creation(mock_get, mock_put):
    # --- Шаг 1: успешное создание ---
    mock_put_response = Mock()
    mock_put_response.status_code = 201
    mock_put.return_value = mock_put_response

    token = "token"
    folder = "/my_folder"

    create_result = create_yd_folder(folder, token)
    assert create_result is True

    # --- Шаг 2: проверка существования папки ---
    mock_get_response = Mock()
    mock_get_response.status_code = 200   # папка найдена
    mock_get.return_value = mock_get_response

    exists = check_folder_exists(folder, token)
    assert exists is True

    # Проверяем, что GET-запрос отправлен с правильными параметрами
    mock_get.assert_called_once_with(
        "https://cloud-api.yandex.net/v1/disk/resources",
        headers={"Authorization": f"OAuth {token}"},
        params={"path": folder}
    )


# --------------------------------------------------------------------
# 4. Тест на случай, если папка НЕ появилась (например, ошибка создания)
# --------------------------------------------------------------------
@patch("yandex_disk.requests.put")
@patch("yandex_disk.requests.get")
def test_folder_does_not_appear_on_failure(mock_get, mock_put):
    # Создание не удалось
    mock_put_response = Mock()
    mock_put_response.status_code = 409   # уже существует
    mock_put.return_value = mock_put_response

    create_result = create_yd_folder("/test", "token")
    assert create_result is False

    # Проверяем, что папка не появилась (GET вернёт 404)
    mock_get_response = Mock()
    mock_get_response.status_code = 404
    mock_get.return_value = mock_get_response

    exists = check_folder_exists("/test", "token")
    assert exists is False
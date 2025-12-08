import logging
from typing import Dict, Any, Optional
from requests import Response, Session

class HTTPClient:
    def __init__(self, base_url: str, session: Optional[Session] = None):
        self.base_url = base_url.rstrip('/')
        self.session = session or Session()
        self._setup_logging()

    def _setup_logging(self):
        """Настройка логирования всех запросов"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger('HTTPClient')

    def _log_request(self, method: str, url: str, headers: Dict = None, data: Any = None):
        """Логирование исходящего запроса"""
        self.logger.info(f"→ {method.upper()} {url}")
        if headers:
            self.logger.debug(f"Headers: {headers}")
        if data:
            self.logger.debug(f"Body: {data}")

    def _log_response(self, response: Response):
        """Логирование ответа"""
        self.logger.info(f"← {response.status_code} {response.reason}")
        if response.text:
            self.logger.debug(f"Response: {response.text[:500]}...")  # Ограничиваем длину

    def _build_url(self, endpoint: str) -> str:
        """Сборка полного URL"""
        endpoint = endpoint.lstrip('/')
        return f"{self.base_url}/{endpoint}"

    def request(self, method: str, endpoint: str,
                headers: Dict[str, str] = None,
                params: Dict[str, Any] = None,
                json: Any = None,
                data: Any = None) -> Response:
        """
        Базовый метод для отправки HTTP запросов
        """
        url = self._build_url(endpoint)

        # Логируем запрос
        self._log_request(method, url, headers, json or data)

        # Отправляем запрос
        response = self.session.request(
            method=method.upper(),
            url=url,
            headers=headers,
            params=params,
            json=json,
            data=data
        )

        # Логируем ответ
        self._log_response(response)

        return response

    # Специфичные HTTP методы
    def get(self, endpoint: str, params: Dict[str, Any] = None,
            headers: Dict[str, str] = None) -> Response:
        return self.request('GET', endpoint, headers=headers, params=params)

    def post(self, endpoint: str, json: Any = None, data: Any = None,
             headers: Dict[str, str] = None) -> Response:
        return self.request('POST', endpoint, headers=headers, json=json, data=data)

    def put(self, endpoint: str, json: Any = None, data: Any = None,
            headers: Dict[str, str] = None) -> Response:
        return self.request('PUT', endpoint, headers=headers, json=json, data=data)

    def patch(self, endpoint: str, json: Any = None, data: Any = None,
              headers: Dict[str, str] = None) -> Response:
        return self.request('PATCH', endpoint, headers=headers, json=json, data=data)

    def delete(self, endpoint: str, headers: Dict[str, str] = None) -> Response:
        return self.request('DELETE', endpoint, headers=headers)

    def set_headers(self, headers: Dict[str, str]):
        """Установка общих заголовков для всех запросов"""
        self.session.headers.update(headers)

    def clear_headers(self):
        """Очистка заголовков сессии"""
        self.session.headers.clear()
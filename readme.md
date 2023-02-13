Сервис для ослеживания маршрута транспорта

Запуск:
  1. Собрать докер "docker-compose build"
  2. Поднять контейнер "docker-compose up"
  3. Создать суперюзера "docker exec -it web_stations python manage.py createsuperuser"
  5. Добавить транспорт, маршрут, остановки "http://0.0.0.0:8088/admin/"
  6. Карта с отображением транспорта "http://0.0.0.0:8088/routes/map"

# Приложение для анализа банковских операций

## Описание проекта

TransactionAnalyzer — это проект, направленный на анализ транзакций. Он предоставляет инструменты для обработки и анализа данных о финансовых операциях, что позволяет получить ценную информацию и выявить закономерности.
Является курсовой работой на курсе Python - разработчик от компании Sky Pro.

## Функциональность

- **Модуль [views.py](src/views.py):** содержит функцию **get_response** которая возвращает данные для Главной страницы в формате json вида:
```python
{
  "greeting": "Добрый день",
  "cards": [
    {
      "last_digits": "5814",
      "total_spent": 1262.00,
      "cashback": 12.62
    },
    {
      "last_digits": "7512",
      "total_spent": 7.94,
      "cashback": 0.08
    }
  ],
  "top_transactions": [
    {
      "date": "21.12.2021",
      "amount": 1198.23,
      "category": "Переводы",
      "description": "Перевод Кредитная карта. ТП 10.2 RUR"
    },
    {
      "date": "20.12.2021",
      "amount": 829.00,
      "category": "Супермаркеты",
      "description": "Лента"
    },
    {
      "date": "20.12.2021",
      "amount": 421.00,
      "category": "Различные товары",
      "description": "Ozon.ru"
    },
    {
      "date": "16.12.2021",
      "amount": -14216.42,
      "category": "ЖКХ",
      "description": "ЖКУ Квартира"
    },
    {
      "date": "16.12.2021",
      "amount": 453.00,
      "category": "Бонусы",
      "description": "Кешбэк за обычные покупки"
    }
  ],
  "currency_rates": [
    {
      "currency": "USD",
      "rate": 73.21
    },
    {
      "currency": "EUR",
      "rate": 87.08
    }
  ],
  "stock_prices": [
    {
      "stock": "AAPL",
      "price": 150.12
    },
    {
      "stock": "AMZN",
      "price": 3173.18
    },
    {
      "stock": "GOOGL",
      "price": 2742.39
    },
    {
      "stock": "MSFT",
      "price": 296.71
    },
    {
      "stock": "TSLA",
      "price": 1007.08
    }
  ]
}
```
Данные о валютах и акциях, по которым нужно получать данные из API берутся из
data/user_settings.json формата:
```python
{
  "user_currencies": [
    "USD",
    "EUR"
  ],
  "user_stocks": [
    "AAPL",
    "AMZN",
    "GOOGL",
    "MSFT",
    "TSLA"
  ]
}
```
- **Модуль [utils.py](src/utils.py):** содержит вспомогательные функции для получения данных в нужном формате. Подробное описание функций содержится в **docstrings**
- **Модуль [services.py](src/services.py):** содержит функцию для подсчета лучших категорий **get_best_categories**
- **Модуль [reports.py](src/reports.py):** содержит функцию получения данных за период по выбранной категории **spending_by_category**. 
Также содержит декоратор **report_to_file** позволяющий записывать отчеты в файл в папке **reports**.   

## Как начать работу

1. **Клонируйте репозиторий:**
   ```bash
   git clone https://github.com/LexaSolovev/TransactionAnalyzer.git
   ```

2. **Установите зависимости:**
   ```bash
   poetry install
   ```

3. **Запустите приложение:**
   ```bash
   python main.py
   ```

## Структура проекта

- **data:** каталог для хранения данных о транзакциях.
- **logs:** каталог с логами
- **reports:** каталог с файлами отчетов
- **src:** каталог с исходным кодом проекта.
- **tests:** каталог с тестами для проекта.
- **pyproject.toml:** файл с зависимостями проекта.

## Тестирование

Для запуска тестов используйте следующую команду:
```bash
pytest
```

## Авторы

- **Алексей Соловьёв:** основной разработчик проекта.

## Лицензия

Этот проект распространяется под лицензией [MIT](https://choosealicense.com/licenses/mit/).

## Обратная связь

Если у вас есть вопросы, предложения или замечания по проекту, пожалуйста, свяжитесь с нами через [GitHub Issues](https://github.com/LexaSolovev/TransactionAnalyzer/issues).
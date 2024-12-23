import yfinance as yf
import pandas as pd


def is_valid_ticker(ticker):
    try:
        stock = yf.Ticker(ticker)
        return stock.info['symbol'] == ticker.upper()
    except KeyError:
        return False  # Если не удалось получить информацию о тикере, считаем его несуществующим


def get_valid_ticker():
    while True:
        ticker = input("Введите тикер акций: ").strip().upper()
        if is_valid_ticker(ticker):
            return ticker
        else:
            print(f"Тикер {ticker} не существует. Пожалуйста, попробуйте снова.")


def fetch_stock_data(ticker, period=None, start_date=None, end_date=None):
    """
    Получает исторические данные акций по заданному тикеру с учетом периода или дат начала и окончания.

    :param ticker: Тикер акций (например, 'AAPL' для Apple).
    :param period: Период исторических данных (например, '1mo', '1y').
    :param start_date: Дата начала в формате 'YYYY-MM-DD'.
    :param end_date: Дата окончания в формате 'YYYY-MM-DD'.
    :return: DataFrame с историческими данными акций.
    """
    stock = yf.Ticker(ticker)

    try:
        if start_date and end_date:
            data = stock.history(start=start_date, end=end_date)
        elif period:
            data = stock.history(period=period)
        else:
            raise ValueError("Укажите либо период, либо даты начала и окончания.")

        if data.empty:
            raise ValueError("Нет доступных данных для указанного тикера.")

        return data
    except Exception as e:
        print(f"Ошибка при получении данных для {ticker}: {e}")
        return pd.DataFrame()  # Возвращаем пустой DataFrame в случае ошибки


def add_moving_average(data, window_size=5):
    if 'Close' not in data.columns:
        raise ValueError("DataFrame не содержит столбец 'Close'.")
    data['Moving_Average'] = data['Close'].rolling(window=window_size).mean()
    return data


def calculate_rsi(data, window=14):
    if 'Close' not in data.columns:
        raise ValueError("DataFrame не содержит столбец 'Close'.")

    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()

    # Обработка деления на ноль
    rs = gain / loss.replace(0, pd.NA)  # Заменяем ноль на NaN, чтобы избежать деления на ноль
    rsi = 100 - (100 / (1 + rs))
    data['RSI'] = rsi
    return data


def calculate_macd(data, short_window=12, long_window=26, signal_window=9):
    if 'Close' not in data.columns:
        raise ValueError("DataFrame не содержит столбец 'Close'.")

    data['EMA_12'] = data['Close'].ewm(span=short_window, adjust=False).mean()
    data['EMA_26'] = data['Close'].ewm(span=long_window, adjust=False).mean()
    data['MACD'] = data['EMA_12'] - data['EMA_26']
    data['Signal_Line'] = data['MACD'].ewm(span=signal_window, adjust=False).mean()
    return data
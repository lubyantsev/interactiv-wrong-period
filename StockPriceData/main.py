import matplotlib.pyplot as plt
import data_download as dd
import data_plotting as dplt
from data_analysis import calculate_and_display_average_price, notify_if_strong_fluctuations, export_data_to_csv, \
    calculate_standard_deviation, calculate_bollinger_bands
from interactive_graph import plot_interactive_graph


def main():
    """
    Основная функция, управляющая процессом загрузки, обработки и визуализации данных о биржевых акциях.

    Функция выполняет следующие действия:
    1. Приветствует пользователя и предоставляет информацию о доступных тикерах и периодах.
    2. Запрашивает ввод тикера акции и периода для получения данных.
    3. Запрашивает порог для уведомления о колебаниях цен.
    4. Загружает данные о выбранной акции за указанный период.
    5. Добавляет скользящее среднее к загруженным данным.
    6. Строит и сохраняет график цен закрытия и скользящих средних.
    7. Рассчитывает и отображает среднюю цену закрытия, индекс относительной силы (RSI), MACD и сигнальную линию.
    8. Уведомляет пользователя о сильных колебаниях цен, если они превышают заданный порог.
    """
    try:
        print("Добро пожаловать в инструмент получения и построения графиков биржевых данных.")
        print(
            "Вот несколько примеров биржевых тикеров, которые вы можете рассмотреть: AAPL (Apple Inc), GOOGL (Alphabet Inc), MSFT (Microsoft Corporation), AMZN (Amazon.com Inc), TSLA (Tesla Inc).")

        while True:
            ticker = input("Введите тикер акции (например, «AAPL» для Apple Inc): ").strip().upper()
            if ticker == "":
                print("Тикер не может быть пустым. Пожалуйста, введите корректный тикер.")
            elif not dd.is_valid_ticker(ticker):
                print("Некорректный тикер. Пожалуйста, введите действительный тикер.")
            else:
                break

        print(
            "Общие периоды времени для данных о записях включают: 1д, 5д, 1мес, 3мес, 6мес, 1г, 2г, 5л, 10л, с начала года, макс.")

        # Запрос выбора периода
        use_custom_dates = input("Хотите использовать конкретные даты начала и окончания? (да/нет): ")

        if use_custom_dates.lower() == 'да':
            start_date = input("Введите дату начала в формате YYYY-MM-DD: ")
            end_date = input("Введите дату окончания в формате YYYY-MM-DD: ")
            period = None  # Период не нужен, если используются конкретные даты
        else:
            period = input("Введите период для данных (например, '1mo' для одного месяца): ")
            start_date = None  # Параметры дат остаются пустыми
            end_date = None

        # Запрос стиля графика
        # Список стилей, которые, как правило, изменяют график
        known_styles = [
            'seaborn-v0_8', 'seaborn-v0_8-whitegrid', 'ggplot',
            'fivethirtyeight', 'bmh', 'dark_background', 'fast',
            'classic', 'Solarize_Light2'
        ]

        print("Доступные стили графика:")
        available_styles = [style for style in plt.style.available if style in known_styles]

        # Вывод доступных стилей в одну строку
        print(", ".join(f"{i + 1}: {style}" for i, style in enumerate(available_styles)))

        # Установка значения по умолчанию
        style = 'classic'  # Значение по умолчанию для стиля графика

        # Запрос стиля с использованием номера
        while True:
            try:
                style_index = int(input("Выберите номер стиля графика из доступных: ")) - 1
                if 0 <= style_index < len(available_styles):
                    style = available_styles[style_index]
                    plt.style.use(style)
                    break
                else:
                    print("Недопустимый номер. Пожалуйста, выберите номер из списка.")
            except ValueError:
                plt.style.use('classic')
                print("Ошибка ввода. Установлен стиль 'classic'.")
                break

        # Запрос порога колебаний
        threshold_input = input("Введите порог для уведомления о колебаниях (в процентах): ")

        # Проверка на пустую строку
        if threshold_input.strip() == "":
            print("Вы не ввели запрашиваемый порог в процентах, уведомления не будет.")
            threshold = None  # Устанавливаем порог в None, если пользователь не ввел значение
        else:
            threshold = float(threshold_input)  # Преобразуем введенное значение в число

        # Fetch stock data
        stock_data = dd.fetch_stock_data(ticker, period, start_date, end_date)

        # Add moving average to the data
        stock_data = dd.add_moving_average(stock_data)

        # Calculate additional indicators
        stock_data = dd.calculate_rsi(stock_data)
        stock_data = dd.calculate_macd(stock_data)

        # Calculate standard deviation
        stock_data = calculate_standard_deviation(stock_data)

        # Calculate Bollinger Bands
        stock_data = calculate_bollinger_bands(stock_data)

        # Plot the data
        if use_custom_dates.lower() == 'да':
            filename = f"{ticker}_{start_date}_to_{end_date}.png"
        else:
            filename = f"{ticker}_{period}.png"

        # Notify if there are strong fluctuations
        notify_if_strong_fluctuations(stock_data, threshold)

        # Calculate and display the average price
        calculate_and_display_average_price(stock_data)

        # Export data to CSV
        export_filename = input("Введите имя файла для экспорта данных (например, 'stock_data.csv'): ")

        # Проверка на пустую строку
        if export_filename.strip() == "":
            print("Соответствующий файл не был создан.")
        else:
            export_data_to_csv(stock_data, export_filename)

        dplt.create_and_save_plot(stock_data, ticker, period, filename, style)

        if use_custom_dates.lower() == 'да':
            filename = f"{ticker}_{start_date}_to_{end_date}.png"
        else:
            filename = f"{ticker}_{period}.png"

        if use_custom_dates == 'да':
            filename = f"{ticker}_{start_date}_to_{end_date}.png"
            period_text = f"за период с {start_date} по {end_date}"
        else:
            filename = f"{ticker}_{period}.png"
            period_text = f"за период {period}"

        # Вызываем функцию для построения графика с передачей дат
        plot_interactive_graph(stock_data, ticker, period, start_date, end_date, period_text)


    except KeyboardInterrupt:
        print("\nПрограмма остановлена пользователем.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()
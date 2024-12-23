import plotly.graph_objects as go

def plot_interactive_graph(stock_data, ticker, period, start_date, end_date, period_text):    # Проверяем, что DataFrame содержит колонку 'Close'
    if 'Close' not in stock_data.columns:
        print("В DataFrame отсутствует колонка 'Close'.")
        return

    # Вычисляем среднее значение колонки 'Close'
    average_close = stock_data['Close'].mean()
    print(f"Среднее значение колонки 'Close': {average_close:.4f}")

    # Создаем интерактивный график
    fig = go.Figure()

    # Добавляем линии для 'Close' и среднего
    fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data['Close'], mode='lines', name='Close'))
    fig.add_trace(go.Scatter(x=stock_data.index, y=[average_close] * len(stock_data), mode='lines', name='Среднее', line=dict(dash='dash')))

    # Настройка графика
    fig.update_layout(title=f'Интерактивный график цен акций: {ticker} за период {period}' if period else f'Интерактивный график цен акций: {ticker}',
                      xaxis_title='Дата',
                      yaxis_title='Цена',
                      legend=dict(x=0, y=1))

    fig.add_annotation(
        text=f'Период: {start_date} - {end_date}',
        xref='paper', yref='paper',
        x=0.5, y=1.1,  # Позиционирование аннотации
        showarrow=False,
        font=dict(size=12)
    )


    # Отображаем график
    fig.show()
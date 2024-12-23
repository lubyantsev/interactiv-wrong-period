import matplotlib.pyplot as plt

# Вывод всех доступных стилей графиков
available_styles = plt.style.available
print("Доступные стили графиков:")
for style in available_styles:
    print(style)

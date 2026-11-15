import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns

print("Читання датасету os_telemetry.csv...")

try:

    df = pd.read_csv('os_telemetry.csv')
except FileNotFoundError:
    print("Помилка: Файл os_telemetry.csv не знайдено. Спочатку запустіть монітор.")
    exit()

df['Context_Switches_per_sec'] = df['Context_Switches'].diff().fillna(0)

sns.set_theme(style="whitegrid")

fig, axes = plt.subplots(4, 1, figsize=(10, 14), sharex=True)
fig.suptitle('Аналіз телеметрії ОС під навантаженням (Ryzen 7 5750G)', fontsize=16, fontweight='bold', y=0.98)

sns.lineplot(ax=axes[0], data=df, x='Time', y='CPU_%', color='#d62728', linewidth=2)
axes[0].set_title('Завантаження CPU (%)', fontsize=12)
axes[0].set_ylabel('CPU %')
axes[0].set_ylim(-5, 105)
axes[0].fill_between(df['Time'], df['CPU_%'], alpha=0.1, color='#d62728')

sns.lineplot(ax=axes[1], data=df, x='Time', y='RAM_Free_MB', color='#1f77b4', linewidth=2)
axes[1].set_title('Вільна оперативна пам\'ять (МБ)', fontsize=12)
axes[1].set_ylabel('Вільна RAM (МБ)')
axes[1].fill_between(df['Time'], df['RAM_Free_MB'], alpha=0.1, color='#1f77b4')

sns.lineplot(ax=axes[2], data=df, x='Time', y='Disk_Write_MB_s', color='#2ca02c', linewidth=2)
axes[2].set_title('Швидкість запису на диск (МБ/с)', fontsize=12)
axes[2].set_ylabel('Запис (МБ/с)')
axes[2].fill_between(df['Time'], df['Disk_Write_MB_s'], alpha=0.1, color='#2ca02c')

sns.lineplot(ax=axes[3], data=df, x='Time', y='Context_Switches_per_sec', color='#9467bd', linewidth=2)
axes[3].set_title('Динаміка перемикань контексту (Кількість операцій на секунду)', fontsize=12)
axes[3].set_ylabel('Перемикань / сек')
axes[3].set_xlabel('Точний час')
axes[3].fill_between(df['Time'], df['Context_Switches_per_sec'], alpha=0.1, color='#9467bd')


for ax in axes:
    ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=10))

plt.xticks(rotation=45)
plt.tight_layout()


filename = 'os_analysis_report.png'
plt.savefig(filename, dpi=300, bbox_inches='tight')
print(f"Графіки успішно згенеровані! Шукайте файл {filename} у папці з проєктом.")

plt.show()
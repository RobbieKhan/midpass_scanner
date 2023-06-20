import time
import constants
import threading
import matplotlib.pyplot as plt
from typing import List, Dict
from collections import OrderedDict


internal_statuses = ['0%', '5%', '10%', '20%', '30%', '60%', '70%', '80%', '90%', '100%']

internal_statuses_str = [(0, "заявление создано"),
                         (5, "готово"),
                         (10, "отправлено"),
                         (20, "принято в обработку"),
                         (20, "приостановлено"),
                         (30, "отправлено на согласование"),
                         (30, "на согласовании"),
                         (30, "дополнительная проверка"),
                         (60, "согласовано письмом"),
                         (60, "согласовано"),
                         (70, "персонализация разрешена"),
                         (70, "на персонализации"),
                         (80, "паспорт поступил"),
                         (80, "паспорт отправлен в РКЗУ"),
                         (90, "паспорт поступил"),
                         (10, "паспорт верен"),
                         (0, "паспорт выдан"),
                         (0, "отказ в согласовании"),
                         (0, "отмена изготовления паспорта"),
                         (0, "почтовое отправление")]

statuses_colors = {0: 'darkgreen',
                   5: 'darkred',
                   10: 'red',
                   20: 'lightcoral',
                   30: 'orange',
                   60: 'gold',
                   70: 'palegoldenrot',
                   80: 'palegreen',
                   90: 'green',
                   100: 'darkgreen'}


class Diagram:

    def __init__(self):
        self.fig, self.ax = plt.subplots()
        self.ax.tick_params(labelrotation=45)
        self.legend = self.ax.legend(internal_statuses)
        self.filename: str = ''

        self.appended_date: str = ''
        self.appended_percent: List[int] = list()

    def set_filename(self, filename: str):
        self.filename = filename

    def build_from_file(self):
        file = open(constants.RESULTS_DIRECTORY_NAME + self.filename, 'r')
        file_recordings: List[str] = file.readlines()
        file.close()
        recordings_number: int = len(file_recordings)
        recordings_date: List[str] = [rec.split(', ')[0] for rec in file_recordings]
        recordings_percent: List[int] = [int(rec.split(', ')[2]) for rec in file_recordings]
        recordings_status: List[str] = [rec.split(', ')[3].rstrip('\n') for rec in file_recordings]
        recordings_types_per_day: Dict[int, float] = dict()
        for rec_idx in range(0, recordings_number - 1):
            recordings_types_per_day[recordings_percent[rec_idx]] = recordings_types_per_day.get(
                recordings_percent[rec_idx], 0) + 1
            # Check if it is already another day
            if recordings_date[rec_idx] != recordings_date[rec_idx + 1]:
                # Next day is another day. Normalize data and plot a diagram for current day
                normalization_factor = 1.0 / sum(recordings_types_per_day.values())
                for item_idx in recordings_types_per_day:
                    recordings_types_per_day[item_idx] = recordings_types_per_day[item_idx] * normalization_factor
                # Sort data by internal status (in percents)
                recordings_types_per_day_sorted = OrderedDict(sorted(recordings_types_per_day.items(), reverse=True))
                # Start plotting
                height_offset = 0
                recordings_freq = list(recordings_types_per_day_sorted.values())
                recordings_type = list(recordings_types_per_day_sorted.keys())
                for rec_type_idx, _ in enumerate(recordings_freq):
                    height_offset += recordings_freq[rec_type_idx]
                    plot_start = 1 - height_offset
                    bar = self.ax.bar(recordings_date[rec_idx], recordings_freq[rec_type_idx],
                                      bottom=plot_start,
                                      width=0.8,
                                      label=recordings_type[rec_type_idx],
                                      color=statuses_colors[recordings_type[rec_type_idx]],
                                      edgecolor='black', linewidth=2)
                    self.ax.bar_label(bar, label_type='center', color='white')
                recordings_types_per_day.clear()
            time.sleep(0.01)
            plt.draw()

    def draw_diagram_from_file(self):
        threading.Thread(target=self.build_from_file, daemon=True).start()
        plt.show()

    def append_data(self, date: str, percent: int):
        self.appended_date = date
        self.appended_percent.append(percent)

    def build_appended(self):
        recordings_types_per_day: Dict[int, float] = dict()
        for rec_idx in range(0, len(self.appended_percent)):
            recordings_types_per_day[self.appended_percent[rec_idx]] = recordings_types_per_day.get(
                self.appended_percent[rec_idx], 0) + 1
        # Normalize data and plot a diagram for current day
        normalization_factor = 1 / sum(recordings_types_per_day.values())
        for item_idx in recordings_types_per_day:
            recordings_types_per_day[item_idx] = round(recordings_types_per_day[item_idx] * normalization_factor, 2)
        # Sort data by internal status (in percents)
        recordings_types_per_day_sorted = OrderedDict(sorted(recordings_types_per_day.items(), reverse=True))
        # Start plotting
        height_offset = 0
        recordings_freq = list(recordings_types_per_day_sorted.values())
        recordings_type = list(recordings_types_per_day_sorted.keys())
        for rec_type_idx, _ in enumerate(recordings_freq):
            height_offset += recordings_freq[rec_type_idx]
            plot_start = 1 - height_offset
            bar = self.ax.bar(self.appended_date, recordings_freq[rec_type_idx],
                              bottom=plot_start,
                              width=0.8,
                              label=recordings_type[rec_type_idx],
                              color=statuses_colors[recordings_type[rec_type_idx]],
                              edgecolor='black', linewidth=2)
            self.ax.bar_label(bar, label_type='center', color='black', rotation=90)
        # self.legend = plt.legend(ncols=len(statuses_colors), bbox_to_anchor=(0, 1), loc='lower left', fontsize='small')
        # self.legend = self.ax.legend(internal_statuses)
        recordings_types_per_day.clear()
        self.appended_percent.clear()
        self.appended_date = ''
        plt.draw()

import time
import threading
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from ui.constants import *
from typing import List, Dict
from collections import OrderedDict

STATUS_COLOR_IDX = 0
STATUS_LABEL_IDX = 1


class Diagram:

    def __init__(self):
        self.fig, self.ax = plt.subplots()
        self.ax.tick_params(labelrotation=45)
        self.ax.set_ylabel('Доля паспортов на каждом этапе / день \n', fontsize='medium')
        self.filename: str = ''

        self.appended_date: str = ''
        self.appended_percent: List[int] = list()

        self.statuses: dict = {5: ['#660033', 'Заявление принято'],
                               10: ['#990033', 'Заявление отправлено в РФ'],
                               20: ['#ff3300', 'В обработке'],
                               30: ['#ff9900', 'На согласовании'],
                               60: ['#cc9900', 'Одобрен'],
                               70: ['#99cc00', 'В печати'],
                               80: ['#669900', 'Отправлен в консульство'],
                               90: ['#009933', 'В консульстве'],
                               100: ['#006600', 'Готов к выдаче'],
                               0: ['#003300', 'Выдан \\ отменен']}
        # Create custom legend based on statuses above
        self.__create_legend()

    def set_filename(self, filename: str):
        self.filename = filename

    def build_from_file(self):
        file = open(RESULTS_DIRECTORY_NAME + self.filename, 'r')
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
                recordings_sum = sum(recordings_types_per_day.values())
                for item_idx in recordings_types_per_day:
                    recordings_types_per_day[item_idx] = recordings_types_per_day[item_idx] / recordings_sum
                recordings_types_per_day[next(iter(recordings_types_per_day))] += 1.0 - sum(recordings_types_per_day.values())
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
                                      color=self.statuses[recordings_type[rec_type_idx]][STATUS_COLOR_IDX],
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
        if not self.appended_percent:
            return
        recordings_types_per_day: Dict[int, float] = dict()
        for rec_idx in range(0, len(self.appended_percent)):
            recordings_types_per_day[self.appended_percent[rec_idx]] = recordings_types_per_day.get(
                self.appended_percent[rec_idx], 0) + 1
        # Normalize data and plot a diagram for current day
        recordings_sum = sum(recordings_types_per_day.values())
        for item_idx in recordings_types_per_day:
            recordings_types_per_day[item_idx] = round(recordings_types_per_day[item_idx] / recordings_sum, 2)
        recordings_types_per_day[next(iter(recordings_types_per_day))] += 1.0 - sum(recordings_types_per_day.values())
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
                              color=self.statuses[recordings_type[rec_type_idx]][STATUS_COLOR_IDX],
                              edgecolor='black', linewidth=2)
            self.ax.bar_label(bar, label_type='center', color='black', rotation=90)
        recordings_types_per_day.clear()
        self.appended_percent.clear()
        self.appended_date = ''
        plt.draw()

    def clear(self):
        self.ax.cla()
        self.ax.set_ylabel('Доля паспортов на каждом этапе / день \n', fontsize='medium')
        plt.draw()

    def __create_legend(self):
        patches = list()
        for idx, _ in enumerate(self.statuses):
            if 90 == list(self.statuses.keys())[idx]:
                # This status is never met anyway
                continue
            color = list(self.statuses.values())[idx][STATUS_COLOR_IDX]
            label = list(self.statuses.values())[idx][STATUS_LABEL_IDX]
            patch = mpatches.Patch(color=color, label=label)
            patches.append(patch)
        self.fig.legend(handles=patches, ncol=len(patches) / 3, loc='upper center')

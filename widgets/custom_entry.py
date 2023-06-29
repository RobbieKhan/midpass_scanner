from typing import Optional, Union
import customtkinter
import gc


class CTkEntry(customtkinter.CTkEntry):

    def __init__(self, limits: tuple = (Optional[Union[None, int]], Optional[Union[None, int]]), **kwargs):
        self._sv = customtkinter.StringVar(value='0')

        super().__init__(textvariable=self._sv, **kwargs)

        self._limit_min = None
        self._limit_max = None
        try:
            self._limit_min = limits[0]
            if self._limit_min is not None:
                self._sv.trace('w', lambda n, i, m, sv=self._sv: self.__validator_entry_input_min(sv))
        except KeyError:
            pass
        try:
            self._limit_max = limits[1]
            if self._limit_max is not None:
                self._sv.trace('w', lambda n, i, m, sv=self._sv: self.__validator_entry_input_max(sv))
        except KeyError:
            pass

    def __validator_entry_input_min(self, sv):
        try:
            new_value = int(sv.get())
            if new_value < self._limit_min:
                sv.set(str(self._limit_min))
            else:
                sv.set(str(new_value))
        except ValueError:
            pass

    def __validator_entry_input_max(self, sv):
        try:
            new_value = int(sv.get())
            if new_value > self._limit_max:
                sv.set(str(self._limit_max))
            else:
                sv.set(str(new_value))
        except ValueError:
            pass

    def get_int(self) -> int:
        try:
            int_val = int(super().get())
        except ValueError:
            int_val = 0
        return int_val

    def set(self, value: str):
        self._sv.set(value)
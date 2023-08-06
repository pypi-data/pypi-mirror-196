from .descriptors import ISO_code_reminder
import pandas as pd
from .logger_helper import logger
from typing import Any, Literal, Optional, Self, Literal
import numpy as np
import json
from .unitils import g_to_v, v_to_s, lazyproperty, g_to_s
from numpy.typing import NDArray
from .unitils import is_most_postive
import os


class CSV_Data_Converter:
    x_code = ISO_code_reminder()
    y_code = ISO_code_reminder()
    z_code = ISO_code_reminder()

    def __init__(self, name: str, path: str, speed_kph: float, **kwargs):
        """必传path关键字参数！
        可选kwargs： step, start,end,x_code,y_code,z_code
        """
        self.name = name
        self.speed_kph = speed_kph
        self.path = path
        self.step = 0.1  # 采样间隔ms数
        self.start = 0
        self.end = 200
        self.data = self._read_data()
        for k, v in kwargs.items():
            setattr(self, k, v)

    def _read_data(self):

        ext = os.path.splitext(self.path)[-1]
        data = None
        if ext == '.csv':
            data = pd.read_csv(self.path, sep=";")
        elif ext == ".xlsx" or ext == ".xls":
            data = pd.read_excel(self.path)
        if data is not None:
            return data
        raise TypeError(f"file ext should be in [.csv,.xlsx,.xls],your input ext is {ext}!")

    def __repr__(self) -> str:
        return f"<{self.name} CSV data converter> -path {self.path}"

    @lazyproperty
    def body_x_g(self):
        x_g = self.find_data_only_by_iso(self.x_code, transformed=True)
        return x_g

    @lazyproperty
    def body_y_g(self):
        y_g = self.find_data_only_by_iso(self.y_code)
        return y_g

    @lazyproperty
    def body_z_g(self):
        z_g = self.find_data_only_by_iso(self.z_code)
        return z_g

    @lazyproperty
    def body_x_v(self):
        res = g_to_v(self.body_x_g, dx=self.step, initial_kph=self.speed_kph)
        return res

    @lazyproperty
    def body_y_v(self):
        return g_to_v(self.body_y_g, dx=self.step, initial_kph=0)

    @lazyproperty
    def body_z_v(self):
        return g_to_v(self.body_z_g, dx=self.step, initial_kph=0)

    @lazyproperty
    def body_x_s(self):
        return v_to_s(self.body_x_v, dx=self.step)

    @lazyproperty
    def body_y_s(self):
        return v_to_s(self.body_y_v, dx=self.step)

    @lazyproperty
    def body_z_s(self):
        return v_to_s(self.body_z_v, dx=self.step)

    def __str__(self):
        return f"<{self.__class__.__name__}>:{self.path}"

    def body_value_getter(self, direction: Literal["x", "y", "z"],
                          value_type: Literal["g", "v", "s"]) -> NDArray:
        direction = str(direction).lower()  # type: ignore
        value_type = str(value_type).lower()  # type: ignore
        attr_name = f"body_{direction}_{value_type}"
        return getattr(self, attr_name)

    @property
    def time_series(self) -> NDArray:
        return np.arange(self.start, self.end + self.step, self.step)

    def _find_series_full_by_iso(self, iso_code: str, order: int = 0) -> pd.Series | None:
        """若找到,则返回一列series,如果根据iso code筛选到DF多列,根据order筛选,其余数据丢弃。
        否会返回None
        """
        res: pd.DataFrame = self.data.loc[:, self.data.iloc[0, :] == iso_code]
        num = len(res.columns)

        if num == 0:  # 没找到数据
            logger.warning(f"iso code:{iso_code}在{self.path}中检索到的数据中找不到")
            return None

        if num > 1:
            logger.warning(f'''iso code:{iso_code}在{self.path}中检索到的数据不唯一,当前使用第{order}条数据，共{num}条:
            {res.columns}
            ''')
        final_res: pd.Series = res.iloc[:, order]
        return final_res

    def find_unit_by_iso(self, iso_code: str) -> str:
        seri = self._find_series_full_by_iso(iso_code=iso_code)
        return str(seri[2])

    def is_data_exsited(self, iso_code: str) -> bool:
        if self.find_data_only_by_iso(iso_code):
            return True
        return False

    def find_data_only_by_iso(self, iso_code: str, order: int = 0,
                              transformed: bool = False) -> NDArray | None:
        """若找到,则返回一列纯数据,如果根据iso code筛选到多列,根据order筛选,默认第0列,其余数据丢弃。
        若找不到会返回None
        transformed: 默认关闭。 将数据翻转为正值
        """
        res_series = self._find_series_full_by_iso(
            iso_code=iso_code, order=order)
        if res_series is None:
            logger.warning(f"{repr(self)} can not find iso-{iso_code} data! ")
            return None
        res = res_series[3:].astype("float").values
        res = np.nan_to_num(res)
        if transformed:
            if not is_most_postive(res):
                res = -res
        return res

    def find_chart_title_by_iso(self, iso_code: str, chart_title: str = None):
        title = self._find_series_full_by_iso(iso_code=iso_code)[1]
        return chart_title if chart_title else title

    def create_draft_clear_iso_code_json_file_wo_seat_position(self,
                                                               start_filter_str: str,
                                                               output_json_file_name: str):
        df = self.data
        bool_col = df.iloc[0, :].str.startswith(start_filter_str)
        bool_col.fillna(False, inplace=True)
        data = df.loc[:3, bool_col]

        res = {}
        for col_index in data.columns:
            seri = data[col_index]
            name = str(seri[1])

            # 替换一些不适合做属性字符串的值
            sybs = [" ", "(", ")"]
            for syb in sybs:
                name = name.replace(syb, "_")

            iso_code = seri[0]

            unit = seri[2]
            res[name] = {"code": iso_code[2:], "unit": unit}

        with open(output_json_file_name, "w") as f:
            json.dump(res, f, indent=4)
        print(f"successful write {output_json_file_name}!")

    @staticmethod
    def confirm_seat_position_by_iso(iso_code: str) -> str:
        position_mapper = {"11": "DR",
                           "13": "PS",
                           "14": "RL",
                           "16": "RR"}
        starts = iso_code.strip()[:2]
        return position_mapper.get(starts, "Unknown")

    @staticmethod
    def confirm_LE_UP(iso_code: str) -> str:  # 针对tibia这种
        """返回左右和上下信息str,如"Left Upper"
        """
        iso_code = iso_code.strip()

        LE_mapper = {
            "LE": "Left",
            "RI": "Right"
        }
        UP_mapper = {
            "UP": "Upper",
            "LO": "lower",
        }
        le = iso_code[6:8]
        up = iso_code[8:10]
        return LE_mapper.get(le, "Unkown") + " " + UP_mapper.get(up, "Unkown")

    def g_to_v_by_iso(self, iso_code: str, initial_kph_mode: bool = False) -> NDArray:
        acc_g = self.find_data_only_by_iso(iso_code, transformed=initial_kph_mode)
        initial_kph = self.speed_kph if initial_kph_mode else 0
        if acc_g is None:
            logger.error(f"g_to_v NG due to acc_g have no value, because {repr(self)} can not find iso-{iso_code} data")
            raise ValueError(
                f"g_to_v NG due to acc_g have no value, because {repr(self)} can not find iso-{iso_code} data")
        res = g_to_v(acc_g=acc_g, dx=self.step, initial_kph=initial_kph)
        return res

    def g_to_s_by_iso(self, iso_code: str, initial_kph_mode: bool = False) -> NDArray:
        acc_g = self.find_data_only_by_iso(iso_code, transformed=initial_kph_mode)
        initial_kph = self.speed_kph if initial_kph_mode else 0
        if acc_g is None:
            logger.error(f"g_to_s NG due to acc_g have no value, because {repr(self)} can not find iso-{iso_code} data")
            raise ValueError(
                f"g_to_s NG due to acc_g have no value, because {repr(self)} can not find iso-{iso_code} data")
        res = g_to_s(acc_g=acc_g, dx=self.step, initial_kph=initial_kph)
        return res

    @property
    def body_codes(self):  # [x_code, y_code, z_code]
        return [self.x_code, self.y_code, self.z_code]

    @staticmethod
    def i_direction(iso_code: str) -> str:  # "X","Y","Z"
        return iso_code[-2].upper()

    @staticmethod
    def is_x_direction(iso_code: str) -> bool:
        return iso_code[-2].upper() == "X"

    @staticmethod
    def is_y_direction(iso_code: str) -> bool:
        return iso_code[-2].upper() == "Y"

    @staticmethod
    def is_z_direction(iso_code: str) -> bool:
        return iso_code[-2].upper() == "Z"

    @staticmethod
    def is_acc_by_iso(iso_code: str) -> bool:
        t = iso_code.strip()[-4:-2]  # ACC 为“AC”
        return t == "AC"

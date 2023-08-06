from enum import Enum


class APIVersion(Enum):
    APRIL_2021 = '2021-04'
    OCTOBER_2021 = '2021-10'
    JANUARY_2022 = '2022-01'
    JULY_2022 = '2022-07'
    JANUARY_2023 = '2023-01'


BASE_VERSION = APIVersion.JANUARY_2023.value

# -*- coding: utf-8 -*-
'''Модели для работы с выделенными серверами'''
import json
from typing import Any
from enum import Enum
from datetime import datetime
from ipaddress import IPv4Address, IPv6Address

from pydantic import Field

from ...time_utils import Period
from ...base import ResponseWithMeta, BaseResponse, BaseData


class ServerStatus(str, Enum):
    '''Статусы выделенных серверов.

    Attributes:
        INSTALLING (str): installing
        INSTALED (str): installed
        ON (str): on
        OFF (str): off
    '''
    INSTALLING = 'installing'
    INSTALED = 'installed'
    ON = 'on'
    OFF = 'off'


class DedicatedServer(BaseData):
    '''Выделенный сервер.

    Attributes:
        id (int): UID выделенного сервера.
        cpu_description (str): Описание CPU.
        hdd_description (str): Описание HDD.
        ram_description (str): Описание RAM.
        created_at (datetime): Дата создания.
        ip (IPv4Address | None): IP-адрес сетевого интерфейса IPv4.
        ipmi_ip (IPv4Address | None): IP-адрес сетевого интерфейса IPMI.
        ipmi_login (str | None): 'Логин для доступа к IPMI-консоли.
        ipmi_password (str | None): Пароль для доступа к IPMI-консоли.
        ipv6 (IPv6Address | None): IP-адрес сетевого интерфейса IPv6.
        mode_id (int | None): Внутренний дополнительный идентификатор сервера.
        name (str): Название выделенного сервера.
        comment (str): Комментарий.
        vnc_pass (str | None): Пароль для доступа к VNC-консоли.
        status (ServerStatus): Статус выделенного сервера.
        os_id (int | None): UID операционной системы.
        cp_id (int | None): UID панели управления.
        bandwidth_id (int | None): UID интернет-канала, установленного на выделенный сервер.
        network_drive_id (list[int] | None): UID сетевых дисков, подключенных к выделенному серверу.
        additional_ip_addr_id (list[int] | None): UID дополнительных IP-адресов, подключенных к выделенному серверу.
        plan_id (int | None): UID списка дополнительных услуг выделенного сервера.
        price (int): Цена выделенного сервера.
        location (str): Локация выделенного сервера.
        autoinstall_ready (int): Количество готовых к автоматической выдаче серверов. Если значение равно 0, сервер будет установлен через инженеров.
    '''
    id: int = Field(..., description='UID выделенного сервера.')
    cpu_description: str = Field(..., description='Описание CPU.')
    hdd_description: str = Field(..., description='Описание HDD.')
    ram_description: str = Field(..., description='Описание RAM.')
    created_at: datetime = Field(..., description='Дата создания.')
    ip: IPv4Address | None = Field(
        None, description='IP-адрес сетевого интерфейса IPv4.'
    )
    ipmi_ip: IPv4Address | None = Field(
        None, description='IP-адрес сетевого интерфейса IPMI.'
    )
    ipmi_login: str | None = Field(
        None, description='Логин для доступа к IPMI-консоли.'
    )
    ipmi_password: str | None = Field(
        None, description='Пароль для доступа к IPMI-консоли.'
    )
    ipv6: IPv6Address | None = Field(
        None, description='IP-адрес сетевого интерфейса IPv6.'
    )
    mode_id: int | None = Field(
        None, description='Внутренний дополнительный идентификатор сервера.'
    )
    name: str = Field(..., description='Название выделенного сервера.')
    comment: str = Field(..., description='Комментарий.')
    vnc_pass: str | None = Field(
        None, description='Пароль для доступа к VNC-консоли.'
    )
    status: ServerStatus = Field(...,
                                 description='Статус выделенного сервера.')
    os_id: int | None = Field(
        None, description='UID операционной системы.'
    )
    cp_id: int | None = Field(
        None, description='UID панели управления.'
    )
    bandwidth_id: int | None = Field(
        None, description='UID интернет-канала, установленного на выделенный сервер.'
    )
    network_drive_id: list[int] | None = Field(
        None, description='UID сетевых дисков, подключенных к выделенному серверу.'
    )
    additional_ip_addr_id: list[int] | None = Field(
        None, description='UID дополнительных IP-адресов, подключенных к выделенному серверу.'
    )
    plan_id: int | None = Field(
        None, description='UID списка дополнительных услуг выделенного сервера.'
    )
    price: int = Field(..., description='Цена выделенного сервера.')
    location: str = Field(..., description='Локация выделенного сервера.')
    autoinstall_ready: int = Field(
        ..., description=('Количество готовых к автоматической выдаче серверов. '
                          'Если значение равно 0, сервер будет установлен через инженеров.')
    )


class PaymentPeriods(Enum):
    '''Периоды оплаты.

    Attributes:
        P1M (Period): 1 месяц
        P3M (Period): 3 месяца
        P6M (Period): 6 месяцев
        P1Y (Period): 1 год
    '''
    P1M = Period('P1M')
    P3M = Period('P3M')
    P6M = Period('P6M')
    P1Y = Period('P1Y')


class PaymentPeriodsEncoder(json.JSONEncoder):
    '''PaymentPeriods encoder for JSON serialization.'''

    def default(self, obj: Any) -> Any:
        if isinstance(obj, PaymentPeriods):
            return str(obj.value)
        return json.JSONEncoder.default(self, obj)


class DedicatedServers(ResponseWithMeta):
    '''Ответ со списком выделенных серверов.

    Attributes:
        dedicated_servers (list[DedicatedServer]): Список выделенных серверов.
    '''
    dedicated_servers: list[DedicatedServer] = Field(
        ..., description='Список выделенных серверов.'
    )


class DedicatedServerResponse(BaseResponse):
    '''Ответ с выделенным сервером.

    Attributes:
        dedicated_server (DedicatedServer): Выделенный сервер.
    '''
    dedicated_server: DedicatedServer = Field(
        ..., description='Выделенный сервер.'
    )

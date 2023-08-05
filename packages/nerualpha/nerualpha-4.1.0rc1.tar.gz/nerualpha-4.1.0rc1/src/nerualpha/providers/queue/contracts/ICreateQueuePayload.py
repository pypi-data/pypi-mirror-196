from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from nerualpha.session.IWrappedCallback import IWrappedCallback
from nerualpha.providers.queue.contracts.ICreateQueueRate import ICreateQueueRate


#interface
class ICreateQueuePayload(ABC):
    name:str
    active:bool
    rate:ICreateQueueRate
    callback:IWrappedCallback

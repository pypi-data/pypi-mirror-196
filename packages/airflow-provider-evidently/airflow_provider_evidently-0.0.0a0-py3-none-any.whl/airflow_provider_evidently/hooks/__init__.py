import logging

from airflow.hooks.base import BaseHook

from airflow_provider_evidently.hooks import *
from airflow_provider_evidently.triggers import *



logger = logging.getLogger("airflow")




class EvidentlyHook(BaseHook):

    default_conn_name = "evidently_default"

    def __init__(self, **kwargs) -> None:

        super().__init__(**kwargs)

        # This is where you set all the attributes you need to for the operator to function
        raise NotImplementedError("You need to implement an __init__ method for this class")

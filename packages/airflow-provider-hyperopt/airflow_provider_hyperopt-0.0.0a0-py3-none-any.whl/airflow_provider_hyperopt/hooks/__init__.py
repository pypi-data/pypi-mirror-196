import logging

from airflow.hooks.base import BaseHook

from airflow_provider_hyperopt.hooks import *
from airflow_provider_hyperopt.triggers import *



logger = logging.getLogger("airflow")




class HyperoptHook(BaseHook):

    default_conn_name = "hyperopt_default"

    def __init__(self, **kwargs) -> None:

        super().__init__(**kwargs)

        # This is where you set all the attributes you need to for the operator to function
        raise NotImplementedError("You need to implement an __init__ method for this class")

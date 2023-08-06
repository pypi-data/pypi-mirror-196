import logging

from airflow.hooks.base import BaseHook

from airflow_provider_weights_and_biases.hooks import *
from airflow_provider_weights_and_biases.triggers import *



logger = logging.getLogger("airflow")




class WeightsAndBiasesHook(BaseHook):

    default_conn_name = "weights_and_biases_default"

    def __init__(self, **kwargs) -> None:

        super().__init__(**kwargs)

        # This is where you set all the attributes you need to for the operator to function
        raise NotImplementedError("You need to implement an __init__ method for this class")

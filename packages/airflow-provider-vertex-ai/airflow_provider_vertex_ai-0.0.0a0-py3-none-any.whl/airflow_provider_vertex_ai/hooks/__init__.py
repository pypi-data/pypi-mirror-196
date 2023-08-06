import logging

from airflow.hooks.base import BaseHook

from airflow_provider_vertex_ai.hooks import *
from airflow_provider_vertex_ai.triggers import *



logger = logging.getLogger("airflow")




class VertexAiHook(BaseHook):

    default_conn_name = "vertex_ai_default"

    def __init__(self, **kwargs) -> None:

        super().__init__(**kwargs)

        # This is where you set all the attributes you need to for the operator to function
        raise NotImplementedError("You need to implement an __init__ method for this class")

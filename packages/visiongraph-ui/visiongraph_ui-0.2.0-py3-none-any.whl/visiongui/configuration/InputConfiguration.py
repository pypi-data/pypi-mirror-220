from pathlib import Path
from typing import Dict, Any

from duit.annotation.AnnotationList import AnnotationList
from duit.arguments.Argument import Argument
from duit.model.DataField import DataField
import visiongraph as vg
import duit.ui as dui


class InputConfiguration:
    def __init__(self):
        self.input = DataField(self._first_entry(vg.input.InputProviders)) | AnnotationList(
            dui.Options("Input Device", list(vg.input.InputProviders.keys())),
            Argument()
        )

        self.source = DataField("0") | AnnotationList(
            dui.Text("Input Source"),
            Argument()
        )

    @staticmethod
    def _first_entry(data: Dict[str, Any]) -> str:
        return list(data.items())[0][0]

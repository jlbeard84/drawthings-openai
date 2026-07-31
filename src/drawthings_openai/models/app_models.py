from typing import Any


class ModelCatalog:
    models: list[dict[str, Any]]
    loras: list[dict[str, Any]]
    control_nets: list[dict[str, Any]]
    textual_inversions: list[dict[str, Any]]
    upscalers: list[dict[str, Any]]

    def __init__(self) -> None:
        self.models = []
        self.loras = []
        self.control_nets = []
        self.textual_inversions = []
        self.upscalers = []

"""
Trajectopy - Trajectory Evaluation in Python

Gereon Tombrink, 2023
mail@gtombrink.de
"""
import logging
from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot
from trajectopy.gui.requests.request import Request
from trajectopy.gui.requests.ui_request import UIRequest, UIRequestType


logger = logging.getLogger("root")


class Manager(QObject):
    operation_started = pyqtSignal()
    operation_finished = pyqtSignal()
    ui_request = pyqtSignal(UIRequest)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._request: Request | None = None
        self.REQUEST_MAPPING = {}
        self.DEFAULT_HANDLER = None

    def get_request(self) -> Request | None:
        return self._request

    def set_request(self, request: Request) -> None:
        self._request = request

    @pyqtSlot(Request)
    def handle_request(self, request: Request) -> None:
        self.set_request(request)

        func = self.REQUEST_MAPPING.get(request.type, self.DEFAULT_HANDLER)
        if func is None:
            logger.error(f"{self.__class__.__name__}: Unable to handle request of type {request.type}")
            return
        try:
            func()
        except Exception as e:
            self.ui_request.emit(
                UIRequest(
                    type=UIRequestType.MESSAGE,
                    payload=f"{self.__class__.__name__}: Error processing request: {self.get_request().type.name} ({e})",
                )
            )
        finally:
            self.operation_finished.emit()
            logger.debug(f"{self.__class__.__name__}: Handled request of type {request.type}")

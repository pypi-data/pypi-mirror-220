import json
import logging
import os
from contextvars import ContextVar
from typing import Any, Dict, Optional
from uuid import uuid4

import google.cloud.logging
from google.cloud.logging.handlers import CloudLoggingHandler

# Keeps track of logger id in the Thread/Task, across different modules.
_current_logger_id: ContextVar = ContextVar("Current logger id")


class LoggingManager:
    def __init__(
        self,
        name: str = __name__,
        logger_id: Optional[str] = None,
        gcp_env_variable: str = "GCP_SERVICE_KEY",
    ):
        """
        Args:
            name (str): Name of the logger. Defaults to __name__.
            logger_id (str, optional): id of the logger.
            gcp_env_variable (str): Name of the Google Service Key environment
                variable. The envionrment variable can hold a file path
                or a json.
        """
        if logger_id:
            self._set_logger_id(logger_id)

        self._gcp_client = None
        try:
            if gcp_env_variable in os.environ:
                # Local testing
                self._gcp_client = (
                    google.cloud.logging.Client.from_service_account_json(
                        os.environ[gcp_env_variable]
                    )
                )
            else:
                self._gcp_client = google.cloud.logging.Client()
        except Exception:
            # What this means is that  there is no GCP logging.
            # The most likely reason for this is local development
            # where there is not a Google Service Key.
            pass

        self._logger = logging.getLogger(name)
        self._logger.handlers.clear()
        self._logger.setLevel(logging.INFO)

        if self._gcp_client:
            cloudlogging_formatter = logging.Formatter("%(name)s: %(message)s")
            cloud_handler = CloudLoggingHandler(self._gcp_client)
            cloud_handler.setFormatter(cloudlogging_formatter)
            self._logger.addHandler(cloud_handler)

        stream_handler = logging.StreamHandler()
        streamlog_format = "%(asctime)s [%(levelname)s] - %(name)s: %(message)s - JSON Payload: %(json_fields)s"  # noqa
        streamlog_formatter = logging.Formatter(fmt=streamlog_format)
        stream_handler.setFormatter(streamlog_formatter)
        self._logger.addHandler(stream_handler)

    @property
    def logger_id(self) -> str:
        """Get logger from Thread ContextVar if one exists or set it."""
        try:
            return _current_logger_id.get()
        except LookupError:
            self._set_logger_id(uuid4().hex)
            return _current_logger_id.get()

    def _set_logger_id(self, logger_id: str) -> None:
        _current_logger_id.set(logger_id)

    def _preprocess_json_payload(
        self,
        msg: str,
        payload: Optional[Dict[str, Any]],
        kwargs: Optional[Dict[str, Any]],
    ) -> Optional[dict]:
        if not payload:
            payload = {}
        if kwargs:
            payload = payload | kwargs

        payload["_message"] = msg
        payload["request_id"] = self.logger_id
        return payload

    def log(
        self,
        msg: str,
        level: int,
        json_params: Optional[Dict[str, Any]],
        skip_if_local: bool,
        **kwargs,
    ) -> None:
        if skip_if_local and not self._gcp_client:
            return

        json_params = self._preprocess_json_payload(msg, json_params, kwargs)
        if self._gcp_client:
            self._logger.log(level, msg, extra={"json_fields": json_params})
        else:
            try:
                self._logger.log(
                    level,
                    msg,
                    extra={"json_fields": json.dumps(json_params, indent=2)},
                )
            except TypeError as e:
                self._logger.warning(f"Error serializing JSON log: {e}")
                self._logger.log(
                    level,
                    msg,
                    extra={"json_fields": json_params},
                )

    def debug(
        self,
        msg: str,
        json_params: Optional[Dict[str, Any]] = None,
        skip_if_local: bool = False,
        **kwargs,
    ) -> None:
        self.log(
            msg,
            level=logging.DEBUG,
            json_params=json_params,
            skip_if_local=skip_if_local,
            **kwargs,
        )

    def info(
        self,
        msg: str,
        json_params: Optional[Dict[str, Any]] = None,
        skip_if_local: bool = False,
        **kwargs,
    ) -> None:
        self.log(
            msg,
            level=logging.INFO,
            json_params=json_params,
            skip_if_local=skip_if_local,
            **kwargs,
        )

    def warning(
        self,
        msg: str,
        json_params: Optional[Dict[str, Any]] = None,
        skip_if_local: bool = False,
        **kwargs,
    ) -> None:
        self.log(
            msg,
            level=logging.WARNING,
            json_params=json_params,
            skip_if_local=skip_if_local,
            **kwargs,
        )

    def error(
        self,
        msg: str,
        json_params: Optional[Dict[str, Any]] = None,
        skip_if_local: bool = False,
        **kwargs,
    ) -> None:
        self.log(
            msg,
            level=logging.ERROR,
            json_params=json_params,
            skip_if_local=skip_if_local,
            **kwargs,
        )

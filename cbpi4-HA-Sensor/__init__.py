import logging
import asyncio
from cbpi.api import *
import requests

logger = logging.getLogger(__name__)

@parameters([
    Property.Select(label="Check Certificate", options=['YES','NO'], description="Enable or disable TLS certificate checking. This setting has no impact for unencrypted connections"),
    Property.Number(label="Request Timeout", configurable=True, description="HTTP request timeout in seconds (default 5)", default_value=5),
    Property.Text(label="Base API entry point", configurable=True, description="REST Api entry point. Must include a uri scheme (http://yourhome:8123/api/...)"),
    Property.Text(label="Entity id", configurable=True, description="Entity id of the temperature sensor in HA (e.g. sensor.kettle_temperature)"),
    Property.Text(label="Authorization Token", configurable=True, description="Authorization token for HA API."),
])

class HATemperatureSensor(CBPiSensor):

    async def on_start(self):
        self.request_session = requests.Session()

        if self.props.get("Check Certificate", "YES") == "YES":
            self.request_session.verify = True
        else:
            self.request_session.verify = False

        self.base_url = self.props.get("Base API entry point")
        self.entity = self.props.get("Entity id")

        self.html_headers = {}
        if self.props.get("Authorization Token") != "":
            self.html_headers["Authorization"] = "Bearer {}".format(self.props.get("Authorization Token"))
        self.html_headers["Content-Type"] = "application/json"

        self.request_session.timeout = float(self.props.get("Request Timeout", 5))

        self.value = None

    async def run(self):
        while self.running:
            try:
                endpoint = self.base_url.strip('/') + '/states/' + self.entity
                response = self.request_session.get(endpoint, headers=self.html_headers)
                if response.status_code == 200:
                    data = response.json()
                    self.value = float(data.get("state", 0))
                    self.data_received(self.value)
                    logger.info(f"Temperature updated: {self.value}")
                else:
                    logger.error(f"Failed to read temperature: HTTP {response.status_code}")
            except Exception as e:
                logger.error(f"Error reading temperature: {e}")

            await asyncio.sleep(5)

def setup(cbpi):
    cbpi.plugin.register("HomeAssistant Temperature Sensor", HATemperatureSensor)

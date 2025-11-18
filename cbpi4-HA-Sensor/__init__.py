from cbpi.api import CBPiSensor, Property, parameters
import asyncio, requests, logging

logger = logging.getLogger(__name__)

@parameters([
    Property.Select(label="Check Certificate", options=['YES','NO'],
                    description="Enable or disable TLS certificate checking. This setting has no impact for unencrypted connections"),
    Property.Number(label="Request Timeout", configurable=True, description="HTTP request timeout in seconds (default 5)", default_value=5),
    Property.Text(label="Base API entry point", configurable=True, description="REST Api entry point. Must include a uri scheme (http://yourhome:8123/api/...)"),
    Property.Text(label="Entity id", configurable=True, description="Entity id of the sensor in HA (e.g. sensor.kettle_temperature)"),
    Property.Text(label="Authorization Token", configurable=True, description="Authorization token for HA API."),
])


class HATemperatureSensor(CBPiSensor):

    async def on_start(self):
        self.value = 0.0  # initial value visible to CBPi4 UI
        self.session = requests.Session()
        self.session.verify = self.props.get("Check Certificate", "YES") == "YES"
        self.session.headers = {
            "Authorization": f"Bearer {self.props.get('Authorization Token')}" if self.props.get('Authorization Token') else "",
            "Content-Type": "application/json"
        }
        self.base_url = self.props.get("Base API entry point")
        self.entity = self.props.get("Entity id")
        self.timeout = float(self.props.get("Request Timeout", 5))

    async def run(self):
        while self.running:
            try:
                r = self.session.get(f"{self.base_url.strip('/')}/states/{self.entity}", timeout=self.timeout)
                if r.status_code == 200:
                    data = r.json()
                    new_value = float(data.get("state", 0))
                    self.value = new_value
                    self.push_update(self.value)  # push update to CBPi4 UI
                    logger.info(f"Temperature updated: {self.value}")
                else:
                    logger.error(f"HTTP error: {r.status_code}")
            except Exception as e:
                logger.error(f"Error reading temperature: {e}")
            await asyncio.sleep(5)

def setup(cbpi):
    cbpi.plugin.register("HomeAssistant Temperature Sensor", HATemperatureSensor)

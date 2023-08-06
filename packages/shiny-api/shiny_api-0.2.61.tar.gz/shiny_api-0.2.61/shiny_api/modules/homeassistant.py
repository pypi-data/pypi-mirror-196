"""Home Assistant module for Shiny API."""
import inspect
import os
from homeassistant_api import Client
import shiny_api.modules.load_config as config

print(f"Importing {os.path.basename(__file__)}...")


class HomeAssistant:
    """Base Class for HomeAsssitant module"""

    default_api_url = "http://ha.store1.logi.wiki/api"

    def __init__(self, api_url: str = default_api_url):
        """Get Home Assistant client"""
        self.client = Client(
            api_url,
            config.HOMEASSISTANT_API_KEY,
        )

    @classmethod
    def get_functions(cls):
        """Return functions"""
        methods = [method for method, _ in inspect.getmembers(cls, predicate=inspect.isfunction) if not method.startswith("__")]
        return methods


class Vacuum(HomeAssistant):
    """Class for Roomba vacuum cleaner"""

    def __init__(self, entity_id: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.domain = "vacuum"
        self.entity_id = f"{self.domain}.{entity_id}"

    def start(self):
        """Start vacuum cleaner"""
        self.client.get_domain(self.domain).start(entity_id=self.entity_id)

    def stop(self):
        """Return vacuum cleaner to base"""
        print(f"{self.entity_id}|{self.domain}")
        self.client.get_domain(self.domain).stop(entity_id=self.entity_id)

    def go_home(self):
        """Return vacuum cleaner to base"""
        self.client.get_domain(self.domain).return_to_base(entity_id=self.entity_id)


class Alarm(HomeAssistant):
    """Class for Alarm panel"""

    def __init__(self, entity_id: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.domain = "alarm_control_panel"
        self.entity_id = f"{self.domain}.{entity_id}"

    def arm(self):
        """Arm alarm panel"""
        self.client.get_domain(self.domain).alarm_arm_away(entity_id=self.entity_id)

    def disarm(self):
        """Arm alarm panel"""
        self.client.get_domain(self.domain).alarm_disarm(entity_id=self.entity_id)


if __name__ == "__main__":
    alarm = Alarm("system")
    alarm.disarm()

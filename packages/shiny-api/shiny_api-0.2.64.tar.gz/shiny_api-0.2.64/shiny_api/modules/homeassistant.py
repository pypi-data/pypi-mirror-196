"""Home Assistant module for Shiny API."""
import inspect
import os
from homeassistant_api import Client
import shiny_api.modules.load_config as config

print(f"Importing {os.path.basename(__file__)}...")


class HomeAssistant:
    """Base Class for HomeAsssitant module"""

    def __init__(self, location: str = "store1"):
        """Get Home Assistant client"""
        self.client = Client(
            config.HOMEASSISTANT_API[location]["url"],
            config.HOMEASSISTANT_API[location]["key"],
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


class Lock(HomeAssistant):
    """Class for Locks"""

    def __init__(self, entity_id: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.domain = "lock"
        self.entity_id = f"{self.domain}.{entity_id}"

    def lock(self):
        """Lock door"""
        self.client.get_domain(self.domain).lock(entity_id=self.entity_id)

    def unlock(self):
        """Unlock door"""
        self.client.get_domain(self.domain).unlock(entity_id=self.entity_id)


if __name__ == "__main__":
    car = Lock(entity_id="taylor_swiftly_doors", location="home")
    car.lock()

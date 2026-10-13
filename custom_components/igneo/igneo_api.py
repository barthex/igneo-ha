"""igneo.pl API Client for Estyma Igneo Slim controller."""

import requests
import json
import time
from pathlib import Path
from typing import Dict, Optional, Any
from dataclasses import dataclass
from enum import Enum

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    HAS_SELENIUM = True
except ImportError:
    HAS_SELENIUM = False


class BurnerStatus(Enum):
    """Status palnika (burner status)."""
    PAUSE = "pauza"
    IGNITION = "rozpalanie"
    HEATING = "grzanie"
    CLEANING = "czyszczenie"
    STOPPED = "zatrzymany"


@dataclass
class BoilerData:
    """Data from boiler."""
    pump_status: int
    fuel_counter: float
    boiler_temp: float
    boiler_temp_calculated: float
    room_temp: float
    cwu_temp: float
    cwu_temp_target: float
    burner_status: str
    oxygen_level: float
    device_type: str
    co_circuits: int
    cwu_circuits: int
    raw: Dict[str, Any]


class IgleoClient:
    """Client for igneo.pl API with cookie caching."""

    BASE_URL = "https://igneo.pl"

    def __init__(self, username: str, password: str, device_id: str, cache_dir: Optional[str] = None):
        self.username = username
        self.password = password
        self.device_id = device_id
        self.session = requests.Session()
        self._authenticated = False

        # Setup cookie cache
        if cache_dir:
            self.cache_dir = Path(cache_dir)
        else:
            self.cache_dir = Path.home() / ".igneo"
        self.cache_dir.mkdir(exist_ok=True)
        self.cookies_file = self.cache_dir / f"cookies_{username}_{device_id}.json"

        self._load_cached_cookies()

    def _load_cached_cookies(self) -> bool:
        """Load cookies from JSON cache."""
        try:
            if self.cookies_file.exists():
                with open(self.cookies_file, 'r') as f:
                    cookies = json.load(f)
                    for name, value in cookies.items():
                        self.session.cookies.set(name, value)
                    return True
        except Exception as e:
            print(f"⚠️  Cookie load error: {e}")
        return False

    def _save_cached_cookies(self) -> None:
        """Save cookies to JSON cache."""
        try:
            cookies_dict = {name: value for name, value in self.session.cookies.items()}
            with open(self.cookies_file, 'w') as f:
                json.dump(cookies_dict, f)
        except Exception as e:
            print(f"⚠️  Cookie save error: {e}")

    def login(self) -> bool:
        """Login with cached cookies or Selenium."""
        # Try cached cookies first
        if self.cookies_file.exists():
            try:
                response = self.session.post(
                    f"{self.BASE_URL}/info_panel_update",
                    data={"id_urzadzenia": self.device_id},
                    timeout=5
                )
                if response.status_code == 200 and response.text.startswith('{'):
                    self._authenticated = True
                    return True
            except:
                pass

        # Need full login
        if not HAS_SELENIUM:
            raise RuntimeError("Selenium required: pip install selenium webdriver-manager")

        try:
            print("🔐 Logging in (headless Chrome)...")
            options = Options()
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--headless")

            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)

            driver.get(self.BASE_URL)
            time.sleep(2)

            inputs = driver.find_elements(By.TAG_NAME, "input")
            inputs[0].send_keys(self.username)
            inputs[1].send_keys(self.password)
            inputs[2].click()
            time.sleep(6)

            # Extract cookies
            for cookie in driver.get_cookies():
                self.session.cookies.set(cookie['name'], cookie['value'])

            driver.quit()

            # Save to cache
            self._save_cached_cookies()
            self._authenticated = True
            return True
        except Exception as e:
            print(f"❌ Login error: {e}")
            return False

    def get_device_data(self) -> Optional[BoilerData]:
        """Get device data."""
        if not self._authenticated:
            if not self.login():
                raise RuntimeError("Not authenticated")

        try:
            response = self.session.post(
                f"{self.BASE_URL}/info_panel_update",
                data={"id_urzadzenia": self.device_id},
                timeout=10
            )

            if response.status_code != 200:
                raise RuntimeError(f"API error: {response.status_code}")

            data = response.json()
            return self._parse_boiler_data(data)
        except Exception as e:
            print(f"❌ Get device data error: {e}")
            return None

    def set_parameter(self, param_name: str, value: Any) -> Optional[int]:
        """Set boiler parameter."""
        if not self._authenticated:
            if not self.login():
                raise RuntimeError("Not authenticated")

        try:
            response = self.session.post(
                f"{self.BASE_URL}/info_set_order",
                data={
                    "id_urzadzenia": self.device_id,
                    "name": param_name,
                    "value": str(value)
                },
                timeout=10
            )

            if response.status_code != 200:
                raise RuntimeError(f"API error: {response.status_code}")

            return int(response.text)
        except Exception as e:
            print(f"❌ Set parameter error: {e}")
            return None

    def check_order_status(self, order_number: int) -> Optional[str]:
        """Check order status."""
        if not self._authenticated:
            if not self.login():
                raise RuntimeError("Not authenticated")

        try:
            response = self.session.post(
                f"{self.BASE_URL}/info_check_order",
                data={
                    "id_urzadzenia": self.device_id,
                    "order_number": str(order_number)
                },
                timeout=10
            )

            if response.status_code != 200:
                raise RuntimeError(f"API error: {response.status_code}")

            return response.text.strip()
        except Exception as e:
            print(f"❌ Check order status error: {e}")
            return None

    def set_cwu_comfort_temp(self, temp: float) -> Optional[int]:
        """Set CWU comfort temperature."""
        return self.set_parameter("cwu_zad_komf_obw1_sub1", int(temp))

    def set_room_comfort_temp(self, temp: float) -> Optional[int]:
        """Set room comfort temperature."""
        return self.set_parameter("tpok_komf_obw1_sub1", int(temp * 10))

    @staticmethod
    def _parse_boiler_data(data: Dict) -> BoilerData:
        """Parse API response."""
        return BoilerData(
            pump_status=data.get("stan_pomp_sub1", 0),
            fuel_counter=data.get("licznik_paliwa_sub1", 0),
            boiler_temp=data.get("kociol_temp_sub1", 0.0),
            boiler_temp_calculated=data.get("kociol_temp_obli_sub1", 0.0),
            room_temp=data.get("tpok_obw1_sub1", 0.0),
            cwu_temp=data.get("cwu_temp_obw1_sub1", 0.0),
            cwu_temp_target=data.get("cwu_temp_obw1_dok_sub1", 0.0),
            burner_status=data.get("palnik_status_sub1", "unknown"),
            oxygen_level=data.get("spaliny_tlen_sub1", 0.0),
            device_type=data.get("typ_urzadzenia_sub1", "unknown"),
            co_circuits=data.get("liczba_obw_co_sub1", 0),
            cwu_circuits=data.get("liczba_obw_cwu_sub1", 0),
            raw=data
        )

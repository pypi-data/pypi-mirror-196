# Proxyrack API

UNOFFICIAL Python bindings for Proxyrack Dashboard API

## Installation

```BASH
pip install pyProxyrack
```

## Usage

---

### Login with API Key:

```PYTHON
from pyProxyrack import Proxyrack

# Your Proxyrack login email and password
API_KEY = "" # Generate an API key from your dashboard and store it here

# Initialise the Proxyrack object
user = Proxyrack()

# Optionally, when instantiating you can pass in the following attributes to the Proxyrack class:
```

| Attribute      | Description        | Default Value                   |
|----------------|--------------------|---------------------------------|
| API_BASE_URL | The API BASE URL | https://peer.proxyrack.com                            |
| API_PREFIX | The API PREFIX | /api                            |
| API_VERSION | The API VERSION | ""                            |

```PYTHON
# Call the complete_login_flow method to login and set the JWT in self.jwt
user.set_api_key(API_KEY)
```

---

### Add proxies for future requests:

```PYTHON
from pyProxyrack import Proxyrack

# With authentication & protocol
user.set_proxy("ip:port:username:password", "socks5")

# Without authentication & protocol
user.set_proxy("ip:port", "socks5")

# Alternative way
user.set_socks5_proxy("ip:port")
user.set_socks5_proxy("ip:port:username:password")
user.set_https_proxy("ip:port")
user.set_https_proxy("ip:port:username:password")
```

## Functions

---

1. Get device bandwidth

    ```PYTHON
    # Get device bandwidth used from date_start to date_end.
    user.get_device_bandwidth_usage(device_id: str, date_start: str, date_end: str)
    ```

    `device_id` is required (if not passed, it'll combine the usage for all the devices and return the same) and `date_start` and `date_end` are optional and need the format `Y-m-d` (Eg: 2023-04-25)

    Do note you need to use `date_start` and `date_end` together even if you just want to use one.
---

2. Remove a proxy

    ```PYTHON
    # Removes a proxy for future requests.
    user.remove_proxy()
    ```
---

3. Add/link a device

    ```PYTHON
    # Add/link a device to your account
    user.add_device(device_id: str, device_name: str)
    ```

    Both are required fields.
---

4. Delete/unlink a device

    ```PYTHON
    # Delete/unlink a device from your account
    user.delete_device(device_id: str)
    ```
---

5. Is Logged In

    ```PYTHON
    # Check if you're logged in
    user.is_logged_in()
    ```
---

6. Logout

    ```PYTHON
    # Logged out
    user.logout()
    ```
---

7. Get payout balance

    ```PYTHON
    # Get available payout balance
    user.get_balance()
    ```
---

## Exceptions

- The following exceptions are defined.
    Exception | Reason
    --- | ---
    `NotLoggedInError` | Raised when you try to access protected routes (bandwidth usage, add devices, delete devices, etc).
---

## Liked my work?

---

Consider donating:

- BTC: bc1qh04l5tx7gd96wnyyqhr68uptdmqmwwwkcg3hj0

- LTC: Lg5mMHUCrsSkaRYrfqaum4hodBAt9BSi91


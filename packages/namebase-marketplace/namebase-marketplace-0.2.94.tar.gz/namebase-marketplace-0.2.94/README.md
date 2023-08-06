Namebase Marketplace Api for Python
==

<p>
<a href="https://namebase-marketplace.readthedocs.io/en/latest/">
<img src="https://readthedocs.org/projects/namebase-exchange-python/badge/?version=latest" alt="Open Issues"/>
</a>
<a href="/issues">
<img src="https://img.shields.io/github/issues/pretended/namebase-marketplace" alt="Open Issues"/>
</a>
<a href="https://pypi.org/project/namebase-marketplace/">
<img src="https://img.shields.io/pypi/v/namebase-marketplace.svg" alt="PyPI"/>
</a>
<a href="/LICENCE">
<img src="https://img.shields.io/github/license/pretended/namebase-marketplace" alt="MIT Licence"/>
</a>
<img src="https://static.pepy.tech/badge/namebase-marketplace/week"/>

  
Python 3.6+ client for interacting with Namebase Marketplace API.

## Usage
Instantiating the Marketplace object can be done either by using email and password or None.
Only post requests can be made authenticated.

Websocket API is not provided.
## Installation

### Requirements

- Python 3.6 or greater

### Install

> pip install namebase-marketplace
  
  
### Upgrade
  
> pip install --upgrade namebase-marketplace

### Usage

##### Core REST API for Namebase MARKETPLACE
```python
from namebase_marketplace.marketplace import *
marketplace = Marketplace(email="YOUR EMAIL", pwd="YOUR PASSWORD")
marketplace.get_user_info()
marketplace.open_bid(domain='domain', bid_amount=0.4, blind_amount=100)
```

##### EXAMPLE WITHOUT AUTHENTICATION:
```python
from namebase_marketplace.marketplace import *
marketplace = Marketplace()
marketplace.get_marketplace_domains(offset=100) # Get 101-200 latest marketplace domains with default options
```

On some endpoints you can pass options, please refer them to the following documentation: https://github.com/namebasehq/api-documentation/blob/master/marketplace-api.md

### Github OAuth bypass and 2FA Auth Bypass
  
#### Recent upgrades
New auth method has been added, now you can auth yourself by using the namebase_cookie in case you cant (or dont want to) login via email-password.
  
This is the cookie Namebase uses to auth you within the app. You can find this cookie when reloading any page and going to Network on Inspection Mode. Head to a request and find this cookie under "Cookies" tab on any explorer along with other kind of cookies. Cookie name is called "namebase-main".
  
###### Example
```python
from namebase_marketplace.marketplace import *
marketplace = Marketplace(namebase_cookie="<My_namebase_cookie>")
marketplace.get_user_info()
marketplace.open_bid(domain='domain', bid_amount=0.4, blind_amount=100)
```
  

## Donations

I have made this library open-sourced and free to use. However, if you consider this library has helped you, or you just want to sponsor me, donations are welcomed to one of my HANDSHAKE addresses. 

> hs1qynh72cuj7lawdcmvjtls4kk0p4auzmj5qq6v3r

# Facebook Business SDK - Campaign Connect Fork

This is Campaign Connect's customized fork of the [Facebook Business SDK for Python](https://github.com/facebook/facebook-python-business-sdk) with added proxy support for Choreograph infrastructure.

## Features at a Glance

✅ **Proxy routing** - Route all Facebook API calls through Choreograph proxy
✅ **Custom headers** - Add x-apikey, X-CC-Account-Id, and custom headers
✅ **Apigee error handling** - Properly detect and parse Apigee errors
✅ **100% compatible** - Drop-in replacement for official SDK
✅ **Fully tested** - 41 unit tests including proxy-specific features
✅ **Easy install** - Public repo, no tokens needed

## Why This Fork?

The official Facebook SDK doesn't support:
- Custom base URLs (for proxy/gateway routing)
- Custom headers (x-apikey, account identifiers)
- Apigee error handling

This fork adds these features while maintaining full compatibility with the original SDK.

## Added Features

### 1. Base Path Injection
Route all API calls through your proxy instead of directly to Facebook.

**Option A: Environment Variable (Recommended)**

Set `FACEBOOK_GRAPH_BASE_URL` in your environment - no code changes needed:

```bash
export FACEBOOK_GRAPH_BASE_URL=https://api.choreograph.com/choreograph/connect/proxy/v1/meta
```

Then initialize normally:
```python
FacebookAdsApi.init()  # Automatically uses FACEBOOK_GRAPH_BASE_URL
```

**Option B: Direct Argument**

Pass `base_path` directly (overrides environment variable):

```python
FacebookAdsApi.init(
    base_path='https://api.choreograph.com/choreograph/connect/proxy/v1/meta'
)
```

**Priority:** `base_path` argument > `FACEBOOK_GRAPH_BASE_URL` env var > default (`https://graph.facebook.com`)

### 2. Custom Headers
Add custom headers to all requests (API keys, auth tokens, etc.).

```python
FacebookAdsApi.init(
    custom_headers={
        'x-apikey': 'your-api-key',
        'X-Custom-Header': 'value',
    }
)
```

### 3. X-CC-Account-Id Header
Automatically adds account ID header (with `act_` prefix stripped).

```python
FacebookAdsApi.init(account_id_header='act_123456789')
# Header sent: X-CC-Account-Id: 123456789

account.get_campaigns()  # Automatically extracts from 'act_123456789'
```

### 4. Apigee Error Handling
Properly detects and parses Apigee error responses.

```python
from facebook_business.exceptions import FacebookRequestError

try:
    response = api.call('GET', ('act_123', 'campaigns'))
except FacebookRequestError as e:
    print(e.api_error_type())     # 'ApigeeError'
    print(e.api_error_code())     # 'oauth.v2.InvalidApiKey'
    print(e.api_error_message())  # 'Invalid ApiKey'
```

### Quick Install

```bash
pip install git+https://gitlab.com/2sixty/activation/radium/facebook-python-business-sdk-cc-fork.git@v24.0.0+cc.1
```

### Adding to Your Project

**pyproject.toml (Poetry, setuptools):**
```toml
[tool.poetry.dependencies]
facebook-business-sdk-radium = {git = "https://gitlab.com/2sixty/activation/radium/facebook-python-business-sdk-cc-fork.git", tag = "v24.0.0+cc.1"}

# Or using PEP 508 format:
[project]
dependencies = [
    "facebook-business-sdk-radium @ git+https://gitlab.com/2sixty/activation/radium/facebook-python-business-sdk-cc-fork.git@v24.0.0+cc.1",
]

# Or with SSH:
dependencies = [
    "facebook-business-sdk-radium @ git+ssh://git@gitlab.com/2sixty/activation/radium/facebook-python-business-sdk-cc-fork.git@v24.0.0+cc.1",
]
```

**requirements.txt:**
```txt
# Specific version (recommended for production)
git+https://gitlab.com/2sixty/activation/radium/facebook-python-business-sdk-cc-fork.git@v24.0.0+cc.1

# Or using SSH
git+ssh://git@gitlab.com/2sixty/activation/radium/facebook-python-business-sdk-cc-fork.git@v24.0.0+cc.1

# Or latest from main branch
git+https://gitlab.com/2sixty/activation/radium/facebook-python-business-sdk-cc-fork.git@main
```

**Note:** Package name is `facebook-business-sdk-radium`, but you still import as `facebook_business`:
```python
from facebook_business.api import FacebookAdsApi  # ← Same import as official SDK
```

## Usage

Same as the original SDK, with optional proxy parameters. Both high-level and low-level API approaches work:

### Initialization

```python
from facebook_business.api import FacebookAdsApi

# Initialize with Choreograph proxy
api = FacebookAdsApi.init(
    base_path='https://api.choreograph.com/choreograph/connect/proxy/v1/meta',
    custom_headers={'x-apikey': 'your-api-key'},
)
```

### Approach 1: High-Level API (Recommended)

Use SDK objects for cleaner, more Pythonic code:

```python
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign

# Get account and campaigns
account = AdAccount('act_123456789')
campaigns = account.get_campaigns(
    fields=[Campaign.Field.name, Campaign.Field.status]
)

for campaign in campaigns:
    print(f"{campaign[Campaign.Field.name]}: {campaign[Campaign.Field.status]}")
```

### Approach 2: Low-Level API

For more control or custom endpoints:

```python
# Direct API call
response = api.call(
    'GET',
    ('act_123456789', 'campaigns'),  # Path: v24.0/act_123456789/campaigns
    params={'fields': 'id,name,status'},
)

data = response.json()
for campaign in data.get('data', []):
    print(f"{campaign['name']}: {campaign['status']}")
```

Both approaches work through the Choreograph proxy with all custom headers automatically included.

## Version

- **Base:** Facebook Business SDK v24.0.0
- **Fork:** v24.0.0+cc.1
- **Package name:** `facebook-business-sdk-radium`
- **Import name:** `facebook_business` (unchanged from official SDK)
- **Python:** 3.7+

## Maintenance

When updating from upstream:

```bash
# Add upstream remote
git remote add upstream https://github.com/facebook/facebook-python-business-sdk.git

# Fetch and merge
git fetch upstream
git merge upstream/main

# Resolve conflicts (if any) in our custom files
# Test and push
```

## Testing

```bash
# Run all tests (41 tests total)
python -m unittest facebook_business.test.unit

# Run proxy-specific tests
python -m unittest facebook_business.test.unit.ProxyFeaturesTestCase
python -m unittest facebook_business.test.unit.ApigeeErrorHandlingTestCase
```

## Original SDK Documentation

For general Facebook SDK documentation:
- [GitHub](https://github.com/facebook/facebook-python-business-sdk)
- [Official Docs](https://developers.facebook.com/docs/business-sdk)

## License

Same as original: [LICENSE.txt](LICENSE.txt)

## Support

- **Proxy features:** Contact Campaign Connect team
- **General SDK issues:** Refer to [upstream repo](https://github.com/facebook/facebook-python-business-sdk/issues)
- **Repository:** https://gitlab.com/2sixty/activation/radium/facebook-python-business-sdk-cc-fork

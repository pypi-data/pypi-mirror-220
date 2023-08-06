# bb-connector

## About this Project

This Project represents a flask service, which connects to bloomberg to get data from the API.

The service has the following REST-endpoints:

### /primary_exchange_securities:
- this endpoint is used if you want to get all securities on the primary exchange


### /fundamental_tickers:
- this endpoint is used if you want to get all securities for a primary exchange on the remote market

### /members:
- this endpoint is used if you want ETF/Index constituents

### /field:
- this endpoint is used if you want a BDP request for a special security

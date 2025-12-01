# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.

# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.

"""
The purpose of the session module is to encapsulate authentication classes and
utilities.
"""
import hashlib
import hmac
import requests
import os


class FacebookSession(object):
    """
    FacebookSession manages the the Graph API authentication and https
    connection.

    Attributes:
        GRAPH (class): The graph url without an ending forward-slash.
        app_id: The application id.
        app_secret: The application secret.
        access_token: The access token.
        appsecret_proof: The application secret proof.
        proxies: Object containing proxies for 'http' and 'https'
        requests: The python requests object through which calls to the api can
            be made.

    Environment Variables:
        FACEBOOK_GRAPH_BASE_URL: Base URL for the Graph API (recommended way to
            configure custom endpoints like Apigee proxy). Takes precedence over
            the default but can be overridden by the base_path argument.
    """
    GRAPH = 'https://graph.facebook.com'

    def __init__(self, app_id=None, app_secret=None, access_token=None,
             proxies=None, timeout=None, debug=False, base_path=None):
        """
        Initializes and populates the instance attributes with app_id,
        app_secret, access_token, appsecret_proof, proxies, timeout and requests
        given arguments app_id, app_secret, access_token, proxies and timeout.

        Args:
            base_path: Optional. Custom base URL for the Graph API. If not provided,
                falls back to FACEBOOK_GRAPH_BASE_URL environment variable (recommended),
                then to the default 'https://graph.facebook.com'.
        """
        self.app_id = app_id
        self.app_secret = app_secret
        self.access_token = access_token
        self.proxies = proxies
        self.timeout = timeout
        self.debug = debug
        # Allow overriding the base path for Apigee proxy support
        # Priority: base_path argument > FACEBOOK_GRAPH_BASE_URL env var > default
        effective_base_path = base_path or os.environ.get('FACEBOOK_GRAPH_BASE_URL')
        if effective_base_path:
            self.GRAPH = effective_base_path.rstrip('/')
        self.requests = requests.Session()
        self.requests.verify = os.path.join(
            os.path.dirname(__file__),
            'fb_ca_chain_bundle.crt',
        )
        params = {
            'access_token': self.access_token
        }
        if app_secret:
            params['appsecret_proof'] = self._gen_appsecret_proof()
        self.requests.params.update(params)

        if self.proxies:
            self.requests.proxies.update(self.proxies)

    def _gen_appsecret_proof(self):
        h = hmac.new(
            self.app_secret.encode('utf-8'),
            msg=self.access_token.encode('utf-8'),
            digestmod=hashlib.sha256
        )

        self.appsecret_proof = h.hexdigest()
        return self.appsecret_proof

__all__ = ['FacebookSession']

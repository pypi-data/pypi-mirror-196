# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------

from typing import Any, TYPE_CHECKING

from azure.core.configuration import Configuration
from azure.core.pipeline import policies

if TYPE_CHECKING:
    # pylint: disable=unused-import,ungrouped-imports
    from azure.core.credentials import TokenCredential

VERSION = "unknown"

class FormRecognizerClientConfiguration(Configuration):  # pylint: disable=too-many-instance-attributes
    """Configuration for FormRecognizerClient.

    Note that all parameters used to create this instance are saved as instance
    attributes.

    :param credential: Credential needed for the client to connect to Azure.
    :type credential: ~azure.core.credentials.TokenCredential
    :param endpoint: Supported Cognitive Services endpoints (protocol and hostname, for
     example: https://westus2.api.cognitive.microsoft.com).
    :type endpoint: str
    :keyword api_version: Api Version. Default value is "2022-08-31". Note that overriding this
     default value may result in unsupported behavior.
    :paramtype api_version: str
    """

    def __init__(
        self,
        credential: "TokenCredential",
        endpoint: str,
        **kwargs: Any
    ) -> None:
        super(FormRecognizerClientConfiguration, self).__init__(**kwargs)
        api_version = kwargs.pop('api_version', "2022-08-31")  # type: str

        if credential is None:
            raise ValueError("Parameter 'credential' must not be None.")
        if endpoint is None:
            raise ValueError("Parameter 'endpoint' must not be None.")

        self.credential = credential
        self.endpoint = endpoint
        self.api_version = api_version
        self.credential_scopes = kwargs.pop('credential_scopes', ['https://cognitiveservices.azure.com/.default'])
        kwargs.setdefault('sdk_moniker', 'ai-formrecognizer/{}'.format(VERSION))
        self._configure(**kwargs)

    def _configure(
        self,
        **kwargs  # type: Any
    ):
        # type: (...) -> None
        self.user_agent_policy = kwargs.get('user_agent_policy') or policies.UserAgentPolicy(**kwargs)
        self.headers_policy = kwargs.get('headers_policy') or policies.HeadersPolicy(**kwargs)
        self.proxy_policy = kwargs.get('proxy_policy') or policies.ProxyPolicy(**kwargs)
        self.logging_policy = kwargs.get('logging_policy') or policies.NetworkTraceLoggingPolicy(**kwargs)
        self.http_logging_policy = kwargs.get('http_logging_policy') or policies.HttpLoggingPolicy(**kwargs)
        self.retry_policy = kwargs.get('retry_policy') or policies.RetryPolicy(**kwargs)
        self.custom_hook_policy = kwargs.get('custom_hook_policy') or policies.CustomHookPolicy(**kwargs)
        self.redirect_policy = kwargs.get('redirect_policy') or policies.RedirectPolicy(**kwargs)
        self.authentication_policy = kwargs.get('authentication_policy')
        if self.credential and not self.authentication_policy:
            self.authentication_policy = policies.BearerTokenCredentialPolicy(self.credential, *self.credential_scopes, **kwargs)

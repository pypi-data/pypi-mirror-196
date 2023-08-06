"""
Type annotations for chime-sdk-voice service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_voice/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_chime_sdk_voice.client import ChimeSDKVoiceClient

    session = get_session()
    async with session.create_client("chime-sdk-voice") as client:
        client: ChimeSDKVoiceClient
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import (
    CapabilityType,
    GeoMatchLevelType,
    NumberSelectionBehaviorType,
    PhoneNumberAssociationNameType,
    PhoneNumberProductTypeType,
    PhoneNumberTypeType,
    ProxySessionStatusType,
    SipRuleTriggerTypeType,
    VoiceConnectorAwsRegionType,
)
from .paginator import ListSipMediaApplicationsPaginator, ListSipRulesPaginator
from .type_defs import (
    AssociatePhoneNumbersWithVoiceConnectorGroupResponseTypeDef,
    AssociatePhoneNumbersWithVoiceConnectorResponseTypeDef,
    BatchDeletePhoneNumberResponseTypeDef,
    BatchUpdatePhoneNumberResponseTypeDef,
    CreatePhoneNumberOrderResponseTypeDef,
    CreateProxySessionResponseTypeDef,
    CreateSipMediaApplicationCallResponseTypeDef,
    CreateSipMediaApplicationResponseTypeDef,
    CreateSipRuleResponseTypeDef,
    CreateVoiceConnectorGroupResponseTypeDef,
    CreateVoiceConnectorResponseTypeDef,
    CredentialTypeDef,
    DisassociatePhoneNumbersFromVoiceConnectorGroupResponseTypeDef,
    DisassociatePhoneNumbersFromVoiceConnectorResponseTypeDef,
    EmergencyCallingConfigurationTypeDef,
    EmptyResponseMetadataTypeDef,
    GeoMatchParamsTypeDef,
    GetGlobalSettingsResponseTypeDef,
    GetPhoneNumberOrderResponseTypeDef,
    GetPhoneNumberResponseTypeDef,
    GetPhoneNumberSettingsResponseTypeDef,
    GetProxySessionResponseTypeDef,
    GetSipMediaApplicationAlexaSkillConfigurationResponseTypeDef,
    GetSipMediaApplicationLoggingConfigurationResponseTypeDef,
    GetSipMediaApplicationResponseTypeDef,
    GetSipRuleResponseTypeDef,
    GetVoiceConnectorEmergencyCallingConfigurationResponseTypeDef,
    GetVoiceConnectorGroupResponseTypeDef,
    GetVoiceConnectorLoggingConfigurationResponseTypeDef,
    GetVoiceConnectorOriginationResponseTypeDef,
    GetVoiceConnectorProxyResponseTypeDef,
    GetVoiceConnectorResponseTypeDef,
    GetVoiceConnectorStreamingConfigurationResponseTypeDef,
    GetVoiceConnectorTerminationHealthResponseTypeDef,
    GetVoiceConnectorTerminationResponseTypeDef,
    ListAvailableVoiceConnectorRegionsResponseTypeDef,
    ListPhoneNumberOrdersResponseTypeDef,
    ListPhoneNumbersResponseTypeDef,
    ListProxySessionsResponseTypeDef,
    ListSipMediaApplicationsResponseTypeDef,
    ListSipRulesResponseTypeDef,
    ListSupportedPhoneNumberCountriesResponseTypeDef,
    ListVoiceConnectorGroupsResponseTypeDef,
    ListVoiceConnectorsResponseTypeDef,
    ListVoiceConnectorTerminationCredentialsResponseTypeDef,
    LoggingConfigurationTypeDef,
    OriginationTypeDef,
    PutSipMediaApplicationAlexaSkillConfigurationResponseTypeDef,
    PutSipMediaApplicationLoggingConfigurationResponseTypeDef,
    PutVoiceConnectorEmergencyCallingConfigurationResponseTypeDef,
    PutVoiceConnectorLoggingConfigurationResponseTypeDef,
    PutVoiceConnectorOriginationResponseTypeDef,
    PutVoiceConnectorProxyResponseTypeDef,
    PutVoiceConnectorStreamingConfigurationResponseTypeDef,
    PutVoiceConnectorTerminationResponseTypeDef,
    RestorePhoneNumberResponseTypeDef,
    SearchAvailablePhoneNumbersResponseTypeDef,
    SipMediaApplicationAlexaSkillConfigurationTypeDef,
    SipMediaApplicationEndpointTypeDef,
    SipMediaApplicationLoggingConfigurationTypeDef,
    SipRuleTargetApplicationTypeDef,
    StreamingConfigurationTypeDef,
    TerminationTypeDef,
    UpdatePhoneNumberRequestItemTypeDef,
    UpdatePhoneNumberResponseTypeDef,
    UpdateProxySessionResponseTypeDef,
    UpdateSipMediaApplicationCallResponseTypeDef,
    UpdateSipMediaApplicationResponseTypeDef,
    UpdateSipRuleResponseTypeDef,
    UpdateVoiceConnectorGroupResponseTypeDef,
    UpdateVoiceConnectorResponseTypeDef,
    ValidateE911AddressResponseTypeDef,
    VoiceConnectorItemTypeDef,
    VoiceConnectorSettingsTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("ChimeSDKVoiceClient",)

class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    BadRequestException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    ForbiddenException: Type[BotocoreClientError]
    NotFoundException: Type[BotocoreClientError]
    ResourceLimitExceededException: Type[BotocoreClientError]
    ServiceFailureException: Type[BotocoreClientError]
    ServiceUnavailableException: Type[BotocoreClientError]
    ThrottledClientException: Type[BotocoreClientError]
    UnauthorizedClientException: Type[BotocoreClientError]

class ChimeSDKVoiceClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_voice/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ChimeSDKVoiceClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_voice/client/#exceptions)
        """
    async def associate_phone_numbers_with_voice_connector(
        self, *, VoiceConnectorId: str, E164PhoneNumbers: Sequence[str], ForceAssociate: bool = ...
    ) -> AssociatePhoneNumbersWithVoiceConnectorResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/AssociatePhoneNumbersWithVoiceConnector).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.associate_phone_numbers_with_voice_connector)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_voice/client/#associate_phone_numbers_with_voice_connector)
        """
    async def associate_phone_numbers_with_voice_connector_group(
        self,
        *,
        VoiceConnectorGroupId: str,
        E164PhoneNumbers: Sequence[str],
        ForceAssociate: bool = ...
    ) -> AssociatePhoneNumbersWithVoiceConnectorGroupResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/AssociatePhoneNumbersWithVoiceConnectorGroup).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.associate_phone_numbers_with_voice_connector_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_voice/client/#associate_phone_numbers_with_voice_connector_group)
        """
    async def batch_delete_phone_number(
        self, *, PhoneNumberIds: Sequence[str]
    ) -> BatchDeletePhoneNumberResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/BatchDeletePhoneNumber).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.batch_delete_phone_number)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_voice/client/#batch_delete_phone_number)
        """
    async def batch_update_phone_number(
        self, *, UpdatePhoneNumberRequestItems: Sequence[UpdatePhoneNumberRequestItemTypeDef]
    ) -> BatchUpdatePhoneNumberResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/BatchUpdatePhoneNumber).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.batch_update_phone_number)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_voice/client/#batch_update_phone_number)
        """
    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_voice/client/#can_paginate)
        """
    async def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.close)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_voice/client/#close)
        """
    async def create_phone_number_order(
        self, *, ProductType: PhoneNumberProductTypeType, E164PhoneNumbers: Sequence[str]
    ) -> CreatePhoneNumberOrderResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/CreatePhoneNumberOrder).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.create_phone_number_order)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_voice/client/#create_phone_number_order)
        """
    async def create_proxy_session(
        self,
        *,
        VoiceConnectorId: str,
        ParticipantPhoneNumbers: Sequence[str],
        Capabilities: Sequence[CapabilityType],
        Name: str = ...,
        ExpiryMinutes: int = ...,
        NumberSelectionBehavior: NumberSelectionBehaviorType = ...,
        GeoMatchLevel: GeoMatchLevelType = ...,
        GeoMatchParams: GeoMatchParamsTypeDef = ...
    ) -> CreateProxySessionResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/CreateProxySession).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.create_proxy_session)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_voice/client/#create_proxy_session)
        """
    async def create_sip_media_application(
        self, *, AwsRegion: str, Name: str, Endpoints: Sequence[SipMediaApplicationEndpointTypeDef]
    ) -> CreateSipMediaApplicationResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/CreateSipMediaApplication).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.create_sip_media_application)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_voice/client/#create_sip_media_application)
        """
    async def create_sip_media_application_call(
        self,
        *,
        FromPhoneNumber: str,
        ToPhoneNumber: str,
        SipMediaApplicationId: str,
        SipHeaders: Mapping[str, str] = ...,
        ArgumentsMap: Mapping[str, str] = ...
    ) -> CreateSipMediaApplicationCallResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/CreateSipMediaApplicationCall).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.create_sip_media_application_call)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_voice/client/#create_sip_media_application_call)
        """
    async def create_sip_rule(
        self,
        *,
        Name: str,
        TriggerType: SipRuleTriggerTypeType,
        TriggerValue: str,
        Disabled: bool = ...,
        TargetApplications: Sequence[SipRuleTargetApplicationTypeDef] = ...
    ) -> CreateSipRuleResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/CreateSipRule).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.create_sip_rule)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_voice/client/#create_sip_rule)
        """
    async def create_voice_connector(
        self, *, Name: str, RequireEncryption: bool, AwsRegion: VoiceConnectorAwsRegionType = ...
    ) -> CreateVoiceConnectorResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/CreateVoiceConnector).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.create_voice_connector)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_voice/client/#create_voice_connector)
        """
    async def create_voice_connector_group(
        self, *, Name: str, VoiceConnectorItems: Sequence[VoiceConnectorItemTypeDef] = ...
    ) -> CreateVoiceConnectorGroupResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/CreateVoiceConnectorGroup).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.create_voice_connector_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_voice/client/#create_voice_connector_group)
        """
    async def delete_phone_number(self, *, PhoneNumberId: str) -> EmptyResponseMetadataTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/DeletePhoneNumber).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.delete_phone_number)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_voice/client/#delete_phone_number)
        """
    async def delete_proxy_session(
        self, *, VoiceConnectorId: str, ProxySessionId: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/DeleteProxySession).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.delete_proxy_session)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_voice/client/#delete_proxy_session)
        """
    async def delete_sip_media_application(
        self, *, SipMediaApplicationId: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/DeleteSipMediaApplication).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.delete_sip_media_application)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_voice/client/#delete_sip_media_application)
        """
    async def delete_sip_rule(self, *, SipRuleId: str) -> EmptyResponseMetadataTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/DeleteSipRule).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.delete_sip_rule)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_voice/client/#delete_sip_rule)
        """
    async def delete_voice_connector(
        self, *, VoiceConnectorId: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/DeleteVoiceConnector).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.delete_voice_connector)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_voice/client/#delete_voice_connector)
        """
    async def delete_voice_connector_emergency_calling_configuration(
        self, *, VoiceConnectorId: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/DeleteVoiceConnectorEmergencyCallingConfiguration).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.delete_voice_connector_emergency_calling_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_voice/client/#delete_voice_connector_emergency_calling_configuration)
        """
    async def delete_voice_connector_group(
        self, *, VoiceConnectorGroupId: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/DeleteVoiceConnectorGroup).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.delete_voice_connector_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_voice/client/#delete_voice_connector_group)
        """
    async def delete_voice_connector_origination(
        self, *, VoiceConnectorId: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/DeleteVoiceConnectorOrigination).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.delete_voice_connector_origination)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_voice/client/#delete_voice_connector_origination)
        """
    async def delete_voice_connector_proxy(
        self, *, VoiceConnectorId: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/DeleteVoiceConnectorProxy).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.delete_voice_connector_proxy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_voice/client/#delete_voice_connector_proxy)
        """
    async def delete_voice_connector_streaming_configuration(
        self, *, VoiceConnectorId: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/DeleteVoiceConnectorStreamingConfiguration).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.delete_voice_connector_streaming_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_voice/client/#delete_voice_connector_streaming_configuration)
        """
    async def delete_voice_connector_termination(
        self, *, VoiceConnectorId: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/DeleteVoiceConnectorTermination).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.delete_voice_connector_termination)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_voice/client/#delete_voice_connector_termination)
        """
    async def delete_voice_connector_termination_credentials(
        self, *, VoiceConnectorId: str, Usernames: Sequence[str]
    ) -> EmptyResponseMetadataTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/DeleteVoiceConnectorTerminationCredentials).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.delete_voice_connector_termination_credentials)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_voice/client/#delete_voice_connector_termination_credentials)
        """
    async def disassociate_phone_numbers_from_voice_connector(
        self, *, VoiceConnectorId: str, E164PhoneNumbers: Sequence[str]
    ) -> DisassociatePhoneNumbersFromVoiceConnectorResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/DisassociatePhoneNumbersFromVoiceConnector).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.disassociate_phone_numbers_from_voice_connector)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_voice/client/#disassociate_phone_numbers_from_voice_connector)
        """
    async def disassociate_phone_numbers_from_voice_connector_group(
        self, *, VoiceConnectorGroupId: str, E164PhoneNumbers: Sequence[str]
    ) -> DisassociatePhoneNumbersFromVoiceConnectorGroupResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/DisassociatePhoneNumbersFromVoiceConnectorGroup).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.disassociate_phone_numbers_from_voice_connector_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_voice/client/#disassociate_phone_numbers_from_voice_connector_group)
        """
    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        Generate a presigned url given a client, its method, and arguments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_voice/client/#generate_presigned_url)
        """
    async def get_global_settings(self) -> GetGlobalSettingsResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/GetGlobalSettings).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.get_global_settings)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_voice/client/#get_global_settings)
        """
    async def get_phone_number(self, *, PhoneNumberId: str) -> GetPhoneNumberResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/GetPhoneNumber).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.get_phone_number)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_voice/client/#get_phone_number)
        """
    async def get_phone_number_order(
        self, *, PhoneNumberOrderId: str
    ) -> GetPhoneNumberOrderResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/GetPhoneNumberOrder).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.get_phone_number_order)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_voice/client/#get_phone_number_order)
        """
    async def get_phone_number_settings(self) -> GetPhoneNumberSettingsResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/GetPhoneNumberSettings).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.get_phone_number_settings)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_voice/client/#get_phone_number_settings)
        """
    async def get_proxy_session(
        self, *, VoiceConnectorId: str, ProxySessionId: str
    ) -> GetProxySessionResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/GetProxySession).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.get_proxy_session)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_voice/client/#get_proxy_session)
        """
    async def get_sip_media_application(
        self, *, SipMediaApplicationId: str
    ) -> GetSipMediaApplicationResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/GetSipMediaApplication).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.get_sip_media_application)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_voice/client/#get_sip_media_application)
        """
    async def get_sip_media_application_alexa_skill_configuration(
        self, *, SipMediaApplicationId: str
    ) -> GetSipMediaApplicationAlexaSkillConfigurationResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/GetSipMediaApplicationAlexaSkillConfiguration).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.get_sip_media_application_alexa_skill_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_voice/client/#get_sip_media_application_alexa_skill_configuration)
        """
    async def get_sip_media_application_logging_configuration(
        self, *, SipMediaApplicationId: str
    ) -> GetSipMediaApplicationLoggingConfigurationResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/GetSipMediaApplicationLoggingConfiguration).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.get_sip_media_application_logging_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_voice/client/#get_sip_media_application_logging_configuration)
        """
    async def get_sip_rule(self, *, SipRuleId: str) -> GetSipRuleResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/GetSipRule).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.get_sip_rule)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_voice/client/#get_sip_rule)
        """
    async def get_voice_connector(
        self, *, VoiceConnectorId: str
    ) -> GetVoiceConnectorResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/GetVoiceConnector).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.get_voice_connector)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_voice/client/#get_voice_connector)
        """
    async def get_voice_connector_emergency_calling_configuration(
        self, *, VoiceConnectorId: str
    ) -> GetVoiceConnectorEmergencyCallingConfigurationResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/GetVoiceConnectorEmergencyCallingConfiguration).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.get_voice_connector_emergency_calling_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_voice/client/#get_voice_connector_emergency_calling_configuration)
        """
    async def get_voice_connector_group(
        self, *, VoiceConnectorGroupId: str
    ) -> GetVoiceConnectorGroupResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/GetVoiceConnectorGroup).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.get_voice_connector_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_voice/client/#get_voice_connector_group)
        """
    async def get_voice_connector_logging_configuration(
        self, *, VoiceConnectorId: str
    ) -> GetVoiceConnectorLoggingConfigurationResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/GetVoiceConnectorLoggingConfiguration).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.get_voice_connector_logging_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_voice/client/#get_voice_connector_logging_configuration)
        """
    async def get_voice_connector_origination(
        self, *, VoiceConnectorId: str
    ) -> GetVoiceConnectorOriginationResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/GetVoiceConnectorOrigination).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.get_voice_connector_origination)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_voice/client/#get_voice_connector_origination)
        """
    async def get_voice_connector_proxy(
        self, *, VoiceConnectorId: str
    ) -> GetVoiceConnectorProxyResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/GetVoiceConnectorProxy).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.get_voice_connector_proxy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_voice/client/#get_voice_connector_proxy)
        """
    async def get_voice_connector_streaming_configuration(
        self, *, VoiceConnectorId: str
    ) -> GetVoiceConnectorStreamingConfigurationResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/GetVoiceConnectorStreamingConfiguration).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.get_voice_connector_streaming_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_voice/client/#get_voice_connector_streaming_configuration)
        """
    async def get_voice_connector_termination(
        self, *, VoiceConnectorId: str
    ) -> GetVoiceConnectorTerminationResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/GetVoiceConnectorTermination).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.get_voice_connector_termination)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_voice/client/#get_voice_connector_termination)
        """
    async def get_voice_connector_termination_health(
        self, *, VoiceConnectorId: str
    ) -> GetVoiceConnectorTerminationHealthResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/GetVoiceConnectorTerminationHealth).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.get_voice_connector_termination_health)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_voice/client/#get_voice_connector_termination_health)
        """
    async def list_available_voice_connector_regions(
        self,
    ) -> ListAvailableVoiceConnectorRegionsResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/ListAvailableVoiceConnectorRegions).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.list_available_voice_connector_regions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_voice/client/#list_available_voice_connector_regions)
        """
    async def list_phone_number_orders(
        self, *, NextToken: str = ..., MaxResults: int = ...
    ) -> ListPhoneNumberOrdersResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/ListPhoneNumberOrders).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.list_phone_number_orders)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_voice/client/#list_phone_number_orders)
        """
    async def list_phone_numbers(
        self,
        *,
        Status: str = ...,
        ProductType: PhoneNumberProductTypeType = ...,
        FilterName: PhoneNumberAssociationNameType = ...,
        FilterValue: str = ...,
        MaxResults: int = ...,
        NextToken: str = ...
    ) -> ListPhoneNumbersResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/ListPhoneNumbers).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.list_phone_numbers)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_voice/client/#list_phone_numbers)
        """
    async def list_proxy_sessions(
        self,
        *,
        VoiceConnectorId: str,
        Status: ProxySessionStatusType = ...,
        NextToken: str = ...,
        MaxResults: int = ...
    ) -> ListProxySessionsResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/ListProxySessions).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.list_proxy_sessions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_voice/client/#list_proxy_sessions)
        """
    async def list_sip_media_applications(
        self, *, MaxResults: int = ..., NextToken: str = ...
    ) -> ListSipMediaApplicationsResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/ListSipMediaApplications).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.list_sip_media_applications)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_voice/client/#list_sip_media_applications)
        """
    async def list_sip_rules(
        self, *, SipMediaApplicationId: str = ..., MaxResults: int = ..., NextToken: str = ...
    ) -> ListSipRulesResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/ListSipRules).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.list_sip_rules)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_voice/client/#list_sip_rules)
        """
    async def list_supported_phone_number_countries(
        self, *, ProductType: PhoneNumberProductTypeType
    ) -> ListSupportedPhoneNumberCountriesResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/ListSupportedPhoneNumberCountries).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.list_supported_phone_number_countries)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_voice/client/#list_supported_phone_number_countries)
        """
    async def list_voice_connector_groups(
        self, *, NextToken: str = ..., MaxResults: int = ...
    ) -> ListVoiceConnectorGroupsResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/ListVoiceConnectorGroups).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.list_voice_connector_groups)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_voice/client/#list_voice_connector_groups)
        """
    async def list_voice_connector_termination_credentials(
        self, *, VoiceConnectorId: str
    ) -> ListVoiceConnectorTerminationCredentialsResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/ListVoiceConnectorTerminationCredentials).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.list_voice_connector_termination_credentials)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_voice/client/#list_voice_connector_termination_credentials)
        """
    async def list_voice_connectors(
        self, *, NextToken: str = ..., MaxResults: int = ...
    ) -> ListVoiceConnectorsResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/ListVoiceConnectors).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.list_voice_connectors)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_voice/client/#list_voice_connectors)
        """
    async def put_sip_media_application_alexa_skill_configuration(
        self,
        *,
        SipMediaApplicationId: str,
        SipMediaApplicationAlexaSkillConfiguration: SipMediaApplicationAlexaSkillConfigurationTypeDef = ...
    ) -> PutSipMediaApplicationAlexaSkillConfigurationResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/PutSipMediaApplicationAlexaSkillConfiguration).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.put_sip_media_application_alexa_skill_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_voice/client/#put_sip_media_application_alexa_skill_configuration)
        """
    async def put_sip_media_application_logging_configuration(
        self,
        *,
        SipMediaApplicationId: str,
        SipMediaApplicationLoggingConfiguration: SipMediaApplicationLoggingConfigurationTypeDef = ...
    ) -> PutSipMediaApplicationLoggingConfigurationResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/PutSipMediaApplicationLoggingConfiguration).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.put_sip_media_application_logging_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_voice/client/#put_sip_media_application_logging_configuration)
        """
    async def put_voice_connector_emergency_calling_configuration(
        self,
        *,
        VoiceConnectorId: str,
        EmergencyCallingConfiguration: EmergencyCallingConfigurationTypeDef
    ) -> PutVoiceConnectorEmergencyCallingConfigurationResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/PutVoiceConnectorEmergencyCallingConfiguration).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.put_voice_connector_emergency_calling_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_voice/client/#put_voice_connector_emergency_calling_configuration)
        """
    async def put_voice_connector_logging_configuration(
        self, *, VoiceConnectorId: str, LoggingConfiguration: LoggingConfigurationTypeDef
    ) -> PutVoiceConnectorLoggingConfigurationResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/PutVoiceConnectorLoggingConfiguration).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.put_voice_connector_logging_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_voice/client/#put_voice_connector_logging_configuration)
        """
    async def put_voice_connector_origination(
        self, *, VoiceConnectorId: str, Origination: OriginationTypeDef
    ) -> PutVoiceConnectorOriginationResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/PutVoiceConnectorOrigination).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.put_voice_connector_origination)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_voice/client/#put_voice_connector_origination)
        """
    async def put_voice_connector_proxy(
        self,
        *,
        VoiceConnectorId: str,
        DefaultSessionExpiryMinutes: int,
        PhoneNumberPoolCountries: Sequence[str],
        FallBackPhoneNumber: str = ...,
        Disabled: bool = ...
    ) -> PutVoiceConnectorProxyResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/PutVoiceConnectorProxy).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.put_voice_connector_proxy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_voice/client/#put_voice_connector_proxy)
        """
    async def put_voice_connector_streaming_configuration(
        self, *, VoiceConnectorId: str, StreamingConfiguration: StreamingConfigurationTypeDef
    ) -> PutVoiceConnectorStreamingConfigurationResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/PutVoiceConnectorStreamingConfiguration).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.put_voice_connector_streaming_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_voice/client/#put_voice_connector_streaming_configuration)
        """
    async def put_voice_connector_termination(
        self, *, VoiceConnectorId: str, Termination: TerminationTypeDef
    ) -> PutVoiceConnectorTerminationResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/PutVoiceConnectorTermination).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.put_voice_connector_termination)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_voice/client/#put_voice_connector_termination)
        """
    async def put_voice_connector_termination_credentials(
        self, *, VoiceConnectorId: str, Credentials: Sequence[CredentialTypeDef] = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/PutVoiceConnectorTerminationCredentials).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.put_voice_connector_termination_credentials)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_voice/client/#put_voice_connector_termination_credentials)
        """
    async def restore_phone_number(
        self, *, PhoneNumberId: str
    ) -> RestorePhoneNumberResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/RestorePhoneNumber).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.restore_phone_number)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_voice/client/#restore_phone_number)
        """
    async def search_available_phone_numbers(
        self,
        *,
        AreaCode: str = ...,
        City: str = ...,
        Country: str = ...,
        State: str = ...,
        TollFreePrefix: str = ...,
        PhoneNumberType: PhoneNumberTypeType = ...,
        MaxResults: int = ...,
        NextToken: str = ...
    ) -> SearchAvailablePhoneNumbersResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/SearchAvailablePhoneNumbers).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.search_available_phone_numbers)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_voice/client/#search_available_phone_numbers)
        """
    async def update_global_settings(
        self, *, VoiceConnector: VoiceConnectorSettingsTypeDef = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/UpdateGlobalSettings).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.update_global_settings)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_voice/client/#update_global_settings)
        """
    async def update_phone_number(
        self,
        *,
        PhoneNumberId: str,
        ProductType: PhoneNumberProductTypeType = ...,
        CallingName: str = ...
    ) -> UpdatePhoneNumberResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/UpdatePhoneNumber).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.update_phone_number)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_voice/client/#update_phone_number)
        """
    async def update_phone_number_settings(
        self, *, CallingName: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/UpdatePhoneNumberSettings).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.update_phone_number_settings)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_voice/client/#update_phone_number_settings)
        """
    async def update_proxy_session(
        self,
        *,
        VoiceConnectorId: str,
        ProxySessionId: str,
        Capabilities: Sequence[CapabilityType],
        ExpiryMinutes: int = ...
    ) -> UpdateProxySessionResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/UpdateProxySession).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.update_proxy_session)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_voice/client/#update_proxy_session)
        """
    async def update_sip_media_application(
        self,
        *,
        SipMediaApplicationId: str,
        Name: str = ...,
        Endpoints: Sequence[SipMediaApplicationEndpointTypeDef] = ...
    ) -> UpdateSipMediaApplicationResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/UpdateSipMediaApplication).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.update_sip_media_application)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_voice/client/#update_sip_media_application)
        """
    async def update_sip_media_application_call(
        self, *, SipMediaApplicationId: str, TransactionId: str, Arguments: Mapping[str, str]
    ) -> UpdateSipMediaApplicationCallResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/UpdateSipMediaApplicationCall).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.update_sip_media_application_call)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_voice/client/#update_sip_media_application_call)
        """
    async def update_sip_rule(
        self,
        *,
        SipRuleId: str,
        Name: str,
        Disabled: bool = ...,
        TargetApplications: Sequence[SipRuleTargetApplicationTypeDef] = ...
    ) -> UpdateSipRuleResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/UpdateSipRule).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.update_sip_rule)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_voice/client/#update_sip_rule)
        """
    async def update_voice_connector(
        self, *, VoiceConnectorId: str, Name: str, RequireEncryption: bool
    ) -> UpdateVoiceConnectorResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/UpdateVoiceConnector).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.update_voice_connector)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_voice/client/#update_voice_connector)
        """
    async def update_voice_connector_group(
        self,
        *,
        VoiceConnectorGroupId: str,
        Name: str,
        VoiceConnectorItems: Sequence[VoiceConnectorItemTypeDef]
    ) -> UpdateVoiceConnectorGroupResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/UpdateVoiceConnectorGroup).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.update_voice_connector_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_voice/client/#update_voice_connector_group)
        """
    async def validate_e911_address(
        self,
        *,
        AwsAccountId: str,
        StreetNumber: str,
        StreetInfo: str,
        City: str,
        State: str,
        Country: str,
        PostalCode: str
    ) -> ValidateE911AddressResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/ValidateE911Address).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.validate_e911_address)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_voice/client/#validate_e911_address)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_sip_media_applications"]
    ) -> ListSipMediaApplicationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_voice/client/#get_paginator)
        """
    @overload
    def get_paginator(self, operation_name: Literal["list_sip_rules"]) -> ListSipRulesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_voice/client/#get_paginator)
        """
    async def __aenter__(self) -> "ChimeSDKVoiceClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_voice/client/)
        """
    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_voice/client/)
        """

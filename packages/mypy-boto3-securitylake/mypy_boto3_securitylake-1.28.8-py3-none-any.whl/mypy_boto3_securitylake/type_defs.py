"""
Type annotations for securitylake service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/type_defs/)

Usage::

    ```python
    from mypy_boto3_securitylake.type_defs import AwsIdentityOutputTypeDef

    data: AwsIdentityOutputTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Any, Dict, List, Mapping, Sequence

from .literals import (
    AccessTypeType,
    AwsLogSourceNameType,
    DataLakeStatusType,
    HttpMethodType,
    SourceCollectionStatusType,
    SubscriberStatusType,
)

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "AwsIdentityOutputTypeDef",
    "AwsIdentityTypeDef",
    "AwsLogSourceConfigurationTypeDef",
    "AwsLogSourceResourceOutputTypeDef",
    "AwsLogSourceResourceTypeDef",
    "ResponseMetadataTypeDef",
    "CreateDataLakeExceptionSubscriptionRequestRequestTypeDef",
    "TagTypeDef",
    "CustomLogSourceAttributesOutputTypeDef",
    "CustomLogSourceAttributesTypeDef",
    "CustomLogSourceCrawlerConfigurationTypeDef",
    "CustomLogSourceProviderOutputTypeDef",
    "CustomLogSourceProviderTypeDef",
    "DataLakeEncryptionConfigurationTypeDef",
    "DataLakeReplicationConfigurationTypeDef",
    "DataLakeEncryptionConfigurationOutputTypeDef",
    "DataLakeExceptionTypeDef",
    "DataLakeLifecycleExpirationOutputTypeDef",
    "DataLakeLifecycleTransitionOutputTypeDef",
    "DataLakeLifecycleExpirationTypeDef",
    "DataLakeLifecycleTransitionTypeDef",
    "DataLakeReplicationConfigurationOutputTypeDef",
    "DataLakeSourceStatusTypeDef",
    "DataLakeUpdateExceptionTypeDef",
    "DeleteCustomLogSourceRequestRequestTypeDef",
    "DeleteDataLakeRequestRequestTypeDef",
    "DeleteSubscriberNotificationRequestRequestTypeDef",
    "DeleteSubscriberRequestRequestTypeDef",
    "PaginatorConfigTypeDef",
    "GetDataLakeSourcesRequestRequestTypeDef",
    "GetSubscriberRequestRequestTypeDef",
    "HttpsNotificationConfigurationTypeDef",
    "ListDataLakeExceptionsRequestRequestTypeDef",
    "ListDataLakesRequestRequestTypeDef",
    "ListSubscribersRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "TagOutputTypeDef",
    "RegisterDataLakeDelegatedAdministratorRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateDataLakeExceptionSubscriptionRequestRequestTypeDef",
    "CreateAwsLogSourceRequestRequestTypeDef",
    "DeleteAwsLogSourceRequestRequestTypeDef",
    "DataLakeAutoEnableNewAccountConfigurationOutputTypeDef",
    "DataLakeAutoEnableNewAccountConfigurationTypeDef",
    "CreateAwsLogSourceResponseTypeDef",
    "CreateSubscriberNotificationResponseTypeDef",
    "DeleteAwsLogSourceResponseTypeDef",
    "GetDataLakeExceptionSubscriptionResponseTypeDef",
    "UpdateSubscriberNotificationResponseTypeDef",
    "TagResourceRequestRequestTypeDef",
    "CustomLogSourceConfigurationTypeDef",
    "CustomLogSourceResourceOutputTypeDef",
    "CustomLogSourceResourceTypeDef",
    "ListDataLakeExceptionsResponseTypeDef",
    "DataLakeLifecycleConfigurationOutputTypeDef",
    "DataLakeLifecycleConfigurationTypeDef",
    "DataLakeSourceTypeDef",
    "DataLakeUpdateStatusTypeDef",
    "GetDataLakeSourcesRequestGetDataLakeSourcesPaginateTypeDef",
    "ListDataLakeExceptionsRequestListDataLakeExceptionsPaginateTypeDef",
    "ListSubscribersRequestListSubscribersPaginateTypeDef",
    "NotificationConfigurationTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "GetDataLakeOrganizationConfigurationResponseTypeDef",
    "CreateDataLakeOrganizationConfigurationRequestRequestTypeDef",
    "DeleteDataLakeOrganizationConfigurationRequestRequestTypeDef",
    "CreateCustomLogSourceRequestRequestTypeDef",
    "CreateCustomLogSourceResponseTypeDef",
    "LogSourceResourceOutputTypeDef",
    "LogSourceResourceTypeDef",
    "DataLakeConfigurationTypeDef",
    "GetDataLakeSourcesResponseTypeDef",
    "DataLakeResourceTypeDef",
    "CreateSubscriberNotificationRequestRequestTypeDef",
    "UpdateSubscriberNotificationRequestRequestTypeDef",
    "LogSourceTypeDef",
    "SubscriberResourceTypeDef",
    "CreateSubscriberRequestRequestTypeDef",
    "ListLogSourcesRequestListLogSourcesPaginateTypeDef",
    "ListLogSourcesRequestRequestTypeDef",
    "UpdateSubscriberRequestRequestTypeDef",
    "CreateDataLakeRequestRequestTypeDef",
    "UpdateDataLakeRequestRequestTypeDef",
    "CreateDataLakeResponseTypeDef",
    "ListDataLakesResponseTypeDef",
    "UpdateDataLakeResponseTypeDef",
    "ListLogSourcesResponseTypeDef",
    "CreateSubscriberResponseTypeDef",
    "GetSubscriberResponseTypeDef",
    "ListSubscribersResponseTypeDef",
    "UpdateSubscriberResponseTypeDef",
)

AwsIdentityOutputTypeDef = TypedDict(
    "AwsIdentityOutputTypeDef",
    {
        "externalId": str,
        "principal": str,
    },
)

AwsIdentityTypeDef = TypedDict(
    "AwsIdentityTypeDef",
    {
        "externalId": str,
        "principal": str,
    },
)

_RequiredAwsLogSourceConfigurationTypeDef = TypedDict(
    "_RequiredAwsLogSourceConfigurationTypeDef",
    {
        "regions": Sequence[str],
        "sourceName": AwsLogSourceNameType,
    },
)
_OptionalAwsLogSourceConfigurationTypeDef = TypedDict(
    "_OptionalAwsLogSourceConfigurationTypeDef",
    {
        "accounts": Sequence[str],
        "sourceVersion": str,
    },
    total=False,
)


class AwsLogSourceConfigurationTypeDef(
    _RequiredAwsLogSourceConfigurationTypeDef, _OptionalAwsLogSourceConfigurationTypeDef
):
    pass


AwsLogSourceResourceOutputTypeDef = TypedDict(
    "AwsLogSourceResourceOutputTypeDef",
    {
        "sourceName": AwsLogSourceNameType,
        "sourceVersion": str,
    },
)

AwsLogSourceResourceTypeDef = TypedDict(
    "AwsLogSourceResourceTypeDef",
    {
        "sourceName": AwsLogSourceNameType,
        "sourceVersion": str,
    },
    total=False,
)

ResponseMetadataTypeDef = TypedDict(
    "ResponseMetadataTypeDef",
    {
        "RequestId": str,
        "HostId": str,
        "HTTPStatusCode": int,
        "HTTPHeaders": Dict[str, str],
        "RetryAttempts": int,
    },
)

_RequiredCreateDataLakeExceptionSubscriptionRequestRequestTypeDef = TypedDict(
    "_RequiredCreateDataLakeExceptionSubscriptionRequestRequestTypeDef",
    {
        "notificationEndpoint": str,
        "subscriptionProtocol": str,
    },
)
_OptionalCreateDataLakeExceptionSubscriptionRequestRequestTypeDef = TypedDict(
    "_OptionalCreateDataLakeExceptionSubscriptionRequestRequestTypeDef",
    {
        "exceptionTimeToLive": int,
    },
    total=False,
)


class CreateDataLakeExceptionSubscriptionRequestRequestTypeDef(
    _RequiredCreateDataLakeExceptionSubscriptionRequestRequestTypeDef,
    _OptionalCreateDataLakeExceptionSubscriptionRequestRequestTypeDef,
):
    pass


TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "key": str,
        "value": str,
    },
)

CustomLogSourceAttributesOutputTypeDef = TypedDict(
    "CustomLogSourceAttributesOutputTypeDef",
    {
        "crawlerArn": str,
        "databaseArn": str,
        "tableArn": str,
    },
)

CustomLogSourceAttributesTypeDef = TypedDict(
    "CustomLogSourceAttributesTypeDef",
    {
        "crawlerArn": str,
        "databaseArn": str,
        "tableArn": str,
    },
    total=False,
)

CustomLogSourceCrawlerConfigurationTypeDef = TypedDict(
    "CustomLogSourceCrawlerConfigurationTypeDef",
    {
        "roleArn": str,
    },
)

CustomLogSourceProviderOutputTypeDef = TypedDict(
    "CustomLogSourceProviderOutputTypeDef",
    {
        "location": str,
        "roleArn": str,
    },
)

CustomLogSourceProviderTypeDef = TypedDict(
    "CustomLogSourceProviderTypeDef",
    {
        "location": str,
        "roleArn": str,
    },
    total=False,
)

DataLakeEncryptionConfigurationTypeDef = TypedDict(
    "DataLakeEncryptionConfigurationTypeDef",
    {
        "kmsKeyId": str,
    },
    total=False,
)

DataLakeReplicationConfigurationTypeDef = TypedDict(
    "DataLakeReplicationConfigurationTypeDef",
    {
        "regions": Sequence[str],
        "roleArn": str,
    },
    total=False,
)

DataLakeEncryptionConfigurationOutputTypeDef = TypedDict(
    "DataLakeEncryptionConfigurationOutputTypeDef",
    {
        "kmsKeyId": str,
    },
)

DataLakeExceptionTypeDef = TypedDict(
    "DataLakeExceptionTypeDef",
    {
        "exception": str,
        "region": str,
        "remediation": str,
        "timestamp": datetime,
    },
)

DataLakeLifecycleExpirationOutputTypeDef = TypedDict(
    "DataLakeLifecycleExpirationOutputTypeDef",
    {
        "days": int,
    },
)

DataLakeLifecycleTransitionOutputTypeDef = TypedDict(
    "DataLakeLifecycleTransitionOutputTypeDef",
    {
        "days": int,
        "storageClass": str,
    },
)

DataLakeLifecycleExpirationTypeDef = TypedDict(
    "DataLakeLifecycleExpirationTypeDef",
    {
        "days": int,
    },
    total=False,
)

DataLakeLifecycleTransitionTypeDef = TypedDict(
    "DataLakeLifecycleTransitionTypeDef",
    {
        "days": int,
        "storageClass": str,
    },
    total=False,
)

DataLakeReplicationConfigurationOutputTypeDef = TypedDict(
    "DataLakeReplicationConfigurationOutputTypeDef",
    {
        "regions": List[str],
        "roleArn": str,
    },
)

DataLakeSourceStatusTypeDef = TypedDict(
    "DataLakeSourceStatusTypeDef",
    {
        "resource": str,
        "status": SourceCollectionStatusType,
    },
)

DataLakeUpdateExceptionTypeDef = TypedDict(
    "DataLakeUpdateExceptionTypeDef",
    {
        "code": str,
        "reason": str,
    },
)

_RequiredDeleteCustomLogSourceRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteCustomLogSourceRequestRequestTypeDef",
    {
        "sourceName": str,
    },
)
_OptionalDeleteCustomLogSourceRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteCustomLogSourceRequestRequestTypeDef",
    {
        "sourceVersion": str,
    },
    total=False,
)


class DeleteCustomLogSourceRequestRequestTypeDef(
    _RequiredDeleteCustomLogSourceRequestRequestTypeDef,
    _OptionalDeleteCustomLogSourceRequestRequestTypeDef,
):
    pass


DeleteDataLakeRequestRequestTypeDef = TypedDict(
    "DeleteDataLakeRequestRequestTypeDef",
    {
        "regions": Sequence[str],
    },
)

DeleteSubscriberNotificationRequestRequestTypeDef = TypedDict(
    "DeleteSubscriberNotificationRequestRequestTypeDef",
    {
        "subscriberId": str,
    },
)

DeleteSubscriberRequestRequestTypeDef = TypedDict(
    "DeleteSubscriberRequestRequestTypeDef",
    {
        "subscriberId": str,
    },
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": int,
        "PageSize": int,
        "StartingToken": str,
    },
    total=False,
)

GetDataLakeSourcesRequestRequestTypeDef = TypedDict(
    "GetDataLakeSourcesRequestRequestTypeDef",
    {
        "accounts": Sequence[str],
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

GetSubscriberRequestRequestTypeDef = TypedDict(
    "GetSubscriberRequestRequestTypeDef",
    {
        "subscriberId": str,
    },
)

_RequiredHttpsNotificationConfigurationTypeDef = TypedDict(
    "_RequiredHttpsNotificationConfigurationTypeDef",
    {
        "endpoint": str,
        "targetRoleArn": str,
    },
)
_OptionalHttpsNotificationConfigurationTypeDef = TypedDict(
    "_OptionalHttpsNotificationConfigurationTypeDef",
    {
        "authorizationApiKeyName": str,
        "authorizationApiKeyValue": str,
        "httpMethod": HttpMethodType,
    },
    total=False,
)


class HttpsNotificationConfigurationTypeDef(
    _RequiredHttpsNotificationConfigurationTypeDef, _OptionalHttpsNotificationConfigurationTypeDef
):
    pass


ListDataLakeExceptionsRequestRequestTypeDef = TypedDict(
    "ListDataLakeExceptionsRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
        "regions": Sequence[str],
    },
    total=False,
)

ListDataLakesRequestRequestTypeDef = TypedDict(
    "ListDataLakesRequestRequestTypeDef",
    {
        "regions": Sequence[str],
    },
    total=False,
)

ListSubscribersRequestRequestTypeDef = TypedDict(
    "ListSubscribersRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
    },
)

TagOutputTypeDef = TypedDict(
    "TagOutputTypeDef",
    {
        "key": str,
        "value": str,
    },
)

RegisterDataLakeDelegatedAdministratorRequestRequestTypeDef = TypedDict(
    "RegisterDataLakeDelegatedAdministratorRequestRequestTypeDef",
    {
        "accountId": str,
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tagKeys": Sequence[str],
    },
)

_RequiredUpdateDataLakeExceptionSubscriptionRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateDataLakeExceptionSubscriptionRequestRequestTypeDef",
    {
        "notificationEndpoint": str,
        "subscriptionProtocol": str,
    },
)
_OptionalUpdateDataLakeExceptionSubscriptionRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateDataLakeExceptionSubscriptionRequestRequestTypeDef",
    {
        "exceptionTimeToLive": int,
    },
    total=False,
)


class UpdateDataLakeExceptionSubscriptionRequestRequestTypeDef(
    _RequiredUpdateDataLakeExceptionSubscriptionRequestRequestTypeDef,
    _OptionalUpdateDataLakeExceptionSubscriptionRequestRequestTypeDef,
):
    pass


CreateAwsLogSourceRequestRequestTypeDef = TypedDict(
    "CreateAwsLogSourceRequestRequestTypeDef",
    {
        "sources": Sequence[AwsLogSourceConfigurationTypeDef],
    },
)

DeleteAwsLogSourceRequestRequestTypeDef = TypedDict(
    "DeleteAwsLogSourceRequestRequestTypeDef",
    {
        "sources": Sequence[AwsLogSourceConfigurationTypeDef],
    },
)

DataLakeAutoEnableNewAccountConfigurationOutputTypeDef = TypedDict(
    "DataLakeAutoEnableNewAccountConfigurationOutputTypeDef",
    {
        "region": str,
        "sources": List[AwsLogSourceResourceOutputTypeDef],
    },
)

DataLakeAutoEnableNewAccountConfigurationTypeDef = TypedDict(
    "DataLakeAutoEnableNewAccountConfigurationTypeDef",
    {
        "region": str,
        "sources": Sequence[AwsLogSourceResourceTypeDef],
    },
)

CreateAwsLogSourceResponseTypeDef = TypedDict(
    "CreateAwsLogSourceResponseTypeDef",
    {
        "failed": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateSubscriberNotificationResponseTypeDef = TypedDict(
    "CreateSubscriberNotificationResponseTypeDef",
    {
        "subscriberEndpoint": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteAwsLogSourceResponseTypeDef = TypedDict(
    "DeleteAwsLogSourceResponseTypeDef",
    {
        "failed": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetDataLakeExceptionSubscriptionResponseTypeDef = TypedDict(
    "GetDataLakeExceptionSubscriptionResponseTypeDef",
    {
        "exceptionTimeToLive": int,
        "notificationEndpoint": str,
        "subscriptionProtocol": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateSubscriberNotificationResponseTypeDef = TypedDict(
    "UpdateSubscriberNotificationResponseTypeDef",
    {
        "subscriberEndpoint": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tags": Sequence[TagTypeDef],
    },
)

CustomLogSourceConfigurationTypeDef = TypedDict(
    "CustomLogSourceConfigurationTypeDef",
    {
        "crawlerConfiguration": CustomLogSourceCrawlerConfigurationTypeDef,
        "providerIdentity": AwsIdentityTypeDef,
    },
)

CustomLogSourceResourceOutputTypeDef = TypedDict(
    "CustomLogSourceResourceOutputTypeDef",
    {
        "attributes": CustomLogSourceAttributesOutputTypeDef,
        "provider": CustomLogSourceProviderOutputTypeDef,
        "sourceName": str,
        "sourceVersion": str,
    },
)

CustomLogSourceResourceTypeDef = TypedDict(
    "CustomLogSourceResourceTypeDef",
    {
        "attributes": CustomLogSourceAttributesTypeDef,
        "provider": CustomLogSourceProviderTypeDef,
        "sourceName": str,
        "sourceVersion": str,
    },
    total=False,
)

ListDataLakeExceptionsResponseTypeDef = TypedDict(
    "ListDataLakeExceptionsResponseTypeDef",
    {
        "exceptions": List[DataLakeExceptionTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DataLakeLifecycleConfigurationOutputTypeDef = TypedDict(
    "DataLakeLifecycleConfigurationOutputTypeDef",
    {
        "expiration": DataLakeLifecycleExpirationOutputTypeDef,
        "transitions": List[DataLakeLifecycleTransitionOutputTypeDef],
    },
)

DataLakeLifecycleConfigurationTypeDef = TypedDict(
    "DataLakeLifecycleConfigurationTypeDef",
    {
        "expiration": DataLakeLifecycleExpirationTypeDef,
        "transitions": Sequence[DataLakeLifecycleTransitionTypeDef],
    },
    total=False,
)

DataLakeSourceTypeDef = TypedDict(
    "DataLakeSourceTypeDef",
    {
        "account": str,
        "eventClasses": List[str],
        "sourceName": str,
        "sourceStatuses": List[DataLakeSourceStatusTypeDef],
    },
)

DataLakeUpdateStatusTypeDef = TypedDict(
    "DataLakeUpdateStatusTypeDef",
    {
        "exception": DataLakeUpdateExceptionTypeDef,
        "requestId": str,
        "status": DataLakeStatusType,
    },
)

GetDataLakeSourcesRequestGetDataLakeSourcesPaginateTypeDef = TypedDict(
    "GetDataLakeSourcesRequestGetDataLakeSourcesPaginateTypeDef",
    {
        "accounts": Sequence[str],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListDataLakeExceptionsRequestListDataLakeExceptionsPaginateTypeDef = TypedDict(
    "ListDataLakeExceptionsRequestListDataLakeExceptionsPaginateTypeDef",
    {
        "regions": Sequence[str],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListSubscribersRequestListSubscribersPaginateTypeDef = TypedDict(
    "ListSubscribersRequestListSubscribersPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

NotificationConfigurationTypeDef = TypedDict(
    "NotificationConfigurationTypeDef",
    {
        "httpsNotificationConfiguration": HttpsNotificationConfigurationTypeDef,
        "sqsNotificationConfiguration": Mapping[str, Any],
    },
    total=False,
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "tags": List[TagOutputTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetDataLakeOrganizationConfigurationResponseTypeDef = TypedDict(
    "GetDataLakeOrganizationConfigurationResponseTypeDef",
    {
        "autoEnableNewAccount": List[DataLakeAutoEnableNewAccountConfigurationOutputTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateDataLakeOrganizationConfigurationRequestRequestTypeDef = TypedDict(
    "CreateDataLakeOrganizationConfigurationRequestRequestTypeDef",
    {
        "autoEnableNewAccount": Sequence[DataLakeAutoEnableNewAccountConfigurationTypeDef],
    },
)

DeleteDataLakeOrganizationConfigurationRequestRequestTypeDef = TypedDict(
    "DeleteDataLakeOrganizationConfigurationRequestRequestTypeDef",
    {
        "autoEnableNewAccount": Sequence[DataLakeAutoEnableNewAccountConfigurationTypeDef],
    },
)

_RequiredCreateCustomLogSourceRequestRequestTypeDef = TypedDict(
    "_RequiredCreateCustomLogSourceRequestRequestTypeDef",
    {
        "sourceName": str,
    },
)
_OptionalCreateCustomLogSourceRequestRequestTypeDef = TypedDict(
    "_OptionalCreateCustomLogSourceRequestRequestTypeDef",
    {
        "configuration": CustomLogSourceConfigurationTypeDef,
        "eventClasses": Sequence[str],
        "sourceVersion": str,
    },
    total=False,
)


class CreateCustomLogSourceRequestRequestTypeDef(
    _RequiredCreateCustomLogSourceRequestRequestTypeDef,
    _OptionalCreateCustomLogSourceRequestRequestTypeDef,
):
    pass


CreateCustomLogSourceResponseTypeDef = TypedDict(
    "CreateCustomLogSourceResponseTypeDef",
    {
        "source": CustomLogSourceResourceOutputTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

LogSourceResourceOutputTypeDef = TypedDict(
    "LogSourceResourceOutputTypeDef",
    {
        "awsLogSource": AwsLogSourceResourceOutputTypeDef,
        "customLogSource": CustomLogSourceResourceOutputTypeDef,
    },
)

LogSourceResourceTypeDef = TypedDict(
    "LogSourceResourceTypeDef",
    {
        "awsLogSource": AwsLogSourceResourceTypeDef,
        "customLogSource": CustomLogSourceResourceTypeDef,
    },
    total=False,
)

_RequiredDataLakeConfigurationTypeDef = TypedDict(
    "_RequiredDataLakeConfigurationTypeDef",
    {
        "region": str,
    },
)
_OptionalDataLakeConfigurationTypeDef = TypedDict(
    "_OptionalDataLakeConfigurationTypeDef",
    {
        "encryptionConfiguration": DataLakeEncryptionConfigurationTypeDef,
        "lifecycleConfiguration": DataLakeLifecycleConfigurationTypeDef,
        "replicationConfiguration": DataLakeReplicationConfigurationTypeDef,
    },
    total=False,
)


class DataLakeConfigurationTypeDef(
    _RequiredDataLakeConfigurationTypeDef, _OptionalDataLakeConfigurationTypeDef
):
    pass


GetDataLakeSourcesResponseTypeDef = TypedDict(
    "GetDataLakeSourcesResponseTypeDef",
    {
        "dataLakeArn": str,
        "dataLakeSources": List[DataLakeSourceTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DataLakeResourceTypeDef = TypedDict(
    "DataLakeResourceTypeDef",
    {
        "createStatus": DataLakeStatusType,
        "dataLakeArn": str,
        "encryptionConfiguration": DataLakeEncryptionConfigurationOutputTypeDef,
        "lifecycleConfiguration": DataLakeLifecycleConfigurationOutputTypeDef,
        "region": str,
        "replicationConfiguration": DataLakeReplicationConfigurationOutputTypeDef,
        "s3BucketArn": str,
        "updateStatus": DataLakeUpdateStatusTypeDef,
    },
)

CreateSubscriberNotificationRequestRequestTypeDef = TypedDict(
    "CreateSubscriberNotificationRequestRequestTypeDef",
    {
        "configuration": NotificationConfigurationTypeDef,
        "subscriberId": str,
    },
)

UpdateSubscriberNotificationRequestRequestTypeDef = TypedDict(
    "UpdateSubscriberNotificationRequestRequestTypeDef",
    {
        "configuration": NotificationConfigurationTypeDef,
        "subscriberId": str,
    },
)

LogSourceTypeDef = TypedDict(
    "LogSourceTypeDef",
    {
        "account": str,
        "region": str,
        "sources": List[LogSourceResourceOutputTypeDef],
    },
)

SubscriberResourceTypeDef = TypedDict(
    "SubscriberResourceTypeDef",
    {
        "accessTypes": List[AccessTypeType],
        "createdAt": datetime,
        "resourceShareArn": str,
        "resourceShareName": str,
        "roleArn": str,
        "s3BucketArn": str,
        "sources": List[LogSourceResourceOutputTypeDef],
        "subscriberArn": str,
        "subscriberDescription": str,
        "subscriberEndpoint": str,
        "subscriberId": str,
        "subscriberIdentity": AwsIdentityOutputTypeDef,
        "subscriberName": str,
        "subscriberStatus": SubscriberStatusType,
        "updatedAt": datetime,
    },
)

_RequiredCreateSubscriberRequestRequestTypeDef = TypedDict(
    "_RequiredCreateSubscriberRequestRequestTypeDef",
    {
        "sources": Sequence[LogSourceResourceTypeDef],
        "subscriberIdentity": AwsIdentityTypeDef,
        "subscriberName": str,
    },
)
_OptionalCreateSubscriberRequestRequestTypeDef = TypedDict(
    "_OptionalCreateSubscriberRequestRequestTypeDef",
    {
        "accessTypes": Sequence[AccessTypeType],
        "subscriberDescription": str,
        "tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateSubscriberRequestRequestTypeDef(
    _RequiredCreateSubscriberRequestRequestTypeDef, _OptionalCreateSubscriberRequestRequestTypeDef
):
    pass


ListLogSourcesRequestListLogSourcesPaginateTypeDef = TypedDict(
    "ListLogSourcesRequestListLogSourcesPaginateTypeDef",
    {
        "accounts": Sequence[str],
        "regions": Sequence[str],
        "sources": Sequence[LogSourceResourceTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListLogSourcesRequestRequestTypeDef = TypedDict(
    "ListLogSourcesRequestRequestTypeDef",
    {
        "accounts": Sequence[str],
        "maxResults": int,
        "nextToken": str,
        "regions": Sequence[str],
        "sources": Sequence[LogSourceResourceTypeDef],
    },
    total=False,
)

_RequiredUpdateSubscriberRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateSubscriberRequestRequestTypeDef",
    {
        "subscriberId": str,
    },
)
_OptionalUpdateSubscriberRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateSubscriberRequestRequestTypeDef",
    {
        "sources": Sequence[LogSourceResourceTypeDef],
        "subscriberDescription": str,
        "subscriberIdentity": AwsIdentityTypeDef,
        "subscriberName": str,
    },
    total=False,
)


class UpdateSubscriberRequestRequestTypeDef(
    _RequiredUpdateSubscriberRequestRequestTypeDef, _OptionalUpdateSubscriberRequestRequestTypeDef
):
    pass


_RequiredCreateDataLakeRequestRequestTypeDef = TypedDict(
    "_RequiredCreateDataLakeRequestRequestTypeDef",
    {
        "configurations": Sequence[DataLakeConfigurationTypeDef],
        "metaStoreManagerRoleArn": str,
    },
)
_OptionalCreateDataLakeRequestRequestTypeDef = TypedDict(
    "_OptionalCreateDataLakeRequestRequestTypeDef",
    {
        "tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateDataLakeRequestRequestTypeDef(
    _RequiredCreateDataLakeRequestRequestTypeDef, _OptionalCreateDataLakeRequestRequestTypeDef
):
    pass


UpdateDataLakeRequestRequestTypeDef = TypedDict(
    "UpdateDataLakeRequestRequestTypeDef",
    {
        "configurations": Sequence[DataLakeConfigurationTypeDef],
    },
)

CreateDataLakeResponseTypeDef = TypedDict(
    "CreateDataLakeResponseTypeDef",
    {
        "dataLakes": List[DataLakeResourceTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListDataLakesResponseTypeDef = TypedDict(
    "ListDataLakesResponseTypeDef",
    {
        "dataLakes": List[DataLakeResourceTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateDataLakeResponseTypeDef = TypedDict(
    "UpdateDataLakeResponseTypeDef",
    {
        "dataLakes": List[DataLakeResourceTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListLogSourcesResponseTypeDef = TypedDict(
    "ListLogSourcesResponseTypeDef",
    {
        "nextToken": str,
        "sources": List[LogSourceTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateSubscriberResponseTypeDef = TypedDict(
    "CreateSubscriberResponseTypeDef",
    {
        "subscriber": SubscriberResourceTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetSubscriberResponseTypeDef = TypedDict(
    "GetSubscriberResponseTypeDef",
    {
        "subscriber": SubscriberResourceTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListSubscribersResponseTypeDef = TypedDict(
    "ListSubscribersResponseTypeDef",
    {
        "nextToken": str,
        "subscribers": List[SubscriberResourceTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateSubscriberResponseTypeDef = TypedDict(
    "UpdateSubscriberResponseTypeDef",
    {
        "subscriber": SubscriberResourceTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

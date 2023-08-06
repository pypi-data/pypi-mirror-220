"""
Type annotations for codecatalyst service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecatalyst/type_defs/)

Usage::

    ```python
    from mypy_boto3_codecatalyst.type_defs import AccessTokenSummaryTypeDef

    data: AccessTokenSummaryTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Sequence, Union

from .literals import (
    ComparisonOperatorType,
    DevEnvironmentSessionTypeType,
    DevEnvironmentStatusType,
    InstanceTypeType,
    OperationTypeType,
    UserTypeType,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "AccessTokenSummaryTypeDef",
    "CreateAccessTokenRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "IdeConfigurationTypeDef",
    "PersistentStorageConfigurationTypeDef",
    "RepositoryInputTypeDef",
    "CreateProjectRequestRequestTypeDef",
    "CreateSourceRepositoryBranchRequestRequestTypeDef",
    "CreateSourceRepositoryRequestRequestTypeDef",
    "DeleteAccessTokenRequestRequestTypeDef",
    "DeleteDevEnvironmentRequestRequestTypeDef",
    "DeleteProjectRequestRequestTypeDef",
    "DeleteSourceRepositoryRequestRequestTypeDef",
    "DeleteSpaceRequestRequestTypeDef",
    "DevEnvironmentAccessDetailsTypeDef",
    "DevEnvironmentRepositorySummaryTypeDef",
    "ExecuteCommandSessionConfigurationTypeDef",
    "DevEnvironmentSessionSummaryTypeDef",
    "IdeTypeDef",
    "PersistentStorageTypeDef",
    "EmailAddressTypeDef",
    "EventPayloadTypeDef",
    "ProjectInformationTypeDef",
    "UserIdentityTypeDef",
    "FilterTypeDef",
    "GetDevEnvironmentRequestRequestTypeDef",
    "GetProjectRequestRequestTypeDef",
    "GetSourceRepositoryCloneUrlsRequestRequestTypeDef",
    "GetSourceRepositoryRequestRequestTypeDef",
    "GetSpaceRequestRequestTypeDef",
    "GetSubscriptionRequestRequestTypeDef",
    "GetUserDetailsRequestRequestTypeDef",
    "IdeConfigurationOutputTypeDef",
    "PaginatorConfigTypeDef",
    "ListAccessTokensRequestRequestTypeDef",
    "ListDevEnvironmentSessionsRequestRequestTypeDef",
    "ListEventLogsRequestRequestTypeDef",
    "ProjectListFilterTypeDef",
    "ProjectSummaryTypeDef",
    "ListSourceRepositoriesItemTypeDef",
    "ListSourceRepositoriesRequestRequestTypeDef",
    "ListSourceRepositoryBranchesItemTypeDef",
    "ListSourceRepositoryBranchesRequestRequestTypeDef",
    "ListSpacesRequestRequestTypeDef",
    "SpaceSummaryTypeDef",
    "StopDevEnvironmentRequestRequestTypeDef",
    "StopDevEnvironmentSessionRequestRequestTypeDef",
    "UpdateProjectRequestRequestTypeDef",
    "UpdateSpaceRequestRequestTypeDef",
    "CreateAccessTokenResponseTypeDef",
    "CreateDevEnvironmentResponseTypeDef",
    "CreateProjectResponseTypeDef",
    "CreateSourceRepositoryBranchResponseTypeDef",
    "CreateSourceRepositoryResponseTypeDef",
    "DeleteDevEnvironmentResponseTypeDef",
    "DeleteProjectResponseTypeDef",
    "DeleteSourceRepositoryResponseTypeDef",
    "DeleteSpaceResponseTypeDef",
    "GetProjectResponseTypeDef",
    "GetSourceRepositoryCloneUrlsResponseTypeDef",
    "GetSourceRepositoryResponseTypeDef",
    "GetSpaceResponseTypeDef",
    "GetSubscriptionResponseTypeDef",
    "ListAccessTokensResponseTypeDef",
    "StartDevEnvironmentResponseTypeDef",
    "StopDevEnvironmentResponseTypeDef",
    "StopDevEnvironmentSessionResponseTypeDef",
    "UpdateProjectResponseTypeDef",
    "UpdateSpaceResponseTypeDef",
    "VerifySessionResponseTypeDef",
    "StartDevEnvironmentRequestRequestTypeDef",
    "UpdateDevEnvironmentRequestRequestTypeDef",
    "CreateDevEnvironmentRequestRequestTypeDef",
    "StartDevEnvironmentSessionResponseTypeDef",
    "DevEnvironmentSessionConfigurationTypeDef",
    "ListDevEnvironmentSessionsResponseTypeDef",
    "DevEnvironmentSummaryTypeDef",
    "GetDevEnvironmentResponseTypeDef",
    "GetUserDetailsResponseTypeDef",
    "EventLogEntryTypeDef",
    "ListDevEnvironmentsRequestRequestTypeDef",
    "UpdateDevEnvironmentResponseTypeDef",
    "ListAccessTokensRequestListAccessTokensPaginateTypeDef",
    "ListDevEnvironmentSessionsRequestListDevEnvironmentSessionsPaginateTypeDef",
    "ListDevEnvironmentsRequestListDevEnvironmentsPaginateTypeDef",
    "ListEventLogsRequestListEventLogsPaginateTypeDef",
    "ListSourceRepositoriesRequestListSourceRepositoriesPaginateTypeDef",
    "ListSourceRepositoryBranchesRequestListSourceRepositoryBranchesPaginateTypeDef",
    "ListSpacesRequestListSpacesPaginateTypeDef",
    "ListProjectsRequestListProjectsPaginateTypeDef",
    "ListProjectsRequestRequestTypeDef",
    "ListProjectsResponseTypeDef",
    "ListSourceRepositoriesResponseTypeDef",
    "ListSourceRepositoryBranchesResponseTypeDef",
    "ListSpacesResponseTypeDef",
    "StartDevEnvironmentSessionRequestRequestTypeDef",
    "ListDevEnvironmentsResponseTypeDef",
    "ListEventLogsResponseTypeDef",
)

AccessTokenSummaryTypeDef = TypedDict(
    "AccessTokenSummaryTypeDef",
    {
        "id": str,
        "name": str,
        "expiresTime": datetime,
    },
)

_RequiredCreateAccessTokenRequestRequestTypeDef = TypedDict(
    "_RequiredCreateAccessTokenRequestRequestTypeDef",
    {
        "name": str,
    },
)
_OptionalCreateAccessTokenRequestRequestTypeDef = TypedDict(
    "_OptionalCreateAccessTokenRequestRequestTypeDef",
    {
        "expiresTime": Union[datetime, str],
    },
    total=False,
)


class CreateAccessTokenRequestRequestTypeDef(
    _RequiredCreateAccessTokenRequestRequestTypeDef, _OptionalCreateAccessTokenRequestRequestTypeDef
):
    pass


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

IdeConfigurationTypeDef = TypedDict(
    "IdeConfigurationTypeDef",
    {
        "runtime": str,
        "name": str,
    },
    total=False,
)

PersistentStorageConfigurationTypeDef = TypedDict(
    "PersistentStorageConfigurationTypeDef",
    {
        "sizeInGiB": int,
    },
)

_RequiredRepositoryInputTypeDef = TypedDict(
    "_RequiredRepositoryInputTypeDef",
    {
        "repositoryName": str,
    },
)
_OptionalRepositoryInputTypeDef = TypedDict(
    "_OptionalRepositoryInputTypeDef",
    {
        "branchName": str,
    },
    total=False,
)


class RepositoryInputTypeDef(_RequiredRepositoryInputTypeDef, _OptionalRepositoryInputTypeDef):
    pass


_RequiredCreateProjectRequestRequestTypeDef = TypedDict(
    "_RequiredCreateProjectRequestRequestTypeDef",
    {
        "spaceName": str,
        "displayName": str,
    },
)
_OptionalCreateProjectRequestRequestTypeDef = TypedDict(
    "_OptionalCreateProjectRequestRequestTypeDef",
    {
        "description": str,
    },
    total=False,
)


class CreateProjectRequestRequestTypeDef(
    _RequiredCreateProjectRequestRequestTypeDef, _OptionalCreateProjectRequestRequestTypeDef
):
    pass


_RequiredCreateSourceRepositoryBranchRequestRequestTypeDef = TypedDict(
    "_RequiredCreateSourceRepositoryBranchRequestRequestTypeDef",
    {
        "spaceName": str,
        "projectName": str,
        "sourceRepositoryName": str,
        "name": str,
    },
)
_OptionalCreateSourceRepositoryBranchRequestRequestTypeDef = TypedDict(
    "_OptionalCreateSourceRepositoryBranchRequestRequestTypeDef",
    {
        "headCommitId": str,
    },
    total=False,
)


class CreateSourceRepositoryBranchRequestRequestTypeDef(
    _RequiredCreateSourceRepositoryBranchRequestRequestTypeDef,
    _OptionalCreateSourceRepositoryBranchRequestRequestTypeDef,
):
    pass


_RequiredCreateSourceRepositoryRequestRequestTypeDef = TypedDict(
    "_RequiredCreateSourceRepositoryRequestRequestTypeDef",
    {
        "spaceName": str,
        "projectName": str,
        "name": str,
    },
)
_OptionalCreateSourceRepositoryRequestRequestTypeDef = TypedDict(
    "_OptionalCreateSourceRepositoryRequestRequestTypeDef",
    {
        "description": str,
    },
    total=False,
)


class CreateSourceRepositoryRequestRequestTypeDef(
    _RequiredCreateSourceRepositoryRequestRequestTypeDef,
    _OptionalCreateSourceRepositoryRequestRequestTypeDef,
):
    pass


DeleteAccessTokenRequestRequestTypeDef = TypedDict(
    "DeleteAccessTokenRequestRequestTypeDef",
    {
        "id": str,
    },
)

DeleteDevEnvironmentRequestRequestTypeDef = TypedDict(
    "DeleteDevEnvironmentRequestRequestTypeDef",
    {
        "spaceName": str,
        "projectName": str,
        "id": str,
    },
)

DeleteProjectRequestRequestTypeDef = TypedDict(
    "DeleteProjectRequestRequestTypeDef",
    {
        "spaceName": str,
        "name": str,
    },
)

DeleteSourceRepositoryRequestRequestTypeDef = TypedDict(
    "DeleteSourceRepositoryRequestRequestTypeDef",
    {
        "spaceName": str,
        "projectName": str,
        "name": str,
    },
)

DeleteSpaceRequestRequestTypeDef = TypedDict(
    "DeleteSpaceRequestRequestTypeDef",
    {
        "name": str,
    },
)

DevEnvironmentAccessDetailsTypeDef = TypedDict(
    "DevEnvironmentAccessDetailsTypeDef",
    {
        "streamUrl": str,
        "tokenValue": str,
    },
)

DevEnvironmentRepositorySummaryTypeDef = TypedDict(
    "DevEnvironmentRepositorySummaryTypeDef",
    {
        "repositoryName": str,
        "branchName": str,
    },
)

_RequiredExecuteCommandSessionConfigurationTypeDef = TypedDict(
    "_RequiredExecuteCommandSessionConfigurationTypeDef",
    {
        "command": str,
    },
)
_OptionalExecuteCommandSessionConfigurationTypeDef = TypedDict(
    "_OptionalExecuteCommandSessionConfigurationTypeDef",
    {
        "arguments": Sequence[str],
    },
    total=False,
)


class ExecuteCommandSessionConfigurationTypeDef(
    _RequiredExecuteCommandSessionConfigurationTypeDef,
    _OptionalExecuteCommandSessionConfigurationTypeDef,
):
    pass


DevEnvironmentSessionSummaryTypeDef = TypedDict(
    "DevEnvironmentSessionSummaryTypeDef",
    {
        "spaceName": str,
        "projectName": str,
        "devEnvironmentId": str,
        "startedTime": datetime,
        "id": str,
    },
)

IdeTypeDef = TypedDict(
    "IdeTypeDef",
    {
        "runtime": str,
        "name": str,
    },
)

PersistentStorageTypeDef = TypedDict(
    "PersistentStorageTypeDef",
    {
        "sizeInGiB": int,
    },
)

EmailAddressTypeDef = TypedDict(
    "EmailAddressTypeDef",
    {
        "email": str,
        "verified": bool,
    },
)

EventPayloadTypeDef = TypedDict(
    "EventPayloadTypeDef",
    {
        "contentType": str,
        "data": str,
    },
)

ProjectInformationTypeDef = TypedDict(
    "ProjectInformationTypeDef",
    {
        "name": str,
        "projectId": str,
    },
)

UserIdentityTypeDef = TypedDict(
    "UserIdentityTypeDef",
    {
        "userType": UserTypeType,
        "principalId": str,
        "userName": str,
        "awsAccountId": str,
    },
)

_RequiredFilterTypeDef = TypedDict(
    "_RequiredFilterTypeDef",
    {
        "key": str,
        "values": Sequence[str],
    },
)
_OptionalFilterTypeDef = TypedDict(
    "_OptionalFilterTypeDef",
    {
        "comparisonOperator": str,
    },
    total=False,
)


class FilterTypeDef(_RequiredFilterTypeDef, _OptionalFilterTypeDef):
    pass


GetDevEnvironmentRequestRequestTypeDef = TypedDict(
    "GetDevEnvironmentRequestRequestTypeDef",
    {
        "spaceName": str,
        "projectName": str,
        "id": str,
    },
)

GetProjectRequestRequestTypeDef = TypedDict(
    "GetProjectRequestRequestTypeDef",
    {
        "spaceName": str,
        "name": str,
    },
)

GetSourceRepositoryCloneUrlsRequestRequestTypeDef = TypedDict(
    "GetSourceRepositoryCloneUrlsRequestRequestTypeDef",
    {
        "spaceName": str,
        "projectName": str,
        "sourceRepositoryName": str,
    },
)

GetSourceRepositoryRequestRequestTypeDef = TypedDict(
    "GetSourceRepositoryRequestRequestTypeDef",
    {
        "spaceName": str,
        "projectName": str,
        "name": str,
    },
)

GetSpaceRequestRequestTypeDef = TypedDict(
    "GetSpaceRequestRequestTypeDef",
    {
        "name": str,
    },
)

GetSubscriptionRequestRequestTypeDef = TypedDict(
    "GetSubscriptionRequestRequestTypeDef",
    {
        "spaceName": str,
    },
)

GetUserDetailsRequestRequestTypeDef = TypedDict(
    "GetUserDetailsRequestRequestTypeDef",
    {
        "id": str,
        "userName": str,
    },
    total=False,
)

IdeConfigurationOutputTypeDef = TypedDict(
    "IdeConfigurationOutputTypeDef",
    {
        "runtime": str,
        "name": str,
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

ListAccessTokensRequestRequestTypeDef = TypedDict(
    "ListAccessTokensRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

_RequiredListDevEnvironmentSessionsRequestRequestTypeDef = TypedDict(
    "_RequiredListDevEnvironmentSessionsRequestRequestTypeDef",
    {
        "spaceName": str,
        "projectName": str,
        "devEnvironmentId": str,
    },
)
_OptionalListDevEnvironmentSessionsRequestRequestTypeDef = TypedDict(
    "_OptionalListDevEnvironmentSessionsRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)


class ListDevEnvironmentSessionsRequestRequestTypeDef(
    _RequiredListDevEnvironmentSessionsRequestRequestTypeDef,
    _OptionalListDevEnvironmentSessionsRequestRequestTypeDef,
):
    pass


_RequiredListEventLogsRequestRequestTypeDef = TypedDict(
    "_RequiredListEventLogsRequestRequestTypeDef",
    {
        "spaceName": str,
        "startTime": Union[datetime, str],
        "endTime": Union[datetime, str],
    },
)
_OptionalListEventLogsRequestRequestTypeDef = TypedDict(
    "_OptionalListEventLogsRequestRequestTypeDef",
    {
        "eventName": str,
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)


class ListEventLogsRequestRequestTypeDef(
    _RequiredListEventLogsRequestRequestTypeDef, _OptionalListEventLogsRequestRequestTypeDef
):
    pass


_RequiredProjectListFilterTypeDef = TypedDict(
    "_RequiredProjectListFilterTypeDef",
    {
        "key": Literal["hasAccessTo"],
        "values": Sequence[str],
    },
)
_OptionalProjectListFilterTypeDef = TypedDict(
    "_OptionalProjectListFilterTypeDef",
    {
        "comparisonOperator": ComparisonOperatorType,
    },
    total=False,
)


class ProjectListFilterTypeDef(
    _RequiredProjectListFilterTypeDef, _OptionalProjectListFilterTypeDef
):
    pass


ProjectSummaryTypeDef = TypedDict(
    "ProjectSummaryTypeDef",
    {
        "name": str,
        "displayName": str,
        "description": str,
    },
)

ListSourceRepositoriesItemTypeDef = TypedDict(
    "ListSourceRepositoriesItemTypeDef",
    {
        "id": str,
        "name": str,
        "description": str,
        "lastUpdatedTime": datetime,
        "createdTime": datetime,
    },
)

_RequiredListSourceRepositoriesRequestRequestTypeDef = TypedDict(
    "_RequiredListSourceRepositoriesRequestRequestTypeDef",
    {
        "spaceName": str,
        "projectName": str,
    },
)
_OptionalListSourceRepositoriesRequestRequestTypeDef = TypedDict(
    "_OptionalListSourceRepositoriesRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)


class ListSourceRepositoriesRequestRequestTypeDef(
    _RequiredListSourceRepositoriesRequestRequestTypeDef,
    _OptionalListSourceRepositoriesRequestRequestTypeDef,
):
    pass


ListSourceRepositoryBranchesItemTypeDef = TypedDict(
    "ListSourceRepositoryBranchesItemTypeDef",
    {
        "ref": str,
        "name": str,
        "lastUpdatedTime": datetime,
        "headCommitId": str,
    },
)

_RequiredListSourceRepositoryBranchesRequestRequestTypeDef = TypedDict(
    "_RequiredListSourceRepositoryBranchesRequestRequestTypeDef",
    {
        "spaceName": str,
        "projectName": str,
        "sourceRepositoryName": str,
    },
)
_OptionalListSourceRepositoryBranchesRequestRequestTypeDef = TypedDict(
    "_OptionalListSourceRepositoryBranchesRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)


class ListSourceRepositoryBranchesRequestRequestTypeDef(
    _RequiredListSourceRepositoryBranchesRequestRequestTypeDef,
    _OptionalListSourceRepositoryBranchesRequestRequestTypeDef,
):
    pass


ListSpacesRequestRequestTypeDef = TypedDict(
    "ListSpacesRequestRequestTypeDef",
    {
        "nextToken": str,
    },
    total=False,
)

SpaceSummaryTypeDef = TypedDict(
    "SpaceSummaryTypeDef",
    {
        "name": str,
        "regionName": str,
        "displayName": str,
        "description": str,
    },
)

StopDevEnvironmentRequestRequestTypeDef = TypedDict(
    "StopDevEnvironmentRequestRequestTypeDef",
    {
        "spaceName": str,
        "projectName": str,
        "id": str,
    },
)

StopDevEnvironmentSessionRequestRequestTypeDef = TypedDict(
    "StopDevEnvironmentSessionRequestRequestTypeDef",
    {
        "spaceName": str,
        "projectName": str,
        "id": str,
        "sessionId": str,
    },
)

_RequiredUpdateProjectRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateProjectRequestRequestTypeDef",
    {
        "spaceName": str,
        "name": str,
    },
)
_OptionalUpdateProjectRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateProjectRequestRequestTypeDef",
    {
        "description": str,
    },
    total=False,
)


class UpdateProjectRequestRequestTypeDef(
    _RequiredUpdateProjectRequestRequestTypeDef, _OptionalUpdateProjectRequestRequestTypeDef
):
    pass


_RequiredUpdateSpaceRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateSpaceRequestRequestTypeDef",
    {
        "name": str,
    },
)
_OptionalUpdateSpaceRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateSpaceRequestRequestTypeDef",
    {
        "description": str,
    },
    total=False,
)


class UpdateSpaceRequestRequestTypeDef(
    _RequiredUpdateSpaceRequestRequestTypeDef, _OptionalUpdateSpaceRequestRequestTypeDef
):
    pass


CreateAccessTokenResponseTypeDef = TypedDict(
    "CreateAccessTokenResponseTypeDef",
    {
        "secret": str,
        "name": str,
        "expiresTime": datetime,
        "accessTokenId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateDevEnvironmentResponseTypeDef = TypedDict(
    "CreateDevEnvironmentResponseTypeDef",
    {
        "spaceName": str,
        "projectName": str,
        "id": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateProjectResponseTypeDef = TypedDict(
    "CreateProjectResponseTypeDef",
    {
        "spaceName": str,
        "name": str,
        "displayName": str,
        "description": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateSourceRepositoryBranchResponseTypeDef = TypedDict(
    "CreateSourceRepositoryBranchResponseTypeDef",
    {
        "ref": str,
        "name": str,
        "lastUpdatedTime": datetime,
        "headCommitId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateSourceRepositoryResponseTypeDef = TypedDict(
    "CreateSourceRepositoryResponseTypeDef",
    {
        "spaceName": str,
        "projectName": str,
        "name": str,
        "description": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteDevEnvironmentResponseTypeDef = TypedDict(
    "DeleteDevEnvironmentResponseTypeDef",
    {
        "spaceName": str,
        "projectName": str,
        "id": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteProjectResponseTypeDef = TypedDict(
    "DeleteProjectResponseTypeDef",
    {
        "spaceName": str,
        "name": str,
        "displayName": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteSourceRepositoryResponseTypeDef = TypedDict(
    "DeleteSourceRepositoryResponseTypeDef",
    {
        "spaceName": str,
        "projectName": str,
        "name": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteSpaceResponseTypeDef = TypedDict(
    "DeleteSpaceResponseTypeDef",
    {
        "name": str,
        "displayName": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetProjectResponseTypeDef = TypedDict(
    "GetProjectResponseTypeDef",
    {
        "spaceName": str,
        "name": str,
        "displayName": str,
        "description": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetSourceRepositoryCloneUrlsResponseTypeDef = TypedDict(
    "GetSourceRepositoryCloneUrlsResponseTypeDef",
    {
        "https": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetSourceRepositoryResponseTypeDef = TypedDict(
    "GetSourceRepositoryResponseTypeDef",
    {
        "spaceName": str,
        "projectName": str,
        "name": str,
        "description": str,
        "lastUpdatedTime": datetime,
        "createdTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetSpaceResponseTypeDef = TypedDict(
    "GetSpaceResponseTypeDef",
    {
        "name": str,
        "regionName": str,
        "displayName": str,
        "description": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetSubscriptionResponseTypeDef = TypedDict(
    "GetSubscriptionResponseTypeDef",
    {
        "subscriptionType": str,
        "awsAccountName": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAccessTokensResponseTypeDef = TypedDict(
    "ListAccessTokensResponseTypeDef",
    {
        "items": List[AccessTokenSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartDevEnvironmentResponseTypeDef = TypedDict(
    "StartDevEnvironmentResponseTypeDef",
    {
        "spaceName": str,
        "projectName": str,
        "id": str,
        "status": DevEnvironmentStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StopDevEnvironmentResponseTypeDef = TypedDict(
    "StopDevEnvironmentResponseTypeDef",
    {
        "spaceName": str,
        "projectName": str,
        "id": str,
        "status": DevEnvironmentStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StopDevEnvironmentSessionResponseTypeDef = TypedDict(
    "StopDevEnvironmentSessionResponseTypeDef",
    {
        "spaceName": str,
        "projectName": str,
        "id": str,
        "sessionId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateProjectResponseTypeDef = TypedDict(
    "UpdateProjectResponseTypeDef",
    {
        "spaceName": str,
        "name": str,
        "displayName": str,
        "description": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateSpaceResponseTypeDef = TypedDict(
    "UpdateSpaceResponseTypeDef",
    {
        "name": str,
        "displayName": str,
        "description": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

VerifySessionResponseTypeDef = TypedDict(
    "VerifySessionResponseTypeDef",
    {
        "identity": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredStartDevEnvironmentRequestRequestTypeDef = TypedDict(
    "_RequiredStartDevEnvironmentRequestRequestTypeDef",
    {
        "spaceName": str,
        "projectName": str,
        "id": str,
    },
)
_OptionalStartDevEnvironmentRequestRequestTypeDef = TypedDict(
    "_OptionalStartDevEnvironmentRequestRequestTypeDef",
    {
        "ides": Sequence[IdeConfigurationTypeDef],
        "instanceType": InstanceTypeType,
        "inactivityTimeoutMinutes": int,
    },
    total=False,
)


class StartDevEnvironmentRequestRequestTypeDef(
    _RequiredStartDevEnvironmentRequestRequestTypeDef,
    _OptionalStartDevEnvironmentRequestRequestTypeDef,
):
    pass


_RequiredUpdateDevEnvironmentRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateDevEnvironmentRequestRequestTypeDef",
    {
        "spaceName": str,
        "projectName": str,
        "id": str,
    },
)
_OptionalUpdateDevEnvironmentRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateDevEnvironmentRequestRequestTypeDef",
    {
        "alias": str,
        "ides": Sequence[IdeConfigurationTypeDef],
        "instanceType": InstanceTypeType,
        "inactivityTimeoutMinutes": int,
        "clientToken": str,
    },
    total=False,
)


class UpdateDevEnvironmentRequestRequestTypeDef(
    _RequiredUpdateDevEnvironmentRequestRequestTypeDef,
    _OptionalUpdateDevEnvironmentRequestRequestTypeDef,
):
    pass


_RequiredCreateDevEnvironmentRequestRequestTypeDef = TypedDict(
    "_RequiredCreateDevEnvironmentRequestRequestTypeDef",
    {
        "spaceName": str,
        "projectName": str,
        "instanceType": InstanceTypeType,
        "persistentStorage": PersistentStorageConfigurationTypeDef,
    },
)
_OptionalCreateDevEnvironmentRequestRequestTypeDef = TypedDict(
    "_OptionalCreateDevEnvironmentRequestRequestTypeDef",
    {
        "repositories": Sequence[RepositoryInputTypeDef],
        "clientToken": str,
        "alias": str,
        "ides": Sequence[IdeConfigurationTypeDef],
        "inactivityTimeoutMinutes": int,
    },
    total=False,
)


class CreateDevEnvironmentRequestRequestTypeDef(
    _RequiredCreateDevEnvironmentRequestRequestTypeDef,
    _OptionalCreateDevEnvironmentRequestRequestTypeDef,
):
    pass


StartDevEnvironmentSessionResponseTypeDef = TypedDict(
    "StartDevEnvironmentSessionResponseTypeDef",
    {
        "accessDetails": DevEnvironmentAccessDetailsTypeDef,
        "sessionId": str,
        "spaceName": str,
        "projectName": str,
        "id": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredDevEnvironmentSessionConfigurationTypeDef = TypedDict(
    "_RequiredDevEnvironmentSessionConfigurationTypeDef",
    {
        "sessionType": DevEnvironmentSessionTypeType,
    },
)
_OptionalDevEnvironmentSessionConfigurationTypeDef = TypedDict(
    "_OptionalDevEnvironmentSessionConfigurationTypeDef",
    {
        "executeCommandSessionConfiguration": ExecuteCommandSessionConfigurationTypeDef,
    },
    total=False,
)


class DevEnvironmentSessionConfigurationTypeDef(
    _RequiredDevEnvironmentSessionConfigurationTypeDef,
    _OptionalDevEnvironmentSessionConfigurationTypeDef,
):
    pass


ListDevEnvironmentSessionsResponseTypeDef = TypedDict(
    "ListDevEnvironmentSessionsResponseTypeDef",
    {
        "items": List[DevEnvironmentSessionSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DevEnvironmentSummaryTypeDef = TypedDict(
    "DevEnvironmentSummaryTypeDef",
    {
        "spaceName": str,
        "projectName": str,
        "id": str,
        "lastUpdatedTime": datetime,
        "creatorId": str,
        "status": DevEnvironmentStatusType,
        "statusReason": str,
        "repositories": List[DevEnvironmentRepositorySummaryTypeDef],
        "alias": str,
        "ides": List[IdeTypeDef],
        "instanceType": InstanceTypeType,
        "inactivityTimeoutMinutes": int,
        "persistentStorage": PersistentStorageTypeDef,
    },
)

GetDevEnvironmentResponseTypeDef = TypedDict(
    "GetDevEnvironmentResponseTypeDef",
    {
        "spaceName": str,
        "projectName": str,
        "id": str,
        "lastUpdatedTime": datetime,
        "creatorId": str,
        "status": DevEnvironmentStatusType,
        "statusReason": str,
        "repositories": List[DevEnvironmentRepositorySummaryTypeDef],
        "alias": str,
        "ides": List[IdeTypeDef],
        "instanceType": InstanceTypeType,
        "inactivityTimeoutMinutes": int,
        "persistentStorage": PersistentStorageTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetUserDetailsResponseTypeDef = TypedDict(
    "GetUserDetailsResponseTypeDef",
    {
        "userId": str,
        "userName": str,
        "displayName": str,
        "primaryEmail": EmailAddressTypeDef,
        "version": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EventLogEntryTypeDef = TypedDict(
    "EventLogEntryTypeDef",
    {
        "id": str,
        "eventName": str,
        "eventType": str,
        "eventCategory": str,
        "eventSource": str,
        "eventTime": datetime,
        "operationType": OperationTypeType,
        "userIdentity": UserIdentityTypeDef,
        "projectInformation": ProjectInformationTypeDef,
        "requestId": str,
        "requestPayload": EventPayloadTypeDef,
        "responsePayload": EventPayloadTypeDef,
        "errorCode": str,
        "sourceIpAddress": str,
        "userAgent": str,
    },
)

_RequiredListDevEnvironmentsRequestRequestTypeDef = TypedDict(
    "_RequiredListDevEnvironmentsRequestRequestTypeDef",
    {
        "spaceName": str,
        "projectName": str,
    },
)
_OptionalListDevEnvironmentsRequestRequestTypeDef = TypedDict(
    "_OptionalListDevEnvironmentsRequestRequestTypeDef",
    {
        "filters": Sequence[FilterTypeDef],
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)


class ListDevEnvironmentsRequestRequestTypeDef(
    _RequiredListDevEnvironmentsRequestRequestTypeDef,
    _OptionalListDevEnvironmentsRequestRequestTypeDef,
):
    pass


UpdateDevEnvironmentResponseTypeDef = TypedDict(
    "UpdateDevEnvironmentResponseTypeDef",
    {
        "id": str,
        "spaceName": str,
        "projectName": str,
        "alias": str,
        "ides": List[IdeConfigurationOutputTypeDef],
        "instanceType": InstanceTypeType,
        "inactivityTimeoutMinutes": int,
        "clientToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAccessTokensRequestListAccessTokensPaginateTypeDef = TypedDict(
    "ListAccessTokensRequestListAccessTokensPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListDevEnvironmentSessionsRequestListDevEnvironmentSessionsPaginateTypeDef = TypedDict(
    "_RequiredListDevEnvironmentSessionsRequestListDevEnvironmentSessionsPaginateTypeDef",
    {
        "spaceName": str,
        "projectName": str,
        "devEnvironmentId": str,
    },
)
_OptionalListDevEnvironmentSessionsRequestListDevEnvironmentSessionsPaginateTypeDef = TypedDict(
    "_OptionalListDevEnvironmentSessionsRequestListDevEnvironmentSessionsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListDevEnvironmentSessionsRequestListDevEnvironmentSessionsPaginateTypeDef(
    _RequiredListDevEnvironmentSessionsRequestListDevEnvironmentSessionsPaginateTypeDef,
    _OptionalListDevEnvironmentSessionsRequestListDevEnvironmentSessionsPaginateTypeDef,
):
    pass


_RequiredListDevEnvironmentsRequestListDevEnvironmentsPaginateTypeDef = TypedDict(
    "_RequiredListDevEnvironmentsRequestListDevEnvironmentsPaginateTypeDef",
    {
        "spaceName": str,
        "projectName": str,
    },
)
_OptionalListDevEnvironmentsRequestListDevEnvironmentsPaginateTypeDef = TypedDict(
    "_OptionalListDevEnvironmentsRequestListDevEnvironmentsPaginateTypeDef",
    {
        "filters": Sequence[FilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListDevEnvironmentsRequestListDevEnvironmentsPaginateTypeDef(
    _RequiredListDevEnvironmentsRequestListDevEnvironmentsPaginateTypeDef,
    _OptionalListDevEnvironmentsRequestListDevEnvironmentsPaginateTypeDef,
):
    pass


_RequiredListEventLogsRequestListEventLogsPaginateTypeDef = TypedDict(
    "_RequiredListEventLogsRequestListEventLogsPaginateTypeDef",
    {
        "spaceName": str,
        "startTime": Union[datetime, str],
        "endTime": Union[datetime, str],
    },
)
_OptionalListEventLogsRequestListEventLogsPaginateTypeDef = TypedDict(
    "_OptionalListEventLogsRequestListEventLogsPaginateTypeDef",
    {
        "eventName": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListEventLogsRequestListEventLogsPaginateTypeDef(
    _RequiredListEventLogsRequestListEventLogsPaginateTypeDef,
    _OptionalListEventLogsRequestListEventLogsPaginateTypeDef,
):
    pass


_RequiredListSourceRepositoriesRequestListSourceRepositoriesPaginateTypeDef = TypedDict(
    "_RequiredListSourceRepositoriesRequestListSourceRepositoriesPaginateTypeDef",
    {
        "spaceName": str,
        "projectName": str,
    },
)
_OptionalListSourceRepositoriesRequestListSourceRepositoriesPaginateTypeDef = TypedDict(
    "_OptionalListSourceRepositoriesRequestListSourceRepositoriesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListSourceRepositoriesRequestListSourceRepositoriesPaginateTypeDef(
    _RequiredListSourceRepositoriesRequestListSourceRepositoriesPaginateTypeDef,
    _OptionalListSourceRepositoriesRequestListSourceRepositoriesPaginateTypeDef,
):
    pass


_RequiredListSourceRepositoryBranchesRequestListSourceRepositoryBranchesPaginateTypeDef = TypedDict(
    "_RequiredListSourceRepositoryBranchesRequestListSourceRepositoryBranchesPaginateTypeDef",
    {
        "spaceName": str,
        "projectName": str,
        "sourceRepositoryName": str,
    },
)
_OptionalListSourceRepositoryBranchesRequestListSourceRepositoryBranchesPaginateTypeDef = TypedDict(
    "_OptionalListSourceRepositoryBranchesRequestListSourceRepositoryBranchesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListSourceRepositoryBranchesRequestListSourceRepositoryBranchesPaginateTypeDef(
    _RequiredListSourceRepositoryBranchesRequestListSourceRepositoryBranchesPaginateTypeDef,
    _OptionalListSourceRepositoryBranchesRequestListSourceRepositoryBranchesPaginateTypeDef,
):
    pass


ListSpacesRequestListSpacesPaginateTypeDef = TypedDict(
    "ListSpacesRequestListSpacesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListProjectsRequestListProjectsPaginateTypeDef = TypedDict(
    "_RequiredListProjectsRequestListProjectsPaginateTypeDef",
    {
        "spaceName": str,
    },
)
_OptionalListProjectsRequestListProjectsPaginateTypeDef = TypedDict(
    "_OptionalListProjectsRequestListProjectsPaginateTypeDef",
    {
        "filters": Sequence[ProjectListFilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListProjectsRequestListProjectsPaginateTypeDef(
    _RequiredListProjectsRequestListProjectsPaginateTypeDef,
    _OptionalListProjectsRequestListProjectsPaginateTypeDef,
):
    pass


_RequiredListProjectsRequestRequestTypeDef = TypedDict(
    "_RequiredListProjectsRequestRequestTypeDef",
    {
        "spaceName": str,
    },
)
_OptionalListProjectsRequestRequestTypeDef = TypedDict(
    "_OptionalListProjectsRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
        "filters": Sequence[ProjectListFilterTypeDef],
    },
    total=False,
)


class ListProjectsRequestRequestTypeDef(
    _RequiredListProjectsRequestRequestTypeDef, _OptionalListProjectsRequestRequestTypeDef
):
    pass


ListProjectsResponseTypeDef = TypedDict(
    "ListProjectsResponseTypeDef",
    {
        "nextToken": str,
        "items": List[ProjectSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListSourceRepositoriesResponseTypeDef = TypedDict(
    "ListSourceRepositoriesResponseTypeDef",
    {
        "items": List[ListSourceRepositoriesItemTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListSourceRepositoryBranchesResponseTypeDef = TypedDict(
    "ListSourceRepositoryBranchesResponseTypeDef",
    {
        "nextToken": str,
        "items": List[ListSourceRepositoryBranchesItemTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListSpacesResponseTypeDef = TypedDict(
    "ListSpacesResponseTypeDef",
    {
        "nextToken": str,
        "items": List[SpaceSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartDevEnvironmentSessionRequestRequestTypeDef = TypedDict(
    "StartDevEnvironmentSessionRequestRequestTypeDef",
    {
        "spaceName": str,
        "projectName": str,
        "id": str,
        "sessionConfiguration": DevEnvironmentSessionConfigurationTypeDef,
    },
)

ListDevEnvironmentsResponseTypeDef = TypedDict(
    "ListDevEnvironmentsResponseTypeDef",
    {
        "items": List[DevEnvironmentSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListEventLogsResponseTypeDef = TypedDict(
    "ListEventLogsResponseTypeDef",
    {
        "nextToken": str,
        "items": List[EventLogEntryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

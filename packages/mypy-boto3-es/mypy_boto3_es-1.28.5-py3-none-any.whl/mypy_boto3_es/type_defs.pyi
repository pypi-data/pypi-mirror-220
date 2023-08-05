"""
Type annotations for es service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/type_defs/)

Usage::

    ```python
    from mypy_boto3_es.type_defs import AcceptInboundCrossClusterSearchConnectionRequestRequestTypeDef

    data: AcceptInboundCrossClusterSearchConnectionRequestRequestTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import (
    AutoTuneDesiredStateType,
    AutoTuneStateType,
    DeploymentStatusType,
    DescribePackagesFilterNameType,
    DomainPackageStatusType,
    EngineTypeType,
    ESPartitionInstanceTypeType,
    ESWarmPartitionInstanceTypeType,
    InboundCrossClusterSearchConnectionStatusCodeType,
    LogTypeType,
    OptionStateType,
    OutboundCrossClusterSearchConnectionStatusCodeType,
    OverallChangeStatusType,
    PackageStatusType,
    PrincipalTypeType,
    ReservedElasticsearchInstancePaymentOptionType,
    RollbackOnDisableType,
    ScheduledAutoTuneActionTypeType,
    ScheduledAutoTuneSeverityTypeType,
    TLSSecurityPolicyType,
    UpgradeStatusType,
    UpgradeStepType,
    VolumeTypeType,
    VpcEndpointErrorCodeType,
    VpcEndpointStatusType,
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
    "AcceptInboundCrossClusterSearchConnectionRequestRequestTypeDef",
    "OptionStatusTypeDef",
    "TagTypeDef",
    "AdditionalLimitTypeDef",
    "MasterUserOptionsTypeDef",
    "AssociatePackageRequestRequestTypeDef",
    "AuthorizeVpcEndpointAccessRequestRequestTypeDef",
    "AuthorizedPrincipalTypeDef",
    "ScheduledAutoTuneDetailsTypeDef",
    "DurationOutputTypeDef",
    "DurationTypeDef",
    "AutoTuneOptionsOutputTypeDef",
    "AutoTuneStatusTypeDef",
    "CancelElasticsearchServiceSoftwareUpdateRequestRequestTypeDef",
    "ServiceSoftwareOptionsTypeDef",
    "ChangeProgressDetailsTypeDef",
    "ChangeProgressStageTypeDef",
    "CognitoOptionsOutputTypeDef",
    "CognitoOptionsTypeDef",
    "ColdStorageOptionsOutputTypeDef",
    "ColdStorageOptionsTypeDef",
    "CompatibleVersionsMapTypeDef",
    "DomainEndpointOptionsTypeDef",
    "EBSOptionsTypeDef",
    "EncryptionAtRestOptionsTypeDef",
    "LogPublishingOptionTypeDef",
    "NodeToNodeEncryptionOptionsTypeDef",
    "SnapshotOptionsTypeDef",
    "VPCOptionsTypeDef",
    "DomainInformationTypeDef",
    "DomainInformationOutputTypeDef",
    "OutboundCrossClusterSearchConnectionStatusTypeDef",
    "PackageSourceTypeDef",
    "DeleteElasticsearchDomainRequestRequestTypeDef",
    "DeleteInboundCrossClusterSearchConnectionRequestRequestTypeDef",
    "DeleteOutboundCrossClusterSearchConnectionRequestRequestTypeDef",
    "DeletePackageRequestRequestTypeDef",
    "DeleteVpcEndpointRequestRequestTypeDef",
    "VpcEndpointSummaryTypeDef",
    "DescribeDomainAutoTunesRequestRequestTypeDef",
    "DescribeDomainChangeProgressRequestRequestTypeDef",
    "DescribeElasticsearchDomainConfigRequestRequestTypeDef",
    "DescribeElasticsearchDomainRequestRequestTypeDef",
    "DescribeElasticsearchDomainsRequestRequestTypeDef",
    "DescribeElasticsearchInstanceTypeLimitsRequestRequestTypeDef",
    "FilterTypeDef",
    "DescribePackagesFilterTypeDef",
    "DescribeReservedElasticsearchInstanceOfferingsRequestDescribeReservedElasticsearchInstanceOfferingsPaginateTypeDef",
    "DescribeReservedElasticsearchInstanceOfferingsRequestRequestTypeDef",
    "DescribeReservedElasticsearchInstancesRequestDescribeReservedElasticsearchInstancesPaginateTypeDef",
    "DescribeReservedElasticsearchInstancesRequestRequestTypeDef",
    "DescribeVpcEndpointsRequestRequestTypeDef",
    "VpcEndpointErrorTypeDef",
    "DissociatePackageRequestRequestTypeDef",
    "DomainEndpointOptionsOutputTypeDef",
    "DomainInfoTypeDef",
    "ErrorDetailsTypeDef",
    "DryRunResultsTypeDef",
    "EBSOptionsOutputTypeDef",
    "ZoneAwarenessConfigOutputTypeDef",
    "ZoneAwarenessConfigTypeDef",
    "EncryptionAtRestOptionsOutputTypeDef",
    "LogPublishingOptionOutputTypeDef",
    "NodeToNodeEncryptionOptionsOutputTypeDef",
    "SnapshotOptionsOutputTypeDef",
    "VPCDerivedInfoTypeDef",
    "EmptyResponseMetadataTypeDef",
    "GetCompatibleElasticsearchVersionsRequestRequestTypeDef",
    "GetPackageVersionHistoryRequestRequestTypeDef",
    "PackageVersionHistoryTypeDef",
    "GetUpgradeHistoryRequestGetUpgradeHistoryPaginateTypeDef",
    "GetUpgradeHistoryRequestRequestTypeDef",
    "GetUpgradeStatusRequestRequestTypeDef",
    "GetUpgradeStatusResponseTypeDef",
    "InboundCrossClusterSearchConnectionStatusTypeDef",
    "InstanceCountLimitsTypeDef",
    "ListDomainNamesRequestRequestTypeDef",
    "ListDomainsForPackageRequestRequestTypeDef",
    "ListElasticsearchInstanceTypesRequestListElasticsearchInstanceTypesPaginateTypeDef",
    "ListElasticsearchInstanceTypesRequestRequestTypeDef",
    "ListElasticsearchInstanceTypesResponseTypeDef",
    "ListElasticsearchVersionsRequestListElasticsearchVersionsPaginateTypeDef",
    "ListElasticsearchVersionsRequestRequestTypeDef",
    "ListElasticsearchVersionsResponseTypeDef",
    "ListPackagesForDomainRequestRequestTypeDef",
    "ListTagsRequestRequestTypeDef",
    "TagOutputTypeDef",
    "ListVpcEndpointAccessRequestRequestTypeDef",
    "ListVpcEndpointsForDomainRequestRequestTypeDef",
    "ListVpcEndpointsRequestRequestTypeDef",
    "PaginatorConfigTypeDef",
    "PurchaseReservedElasticsearchInstanceOfferingRequestRequestTypeDef",
    "PurchaseReservedElasticsearchInstanceOfferingResponseTypeDef",
    "RecurringChargeTypeDef",
    "RejectInboundCrossClusterSearchConnectionRequestRequestTypeDef",
    "RemoveTagsRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "RevokeVpcEndpointAccessRequestRequestTypeDef",
    "SAMLIdpOutputTypeDef",
    "SAMLIdpTypeDef",
    "StartElasticsearchServiceSoftwareUpdateRequestRequestTypeDef",
    "StorageTypeLimitTypeDef",
    "UpgradeElasticsearchDomainRequestRequestTypeDef",
    "UpgradeStepItemTypeDef",
    "AccessPoliciesStatusTypeDef",
    "AdvancedOptionsStatusTypeDef",
    "ElasticsearchVersionStatusTypeDef",
    "AddTagsRequestRequestTypeDef",
    "AuthorizeVpcEndpointAccessResponseTypeDef",
    "ListVpcEndpointAccessResponseTypeDef",
    "AutoTuneDetailsTypeDef",
    "AutoTuneMaintenanceScheduleOutputTypeDef",
    "AutoTuneMaintenanceScheduleTypeDef",
    "CancelElasticsearchServiceSoftwareUpdateResponseTypeDef",
    "StartElasticsearchServiceSoftwareUpdateResponseTypeDef",
    "UpgradeElasticsearchDomainResponseTypeDef",
    "ChangeProgressStatusDetailsTypeDef",
    "CognitoOptionsStatusTypeDef",
    "GetCompatibleElasticsearchVersionsResponseTypeDef",
    "CreateVpcEndpointRequestRequestTypeDef",
    "UpdateVpcEndpointRequestRequestTypeDef",
    "CreateOutboundCrossClusterSearchConnectionRequestRequestTypeDef",
    "CreateOutboundCrossClusterSearchConnectionResponseTypeDef",
    "OutboundCrossClusterSearchConnectionTypeDef",
    "CreatePackageRequestRequestTypeDef",
    "UpdatePackageRequestRequestTypeDef",
    "DeleteVpcEndpointResponseTypeDef",
    "ListVpcEndpointsForDomainResponseTypeDef",
    "ListVpcEndpointsResponseTypeDef",
    "DescribeInboundCrossClusterSearchConnectionsRequestRequestTypeDef",
    "DescribeOutboundCrossClusterSearchConnectionsRequestRequestTypeDef",
    "DescribePackagesRequestRequestTypeDef",
    "DomainEndpointOptionsStatusTypeDef",
    "ListDomainNamesResponseTypeDef",
    "DomainPackageDetailsTypeDef",
    "PackageDetailsTypeDef",
    "EBSOptionsStatusTypeDef",
    "ElasticsearchClusterConfigOutputTypeDef",
    "ElasticsearchClusterConfigTypeDef",
    "EncryptionAtRestOptionsStatusTypeDef",
    "LogPublishingOptionsStatusTypeDef",
    "NodeToNodeEncryptionOptionsStatusTypeDef",
    "SnapshotOptionsStatusTypeDef",
    "VPCDerivedInfoStatusTypeDef",
    "VpcEndpointTypeDef",
    "GetPackageVersionHistoryResponseTypeDef",
    "InboundCrossClusterSearchConnectionTypeDef",
    "InstanceLimitsTypeDef",
    "ListTagsResponseTypeDef",
    "ReservedElasticsearchInstanceOfferingTypeDef",
    "ReservedElasticsearchInstanceTypeDef",
    "SAMLOptionsOutputTypeDef",
    "SAMLOptionsInputTypeDef",
    "StorageTypeTypeDef",
    "UpgradeHistoryTypeDef",
    "AutoTuneTypeDef",
    "AutoTuneOptionsExtraOutputTypeDef",
    "AutoTuneOptionsInputTypeDef",
    "AutoTuneOptionsTypeDef",
    "DescribeDomainChangeProgressResponseTypeDef",
    "DeleteOutboundCrossClusterSearchConnectionResponseTypeDef",
    "DescribeOutboundCrossClusterSearchConnectionsResponseTypeDef",
    "AssociatePackageResponseTypeDef",
    "DissociatePackageResponseTypeDef",
    "ListDomainsForPackageResponseTypeDef",
    "ListPackagesForDomainResponseTypeDef",
    "CreatePackageResponseTypeDef",
    "DeletePackageResponseTypeDef",
    "DescribePackagesResponseTypeDef",
    "UpdatePackageResponseTypeDef",
    "ElasticsearchClusterConfigStatusTypeDef",
    "CreateVpcEndpointResponseTypeDef",
    "DescribeVpcEndpointsResponseTypeDef",
    "UpdateVpcEndpointResponseTypeDef",
    "AcceptInboundCrossClusterSearchConnectionResponseTypeDef",
    "DeleteInboundCrossClusterSearchConnectionResponseTypeDef",
    "DescribeInboundCrossClusterSearchConnectionsResponseTypeDef",
    "RejectInboundCrossClusterSearchConnectionResponseTypeDef",
    "DescribeReservedElasticsearchInstanceOfferingsResponseTypeDef",
    "DescribeReservedElasticsearchInstancesResponseTypeDef",
    "AdvancedSecurityOptionsTypeDef",
    "AdvancedSecurityOptionsInputTypeDef",
    "LimitsTypeDef",
    "GetUpgradeHistoryResponseTypeDef",
    "DescribeDomainAutoTunesResponseTypeDef",
    "AutoTuneOptionsStatusTypeDef",
    "AdvancedSecurityOptionsStatusTypeDef",
    "ElasticsearchDomainStatusTypeDef",
    "CreateElasticsearchDomainRequestRequestTypeDef",
    "UpdateElasticsearchDomainConfigRequestRequestTypeDef",
    "DescribeElasticsearchInstanceTypeLimitsResponseTypeDef",
    "ElasticsearchDomainConfigTypeDef",
    "CreateElasticsearchDomainResponseTypeDef",
    "DeleteElasticsearchDomainResponseTypeDef",
    "DescribeElasticsearchDomainResponseTypeDef",
    "DescribeElasticsearchDomainsResponseTypeDef",
    "DescribeElasticsearchDomainConfigResponseTypeDef",
    "UpdateElasticsearchDomainConfigResponseTypeDef",
)

AcceptInboundCrossClusterSearchConnectionRequestRequestTypeDef = TypedDict(
    "AcceptInboundCrossClusterSearchConnectionRequestRequestTypeDef",
    {
        "CrossClusterSearchConnectionId": str,
    },
)

OptionStatusTypeDef = TypedDict(
    "OptionStatusTypeDef",
    {
        "CreationDate": datetime,
        "UpdateDate": datetime,
        "UpdateVersion": int,
        "State": OptionStateType,
        "PendingDeletion": bool,
    },
)

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
    },
)

AdditionalLimitTypeDef = TypedDict(
    "AdditionalLimitTypeDef",
    {
        "LimitName": str,
        "LimitValues": List[str],
    },
)

MasterUserOptionsTypeDef = TypedDict(
    "MasterUserOptionsTypeDef",
    {
        "MasterUserARN": str,
        "MasterUserName": str,
        "MasterUserPassword": str,
    },
    total=False,
)

AssociatePackageRequestRequestTypeDef = TypedDict(
    "AssociatePackageRequestRequestTypeDef",
    {
        "PackageID": str,
        "DomainName": str,
    },
)

AuthorizeVpcEndpointAccessRequestRequestTypeDef = TypedDict(
    "AuthorizeVpcEndpointAccessRequestRequestTypeDef",
    {
        "DomainName": str,
        "Account": str,
    },
)

AuthorizedPrincipalTypeDef = TypedDict(
    "AuthorizedPrincipalTypeDef",
    {
        "PrincipalType": PrincipalTypeType,
        "Principal": str,
    },
)

ScheduledAutoTuneDetailsTypeDef = TypedDict(
    "ScheduledAutoTuneDetailsTypeDef",
    {
        "Date": datetime,
        "ActionType": ScheduledAutoTuneActionTypeType,
        "Action": str,
        "Severity": ScheduledAutoTuneSeverityTypeType,
    },
)

DurationOutputTypeDef = TypedDict(
    "DurationOutputTypeDef",
    {
        "Value": int,
        "Unit": Literal["HOURS"],
    },
)

DurationTypeDef = TypedDict(
    "DurationTypeDef",
    {
        "Value": int,
        "Unit": Literal["HOURS"],
    },
    total=False,
)

AutoTuneOptionsOutputTypeDef = TypedDict(
    "AutoTuneOptionsOutputTypeDef",
    {
        "State": AutoTuneStateType,
        "ErrorMessage": str,
    },
)

AutoTuneStatusTypeDef = TypedDict(
    "AutoTuneStatusTypeDef",
    {
        "CreationDate": datetime,
        "UpdateDate": datetime,
        "UpdateVersion": int,
        "State": AutoTuneStateType,
        "ErrorMessage": str,
        "PendingDeletion": bool,
    },
)

CancelElasticsearchServiceSoftwareUpdateRequestRequestTypeDef = TypedDict(
    "CancelElasticsearchServiceSoftwareUpdateRequestRequestTypeDef",
    {
        "DomainName": str,
    },
)

ServiceSoftwareOptionsTypeDef = TypedDict(
    "ServiceSoftwareOptionsTypeDef",
    {
        "CurrentVersion": str,
        "NewVersion": str,
        "UpdateAvailable": bool,
        "Cancellable": bool,
        "UpdateStatus": DeploymentStatusType,
        "Description": str,
        "AutomatedUpdateDate": datetime,
        "OptionalDeployment": bool,
    },
)

ChangeProgressDetailsTypeDef = TypedDict(
    "ChangeProgressDetailsTypeDef",
    {
        "ChangeId": str,
        "Message": str,
    },
)

ChangeProgressStageTypeDef = TypedDict(
    "ChangeProgressStageTypeDef",
    {
        "Name": str,
        "Status": str,
        "Description": str,
        "LastUpdated": datetime,
    },
)

CognitoOptionsOutputTypeDef = TypedDict(
    "CognitoOptionsOutputTypeDef",
    {
        "Enabled": bool,
        "UserPoolId": str,
        "IdentityPoolId": str,
        "RoleArn": str,
    },
)

CognitoOptionsTypeDef = TypedDict(
    "CognitoOptionsTypeDef",
    {
        "Enabled": bool,
        "UserPoolId": str,
        "IdentityPoolId": str,
        "RoleArn": str,
    },
    total=False,
)

ColdStorageOptionsOutputTypeDef = TypedDict(
    "ColdStorageOptionsOutputTypeDef",
    {
        "Enabled": bool,
    },
)

ColdStorageOptionsTypeDef = TypedDict(
    "ColdStorageOptionsTypeDef",
    {
        "Enabled": bool,
    },
)

CompatibleVersionsMapTypeDef = TypedDict(
    "CompatibleVersionsMapTypeDef",
    {
        "SourceVersion": str,
        "TargetVersions": List[str],
    },
)

DomainEndpointOptionsTypeDef = TypedDict(
    "DomainEndpointOptionsTypeDef",
    {
        "EnforceHTTPS": bool,
        "TLSSecurityPolicy": TLSSecurityPolicyType,
        "CustomEndpointEnabled": bool,
        "CustomEndpoint": str,
        "CustomEndpointCertificateArn": str,
    },
    total=False,
)

EBSOptionsTypeDef = TypedDict(
    "EBSOptionsTypeDef",
    {
        "EBSEnabled": bool,
        "VolumeType": VolumeTypeType,
        "VolumeSize": int,
        "Iops": int,
        "Throughput": int,
    },
    total=False,
)

EncryptionAtRestOptionsTypeDef = TypedDict(
    "EncryptionAtRestOptionsTypeDef",
    {
        "Enabled": bool,
        "KmsKeyId": str,
    },
    total=False,
)

LogPublishingOptionTypeDef = TypedDict(
    "LogPublishingOptionTypeDef",
    {
        "CloudWatchLogsLogGroupArn": str,
        "Enabled": bool,
    },
    total=False,
)

NodeToNodeEncryptionOptionsTypeDef = TypedDict(
    "NodeToNodeEncryptionOptionsTypeDef",
    {
        "Enabled": bool,
    },
    total=False,
)

SnapshotOptionsTypeDef = TypedDict(
    "SnapshotOptionsTypeDef",
    {
        "AutomatedSnapshotStartHour": int,
    },
    total=False,
)

VPCOptionsTypeDef = TypedDict(
    "VPCOptionsTypeDef",
    {
        "SubnetIds": Sequence[str],
        "SecurityGroupIds": Sequence[str],
    },
    total=False,
)

_RequiredDomainInformationTypeDef = TypedDict(
    "_RequiredDomainInformationTypeDef",
    {
        "DomainName": str,
    },
)
_OptionalDomainInformationTypeDef = TypedDict(
    "_OptionalDomainInformationTypeDef",
    {
        "OwnerId": str,
        "Region": str,
    },
    total=False,
)

class DomainInformationTypeDef(
    _RequiredDomainInformationTypeDef, _OptionalDomainInformationTypeDef
):
    pass

DomainInformationOutputTypeDef = TypedDict(
    "DomainInformationOutputTypeDef",
    {
        "OwnerId": str,
        "DomainName": str,
        "Region": str,
    },
)

OutboundCrossClusterSearchConnectionStatusTypeDef = TypedDict(
    "OutboundCrossClusterSearchConnectionStatusTypeDef",
    {
        "StatusCode": OutboundCrossClusterSearchConnectionStatusCodeType,
        "Message": str,
    },
)

PackageSourceTypeDef = TypedDict(
    "PackageSourceTypeDef",
    {
        "S3BucketName": str,
        "S3Key": str,
    },
    total=False,
)

DeleteElasticsearchDomainRequestRequestTypeDef = TypedDict(
    "DeleteElasticsearchDomainRequestRequestTypeDef",
    {
        "DomainName": str,
    },
)

DeleteInboundCrossClusterSearchConnectionRequestRequestTypeDef = TypedDict(
    "DeleteInboundCrossClusterSearchConnectionRequestRequestTypeDef",
    {
        "CrossClusterSearchConnectionId": str,
    },
)

DeleteOutboundCrossClusterSearchConnectionRequestRequestTypeDef = TypedDict(
    "DeleteOutboundCrossClusterSearchConnectionRequestRequestTypeDef",
    {
        "CrossClusterSearchConnectionId": str,
    },
)

DeletePackageRequestRequestTypeDef = TypedDict(
    "DeletePackageRequestRequestTypeDef",
    {
        "PackageID": str,
    },
)

DeleteVpcEndpointRequestRequestTypeDef = TypedDict(
    "DeleteVpcEndpointRequestRequestTypeDef",
    {
        "VpcEndpointId": str,
    },
)

VpcEndpointSummaryTypeDef = TypedDict(
    "VpcEndpointSummaryTypeDef",
    {
        "VpcEndpointId": str,
        "VpcEndpointOwner": str,
        "DomainArn": str,
        "Status": VpcEndpointStatusType,
    },
)

_RequiredDescribeDomainAutoTunesRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeDomainAutoTunesRequestRequestTypeDef",
    {
        "DomainName": str,
    },
)
_OptionalDescribeDomainAutoTunesRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeDomainAutoTunesRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

class DescribeDomainAutoTunesRequestRequestTypeDef(
    _RequiredDescribeDomainAutoTunesRequestRequestTypeDef,
    _OptionalDescribeDomainAutoTunesRequestRequestTypeDef,
):
    pass

_RequiredDescribeDomainChangeProgressRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeDomainChangeProgressRequestRequestTypeDef",
    {
        "DomainName": str,
    },
)
_OptionalDescribeDomainChangeProgressRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeDomainChangeProgressRequestRequestTypeDef",
    {
        "ChangeId": str,
    },
    total=False,
)

class DescribeDomainChangeProgressRequestRequestTypeDef(
    _RequiredDescribeDomainChangeProgressRequestRequestTypeDef,
    _OptionalDescribeDomainChangeProgressRequestRequestTypeDef,
):
    pass

DescribeElasticsearchDomainConfigRequestRequestTypeDef = TypedDict(
    "DescribeElasticsearchDomainConfigRequestRequestTypeDef",
    {
        "DomainName": str,
    },
)

DescribeElasticsearchDomainRequestRequestTypeDef = TypedDict(
    "DescribeElasticsearchDomainRequestRequestTypeDef",
    {
        "DomainName": str,
    },
)

DescribeElasticsearchDomainsRequestRequestTypeDef = TypedDict(
    "DescribeElasticsearchDomainsRequestRequestTypeDef",
    {
        "DomainNames": Sequence[str],
    },
)

_RequiredDescribeElasticsearchInstanceTypeLimitsRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeElasticsearchInstanceTypeLimitsRequestRequestTypeDef",
    {
        "InstanceType": ESPartitionInstanceTypeType,
        "ElasticsearchVersion": str,
    },
)
_OptionalDescribeElasticsearchInstanceTypeLimitsRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeElasticsearchInstanceTypeLimitsRequestRequestTypeDef",
    {
        "DomainName": str,
    },
    total=False,
)

class DescribeElasticsearchInstanceTypeLimitsRequestRequestTypeDef(
    _RequiredDescribeElasticsearchInstanceTypeLimitsRequestRequestTypeDef,
    _OptionalDescribeElasticsearchInstanceTypeLimitsRequestRequestTypeDef,
):
    pass

FilterTypeDef = TypedDict(
    "FilterTypeDef",
    {
        "Name": str,
        "Values": Sequence[str],
    },
    total=False,
)

DescribePackagesFilterTypeDef = TypedDict(
    "DescribePackagesFilterTypeDef",
    {
        "Name": DescribePackagesFilterNameType,
        "Value": Sequence[str],
    },
    total=False,
)

DescribeReservedElasticsearchInstanceOfferingsRequestDescribeReservedElasticsearchInstanceOfferingsPaginateTypeDef = TypedDict(
    "DescribeReservedElasticsearchInstanceOfferingsRequestDescribeReservedElasticsearchInstanceOfferingsPaginateTypeDef",
    {
        "ReservedElasticsearchInstanceOfferingId": str,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

DescribeReservedElasticsearchInstanceOfferingsRequestRequestTypeDef = TypedDict(
    "DescribeReservedElasticsearchInstanceOfferingsRequestRequestTypeDef",
    {
        "ReservedElasticsearchInstanceOfferingId": str,
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

DescribeReservedElasticsearchInstancesRequestDescribeReservedElasticsearchInstancesPaginateTypeDef = TypedDict(
    "DescribeReservedElasticsearchInstancesRequestDescribeReservedElasticsearchInstancesPaginateTypeDef",
    {
        "ReservedElasticsearchInstanceId": str,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

DescribeReservedElasticsearchInstancesRequestRequestTypeDef = TypedDict(
    "DescribeReservedElasticsearchInstancesRequestRequestTypeDef",
    {
        "ReservedElasticsearchInstanceId": str,
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

DescribeVpcEndpointsRequestRequestTypeDef = TypedDict(
    "DescribeVpcEndpointsRequestRequestTypeDef",
    {
        "VpcEndpointIds": Sequence[str],
    },
)

VpcEndpointErrorTypeDef = TypedDict(
    "VpcEndpointErrorTypeDef",
    {
        "VpcEndpointId": str,
        "ErrorCode": VpcEndpointErrorCodeType,
        "ErrorMessage": str,
    },
)

DissociatePackageRequestRequestTypeDef = TypedDict(
    "DissociatePackageRequestRequestTypeDef",
    {
        "PackageID": str,
        "DomainName": str,
    },
)

DomainEndpointOptionsOutputTypeDef = TypedDict(
    "DomainEndpointOptionsOutputTypeDef",
    {
        "EnforceHTTPS": bool,
        "TLSSecurityPolicy": TLSSecurityPolicyType,
        "CustomEndpointEnabled": bool,
        "CustomEndpoint": str,
        "CustomEndpointCertificateArn": str,
    },
)

DomainInfoTypeDef = TypedDict(
    "DomainInfoTypeDef",
    {
        "DomainName": str,
        "EngineType": EngineTypeType,
    },
)

ErrorDetailsTypeDef = TypedDict(
    "ErrorDetailsTypeDef",
    {
        "ErrorType": str,
        "ErrorMessage": str,
    },
)

DryRunResultsTypeDef = TypedDict(
    "DryRunResultsTypeDef",
    {
        "DeploymentType": str,
        "Message": str,
    },
)

EBSOptionsOutputTypeDef = TypedDict(
    "EBSOptionsOutputTypeDef",
    {
        "EBSEnabled": bool,
        "VolumeType": VolumeTypeType,
        "VolumeSize": int,
        "Iops": int,
        "Throughput": int,
    },
)

ZoneAwarenessConfigOutputTypeDef = TypedDict(
    "ZoneAwarenessConfigOutputTypeDef",
    {
        "AvailabilityZoneCount": int,
    },
)

ZoneAwarenessConfigTypeDef = TypedDict(
    "ZoneAwarenessConfigTypeDef",
    {
        "AvailabilityZoneCount": int,
    },
    total=False,
)

EncryptionAtRestOptionsOutputTypeDef = TypedDict(
    "EncryptionAtRestOptionsOutputTypeDef",
    {
        "Enabled": bool,
        "KmsKeyId": str,
    },
)

LogPublishingOptionOutputTypeDef = TypedDict(
    "LogPublishingOptionOutputTypeDef",
    {
        "CloudWatchLogsLogGroupArn": str,
        "Enabled": bool,
    },
)

NodeToNodeEncryptionOptionsOutputTypeDef = TypedDict(
    "NodeToNodeEncryptionOptionsOutputTypeDef",
    {
        "Enabled": bool,
    },
)

SnapshotOptionsOutputTypeDef = TypedDict(
    "SnapshotOptionsOutputTypeDef",
    {
        "AutomatedSnapshotStartHour": int,
    },
)

VPCDerivedInfoTypeDef = TypedDict(
    "VPCDerivedInfoTypeDef",
    {
        "VPCId": str,
        "SubnetIds": List[str],
        "AvailabilityZones": List[str],
        "SecurityGroupIds": List[str],
    },
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetCompatibleElasticsearchVersionsRequestRequestTypeDef = TypedDict(
    "GetCompatibleElasticsearchVersionsRequestRequestTypeDef",
    {
        "DomainName": str,
    },
    total=False,
)

_RequiredGetPackageVersionHistoryRequestRequestTypeDef = TypedDict(
    "_RequiredGetPackageVersionHistoryRequestRequestTypeDef",
    {
        "PackageID": str,
    },
)
_OptionalGetPackageVersionHistoryRequestRequestTypeDef = TypedDict(
    "_OptionalGetPackageVersionHistoryRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

class GetPackageVersionHistoryRequestRequestTypeDef(
    _RequiredGetPackageVersionHistoryRequestRequestTypeDef,
    _OptionalGetPackageVersionHistoryRequestRequestTypeDef,
):
    pass

PackageVersionHistoryTypeDef = TypedDict(
    "PackageVersionHistoryTypeDef",
    {
        "PackageVersion": str,
        "CommitMessage": str,
        "CreatedAt": datetime,
    },
)

_RequiredGetUpgradeHistoryRequestGetUpgradeHistoryPaginateTypeDef = TypedDict(
    "_RequiredGetUpgradeHistoryRequestGetUpgradeHistoryPaginateTypeDef",
    {
        "DomainName": str,
    },
)
_OptionalGetUpgradeHistoryRequestGetUpgradeHistoryPaginateTypeDef = TypedDict(
    "_OptionalGetUpgradeHistoryRequestGetUpgradeHistoryPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

class GetUpgradeHistoryRequestGetUpgradeHistoryPaginateTypeDef(
    _RequiredGetUpgradeHistoryRequestGetUpgradeHistoryPaginateTypeDef,
    _OptionalGetUpgradeHistoryRequestGetUpgradeHistoryPaginateTypeDef,
):
    pass

_RequiredGetUpgradeHistoryRequestRequestTypeDef = TypedDict(
    "_RequiredGetUpgradeHistoryRequestRequestTypeDef",
    {
        "DomainName": str,
    },
)
_OptionalGetUpgradeHistoryRequestRequestTypeDef = TypedDict(
    "_OptionalGetUpgradeHistoryRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

class GetUpgradeHistoryRequestRequestTypeDef(
    _RequiredGetUpgradeHistoryRequestRequestTypeDef, _OptionalGetUpgradeHistoryRequestRequestTypeDef
):
    pass

GetUpgradeStatusRequestRequestTypeDef = TypedDict(
    "GetUpgradeStatusRequestRequestTypeDef",
    {
        "DomainName": str,
    },
)

GetUpgradeStatusResponseTypeDef = TypedDict(
    "GetUpgradeStatusResponseTypeDef",
    {
        "UpgradeStep": UpgradeStepType,
        "StepStatus": UpgradeStatusType,
        "UpgradeName": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

InboundCrossClusterSearchConnectionStatusTypeDef = TypedDict(
    "InboundCrossClusterSearchConnectionStatusTypeDef",
    {
        "StatusCode": InboundCrossClusterSearchConnectionStatusCodeType,
        "Message": str,
    },
)

InstanceCountLimitsTypeDef = TypedDict(
    "InstanceCountLimitsTypeDef",
    {
        "MinimumInstanceCount": int,
        "MaximumInstanceCount": int,
    },
)

ListDomainNamesRequestRequestTypeDef = TypedDict(
    "ListDomainNamesRequestRequestTypeDef",
    {
        "EngineType": EngineTypeType,
    },
    total=False,
)

_RequiredListDomainsForPackageRequestRequestTypeDef = TypedDict(
    "_RequiredListDomainsForPackageRequestRequestTypeDef",
    {
        "PackageID": str,
    },
)
_OptionalListDomainsForPackageRequestRequestTypeDef = TypedDict(
    "_OptionalListDomainsForPackageRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

class ListDomainsForPackageRequestRequestTypeDef(
    _RequiredListDomainsForPackageRequestRequestTypeDef,
    _OptionalListDomainsForPackageRequestRequestTypeDef,
):
    pass

_RequiredListElasticsearchInstanceTypesRequestListElasticsearchInstanceTypesPaginateTypeDef = TypedDict(
    "_RequiredListElasticsearchInstanceTypesRequestListElasticsearchInstanceTypesPaginateTypeDef",
    {
        "ElasticsearchVersion": str,
    },
)
_OptionalListElasticsearchInstanceTypesRequestListElasticsearchInstanceTypesPaginateTypeDef = TypedDict(
    "_OptionalListElasticsearchInstanceTypesRequestListElasticsearchInstanceTypesPaginateTypeDef",
    {
        "DomainName": str,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

class ListElasticsearchInstanceTypesRequestListElasticsearchInstanceTypesPaginateTypeDef(
    _RequiredListElasticsearchInstanceTypesRequestListElasticsearchInstanceTypesPaginateTypeDef,
    _OptionalListElasticsearchInstanceTypesRequestListElasticsearchInstanceTypesPaginateTypeDef,
):
    pass

_RequiredListElasticsearchInstanceTypesRequestRequestTypeDef = TypedDict(
    "_RequiredListElasticsearchInstanceTypesRequestRequestTypeDef",
    {
        "ElasticsearchVersion": str,
    },
)
_OptionalListElasticsearchInstanceTypesRequestRequestTypeDef = TypedDict(
    "_OptionalListElasticsearchInstanceTypesRequestRequestTypeDef",
    {
        "DomainName": str,
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

class ListElasticsearchInstanceTypesRequestRequestTypeDef(
    _RequiredListElasticsearchInstanceTypesRequestRequestTypeDef,
    _OptionalListElasticsearchInstanceTypesRequestRequestTypeDef,
):
    pass

ListElasticsearchInstanceTypesResponseTypeDef = TypedDict(
    "ListElasticsearchInstanceTypesResponseTypeDef",
    {
        "ElasticsearchInstanceTypes": List[ESPartitionInstanceTypeType],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListElasticsearchVersionsRequestListElasticsearchVersionsPaginateTypeDef = TypedDict(
    "ListElasticsearchVersionsRequestListElasticsearchVersionsPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListElasticsearchVersionsRequestRequestTypeDef = TypedDict(
    "ListElasticsearchVersionsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

ListElasticsearchVersionsResponseTypeDef = TypedDict(
    "ListElasticsearchVersionsResponseTypeDef",
    {
        "ElasticsearchVersions": List[str],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredListPackagesForDomainRequestRequestTypeDef = TypedDict(
    "_RequiredListPackagesForDomainRequestRequestTypeDef",
    {
        "DomainName": str,
    },
)
_OptionalListPackagesForDomainRequestRequestTypeDef = TypedDict(
    "_OptionalListPackagesForDomainRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

class ListPackagesForDomainRequestRequestTypeDef(
    _RequiredListPackagesForDomainRequestRequestTypeDef,
    _OptionalListPackagesForDomainRequestRequestTypeDef,
):
    pass

ListTagsRequestRequestTypeDef = TypedDict(
    "ListTagsRequestRequestTypeDef",
    {
        "ARN": str,
    },
)

TagOutputTypeDef = TypedDict(
    "TagOutputTypeDef",
    {
        "Key": str,
        "Value": str,
    },
)

_RequiredListVpcEndpointAccessRequestRequestTypeDef = TypedDict(
    "_RequiredListVpcEndpointAccessRequestRequestTypeDef",
    {
        "DomainName": str,
    },
)
_OptionalListVpcEndpointAccessRequestRequestTypeDef = TypedDict(
    "_OptionalListVpcEndpointAccessRequestRequestTypeDef",
    {
        "NextToken": str,
    },
    total=False,
)

class ListVpcEndpointAccessRequestRequestTypeDef(
    _RequiredListVpcEndpointAccessRequestRequestTypeDef,
    _OptionalListVpcEndpointAccessRequestRequestTypeDef,
):
    pass

_RequiredListVpcEndpointsForDomainRequestRequestTypeDef = TypedDict(
    "_RequiredListVpcEndpointsForDomainRequestRequestTypeDef",
    {
        "DomainName": str,
    },
)
_OptionalListVpcEndpointsForDomainRequestRequestTypeDef = TypedDict(
    "_OptionalListVpcEndpointsForDomainRequestRequestTypeDef",
    {
        "NextToken": str,
    },
    total=False,
)

class ListVpcEndpointsForDomainRequestRequestTypeDef(
    _RequiredListVpcEndpointsForDomainRequestRequestTypeDef,
    _OptionalListVpcEndpointsForDomainRequestRequestTypeDef,
):
    pass

ListVpcEndpointsRequestRequestTypeDef = TypedDict(
    "ListVpcEndpointsRequestRequestTypeDef",
    {
        "NextToken": str,
    },
    total=False,
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

_RequiredPurchaseReservedElasticsearchInstanceOfferingRequestRequestTypeDef = TypedDict(
    "_RequiredPurchaseReservedElasticsearchInstanceOfferingRequestRequestTypeDef",
    {
        "ReservedElasticsearchInstanceOfferingId": str,
        "ReservationName": str,
    },
)
_OptionalPurchaseReservedElasticsearchInstanceOfferingRequestRequestTypeDef = TypedDict(
    "_OptionalPurchaseReservedElasticsearchInstanceOfferingRequestRequestTypeDef",
    {
        "InstanceCount": int,
    },
    total=False,
)

class PurchaseReservedElasticsearchInstanceOfferingRequestRequestTypeDef(
    _RequiredPurchaseReservedElasticsearchInstanceOfferingRequestRequestTypeDef,
    _OptionalPurchaseReservedElasticsearchInstanceOfferingRequestRequestTypeDef,
):
    pass

PurchaseReservedElasticsearchInstanceOfferingResponseTypeDef = TypedDict(
    "PurchaseReservedElasticsearchInstanceOfferingResponseTypeDef",
    {
        "ReservedElasticsearchInstanceId": str,
        "ReservationName": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

RecurringChargeTypeDef = TypedDict(
    "RecurringChargeTypeDef",
    {
        "RecurringChargeAmount": float,
        "RecurringChargeFrequency": str,
    },
)

RejectInboundCrossClusterSearchConnectionRequestRequestTypeDef = TypedDict(
    "RejectInboundCrossClusterSearchConnectionRequestRequestTypeDef",
    {
        "CrossClusterSearchConnectionId": str,
    },
)

RemoveTagsRequestRequestTypeDef = TypedDict(
    "RemoveTagsRequestRequestTypeDef",
    {
        "ARN": str,
        "TagKeys": Sequence[str],
    },
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

RevokeVpcEndpointAccessRequestRequestTypeDef = TypedDict(
    "RevokeVpcEndpointAccessRequestRequestTypeDef",
    {
        "DomainName": str,
        "Account": str,
    },
)

SAMLIdpOutputTypeDef = TypedDict(
    "SAMLIdpOutputTypeDef",
    {
        "MetadataContent": str,
        "EntityId": str,
    },
)

SAMLIdpTypeDef = TypedDict(
    "SAMLIdpTypeDef",
    {
        "MetadataContent": str,
        "EntityId": str,
    },
)

StartElasticsearchServiceSoftwareUpdateRequestRequestTypeDef = TypedDict(
    "StartElasticsearchServiceSoftwareUpdateRequestRequestTypeDef",
    {
        "DomainName": str,
    },
)

StorageTypeLimitTypeDef = TypedDict(
    "StorageTypeLimitTypeDef",
    {
        "LimitName": str,
        "LimitValues": List[str],
    },
)

_RequiredUpgradeElasticsearchDomainRequestRequestTypeDef = TypedDict(
    "_RequiredUpgradeElasticsearchDomainRequestRequestTypeDef",
    {
        "DomainName": str,
        "TargetVersion": str,
    },
)
_OptionalUpgradeElasticsearchDomainRequestRequestTypeDef = TypedDict(
    "_OptionalUpgradeElasticsearchDomainRequestRequestTypeDef",
    {
        "PerformCheckOnly": bool,
    },
    total=False,
)

class UpgradeElasticsearchDomainRequestRequestTypeDef(
    _RequiredUpgradeElasticsearchDomainRequestRequestTypeDef,
    _OptionalUpgradeElasticsearchDomainRequestRequestTypeDef,
):
    pass

UpgradeStepItemTypeDef = TypedDict(
    "UpgradeStepItemTypeDef",
    {
        "UpgradeStep": UpgradeStepType,
        "UpgradeStepStatus": UpgradeStatusType,
        "Issues": List[str],
        "ProgressPercent": float,
    },
)

AccessPoliciesStatusTypeDef = TypedDict(
    "AccessPoliciesStatusTypeDef",
    {
        "Options": str,
        "Status": OptionStatusTypeDef,
    },
)

AdvancedOptionsStatusTypeDef = TypedDict(
    "AdvancedOptionsStatusTypeDef",
    {
        "Options": Dict[str, str],
        "Status": OptionStatusTypeDef,
    },
)

ElasticsearchVersionStatusTypeDef = TypedDict(
    "ElasticsearchVersionStatusTypeDef",
    {
        "Options": str,
        "Status": OptionStatusTypeDef,
    },
)

AddTagsRequestRequestTypeDef = TypedDict(
    "AddTagsRequestRequestTypeDef",
    {
        "ARN": str,
        "TagList": Sequence[TagTypeDef],
    },
)

AuthorizeVpcEndpointAccessResponseTypeDef = TypedDict(
    "AuthorizeVpcEndpointAccessResponseTypeDef",
    {
        "AuthorizedPrincipal": AuthorizedPrincipalTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListVpcEndpointAccessResponseTypeDef = TypedDict(
    "ListVpcEndpointAccessResponseTypeDef",
    {
        "AuthorizedPrincipalList": List[AuthorizedPrincipalTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

AutoTuneDetailsTypeDef = TypedDict(
    "AutoTuneDetailsTypeDef",
    {
        "ScheduledAutoTuneDetails": ScheduledAutoTuneDetailsTypeDef,
    },
)

AutoTuneMaintenanceScheduleOutputTypeDef = TypedDict(
    "AutoTuneMaintenanceScheduleOutputTypeDef",
    {
        "StartAt": datetime,
        "Duration": DurationOutputTypeDef,
        "CronExpressionForRecurrence": str,
    },
)

AutoTuneMaintenanceScheduleTypeDef = TypedDict(
    "AutoTuneMaintenanceScheduleTypeDef",
    {
        "StartAt": Union[datetime, str],
        "Duration": DurationTypeDef,
        "CronExpressionForRecurrence": str,
    },
    total=False,
)

CancelElasticsearchServiceSoftwareUpdateResponseTypeDef = TypedDict(
    "CancelElasticsearchServiceSoftwareUpdateResponseTypeDef",
    {
        "ServiceSoftwareOptions": ServiceSoftwareOptionsTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

StartElasticsearchServiceSoftwareUpdateResponseTypeDef = TypedDict(
    "StartElasticsearchServiceSoftwareUpdateResponseTypeDef",
    {
        "ServiceSoftwareOptions": ServiceSoftwareOptionsTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpgradeElasticsearchDomainResponseTypeDef = TypedDict(
    "UpgradeElasticsearchDomainResponseTypeDef",
    {
        "DomainName": str,
        "TargetVersion": str,
        "PerformCheckOnly": bool,
        "ChangeProgressDetails": ChangeProgressDetailsTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ChangeProgressStatusDetailsTypeDef = TypedDict(
    "ChangeProgressStatusDetailsTypeDef",
    {
        "ChangeId": str,
        "StartTime": datetime,
        "Status": OverallChangeStatusType,
        "PendingProperties": List[str],
        "CompletedProperties": List[str],
        "TotalNumberOfStages": int,
        "ChangeProgressStages": List[ChangeProgressStageTypeDef],
    },
)

CognitoOptionsStatusTypeDef = TypedDict(
    "CognitoOptionsStatusTypeDef",
    {
        "Options": CognitoOptionsOutputTypeDef,
        "Status": OptionStatusTypeDef,
    },
)

GetCompatibleElasticsearchVersionsResponseTypeDef = TypedDict(
    "GetCompatibleElasticsearchVersionsResponseTypeDef",
    {
        "CompatibleElasticsearchVersions": List[CompatibleVersionsMapTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreateVpcEndpointRequestRequestTypeDef = TypedDict(
    "_RequiredCreateVpcEndpointRequestRequestTypeDef",
    {
        "DomainArn": str,
        "VpcOptions": VPCOptionsTypeDef,
    },
)
_OptionalCreateVpcEndpointRequestRequestTypeDef = TypedDict(
    "_OptionalCreateVpcEndpointRequestRequestTypeDef",
    {
        "ClientToken": str,
    },
    total=False,
)

class CreateVpcEndpointRequestRequestTypeDef(
    _RequiredCreateVpcEndpointRequestRequestTypeDef, _OptionalCreateVpcEndpointRequestRequestTypeDef
):
    pass

UpdateVpcEndpointRequestRequestTypeDef = TypedDict(
    "UpdateVpcEndpointRequestRequestTypeDef",
    {
        "VpcEndpointId": str,
        "VpcOptions": VPCOptionsTypeDef,
    },
)

CreateOutboundCrossClusterSearchConnectionRequestRequestTypeDef = TypedDict(
    "CreateOutboundCrossClusterSearchConnectionRequestRequestTypeDef",
    {
        "SourceDomainInfo": DomainInformationTypeDef,
        "DestinationDomainInfo": DomainInformationTypeDef,
        "ConnectionAlias": str,
    },
)

CreateOutboundCrossClusterSearchConnectionResponseTypeDef = TypedDict(
    "CreateOutboundCrossClusterSearchConnectionResponseTypeDef",
    {
        "SourceDomainInfo": DomainInformationOutputTypeDef,
        "DestinationDomainInfo": DomainInformationOutputTypeDef,
        "ConnectionAlias": str,
        "ConnectionStatus": OutboundCrossClusterSearchConnectionStatusTypeDef,
        "CrossClusterSearchConnectionId": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

OutboundCrossClusterSearchConnectionTypeDef = TypedDict(
    "OutboundCrossClusterSearchConnectionTypeDef",
    {
        "SourceDomainInfo": DomainInformationOutputTypeDef,
        "DestinationDomainInfo": DomainInformationOutputTypeDef,
        "CrossClusterSearchConnectionId": str,
        "ConnectionAlias": str,
        "ConnectionStatus": OutboundCrossClusterSearchConnectionStatusTypeDef,
    },
)

_RequiredCreatePackageRequestRequestTypeDef = TypedDict(
    "_RequiredCreatePackageRequestRequestTypeDef",
    {
        "PackageName": str,
        "PackageType": Literal["TXT-DICTIONARY"],
        "PackageSource": PackageSourceTypeDef,
    },
)
_OptionalCreatePackageRequestRequestTypeDef = TypedDict(
    "_OptionalCreatePackageRequestRequestTypeDef",
    {
        "PackageDescription": str,
    },
    total=False,
)

class CreatePackageRequestRequestTypeDef(
    _RequiredCreatePackageRequestRequestTypeDef, _OptionalCreatePackageRequestRequestTypeDef
):
    pass

_RequiredUpdatePackageRequestRequestTypeDef = TypedDict(
    "_RequiredUpdatePackageRequestRequestTypeDef",
    {
        "PackageID": str,
        "PackageSource": PackageSourceTypeDef,
    },
)
_OptionalUpdatePackageRequestRequestTypeDef = TypedDict(
    "_OptionalUpdatePackageRequestRequestTypeDef",
    {
        "PackageDescription": str,
        "CommitMessage": str,
    },
    total=False,
)

class UpdatePackageRequestRequestTypeDef(
    _RequiredUpdatePackageRequestRequestTypeDef, _OptionalUpdatePackageRequestRequestTypeDef
):
    pass

DeleteVpcEndpointResponseTypeDef = TypedDict(
    "DeleteVpcEndpointResponseTypeDef",
    {
        "VpcEndpointSummary": VpcEndpointSummaryTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListVpcEndpointsForDomainResponseTypeDef = TypedDict(
    "ListVpcEndpointsForDomainResponseTypeDef",
    {
        "VpcEndpointSummaryList": List[VpcEndpointSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListVpcEndpointsResponseTypeDef = TypedDict(
    "ListVpcEndpointsResponseTypeDef",
    {
        "VpcEndpointSummaryList": List[VpcEndpointSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeInboundCrossClusterSearchConnectionsRequestRequestTypeDef = TypedDict(
    "DescribeInboundCrossClusterSearchConnectionsRequestRequestTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

DescribeOutboundCrossClusterSearchConnectionsRequestRequestTypeDef = TypedDict(
    "DescribeOutboundCrossClusterSearchConnectionsRequestRequestTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

DescribePackagesRequestRequestTypeDef = TypedDict(
    "DescribePackagesRequestRequestTypeDef",
    {
        "Filters": Sequence[DescribePackagesFilterTypeDef],
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

DomainEndpointOptionsStatusTypeDef = TypedDict(
    "DomainEndpointOptionsStatusTypeDef",
    {
        "Options": DomainEndpointOptionsOutputTypeDef,
        "Status": OptionStatusTypeDef,
    },
)

ListDomainNamesResponseTypeDef = TypedDict(
    "ListDomainNamesResponseTypeDef",
    {
        "DomainNames": List[DomainInfoTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DomainPackageDetailsTypeDef = TypedDict(
    "DomainPackageDetailsTypeDef",
    {
        "PackageID": str,
        "PackageName": str,
        "PackageType": Literal["TXT-DICTIONARY"],
        "LastUpdated": datetime,
        "DomainName": str,
        "DomainPackageStatus": DomainPackageStatusType,
        "PackageVersion": str,
        "ReferencePath": str,
        "ErrorDetails": ErrorDetailsTypeDef,
    },
)

PackageDetailsTypeDef = TypedDict(
    "PackageDetailsTypeDef",
    {
        "PackageID": str,
        "PackageName": str,
        "PackageType": Literal["TXT-DICTIONARY"],
        "PackageDescription": str,
        "PackageStatus": PackageStatusType,
        "CreatedAt": datetime,
        "LastUpdatedAt": datetime,
        "AvailablePackageVersion": str,
        "ErrorDetails": ErrorDetailsTypeDef,
    },
)

EBSOptionsStatusTypeDef = TypedDict(
    "EBSOptionsStatusTypeDef",
    {
        "Options": EBSOptionsOutputTypeDef,
        "Status": OptionStatusTypeDef,
    },
)

ElasticsearchClusterConfigOutputTypeDef = TypedDict(
    "ElasticsearchClusterConfigOutputTypeDef",
    {
        "InstanceType": ESPartitionInstanceTypeType,
        "InstanceCount": int,
        "DedicatedMasterEnabled": bool,
        "ZoneAwarenessEnabled": bool,
        "ZoneAwarenessConfig": ZoneAwarenessConfigOutputTypeDef,
        "DedicatedMasterType": ESPartitionInstanceTypeType,
        "DedicatedMasterCount": int,
        "WarmEnabled": bool,
        "WarmType": ESWarmPartitionInstanceTypeType,
        "WarmCount": int,
        "ColdStorageOptions": ColdStorageOptionsOutputTypeDef,
    },
)

ElasticsearchClusterConfigTypeDef = TypedDict(
    "ElasticsearchClusterConfigTypeDef",
    {
        "InstanceType": ESPartitionInstanceTypeType,
        "InstanceCount": int,
        "DedicatedMasterEnabled": bool,
        "ZoneAwarenessEnabled": bool,
        "ZoneAwarenessConfig": ZoneAwarenessConfigTypeDef,
        "DedicatedMasterType": ESPartitionInstanceTypeType,
        "DedicatedMasterCount": int,
        "WarmEnabled": bool,
        "WarmType": ESWarmPartitionInstanceTypeType,
        "WarmCount": int,
        "ColdStorageOptions": ColdStorageOptionsTypeDef,
    },
    total=False,
)

EncryptionAtRestOptionsStatusTypeDef = TypedDict(
    "EncryptionAtRestOptionsStatusTypeDef",
    {
        "Options": EncryptionAtRestOptionsOutputTypeDef,
        "Status": OptionStatusTypeDef,
    },
)

LogPublishingOptionsStatusTypeDef = TypedDict(
    "LogPublishingOptionsStatusTypeDef",
    {
        "Options": Dict[LogTypeType, LogPublishingOptionOutputTypeDef],
        "Status": OptionStatusTypeDef,
    },
)

NodeToNodeEncryptionOptionsStatusTypeDef = TypedDict(
    "NodeToNodeEncryptionOptionsStatusTypeDef",
    {
        "Options": NodeToNodeEncryptionOptionsOutputTypeDef,
        "Status": OptionStatusTypeDef,
    },
)

SnapshotOptionsStatusTypeDef = TypedDict(
    "SnapshotOptionsStatusTypeDef",
    {
        "Options": SnapshotOptionsOutputTypeDef,
        "Status": OptionStatusTypeDef,
    },
)

VPCDerivedInfoStatusTypeDef = TypedDict(
    "VPCDerivedInfoStatusTypeDef",
    {
        "Options": VPCDerivedInfoTypeDef,
        "Status": OptionStatusTypeDef,
    },
)

VpcEndpointTypeDef = TypedDict(
    "VpcEndpointTypeDef",
    {
        "VpcEndpointId": str,
        "VpcEndpointOwner": str,
        "DomainArn": str,
        "VpcOptions": VPCDerivedInfoTypeDef,
        "Status": VpcEndpointStatusType,
        "Endpoint": str,
    },
)

GetPackageVersionHistoryResponseTypeDef = TypedDict(
    "GetPackageVersionHistoryResponseTypeDef",
    {
        "PackageID": str,
        "PackageVersionHistoryList": List[PackageVersionHistoryTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

InboundCrossClusterSearchConnectionTypeDef = TypedDict(
    "InboundCrossClusterSearchConnectionTypeDef",
    {
        "SourceDomainInfo": DomainInformationOutputTypeDef,
        "DestinationDomainInfo": DomainInformationOutputTypeDef,
        "CrossClusterSearchConnectionId": str,
        "ConnectionStatus": InboundCrossClusterSearchConnectionStatusTypeDef,
    },
)

InstanceLimitsTypeDef = TypedDict(
    "InstanceLimitsTypeDef",
    {
        "InstanceCountLimits": InstanceCountLimitsTypeDef,
    },
)

ListTagsResponseTypeDef = TypedDict(
    "ListTagsResponseTypeDef",
    {
        "TagList": List[TagOutputTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ReservedElasticsearchInstanceOfferingTypeDef = TypedDict(
    "ReservedElasticsearchInstanceOfferingTypeDef",
    {
        "ReservedElasticsearchInstanceOfferingId": str,
        "ElasticsearchInstanceType": ESPartitionInstanceTypeType,
        "Duration": int,
        "FixedPrice": float,
        "UsagePrice": float,
        "CurrencyCode": str,
        "PaymentOption": ReservedElasticsearchInstancePaymentOptionType,
        "RecurringCharges": List[RecurringChargeTypeDef],
    },
)

ReservedElasticsearchInstanceTypeDef = TypedDict(
    "ReservedElasticsearchInstanceTypeDef",
    {
        "ReservationName": str,
        "ReservedElasticsearchInstanceId": str,
        "ReservedElasticsearchInstanceOfferingId": str,
        "ElasticsearchInstanceType": ESPartitionInstanceTypeType,
        "StartTime": datetime,
        "Duration": int,
        "FixedPrice": float,
        "UsagePrice": float,
        "CurrencyCode": str,
        "ElasticsearchInstanceCount": int,
        "State": str,
        "PaymentOption": ReservedElasticsearchInstancePaymentOptionType,
        "RecurringCharges": List[RecurringChargeTypeDef],
    },
)

SAMLOptionsOutputTypeDef = TypedDict(
    "SAMLOptionsOutputTypeDef",
    {
        "Enabled": bool,
        "Idp": SAMLIdpOutputTypeDef,
        "SubjectKey": str,
        "RolesKey": str,
        "SessionTimeoutMinutes": int,
    },
)

SAMLOptionsInputTypeDef = TypedDict(
    "SAMLOptionsInputTypeDef",
    {
        "Enabled": bool,
        "Idp": SAMLIdpTypeDef,
        "MasterUserName": str,
        "MasterBackendRole": str,
        "SubjectKey": str,
        "RolesKey": str,
        "SessionTimeoutMinutes": int,
    },
    total=False,
)

StorageTypeTypeDef = TypedDict(
    "StorageTypeTypeDef",
    {
        "StorageTypeName": str,
        "StorageSubTypeName": str,
        "StorageTypeLimits": List[StorageTypeLimitTypeDef],
    },
)

UpgradeHistoryTypeDef = TypedDict(
    "UpgradeHistoryTypeDef",
    {
        "UpgradeName": str,
        "StartTimestamp": datetime,
        "UpgradeStatus": UpgradeStatusType,
        "StepsList": List[UpgradeStepItemTypeDef],
    },
)

AutoTuneTypeDef = TypedDict(
    "AutoTuneTypeDef",
    {
        "AutoTuneType": Literal["SCHEDULED_ACTION"],
        "AutoTuneDetails": AutoTuneDetailsTypeDef,
    },
)

AutoTuneOptionsExtraOutputTypeDef = TypedDict(
    "AutoTuneOptionsExtraOutputTypeDef",
    {
        "DesiredState": AutoTuneDesiredStateType,
        "RollbackOnDisable": RollbackOnDisableType,
        "MaintenanceSchedules": List[AutoTuneMaintenanceScheduleOutputTypeDef],
    },
)

AutoTuneOptionsInputTypeDef = TypedDict(
    "AutoTuneOptionsInputTypeDef",
    {
        "DesiredState": AutoTuneDesiredStateType,
        "MaintenanceSchedules": Sequence[AutoTuneMaintenanceScheduleTypeDef],
    },
    total=False,
)

AutoTuneOptionsTypeDef = TypedDict(
    "AutoTuneOptionsTypeDef",
    {
        "DesiredState": AutoTuneDesiredStateType,
        "RollbackOnDisable": RollbackOnDisableType,
        "MaintenanceSchedules": Sequence[AutoTuneMaintenanceScheduleTypeDef],
    },
    total=False,
)

DescribeDomainChangeProgressResponseTypeDef = TypedDict(
    "DescribeDomainChangeProgressResponseTypeDef",
    {
        "ChangeProgressStatus": ChangeProgressStatusDetailsTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeleteOutboundCrossClusterSearchConnectionResponseTypeDef = TypedDict(
    "DeleteOutboundCrossClusterSearchConnectionResponseTypeDef",
    {
        "CrossClusterSearchConnection": OutboundCrossClusterSearchConnectionTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeOutboundCrossClusterSearchConnectionsResponseTypeDef = TypedDict(
    "DescribeOutboundCrossClusterSearchConnectionsResponseTypeDef",
    {
        "CrossClusterSearchConnections": List[OutboundCrossClusterSearchConnectionTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

AssociatePackageResponseTypeDef = TypedDict(
    "AssociatePackageResponseTypeDef",
    {
        "DomainPackageDetails": DomainPackageDetailsTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DissociatePackageResponseTypeDef = TypedDict(
    "DissociatePackageResponseTypeDef",
    {
        "DomainPackageDetails": DomainPackageDetailsTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListDomainsForPackageResponseTypeDef = TypedDict(
    "ListDomainsForPackageResponseTypeDef",
    {
        "DomainPackageDetailsList": List[DomainPackageDetailsTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListPackagesForDomainResponseTypeDef = TypedDict(
    "ListPackagesForDomainResponseTypeDef",
    {
        "DomainPackageDetailsList": List[DomainPackageDetailsTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreatePackageResponseTypeDef = TypedDict(
    "CreatePackageResponseTypeDef",
    {
        "PackageDetails": PackageDetailsTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeletePackageResponseTypeDef = TypedDict(
    "DeletePackageResponseTypeDef",
    {
        "PackageDetails": PackageDetailsTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribePackagesResponseTypeDef = TypedDict(
    "DescribePackagesResponseTypeDef",
    {
        "PackageDetailsList": List[PackageDetailsTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdatePackageResponseTypeDef = TypedDict(
    "UpdatePackageResponseTypeDef",
    {
        "PackageDetails": PackageDetailsTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ElasticsearchClusterConfigStatusTypeDef = TypedDict(
    "ElasticsearchClusterConfigStatusTypeDef",
    {
        "Options": ElasticsearchClusterConfigOutputTypeDef,
        "Status": OptionStatusTypeDef,
    },
)

CreateVpcEndpointResponseTypeDef = TypedDict(
    "CreateVpcEndpointResponseTypeDef",
    {
        "VpcEndpoint": VpcEndpointTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeVpcEndpointsResponseTypeDef = TypedDict(
    "DescribeVpcEndpointsResponseTypeDef",
    {
        "VpcEndpoints": List[VpcEndpointTypeDef],
        "VpcEndpointErrors": List[VpcEndpointErrorTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateVpcEndpointResponseTypeDef = TypedDict(
    "UpdateVpcEndpointResponseTypeDef",
    {
        "VpcEndpoint": VpcEndpointTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

AcceptInboundCrossClusterSearchConnectionResponseTypeDef = TypedDict(
    "AcceptInboundCrossClusterSearchConnectionResponseTypeDef",
    {
        "CrossClusterSearchConnection": InboundCrossClusterSearchConnectionTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeleteInboundCrossClusterSearchConnectionResponseTypeDef = TypedDict(
    "DeleteInboundCrossClusterSearchConnectionResponseTypeDef",
    {
        "CrossClusterSearchConnection": InboundCrossClusterSearchConnectionTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeInboundCrossClusterSearchConnectionsResponseTypeDef = TypedDict(
    "DescribeInboundCrossClusterSearchConnectionsResponseTypeDef",
    {
        "CrossClusterSearchConnections": List[InboundCrossClusterSearchConnectionTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

RejectInboundCrossClusterSearchConnectionResponseTypeDef = TypedDict(
    "RejectInboundCrossClusterSearchConnectionResponseTypeDef",
    {
        "CrossClusterSearchConnection": InboundCrossClusterSearchConnectionTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeReservedElasticsearchInstanceOfferingsResponseTypeDef = TypedDict(
    "DescribeReservedElasticsearchInstanceOfferingsResponseTypeDef",
    {
        "NextToken": str,
        "ReservedElasticsearchInstanceOfferings": List[
            ReservedElasticsearchInstanceOfferingTypeDef
        ],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeReservedElasticsearchInstancesResponseTypeDef = TypedDict(
    "DescribeReservedElasticsearchInstancesResponseTypeDef",
    {
        "NextToken": str,
        "ReservedElasticsearchInstances": List[ReservedElasticsearchInstanceTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

AdvancedSecurityOptionsTypeDef = TypedDict(
    "AdvancedSecurityOptionsTypeDef",
    {
        "Enabled": bool,
        "InternalUserDatabaseEnabled": bool,
        "SAMLOptions": SAMLOptionsOutputTypeDef,
        "AnonymousAuthDisableDate": datetime,
        "AnonymousAuthEnabled": bool,
    },
)

AdvancedSecurityOptionsInputTypeDef = TypedDict(
    "AdvancedSecurityOptionsInputTypeDef",
    {
        "Enabled": bool,
        "InternalUserDatabaseEnabled": bool,
        "MasterUserOptions": MasterUserOptionsTypeDef,
        "SAMLOptions": SAMLOptionsInputTypeDef,
        "AnonymousAuthEnabled": bool,
    },
    total=False,
)

LimitsTypeDef = TypedDict(
    "LimitsTypeDef",
    {
        "StorageTypes": List[StorageTypeTypeDef],
        "InstanceLimits": InstanceLimitsTypeDef,
        "AdditionalLimits": List[AdditionalLimitTypeDef],
    },
)

GetUpgradeHistoryResponseTypeDef = TypedDict(
    "GetUpgradeHistoryResponseTypeDef",
    {
        "UpgradeHistories": List[UpgradeHistoryTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeDomainAutoTunesResponseTypeDef = TypedDict(
    "DescribeDomainAutoTunesResponseTypeDef",
    {
        "AutoTunes": List[AutoTuneTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

AutoTuneOptionsStatusTypeDef = TypedDict(
    "AutoTuneOptionsStatusTypeDef",
    {
        "Options": AutoTuneOptionsExtraOutputTypeDef,
        "Status": AutoTuneStatusTypeDef,
    },
)

AdvancedSecurityOptionsStatusTypeDef = TypedDict(
    "AdvancedSecurityOptionsStatusTypeDef",
    {
        "Options": AdvancedSecurityOptionsTypeDef,
        "Status": OptionStatusTypeDef,
    },
)

ElasticsearchDomainStatusTypeDef = TypedDict(
    "ElasticsearchDomainStatusTypeDef",
    {
        "DomainId": str,
        "DomainName": str,
        "ARN": str,
        "Created": bool,
        "Deleted": bool,
        "Endpoint": str,
        "Endpoints": Dict[str, str],
        "Processing": bool,
        "UpgradeProcessing": bool,
        "ElasticsearchVersion": str,
        "ElasticsearchClusterConfig": ElasticsearchClusterConfigOutputTypeDef,
        "EBSOptions": EBSOptionsOutputTypeDef,
        "AccessPolicies": str,
        "SnapshotOptions": SnapshotOptionsOutputTypeDef,
        "VPCOptions": VPCDerivedInfoTypeDef,
        "CognitoOptions": CognitoOptionsOutputTypeDef,
        "EncryptionAtRestOptions": EncryptionAtRestOptionsOutputTypeDef,
        "NodeToNodeEncryptionOptions": NodeToNodeEncryptionOptionsOutputTypeDef,
        "AdvancedOptions": Dict[str, str],
        "LogPublishingOptions": Dict[LogTypeType, LogPublishingOptionOutputTypeDef],
        "ServiceSoftwareOptions": ServiceSoftwareOptionsTypeDef,
        "DomainEndpointOptions": DomainEndpointOptionsOutputTypeDef,
        "AdvancedSecurityOptions": AdvancedSecurityOptionsTypeDef,
        "AutoTuneOptions": AutoTuneOptionsOutputTypeDef,
        "ChangeProgressDetails": ChangeProgressDetailsTypeDef,
    },
)

_RequiredCreateElasticsearchDomainRequestRequestTypeDef = TypedDict(
    "_RequiredCreateElasticsearchDomainRequestRequestTypeDef",
    {
        "DomainName": str,
    },
)
_OptionalCreateElasticsearchDomainRequestRequestTypeDef = TypedDict(
    "_OptionalCreateElasticsearchDomainRequestRequestTypeDef",
    {
        "ElasticsearchVersion": str,
        "ElasticsearchClusterConfig": ElasticsearchClusterConfigTypeDef,
        "EBSOptions": EBSOptionsTypeDef,
        "AccessPolicies": str,
        "SnapshotOptions": SnapshotOptionsTypeDef,
        "VPCOptions": VPCOptionsTypeDef,
        "CognitoOptions": CognitoOptionsTypeDef,
        "EncryptionAtRestOptions": EncryptionAtRestOptionsTypeDef,
        "NodeToNodeEncryptionOptions": NodeToNodeEncryptionOptionsTypeDef,
        "AdvancedOptions": Mapping[str, str],
        "LogPublishingOptions": Mapping[LogTypeType, LogPublishingOptionTypeDef],
        "DomainEndpointOptions": DomainEndpointOptionsTypeDef,
        "AdvancedSecurityOptions": AdvancedSecurityOptionsInputTypeDef,
        "AutoTuneOptions": AutoTuneOptionsInputTypeDef,
        "TagList": Sequence[TagTypeDef],
    },
    total=False,
)

class CreateElasticsearchDomainRequestRequestTypeDef(
    _RequiredCreateElasticsearchDomainRequestRequestTypeDef,
    _OptionalCreateElasticsearchDomainRequestRequestTypeDef,
):
    pass

_RequiredUpdateElasticsearchDomainConfigRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateElasticsearchDomainConfigRequestRequestTypeDef",
    {
        "DomainName": str,
    },
)
_OptionalUpdateElasticsearchDomainConfigRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateElasticsearchDomainConfigRequestRequestTypeDef",
    {
        "ElasticsearchClusterConfig": ElasticsearchClusterConfigTypeDef,
        "EBSOptions": EBSOptionsTypeDef,
        "SnapshotOptions": SnapshotOptionsTypeDef,
        "VPCOptions": VPCOptionsTypeDef,
        "CognitoOptions": CognitoOptionsTypeDef,
        "AdvancedOptions": Mapping[str, str],
        "AccessPolicies": str,
        "LogPublishingOptions": Mapping[LogTypeType, LogPublishingOptionTypeDef],
        "DomainEndpointOptions": DomainEndpointOptionsTypeDef,
        "AdvancedSecurityOptions": AdvancedSecurityOptionsInputTypeDef,
        "NodeToNodeEncryptionOptions": NodeToNodeEncryptionOptionsTypeDef,
        "EncryptionAtRestOptions": EncryptionAtRestOptionsTypeDef,
        "AutoTuneOptions": AutoTuneOptionsTypeDef,
        "DryRun": bool,
    },
    total=False,
)

class UpdateElasticsearchDomainConfigRequestRequestTypeDef(
    _RequiredUpdateElasticsearchDomainConfigRequestRequestTypeDef,
    _OptionalUpdateElasticsearchDomainConfigRequestRequestTypeDef,
):
    pass

DescribeElasticsearchInstanceTypeLimitsResponseTypeDef = TypedDict(
    "DescribeElasticsearchInstanceTypeLimitsResponseTypeDef",
    {
        "LimitsByRole": Dict[str, LimitsTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ElasticsearchDomainConfigTypeDef = TypedDict(
    "ElasticsearchDomainConfigTypeDef",
    {
        "ElasticsearchVersion": ElasticsearchVersionStatusTypeDef,
        "ElasticsearchClusterConfig": ElasticsearchClusterConfigStatusTypeDef,
        "EBSOptions": EBSOptionsStatusTypeDef,
        "AccessPolicies": AccessPoliciesStatusTypeDef,
        "SnapshotOptions": SnapshotOptionsStatusTypeDef,
        "VPCOptions": VPCDerivedInfoStatusTypeDef,
        "CognitoOptions": CognitoOptionsStatusTypeDef,
        "EncryptionAtRestOptions": EncryptionAtRestOptionsStatusTypeDef,
        "NodeToNodeEncryptionOptions": NodeToNodeEncryptionOptionsStatusTypeDef,
        "AdvancedOptions": AdvancedOptionsStatusTypeDef,
        "LogPublishingOptions": LogPublishingOptionsStatusTypeDef,
        "DomainEndpointOptions": DomainEndpointOptionsStatusTypeDef,
        "AdvancedSecurityOptions": AdvancedSecurityOptionsStatusTypeDef,
        "AutoTuneOptions": AutoTuneOptionsStatusTypeDef,
        "ChangeProgressDetails": ChangeProgressDetailsTypeDef,
    },
)

CreateElasticsearchDomainResponseTypeDef = TypedDict(
    "CreateElasticsearchDomainResponseTypeDef",
    {
        "DomainStatus": ElasticsearchDomainStatusTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeleteElasticsearchDomainResponseTypeDef = TypedDict(
    "DeleteElasticsearchDomainResponseTypeDef",
    {
        "DomainStatus": ElasticsearchDomainStatusTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeElasticsearchDomainResponseTypeDef = TypedDict(
    "DescribeElasticsearchDomainResponseTypeDef",
    {
        "DomainStatus": ElasticsearchDomainStatusTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeElasticsearchDomainsResponseTypeDef = TypedDict(
    "DescribeElasticsearchDomainsResponseTypeDef",
    {
        "DomainStatusList": List[ElasticsearchDomainStatusTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeElasticsearchDomainConfigResponseTypeDef = TypedDict(
    "DescribeElasticsearchDomainConfigResponseTypeDef",
    {
        "DomainConfig": ElasticsearchDomainConfigTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateElasticsearchDomainConfigResponseTypeDef = TypedDict(
    "UpdateElasticsearchDomainConfigResponseTypeDef",
    {
        "DomainConfig": ElasticsearchDomainConfigTypeDef,
        "DryRunResults": DryRunResultsTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

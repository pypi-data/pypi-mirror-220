from google.protobuf import wrappers_pb2 as _wrappers_pb2
from ..config_manage import config_file_pb2 as _config_file_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ConfigSimpleResponse(_message.Message):
    __slots__ = ["code", "info"]
    CODE_FIELD_NUMBER: _ClassVar[int]
    INFO_FIELD_NUMBER: _ClassVar[int]
    code: _wrappers_pb2.UInt32Value
    info: _wrappers_pb2.StringValue
    def __init__(self, code: _Optional[_Union[_wrappers_pb2.UInt32Value, _Mapping]] = ..., info: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ...) -> None: ...

class ConfigResponse(_message.Message):
    __slots__ = ["code", "info", "configFileGroup", "configFile", "configFileRelease", "configFileReleaseHistory", "configFileTemplate"]
    CODE_FIELD_NUMBER: _ClassVar[int]
    INFO_FIELD_NUMBER: _ClassVar[int]
    CONFIGFILEGROUP_FIELD_NUMBER: _ClassVar[int]
    CONFIGFILE_FIELD_NUMBER: _ClassVar[int]
    CONFIGFILERELEASE_FIELD_NUMBER: _ClassVar[int]
    CONFIGFILERELEASEHISTORY_FIELD_NUMBER: _ClassVar[int]
    CONFIGFILETEMPLATE_FIELD_NUMBER: _ClassVar[int]
    code: _wrappers_pb2.UInt32Value
    info: _wrappers_pb2.StringValue
    configFileGroup: _config_file_pb2.ConfigFileGroup
    configFile: _config_file_pb2.ConfigFile
    configFileRelease: _config_file_pb2.ConfigFileRelease
    configFileReleaseHistory: _config_file_pb2.ConfigFileReleaseHistory
    configFileTemplate: _config_file_pb2.ConfigFileTemplate
    def __init__(self, code: _Optional[_Union[_wrappers_pb2.UInt32Value, _Mapping]] = ..., info: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., configFileGroup: _Optional[_Union[_config_file_pb2.ConfigFileGroup, _Mapping]] = ..., configFile: _Optional[_Union[_config_file_pb2.ConfigFile, _Mapping]] = ..., configFileRelease: _Optional[_Union[_config_file_pb2.ConfigFileRelease, _Mapping]] = ..., configFileReleaseHistory: _Optional[_Union[_config_file_pb2.ConfigFileReleaseHistory, _Mapping]] = ..., configFileTemplate: _Optional[_Union[_config_file_pb2.ConfigFileTemplate, _Mapping]] = ...) -> None: ...

class ConfigBatchWriteResponse(_message.Message):
    __slots__ = ["code", "info", "total", "responses"]
    CODE_FIELD_NUMBER: _ClassVar[int]
    INFO_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    RESPONSES_FIELD_NUMBER: _ClassVar[int]
    code: _wrappers_pb2.UInt32Value
    info: _wrappers_pb2.StringValue
    total: _wrappers_pb2.UInt32Value
    responses: _containers.RepeatedCompositeFieldContainer[ConfigResponse]
    def __init__(self, code: _Optional[_Union[_wrappers_pb2.UInt32Value, _Mapping]] = ..., info: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., total: _Optional[_Union[_wrappers_pb2.UInt32Value, _Mapping]] = ..., responses: _Optional[_Iterable[_Union[ConfigResponse, _Mapping]]] = ...) -> None: ...

class ConfigBatchQueryResponse(_message.Message):
    __slots__ = ["code", "info", "total", "configFileGroups", "configFiles", "configFileReleases", "configFileReleaseHistories", "configFileTemplates"]
    CODE_FIELD_NUMBER: _ClassVar[int]
    INFO_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    CONFIGFILEGROUPS_FIELD_NUMBER: _ClassVar[int]
    CONFIGFILES_FIELD_NUMBER: _ClassVar[int]
    CONFIGFILERELEASES_FIELD_NUMBER: _ClassVar[int]
    CONFIGFILERELEASEHISTORIES_FIELD_NUMBER: _ClassVar[int]
    CONFIGFILETEMPLATES_FIELD_NUMBER: _ClassVar[int]
    code: _wrappers_pb2.UInt32Value
    info: _wrappers_pb2.StringValue
    total: _wrappers_pb2.UInt32Value
    configFileGroups: _containers.RepeatedCompositeFieldContainer[_config_file_pb2.ConfigFileGroup]
    configFiles: _containers.RepeatedCompositeFieldContainer[_config_file_pb2.ConfigFile]
    configFileReleases: _containers.RepeatedCompositeFieldContainer[_config_file_pb2.ConfigFileRelease]
    configFileReleaseHistories: _containers.RepeatedCompositeFieldContainer[_config_file_pb2.ConfigFileReleaseHistory]
    configFileTemplates: _containers.RepeatedCompositeFieldContainer[_config_file_pb2.ConfigFileTemplate]
    def __init__(self, code: _Optional[_Union[_wrappers_pb2.UInt32Value, _Mapping]] = ..., info: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., total: _Optional[_Union[_wrappers_pb2.UInt32Value, _Mapping]] = ..., configFileGroups: _Optional[_Iterable[_Union[_config_file_pb2.ConfigFileGroup, _Mapping]]] = ..., configFiles: _Optional[_Iterable[_Union[_config_file_pb2.ConfigFile, _Mapping]]] = ..., configFileReleases: _Optional[_Iterable[_Union[_config_file_pb2.ConfigFileRelease, _Mapping]]] = ..., configFileReleaseHistories: _Optional[_Iterable[_Union[_config_file_pb2.ConfigFileReleaseHistory, _Mapping]]] = ..., configFileTemplates: _Optional[_Iterable[_Union[_config_file_pb2.ConfigFileTemplate, _Mapping]]] = ...) -> None: ...

class ConfigClientResponse(_message.Message):
    __slots__ = ["code", "info", "configFile"]
    CODE_FIELD_NUMBER: _ClassVar[int]
    INFO_FIELD_NUMBER: _ClassVar[int]
    CONFIGFILE_FIELD_NUMBER: _ClassVar[int]
    code: _wrappers_pb2.UInt32Value
    info: _wrappers_pb2.StringValue
    configFile: _config_file_pb2.ClientConfigFileInfo
    def __init__(self, code: _Optional[_Union[_wrappers_pb2.UInt32Value, _Mapping]] = ..., info: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., configFile: _Optional[_Union[_config_file_pb2.ClientConfigFileInfo, _Mapping]] = ...) -> None: ...

class ConfigImportResponse(_message.Message):
    __slots__ = ["code", "info", "createConfigFiles", "skipConfigFiles", "overwriteConfigFiles"]
    CODE_FIELD_NUMBER: _ClassVar[int]
    INFO_FIELD_NUMBER: _ClassVar[int]
    CREATECONFIGFILES_FIELD_NUMBER: _ClassVar[int]
    SKIPCONFIGFILES_FIELD_NUMBER: _ClassVar[int]
    OVERWRITECONFIGFILES_FIELD_NUMBER: _ClassVar[int]
    code: _wrappers_pb2.UInt32Value
    info: _wrappers_pb2.StringValue
    createConfigFiles: _containers.RepeatedCompositeFieldContainer[_config_file_pb2.ConfigFile]
    skipConfigFiles: _containers.RepeatedCompositeFieldContainer[_config_file_pb2.ConfigFile]
    overwriteConfigFiles: _containers.RepeatedCompositeFieldContainer[_config_file_pb2.ConfigFile]
    def __init__(self, code: _Optional[_Union[_wrappers_pb2.UInt32Value, _Mapping]] = ..., info: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., createConfigFiles: _Optional[_Iterable[_Union[_config_file_pb2.ConfigFile, _Mapping]]] = ..., skipConfigFiles: _Optional[_Iterable[_Union[_config_file_pb2.ConfigFile, _Mapping]]] = ..., overwriteConfigFiles: _Optional[_Iterable[_Union[_config_file_pb2.ConfigFile, _Mapping]]] = ...) -> None: ...

class ConfigExportResponse(_message.Message):
    __slots__ = ["code", "info", "data"]
    CODE_FIELD_NUMBER: _ClassVar[int]
    INFO_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    code: _wrappers_pb2.UInt32Value
    info: _wrappers_pb2.StringValue
    data: _wrappers_pb2.BytesValue
    def __init__(self, code: _Optional[_Union[_wrappers_pb2.UInt32Value, _Mapping]] = ..., info: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., data: _Optional[_Union[_wrappers_pb2.BytesValue, _Mapping]] = ...) -> None: ...

class ConfigEncryptAlgorithmResponse(_message.Message):
    __slots__ = ["code", "info", "algorithms"]
    CODE_FIELD_NUMBER: _ClassVar[int]
    INFO_FIELD_NUMBER: _ClassVar[int]
    ALGORITHMS_FIELD_NUMBER: _ClassVar[int]
    code: _wrappers_pb2.UInt32Value
    info: _wrappers_pb2.StringValue
    algorithms: _containers.RepeatedCompositeFieldContainer[_wrappers_pb2.StringValue]
    def __init__(self, code: _Optional[_Union[_wrappers_pb2.UInt32Value, _Mapping]] = ..., info: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., algorithms: _Optional[_Iterable[_Union[_wrappers_pb2.StringValue, _Mapping]]] = ...) -> None: ...

class ConfigDiscoverResponse(_message.Message):
    __slots__ = ["code", "info", "revision", "type", "namespace", "group", "file_name", "config_file", "config_file_names"]
    class ConfigDiscoverResponseType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
        UNKNOWN: _ClassVar[ConfigDiscoverResponse.ConfigDiscoverResponseType]
        CONFIG_FILE: _ClassVar[ConfigDiscoverResponse.ConfigDiscoverResponseType]
        CONFIG_FILE_Names: _ClassVar[ConfigDiscoverResponse.ConfigDiscoverResponseType]
    UNKNOWN: ConfigDiscoverResponse.ConfigDiscoverResponseType
    CONFIG_FILE: ConfigDiscoverResponse.ConfigDiscoverResponseType
    CONFIG_FILE_Names: ConfigDiscoverResponse.ConfigDiscoverResponseType
    CODE_FIELD_NUMBER: _ClassVar[int]
    INFO_FIELD_NUMBER: _ClassVar[int]
    REVISION_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    GROUP_FIELD_NUMBER: _ClassVar[int]
    FILE_NAME_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FILE_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FILE_NAMES_FIELD_NUMBER: _ClassVar[int]
    code: int
    info: str
    revision: str
    type: ConfigDiscoverResponse.ConfigDiscoverResponseType
    namespace: str
    group: str
    file_name: str
    config_file: _config_file_pb2.ClientConfigFileInfo
    config_file_names: _containers.RepeatedCompositeFieldContainer[_config_file_pb2.ClientConfigFileInfo]
    def __init__(self, code: _Optional[int] = ..., info: _Optional[str] = ..., revision: _Optional[str] = ..., type: _Optional[_Union[ConfigDiscoverResponse.ConfigDiscoverResponseType, str]] = ..., namespace: _Optional[str] = ..., group: _Optional[str] = ..., file_name: _Optional[str] = ..., config_file: _Optional[_Union[_config_file_pb2.ClientConfigFileInfo, _Mapping]] = ..., config_file_names: _Optional[_Iterable[_Union[_config_file_pb2.ClientConfigFileInfo, _Mapping]]] = ...) -> None: ...

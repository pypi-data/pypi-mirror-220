# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: strmprivacy/api/monitoring/v1/monitoring.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.api import field_behavior_pb2 as google_dot_api_dot_field__behavior__pb2
from google.protobuf import field_mask_pb2 as google_dot_protobuf_dot_field__mask__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n.strmprivacy/api/monitoring/v1/monitoring.proto\x12\x1dstrmprivacy.api.monitoring.v1\x1a\x1fgoogle/api/field_behavior.proto\x1a google/protobuf/field_mask.proto\x1a\x1fgoogle/protobuf/timestamp.proto\"\xe9\x01\n\x15GetEntityStateRequest\x12@\n\x03ref\x18\x01 \x01(\x0b\x32..strmprivacy.api.monitoring.v1.EntityState.RefR\x03ref\x12I\n\x06status\x18\x02 \x01(\x0e\x32\x31.strmprivacy.api.monitoring.v1.EntityState.StatusR\x06status\x12\x43\n\x0fprojection_mask\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.FieldMaskR\x0eprojectionMask\"Z\n\x16GetEntityStateResponse\x12@\n\x05state\x18\x01 \x01(\x0b\x32*.strmprivacy.api.monitoring.v1.EntityStateR\x05state\"\xf0\x01\n\x1cGetLatestEntityStatesRequest\x12@\n\x03ref\x18\x01 \x01(\x0b\x32..strmprivacy.api.monitoring.v1.EntityState.RefR\x03ref\x12I\n\x06status\x18\x02 \x01(\x0e\x32\x31.strmprivacy.api.monitoring.v1.EntityState.StatusR\x06status\x12\x43\n\x0fprojection_mask\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.FieldMaskR\x0eprojectionMask\"a\n\x1dGetLatestEntityStatesResponse\x12@\n\x05state\x18\x01 \x03(\x0b\x32*.strmprivacy.api.monitoring.v1.EntityStateR\x05state\"_\n\x19UpdateEntityStatesRequest\x12\x42\n\x06states\x18\x01 \x03(\x0b\x32*.strmprivacy.api.monitoring.v1.EntityStateR\x06states\"\x1c\n\x1aUpdateEntityStatesResponse\"\xd8\x08\n\x0b\x45ntityState\x12>\n\nstate_time\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.TimestampB\x03\xe0\x41\x02R\tstateTime\x12\x45\n\x03ref\x18\x02 \x01(\x0b\x32..strmprivacy.api.monitoring.v1.EntityState.RefB\x03\xe0\x41\x02R\x03ref\x12N\n\x06status\x18\x03 \x01(\x0e\x32\x31.strmprivacy.api.monitoring.v1.EntityState.StatusB\x03\xe0\x41\x02R\x06status\x12\x18\n\x07message\x18\x04 \x01(\tR\x07message\x12\x12\n\x04logs\x18\x05 \x03(\tR\x04logs\x12\\\n\rresource_type\x18\x06 \x01(\x0e\x32\x37.strmprivacy.api.monitoring.v1.EntityState.ResourceTypeR\x0cresourceType\x1a\x88\x01\n\x03Ref\x12I\n\x04type\x18\x01 \x01(\x0e\x32\x35.strmprivacy.api.monitoring.v1.EntityState.EntityTypeR\x04type\x12\"\n\nproject_id\x18\x02 \x01(\tB\x03\xe0\x41\x02R\tprojectId\x12\x12\n\x04name\x18\x03 \x01(\tR\x04name\"w\n\x06Status\x12\x16\n\x12STATUS_UNSPECIFIED\x10\x00\x12\x0b\n\x07HEALTHY\x10\x01\x12\x0b\n\x07REMOVED\x10\x02\x12\x0b\n\x07PENDING\x10\x03\x12\x0f\n\x0bTERMINATING\x10\x04\x12\r\n\tUNHEALTHY\x10\x05\x12\x0e\n\nRESTARTING\x10\x06\"\x80\x01\n\nEntityType\x12\x1b\n\x17\x45NTITY_TYPE_UNSPECIFIED\x10\x00\x12\r\n\tBATCH_JOB\x10\x01\x12\n\n\x06STREAM\x10\x02\x12\x12\n\x0e\x42\x41TCH_EXPORTER\x10\x03\x12\x12\n\x0e\x44\x41TA_CONNECTOR\x10\x04\x12\x12\n\x0eKAFKA_EXPORTER\x10\x05\"\xde\x02\n\x0cResourceType\x12\x1d\n\x19RESOURCE_TYPE_UNSPECIFIED\x10\x00\x12\x11\n\rBATCH_JOB_JOB\x10\x64\x12\x14\n\x10\x42\x41TCH_JOB_SECRET\x10\x65\x12\x18\n\x14\x42\x41TCH_JOB_CONFIG_MAP\x10\x66\x12\x10\n\x0cSTREAM_TOPIC\x10x\x12 \n\x1cSTREAM_ENCRYPTION_KEYS_TOPIC\x10y\x12\x1f\n\x1bSTREAM_DECRYPTER_DEPLOYMENT\x10z\x12\x1f\n\x1bSTREAM_DECRYPTER_CONFIG_MAP\x10{\x12\x1e\n\x19\x42\x41TCH_EXPORTER_DEPLOYMENT\x10\x8c\x01\x12\x1a\n\x15\x42\x41TCH_EXPORTER_SECRET\x10\x8d\x01\x12\x1a\n\x15\x44\x41TA_CONNECTOR_SECRET\x10\x96\x01\x12\x1e\n\x19KAFKA_EXPORTER_DEPLOYMENT\x10\xa0\x01\x32\xb7\x03\n\x11MonitoringService\x12\x7f\n\x0eGetEntityState\x12\x34.strmprivacy.api.monitoring.v1.GetEntityStateRequest\x1a\x35.strmprivacy.api.monitoring.v1.GetEntityStateResponse0\x01\x12\x92\x01\n\x15GetLatestEntityStates\x12;.strmprivacy.api.monitoring.v1.GetLatestEntityStatesRequest\x1a<.strmprivacy.api.monitoring.v1.GetLatestEntityStatesResponse\x12\x8b\x01\n\x12UpdateEntityStates\x12\x38.strmprivacy.api.monitoring.v1.UpdateEntityStatesRequest\x1a\x39.strmprivacy.api.monitoring.v1.UpdateEntityStatesResponse(\x01\x42o\n io.strmprivacy.api.monitoring.v1P\x01ZIgithub.com/strmprivacy/api-definitions-go/v2/api/monitoring/v1;monitoringb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'strmprivacy.api.monitoring.v1.monitoring_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n io.strmprivacy.api.monitoring.v1P\001ZIgithub.com/strmprivacy/api-definitions-go/v2/api/monitoring/v1;monitoring'
  _ENTITYSTATE_REF.fields_by_name['project_id']._options = None
  _ENTITYSTATE_REF.fields_by_name['project_id']._serialized_options = b'\340A\002'
  _ENTITYSTATE.fields_by_name['state_time']._options = None
  _ENTITYSTATE.fields_by_name['state_time']._serialized_options = b'\340A\002'
  _ENTITYSTATE.fields_by_name['ref']._options = None
  _ENTITYSTATE.fields_by_name['ref']._serialized_options = b'\340A\002'
  _ENTITYSTATE.fields_by_name['status']._options = None
  _ENTITYSTATE.fields_by_name['status']._serialized_options = b'\340A\002'
  _GETENTITYSTATEREQUEST._serialized_start=182
  _GETENTITYSTATEREQUEST._serialized_end=415
  _GETENTITYSTATERESPONSE._serialized_start=417
  _GETENTITYSTATERESPONSE._serialized_end=507
  _GETLATESTENTITYSTATESREQUEST._serialized_start=510
  _GETLATESTENTITYSTATESREQUEST._serialized_end=750
  _GETLATESTENTITYSTATESRESPONSE._serialized_start=752
  _GETLATESTENTITYSTATESRESPONSE._serialized_end=849
  _UPDATEENTITYSTATESREQUEST._serialized_start=851
  _UPDATEENTITYSTATESREQUEST._serialized_end=946
  _UPDATEENTITYSTATESRESPONSE._serialized_start=948
  _UPDATEENTITYSTATESRESPONSE._serialized_end=976
  _ENTITYSTATE._serialized_start=979
  _ENTITYSTATE._serialized_end=2091
  _ENTITYSTATE_REF._serialized_start=1350
  _ENTITYSTATE_REF._serialized_end=1486
  _ENTITYSTATE_STATUS._serialized_start=1488
  _ENTITYSTATE_STATUS._serialized_end=1607
  _ENTITYSTATE_ENTITYTYPE._serialized_start=1610
  _ENTITYSTATE_ENTITYTYPE._serialized_end=1738
  _ENTITYSTATE_RESOURCETYPE._serialized_start=1741
  _ENTITYSTATE_RESOURCETYPE._serialized_end=2091
  _MONITORINGSERVICE._serialized_start=2094
  _MONITORINGSERVICE._serialized_end=2533
# @@protoc_insertion_point(module_scope)

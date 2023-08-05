# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: strmprivacy/api/credentials/v1/credentials_v1.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.api import field_behavior_pb2 as google_dot_api_dot_field__behavior__pb2
from strmprivacy.api.entities.v1 import entities_v1_pb2 as strmprivacy_dot_api_dot_entities_dot_v1_dot_entities__v1__pb2
from validate import validate_pb2 as validate_dot_validate__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n3strmprivacy/api/credentials/v1/credentials_v1.proto\x12\x1estrmprivacy.api.credentials.v1\x1a\x1fgoogle/api/field_behavior.proto\x1a-strmprivacy/api/entities/v1/entities_v1.proto\x1a\x17validate/validate.proto\"i\n\x16ListCredentialsRequest\x12O\n\nstream_ref\x18\x01 \x01(\x0b\x32&.strmprivacy.api.entities.v1.StreamRefB\x08\xfa\x42\x05\x8a\x01\x02\x10\x01R\tstreamRef\"e\n\x17ListCredentialsResponse\x12J\n\x0b\x63redentials\x18\x01 \x03(\x0b\x32(.strmprivacy.api.entities.v1.CredentialsR\x0b\x63redentials\"@\n\x17\x44\x65leteCredentialRequest\x12%\n\tclient_id\x18\x01 \x01(\tB\x08\xfa\x42\x05r\x03\xb0\x01\x01R\x08\x63lientId\"\x1a\n\x18\x44\x65leteCredentialResponse\"=\n\x14GetCredentialRequest\x12%\n\tclient_id\x18\x01 \x01(\tB\x08\xfa\x42\x05r\x03\xb0\x01\x01R\x08\x63lientId\"a\n\x15GetCredentialResponse\x12H\n\ncredential\x18\x01 \x01(\x0b\x32(.strmprivacy.api.entities.v1.CredentialsR\ncredential\"j\n\x17\x43reateCredentialRequest\x12O\n\nstream_ref\x18\x01 \x01(\x0b\x32&.strmprivacy.api.entities.v1.StreamRefB\x08\xfa\x42\x05\x8a\x01\x02\x10\x01R\tstreamRef\"k\n\x18\x43reateCredentialResponse\x12O\n\x0b\x63redentials\x18\x01 \x01(\x0b\x32(.strmprivacy.api.entities.v1.CredentialsB\x03\xe0\x41\x02R\x0b\x63redentials2\xa7\x04\n\x12\x43redentialsService\x12\x82\x01\n\x0fListCredentials\x12\x36.strmprivacy.api.credentials.v1.ListCredentialsRequest\x1a\x37.strmprivacy.api.credentials.v1.ListCredentialsResponse\x12|\n\rGetCredential\x12\x34.strmprivacy.api.credentials.v1.GetCredentialRequest\x1a\x35.strmprivacy.api.credentials.v1.GetCredentialResponse\x12\x85\x01\n\x10\x43reateCredential\x12\x37.strmprivacy.api.credentials.v1.CreateCredentialRequest\x1a\x38.strmprivacy.api.credentials.v1.CreateCredentialResponse\x12\x85\x01\n\x10\x44\x65leteCredential\x12\x37.strmprivacy.api.credentials.v1.DeleteCredentialRequest\x1a\x38.strmprivacy.api.credentials.v1.DeleteCredentialResponseBr\n!io.strmprivacy.api.credentials.v1P\x01ZKgithub.com/strmprivacy/api-definitions-go/v2/api/credentials/v1;credentialsb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'strmprivacy.api.credentials.v1.credentials_v1_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n!io.strmprivacy.api.credentials.v1P\001ZKgithub.com/strmprivacy/api-definitions-go/v2/api/credentials/v1;credentials'
  _LISTCREDENTIALSREQUEST.fields_by_name['stream_ref']._options = None
  _LISTCREDENTIALSREQUEST.fields_by_name['stream_ref']._serialized_options = b'\372B\005\212\001\002\020\001'
  _DELETECREDENTIALREQUEST.fields_by_name['client_id']._options = None
  _DELETECREDENTIALREQUEST.fields_by_name['client_id']._serialized_options = b'\372B\005r\003\260\001\001'
  _GETCREDENTIALREQUEST.fields_by_name['client_id']._options = None
  _GETCREDENTIALREQUEST.fields_by_name['client_id']._serialized_options = b'\372B\005r\003\260\001\001'
  _CREATECREDENTIALREQUEST.fields_by_name['stream_ref']._options = None
  _CREATECREDENTIALREQUEST.fields_by_name['stream_ref']._serialized_options = b'\372B\005\212\001\002\020\001'
  _CREATECREDENTIALRESPONSE.fields_by_name['credentials']._options = None
  _CREATECREDENTIALRESPONSE.fields_by_name['credentials']._serialized_options = b'\340A\002'
  _LISTCREDENTIALSREQUEST._serialized_start=192
  _LISTCREDENTIALSREQUEST._serialized_end=297
  _LISTCREDENTIALSRESPONSE._serialized_start=299
  _LISTCREDENTIALSRESPONSE._serialized_end=400
  _DELETECREDENTIALREQUEST._serialized_start=402
  _DELETECREDENTIALREQUEST._serialized_end=466
  _DELETECREDENTIALRESPONSE._serialized_start=468
  _DELETECREDENTIALRESPONSE._serialized_end=494
  _GETCREDENTIALREQUEST._serialized_start=496
  _GETCREDENTIALREQUEST._serialized_end=557
  _GETCREDENTIALRESPONSE._serialized_start=559
  _GETCREDENTIALRESPONSE._serialized_end=656
  _CREATECREDENTIALREQUEST._serialized_start=658
  _CREATECREDENTIALREQUEST._serialized_end=764
  _CREATECREDENTIALRESPONSE._serialized_start=766
  _CREATECREDENTIALRESPONSE._serialized_end=873
  _CREDENTIALSSERVICE._serialized_start=876
  _CREDENTIALSSERVICE._serialized_end=1427
# @@protoc_insertion_point(module_scope)

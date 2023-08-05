# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: strmprivacy/api/batch_jobs/v1/batch_jobs_v1.proto
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


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n1strmprivacy/api/batch_jobs/v1/batch_jobs_v1.proto\x12\x1dstrmprivacy.api.batch_jobs.v1\x1a\x1fgoogle/api/field_behavior.proto\x1a-strmprivacy/api/entities/v1/entities_v1.proto\x1a\x17validate/validate.proto\"Z\n\x12GetBatchJobRequest\x12\x44\n\x03ref\x18\x01 \x01(\x0b\x32(.strmprivacy.api.entities.v1.BatchJobRefB\x08\xfa\x42\x05\x8a\x01\x02\x10\x01R\x03ref\"\xa2\x01\n\x13GetBatchJobResponse\x12\x46\n\tbatch_job\x18\x01 \x01(\x0b\x32%.strmprivacy.api.entities.v1.BatchJobB\x02\x18\x01R\x08\x62\x61tchJob\x12\x43\n\x03job\x18\x02 \x01(\x0b\x32,.strmprivacy.api.entities.v1.BatchJobWrapperB\x03\xe0\x41\x02R\x03job\"m\n\x14ListBatchJobsRequest\x12,\n\nbilling_id\x18\x01 \x01(\tB\r\x18\x01\xfa\x42\x08r\x06\x98\x01\x00\xd0\x01\x01R\tbillingId\x12\'\n\nproject_id\x18\x02 \x01(\tB\x08\xfa\x42\x05r\x03\xb0\x01\x01R\tprojectId\"\xa8\x01\n\x15ListBatchJobsResponse\x12H\n\nbatch_jobs\x18\x01 \x03(\x0b\x32%.strmprivacy.api.entities.v1.BatchJobB\x02\x18\x01R\tbatchJobs\x12\x45\n\x04jobs\x18\x02 \x03(\x0b\x32,.strmprivacy.api.entities.v1.BatchJobWrapperB\x03\xe0\x41\x02R\x04jobs\"\xa4\x01\n\x15\x43reateBatchJobRequest\x12\x46\n\tbatch_job\x18\x01 \x01(\x0b\x32%.strmprivacy.api.entities.v1.BatchJobB\x02\x18\x01R\x08\x62\x61tchJob\x12\x43\n\x03job\x18\x02 \x01(\x0b\x32,.strmprivacy.api.entities.v1.BatchJobWrapperB\x03\xe0\x41\x02R\x03job\"\xa8\x01\n\x16\x43reateBatchJobResponse\x12I\n\tbatch_job\x18\x01 \x01(\x0b\x32%.strmprivacy.api.entities.v1.BatchJobB\x05\x18\x01\xe0\x41\x02R\x08\x62\x61tchJob\x12\x43\n\x03job\x18\x02 \x01(\x0b\x32,.strmprivacy.api.entities.v1.BatchJobWrapperB\x03\xe0\x41\x02R\x03job\"]\n\x15\x44\x65leteBatchJobRequest\x12\x44\n\x03ref\x18\x01 \x01(\x0b\x32(.strmprivacy.api.entities.v1.BatchJobRefB\x08\xfa\x42\x05\x8a\x01\x02\x10\x01R\x03ref\"\x18\n\x16\x44\x65leteBatchJobResponse\"\xc0\x01\n\x1aUpdateBatchJobStateRequest\x12\x44\n\x03ref\x18\x01 \x01(\x0b\x32(.strmprivacy.api.entities.v1.BatchJobRefB\x08\xfa\x42\x05\x8a\x01\x02\x10\x01R\x03ref\x12\\\n\x0f\x62\x61tch_job_state\x18\x02 \x01(\x0b\x32*.strmprivacy.api.entities.v1.BatchJobStateB\x08\xfa\x42\x05\x8a\x01\x02\x10\x01R\rbatchJobState\"\x1d\n\x1bUpdateBatchJobStateResponse2\x91\x05\n\x10\x42\x61tchJobsService\x12t\n\x0bGetBatchJob\x12\x31.strmprivacy.api.batch_jobs.v1.GetBatchJobRequest\x1a\x32.strmprivacy.api.batch_jobs.v1.GetBatchJobResponse\x12z\n\rListBatchJobs\x12\x33.strmprivacy.api.batch_jobs.v1.ListBatchJobsRequest\x1a\x34.strmprivacy.api.batch_jobs.v1.ListBatchJobsResponse\x12}\n\x0e\x43reateBatchJob\x12\x34.strmprivacy.api.batch_jobs.v1.CreateBatchJobRequest\x1a\x35.strmprivacy.api.batch_jobs.v1.CreateBatchJobResponse\x12}\n\x0e\x44\x65leteBatchJob\x12\x34.strmprivacy.api.batch_jobs.v1.DeleteBatchJobRequest\x1a\x35.strmprivacy.api.batch_jobs.v1.DeleteBatchJobResponse\x12\x8c\x01\n\x13UpdateBatchJobState\x12\x39.strmprivacy.api.batch_jobs.v1.UpdateBatchJobStateRequest\x1a:.strmprivacy.api.batch_jobs.v1.UpdateBatchJobStateResponseBo\n io.strmprivacy.api.batch_jobs.v1P\x01ZIgithub.com/strmprivacy/api-definitions-go/v2/api/batch_jobs/v1;batch_jobsb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'strmprivacy.api.batch_jobs.v1.batch_jobs_v1_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n io.strmprivacy.api.batch_jobs.v1P\001ZIgithub.com/strmprivacy/api-definitions-go/v2/api/batch_jobs/v1;batch_jobs'
  _GETBATCHJOBREQUEST.fields_by_name['ref']._options = None
  _GETBATCHJOBREQUEST.fields_by_name['ref']._serialized_options = b'\372B\005\212\001\002\020\001'
  _GETBATCHJOBRESPONSE.fields_by_name['batch_job']._options = None
  _GETBATCHJOBRESPONSE.fields_by_name['batch_job']._serialized_options = b'\030\001'
  _GETBATCHJOBRESPONSE.fields_by_name['job']._options = None
  _GETBATCHJOBRESPONSE.fields_by_name['job']._serialized_options = b'\340A\002'
  _LISTBATCHJOBSREQUEST.fields_by_name['billing_id']._options = None
  _LISTBATCHJOBSREQUEST.fields_by_name['billing_id']._serialized_options = b'\030\001\372B\010r\006\230\001\000\320\001\001'
  _LISTBATCHJOBSREQUEST.fields_by_name['project_id']._options = None
  _LISTBATCHJOBSREQUEST.fields_by_name['project_id']._serialized_options = b'\372B\005r\003\260\001\001'
  _LISTBATCHJOBSRESPONSE.fields_by_name['batch_jobs']._options = None
  _LISTBATCHJOBSRESPONSE.fields_by_name['batch_jobs']._serialized_options = b'\030\001'
  _LISTBATCHJOBSRESPONSE.fields_by_name['jobs']._options = None
  _LISTBATCHJOBSRESPONSE.fields_by_name['jobs']._serialized_options = b'\340A\002'
  _CREATEBATCHJOBREQUEST.fields_by_name['batch_job']._options = None
  _CREATEBATCHJOBREQUEST.fields_by_name['batch_job']._serialized_options = b'\030\001'
  _CREATEBATCHJOBREQUEST.fields_by_name['job']._options = None
  _CREATEBATCHJOBREQUEST.fields_by_name['job']._serialized_options = b'\340A\002'
  _CREATEBATCHJOBRESPONSE.fields_by_name['batch_job']._options = None
  _CREATEBATCHJOBRESPONSE.fields_by_name['batch_job']._serialized_options = b'\030\001\340A\002'
  _CREATEBATCHJOBRESPONSE.fields_by_name['job']._options = None
  _CREATEBATCHJOBRESPONSE.fields_by_name['job']._serialized_options = b'\340A\002'
  _DELETEBATCHJOBREQUEST.fields_by_name['ref']._options = None
  _DELETEBATCHJOBREQUEST.fields_by_name['ref']._serialized_options = b'\372B\005\212\001\002\020\001'
  _UPDATEBATCHJOBSTATEREQUEST.fields_by_name['ref']._options = None
  _UPDATEBATCHJOBSTATEREQUEST.fields_by_name['ref']._serialized_options = b'\372B\005\212\001\002\020\001'
  _UPDATEBATCHJOBSTATEREQUEST.fields_by_name['batch_job_state']._options = None
  _UPDATEBATCHJOBSTATEREQUEST.fields_by_name['batch_job_state']._serialized_options = b'\372B\005\212\001\002\020\001'
  _GETBATCHJOBREQUEST._serialized_start=189
  _GETBATCHJOBREQUEST._serialized_end=279
  _GETBATCHJOBRESPONSE._serialized_start=282
  _GETBATCHJOBRESPONSE._serialized_end=444
  _LISTBATCHJOBSREQUEST._serialized_start=446
  _LISTBATCHJOBSREQUEST._serialized_end=555
  _LISTBATCHJOBSRESPONSE._serialized_start=558
  _LISTBATCHJOBSRESPONSE._serialized_end=726
  _CREATEBATCHJOBREQUEST._serialized_start=729
  _CREATEBATCHJOBREQUEST._serialized_end=893
  _CREATEBATCHJOBRESPONSE._serialized_start=896
  _CREATEBATCHJOBRESPONSE._serialized_end=1064
  _DELETEBATCHJOBREQUEST._serialized_start=1066
  _DELETEBATCHJOBREQUEST._serialized_end=1159
  _DELETEBATCHJOBRESPONSE._serialized_start=1161
  _DELETEBATCHJOBRESPONSE._serialized_end=1185
  _UPDATEBATCHJOBSTATEREQUEST._serialized_start=1188
  _UPDATEBATCHJOBSTATEREQUEST._serialized_end=1380
  _UPDATEBATCHJOBSTATERESPONSE._serialized_start=1382
  _UPDATEBATCHJOBSTATERESPONSE._serialized_end=1411
  _BATCHJOBSSERVICE._serialized_start=1414
  _BATCHJOBSSERVICE._serialized_end=2071
# @@protoc_insertion_point(module_scope)

# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: flyteidl/core/errors.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from flyteidl.core import execution_pb2 as flyteidl_dot_core_dot_execution__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1a\x66lyteidl/core/errors.proto\x12\rflyteidl.core\x1a\x1d\x66lyteidl/core/execution.proto\"\xe5\x01\n\x0e\x43ontainerError\x12\x12\n\x04\x63ode\x18\x01 \x01(\tR\x04\x63ode\x12\x18\n\x07message\x18\x02 \x01(\tR\x07message\x12\x36\n\x04kind\x18\x03 \x01(\x0e\x32\".flyteidl.core.ContainerError.KindR\x04kind\x12?\n\x06origin\x18\x04 \x01(\x0e\x32\'.flyteidl.core.ExecutionError.ErrorKindR\x06origin\",\n\x04Kind\x12\x13\n\x0fNON_RECOVERABLE\x10\x00\x12\x0f\n\x0bRECOVERABLE\x10\x01\"D\n\rErrorDocument\x12\x33\n\x05\x65rror\x18\x01 \x01(\x0b\x32\x1d.flyteidl.core.ContainerErrorR\x05\x65rrorB\xab\x01\n\x11\x63om.flyteidl.coreB\x0b\x45rrorsProtoP\x01Z4github.com/flyteorg/flyteidl/gen/pb-go/flyteidl/core\xa2\x02\x03\x46\x43X\xaa\x02\rFlyteidl.Core\xca\x02\rFlyteidl\\Core\xe2\x02\x19\x46lyteidl\\Core\\GPBMetadata\xea\x02\x0e\x46lyteidl::Coreb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'flyteidl.core.errors_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\021com.flyteidl.coreB\013ErrorsProtoP\001Z4github.com/flyteorg/flyteidl/gen/pb-go/flyteidl/core\242\002\003FCX\252\002\rFlyteidl.Core\312\002\rFlyteidl\\Core\342\002\031Flyteidl\\Core\\GPBMetadata\352\002\016Flyteidl::Core'
  _CONTAINERERROR._serialized_start=77
  _CONTAINERERROR._serialized_end=306
  _CONTAINERERROR_KIND._serialized_start=262
  _CONTAINERERROR_KIND._serialized_end=306
  _ERRORDOCUMENT._serialized_start=308
  _ERRORDOCUMENT._serialized_end=376
# @@protoc_insertion_point(module_scope)

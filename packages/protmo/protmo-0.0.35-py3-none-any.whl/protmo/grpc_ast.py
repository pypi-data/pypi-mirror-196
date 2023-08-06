'''

A gRPC service definition looks like this:

```protobuf
message Employee {   <--------------------------------- This is a ProtoMessage
  string id = 1;
  string firstName = 2; <------------------------------ This is a ProtoField
  int32 age = 3;
  repeated string roles = 4;
  Address address = 5;
  repeated Dress dresses = 6;
  int64 createdAt = 7;
  int64 lastUpdatedAt = 8;
}

service EmployeeMethods { <---------------------------- This is a GrpcService
  rpc collect (stream EmployeeCollectParam) returns (EmployeeCollectResult);
  rpc collectLive (stream EmployeeCollectLiveParam) returns (stream EmployeeCollectLiveResult);
  rpc doNothing (Void) returns (Void); <--------------- This is a GrpcProcedure
}
```

- You can see that there are messages and services at the top level.


- The messages are represented with the class ProtoMessage
- Each ProtoMessage has multiple ProtoFields. These are the content of the message above,
  for example `string id = 1` or `string firstName = 2`;

- The services, like EmployeeMethods, are represented with the class
  GrpcService, which contains multiple GrpcProcedures, like collect, sayHello, etc. from above

'''

from protmo.ast import *


class ProtoMessage:
    '''
    Describes a protobuf-message. It groups together a bunch of
    ProtoFields.
    Thus a ProtoMessage contains multiple ProtoFields.
    You can use the str-method to generate valid protobuf code.
    '''

    def __init__(self, name: str) -> None:
        self.name = name
        self.fields: list[ProtoField] = []

    def __str__(self) -> str:
        '''
        Returns valid protobuf code, thus converts the abstract represenation
        of this class into valid code.
        You can use it for code-generation.
        '''
        res = f'message {self.name} {{\n'
        for field in self.fields:
            res += f'  {field};\n'
        res += '}'
        return res

    @property
    def is_entity(self) -> bool:
        '''
        Returns True if this message is an entity, i.e. it has a field
        `id` of type `string` and `createdAt` and `lastUpdatedAt` of type
        `int64`.
        '''
        for field in self.fields:
            if field.tag == 1:
                if field.name == 'id':
                    return True
        return False


class ProtoField:

    def __init__(
            self,
            pythonType: str,
            name: str,
            tag: int,
            repeated: bool = False) -> None:
        self.protoType = _python_to_proto.python_datatype_to_proto(pythonType)
        self.name = name
        self.tag = tag
        self.repeated = repeated

    def __str__(self) -> str:
        t = self.protoType
        if self.repeated:
            t = 'repeated ' + t
        return f'{t} {self.name} = {self.tag}'


##############################


class GrpcService:
    '''
    Describes a gRPC service, thus something like `service Name { ... }`.
    It groups a bunch of `GrpcProcedures` together.
    Thus one GrpcService has many GrpcProcedures
    You can use the str() method to generate valid gRPC-service-defintion code
    '''

    def __init__(self, name: str) -> None:
        self.name = name
        self.procedures: list[GrpcProcedure] = []

    def __str__(self) -> str:
        '''
        returns valid gRPC service defintion of the information stored in this
        abstract representation.
        You can use it for code generation.
        '''
        res = f'service {self.name} {{\n'
        for proc in self.procedures:
            res += f'  {proc};\n'
        res += '}'
        return res


class GrpcProcedure:
    '''
    The actual procedures, that are grouped by the GrpcService.
    There is either:
    - no streaming
    - client side streaming
    - server side streaming or
    - bidirectionalstreaming (which is client side streaming + server side streaming)

    To get the gRPC definition, you can use the str-method
    '''

    def __init__(
            self,
            name: str,
            paramType: str,
            returnType: str,
            clientSideStreaming: bool = False,
            serverSideStreaming: bool = False):
        self.name = name
        self.paramType = paramType
        self.returnType = returnType
        self.clientSideStreaming = clientSideStreaming
        self.serverSideStreaming = serverSideStreaming

    def __str__(self) -> str:
        '''
        Creates the gRPC procedure in valid gRPC code and can be used for
        code generation.
        '''

        param = str(self.paramType)
        if self.clientSideStreaming:
            param = 'stream ' + param
        ret = str(self.returnType)
        if self.serverSideStreaming:
            ret = 'stream ' + ret
        return f'rpc {self.name} ({param}) returns ({ret})'


class _PythonToProto:

    python_dt_to_proto = {
        float: 'double',
        'float': 'double',
        int: 'int32',
        'int': 'int32',
        bool: 'bool',
        str: 'string',
        'str': 'string'
    }

    def __init__(self):
        self.proto_dt_to_python = {}
        for dt in self.python_dt_to_proto:
            self.proto_dt_to_python[self.python_dt_to_proto[dt]] = dt

    def python_datatype_to_proto(self, python_datatype: str) -> str:
        return self.python_dt_to_proto.get(python_datatype, python_datatype)

    def proto_datatype_to_python(self, proto_datatype: str) -> str:
        return self.proto_dt_to_python[proto_datatype]


_python_to_proto = _PythonToProto()


#####


class AstToGrpcAst:
    '''
    Generates multiple ProtoMessage for a given Message
    '''

    def __init__(self, modelMessage: MessageInfo):
        self.messages: list[ProtoMessage] = []
        has_void = False

        # 1. create message of the model
        protoMsg = ProtoMessage(modelMessage.name)
        for field in modelMessage.fields:
            protoMsg.fields.append(
                ProtoField(
                    field.protoType,
                    field.name,
                    field.tag,
                    field.repeated))
        self.messages.append(protoMsg)

        if protoMsg.is_entity:
            refMessage = ProtoMessage(modelMessage.name + 'Ref')
            refMessage.fields.append(ProtoField('string', 'id', 1))
            refMessage.fields.append(ProtoField('bool', 'resolved', 2))
            refMessage.fields.append(ProtoField(protoMsg.name, 'data', 3))
            self.messages.append(
                refMessage
            )

        # 2. create all required messages for the rpc-methods
        for method in modelMessage.rpc_methods:

            # 2.1 create ParameterMessage
            if method.has_params:
                paramMessage = ProtoMessage(
                    modelMessage.name + cap(method.name) + 'Param')
                tag_offset = 1
                if not method.is_static:
                    # add self reference
                    tag_offset += 1
                    paramMessage.fields.append(ProtoField('string', 'self', 1))
                for idx, param in enumerate(method.parameters):
                    tag = idx + tag_offset
                    name = param.name
                    if method.clientSideStreaming:
                        name = 'request'
                    field = ProtoField(
                        param.pythonType, name, tag, repeated=param.repeated)
                    paramMessage.fields.append(field)
                self.messages.append(paramMessage)
            else:
                has_void = True

            # 2.2 create ResultMessage
            if not method.returnType.is_void:
                resultMessage = ProtoMessage(
                    modelMessage.name + cap(method.name) + 'Result')
                field = ProtoField(
                    method.returnType.python_type,
                    'result',
                    1,
                    repeated=method.returnType.repeated)
                resultMessage.fields.append(field)
                self.messages.append(resultMessage)
            else:
                has_void = True

        # 3. create a service for the model
        service = GrpcService(modelMessage.name + 'Methods')
        for method in modelMessage.rpc_methods:

            if not method.has_params:
                param_type = 'Void'
            else:
                param_type = modelMessage.name + cap(method.name) + 'Param'

            if method.returnType.is_void:
                return_type = 'Void'
            else:
                return_type = modelMessage.name + cap(method.name) + 'Result'

            procedure = GrpcProcedure(
                method.name,
                param_type,
                return_type,
                clientSideStreaming=method.clientSideStreaming,
                serverSideStreaming=method.serverSideStreaming
            )
            service.procedures.append(procedure)
        self.service = service if modelMessage.rpc_methods else None

        if has_void:
            void_msg = ProtoMessage('Void')
            void_msg.fields.append(ProtoField('string', 'self', 1))
            self.messages.append(void_msg)

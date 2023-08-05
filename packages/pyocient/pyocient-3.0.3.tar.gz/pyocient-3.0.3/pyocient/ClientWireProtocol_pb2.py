# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: sharedMessages/clientWireProtocol.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import wrappers_pb2 as google_dot_protobuf_dot_wrappers__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\'sharedMessages/clientWireProtocol.proto\x12\nxg.cmdcomp\x1a\x1egoogle/protobuf/wrappers.proto\"\xbe\x01\n\x10\x43lientConnection\x12\x0e\n\x06userid\x18\x01 \x01(\t\x12\x10\n\x08\x64\x61tabase\x18\x02 \x01(\t\x12\x10\n\x08\x63lientid\x18\x03 \x01(\t\x12\x0f\n\x07version\x18\x04 \x01(\t\x12\x1a\n\x12majorClientVersion\x18\x05 \x01(\x05\x12\x1a\n\x12minorClientVersion\x18\x06 \x01(\x05\x12\x1a\n\x12patchClientVersion\x18\x08 \x01(\t\x12\x11\n\tsessionID\x18\x07 \x01(\t\"\xd6\x01\n\x13\x43lientConnectionGCM\x12\x0e\n\x06userid\x18\x01 \x01(\t\x12\x10\n\x08\x64\x61tabase\x18\x02 \x01(\t\x12\x10\n\x08\x63lientid\x18\x03 \x01(\t\x12\x0f\n\x07version\x18\x04 \x01(\t\x12\x1a\n\x12majorClientVersion\x18\x05 \x01(\x05\x12\x1a\n\x12minorClientVersion\x18\x06 \x01(\x05\x12\x1a\n\x12patchClientVersion\x18\t \x01(\t\x12\x11\n\tsessionID\x18\x07 \x01(\t\x12\x13\n\x0b\x65xplicitSSO\x18\x08 \x01(\x08\"\xb1\x01\n\x13\x43lientConnectionSSO\x12\x10\n\x08\x64\x61tabase\x18\x01 \x01(\t\x12\x10\n\x08\x63lientid\x18\x02 \x01(\t\x12\x0f\n\x07version\x18\x03 \x01(\t\x12\x1a\n\x12majorClientVersion\x18\x04 \x01(\x05\x12\x1a\n\x12minorClientVersion\x18\x05 \x01(\x05\x12\x1a\n\x12patchClientVersion\x18\x07 \x01(\t\x12\x11\n\tsessionID\x18\x06 \x01(\t\"\x94\x02\n\x1d\x43lientConnectionSecurityToken\x12\x10\n\x08\x64\x61tabase\x18\x01 \x01(\t\x12\x10\n\x08\x63lientid\x18\x02 \x01(\t\x12\x0f\n\x07version\x18\x03 \x01(\t\x12\x1a\n\x12majorClientVersion\x18\x04 \x01(\x05\x12\x1a\n\x12minorClientVersion\x18\x05 \x01(\x05\x12\x1a\n\x12patchClientVersion\x18\x0b \x01(\t\x12\x11\n\tsessionID\x18\x06 \x01(\t\x12\x15\n\rsecurityToken\x18\x07 \x01(\t\x12\x16\n\x0etokenSignature\x18\x08 \x01(\t\x12\x19\n\x11issuerFingerprint\x18\t \x01(\t\x12\r\n\x05\x66orce\x18\n \x01(\x08\"j\n\x18\x43lientConnectionResponse\x12\x32\n\x08response\x18\x01 \x01(\x0b\x32 .xg.cmdcomp.ConfirmationResponse\x12\n\n\x02iv\x18\x02 \x01(\x0c\x12\x0e\n\x06pubKey\x18\x03 \x01(\t\"m\n\x1b\x43lientConnectionGCMResponse\x12\x32\n\x08response\x18\x01 \x01(\x0b\x32 .xg.cmdcomp.ConfirmationResponse\x12\n\n\x02iv\x18\x02 \x01(\x0c\x12\x0e\n\x06pubKey\x18\x03 \x01(\t\"u\n\x1b\x43lientConnectionSSOResponse\x12\x32\n\x08response\x18\x01 \x01(\x0b\x32 .xg.cmdcomp.ConfirmationResponse\x12\x11\n\trequestId\x18\x02 \x01(\t\x12\x0f\n\x07\x61uthUrl\x18\x03 \x01(\t\"\xfb\x01\n%ClientConnectionSecurityTokenResponse\x12\x32\n\x08response\x18\x01 \x01(\x0b\x32 .xg.cmdcomp.ConfirmationResponse\x12\x10\n\x08redirect\x18\x02 \x01(\x08\x12\x14\n\x0credirectHost\x18\x03 \x01(\t\x12\x14\n\x0credirectPort\x18\x04 \x01(\x07\x12\x10\n\x08\x63mdcomps\x18\x05 \x03(\t\x12\x35\n\tsecondary\x18\x06 \x03(\x0b\x32\".xg.cmdcomp.SecondaryInterfaceList\x12\x17\n\x0fserverSessionId\x18\x07 \x01(\t\"P\n\x11\x43lientConnection2\x12\x0e\n\x06\x63ipher\x18\x01 \x01(\x0c\x12\r\n\x05\x66orce\x18\x02 \x01(\x08\x12\x0c\n\x04hmac\x18\x03 \x01(\x0c\x12\x0e\n\x06pubKey\x18\x04 \x01(\t\"h\n\x14\x43lientConnectionGCM2\x12\x0e\n\x06\x63ipher\x18\x01 \x01(\x0c\x12\r\n\x05\x66orce\x18\x02 \x01(\x08\x12\x0c\n\x04hmac\x18\x03 \x01(\x0c\x12\x0e\n\x06pubKey\x18\x04 \x01(\t\x12\x13\n\x0b\x65xplicitSSO\x18\x05 \x01(\x08\"8\n\x14\x43lientConnectionSSO2\x12\x11\n\trequestId\x18\x01 \x01(\t\x12\r\n\x05\x66orce\x18\x02 \x01(\x08\"K\n\rSecurityToken\x12\x0c\n\x04\x64\x61ta\x18\x01 \x01(\t\x12\x11\n\tsignature\x18\x02 \x01(\t\x12\x19\n\x11issuerFingerprint\x18\x03 \x01(\t\"X\n\x0bSessionInfo\x12\x17\n\x0fserverSessionId\x18\x01 \x01(\t\x12\x30\n\rsecurityToken\x18\x02 \x01(\x0b\x32\x19.xg.cmdcomp.SecurityToken\" \n\x1e\x43lientConnectionRefreshSession\"\x8a\x01\n&ClientConnectionRefreshSessionResponse\x12\x32\n\x08response\x18\x01 \x01(\x0b\x32 .xg.cmdcomp.ConfirmationResponse\x12,\n\x0bsessionInfo\x18\x02 \x01(\x0b\x32\x17.xg.cmdcomp.SessionInfo\"S\n\x1c\x43lientConnectionRefreshToken\x12\x33\n\x10oldSecurityToken\x18\x01 \x01(\x0b\x32\x19.xg.cmdcomp.SecurityToken\"\x8f\x01\n$ClientConnectionRefreshTokenResponse\x12\x32\n\x08response\x18\x01 \x01(\x0b\x32 .xg.cmdcomp.ConfirmationResponse\x12\x33\n\x10newSecurityToken\x18\x02 \x01(\x0b\x32\x19.xg.cmdcomp.SecurityToken\")\n\x16SecondaryInterfaceList\x12\x0f\n\x07\x61\x64\x64ress\x18\x01 \x03(\t\"\xa1\x02\n\x19\x43lientConnection2Response\x12\x32\n\x08response\x18\x01 \x01(\x0b\x32 .xg.cmdcomp.ConfirmationResponse\x12\x10\n\x08redirect\x18\x02 \x01(\x08\x12\x14\n\x0credirectHost\x18\x03 \x01(\t\x12\x14\n\x0credirectPort\x18\x04 \x01(\x07\x12\x10\n\x08\x63mdcomps\x18\x05 \x03(\t\x12\x35\n\tsecondary\x18\x06 \x03(\x0b\x32\".xg.cmdcomp.SecondaryInterfaceList\x12\x17\n\x0fserverSessionId\x18\x07 \x01(\t\x12\x30\n\rsecurityToken\x18\x08 \x01(\x0b\x32\x19.xg.cmdcomp.SecurityToken\"\xa4\x02\n\x1c\x43lientConnectionGCM2Response\x12\x32\n\x08response\x18\x01 \x01(\x0b\x32 .xg.cmdcomp.ConfirmationResponse\x12\x10\n\x08redirect\x18\x02 \x01(\x08\x12\x14\n\x0credirectHost\x18\x03 \x01(\t\x12\x14\n\x0credirectPort\x18\x04 \x01(\x07\x12\x10\n\x08\x63mdcomps\x18\x05 \x03(\t\x12\x35\n\tsecondary\x18\x06 \x03(\x0b\x32\".xg.cmdcomp.SecondaryInterfaceList\x12\x17\n\x0fserverSessionId\x18\x07 \x01(\t\x12\x30\n\rsecurityToken\x18\x08 \x01(\x0b\x32\x19.xg.cmdcomp.SecurityToken\"\xbd\x02\n\x1c\x43lientConnectionSSO2Response\x12\x32\n\x08response\x18\x01 \x01(\x0b\x32 .xg.cmdcomp.ConfirmationResponse\x12 \n\x16pollingIntervalSeconds\x18\x02 \x01(\x05H\x00\x12.\n\x0bsessionInfo\x18\x03 \x01(\x0b\x32\x17.xg.cmdcomp.SessionInfoH\x00\x12\x10\n\x08redirect\x18\x04 \x01(\x08\x12\x14\n\x0credirectHost\x18\x05 \x01(\t\x12\x14\n\x0credirectPort\x18\x06 \x01(\x07\x12\x10\n\x08\x63mdcomps\x18\x07 \x03(\t\x12\x35\n\tsecondary\x18\x08 \x03(\x0b\x32\".xg.cmdcomp.SecondaryInterfaceListB\x10\n\x0eresponse_oneof\"F\n\x13OpenIDAuthenticator\x12\x0e\n\x06issuer\x18\x01 \x01(\t\x12\x10\n\x08\x63lientId\x18\x02 \x01(\t\x12\r\n\x05scope\x18\x03 \x03(\t\"a\n\rAuthenticator\x12>\n\x13openidauthenticator\x18\x01 \x01(\x0b\x32\x1f.xg.cmdcomp.OpenIDAuthenticatorH\x00\x42\x10\n\x0eresponse_oneof\"\'\n\x13\x46\x65tchAuthenticators\x12\x10\n\x08\x64\x61tabase\x18\x01 \x01(\t\"\x83\x01\n\x1b\x46\x65tchAuthenticatorsResponse\x12\x32\n\x08response\x18\x01 \x01(\x0b\x32 .xg.cmdcomp.ConfirmationResponse\x12\x30\n\rauthenticator\x18\x02 \x03(\x0b\x32\x19.xg.cmdcomp.Authenticator\"\x0b\n\tGetSchema\"W\n\x11GetSchemaResponse\x12\x32\n\x08response\x18\x01 \x01(\x0b\x32 .xg.cmdcomp.ConfirmationResponse\x12\x0e\n\x06schema\x18\x02 \x01(\t\"\x1b\n\tSetSchema\x12\x0e\n\x06schema\x18\x01 \x01(\t\"%\n\x0f\x43loseConnection\x12\x12\n\nendSession\x18\x01 \x01(\x08\"\x10\n\x0eTestConnection\" \n\rAttachToQuery\x12\x0f\n\x07queryId\x18\x01 \x01(\t\"\x1f\n\tFetchData\x12\x12\n\nfetch_size\x18\x01 \x01(\x0f\"A\n\tResultSet\x12\x10\n\x08numParts\x18\x01 \x01(\x05\x12\x13\n\x0b\x62lobLengths\x18\x02 \x03(\x05\x12\r\n\x05\x62lobs\x18\x03 \x03(\x0c\"r\n\x11\x46\x65tchDataResponse\x12\x32\n\x08response\x18\x01 \x01(\x0b\x32 .xg.cmdcomp.ConfirmationResponse\x12)\n\nresult_set\x18\x02 \x01(\x0b\x32\x15.xg.cmdcomp.ResultSet\"\x0f\n\rFetchMetadata\"\xb9\x02\n\x15\x46\x65tchMetadataResponse\x12\x32\n\x08response\x18\x01 \x01(\x0b\x32 .xg.cmdcomp.ConfirmationResponse\x12\x41\n\x08\x63ols2pos\x18\x02 \x03(\x0b\x32/.xg.cmdcomp.FetchMetadataResponse.Cols2posEntry\x12\x45\n\ncols2Types\x18\x03 \x03(\x0b\x32\x31.xg.cmdcomp.FetchMetadataResponse.Cols2TypesEntry\x1a/\n\rCols2posEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x0f:\x02\x38\x01\x1a\x31\n\x0f\x43ols2TypesEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"\xde\x04\n\x13\x46\x65tchSystemMetadata\x12@\n\x04\x63\x61ll\x18\x01 \x01(\x0e\x32\x32.xg.cmdcomp.FetchSystemMetadata.SystemMetadataCall\x12\x0e\n\x06schema\x18\x02 \x01(\t\x12\r\n\x05table\x18\x03 \x01(\t\x12\x0e\n\x06\x63olumn\x18\x04 \x01(\t\x12\x0c\n\x04view\x18\x05 \x01(\t\x12\x0c\n\x04test\x18\x06 \x01(\x08\"\xb9\x03\n\x12SystemMetadataCall\x12\x0b\n\x07INVALID\x10\x00\x12\x0f\n\x0bGET_SCHEMAS\x10\x01\x12\x0e\n\nGET_TABLES\x10\x02\x12\x15\n\x11GET_SYSTEM_TABLES\x10\x0e\x12\x18\n\x14GET_TABLE_PRIVILEGES\x10\x0f\x12\x19\n\x15GET_COLUMN_PRIVILEGES\x10\x10\x12\r\n\tGET_VIEWS\x10\x19\x12\x0f\n\x0bGET_COLUMNS\x10\x03\x12\x12\n\x0eGET_INDEX_INFO\x10\x04\x12\x11\n\rGET_TYPE_INFO\x10\x05\x12\x14\n\x10GET_SQL_KEYWORDS\x10\x06\x12\x19\n\x15GET_NUMERIC_FUNCTIONS\x10\x07\x12\x18\n\x14GET_STRING_FUNCTIONS\x10\x08\x12\x1b\n\x17GET_TIME_DATE_FUNCTIONS\x10\t\x12\x18\n\x14GET_SYSTEM_FUNCTIONS\x10\n\x12 \n\x1cGET_DATABASE_PRODUCT_VERSION\x10\x0b\x12\x1e\n\x1aGET_DATABASE_MAJOR_VERSION\x10\x0c\x12\x1e\n\x1aGET_DATABASE_MINOR_VERSION\x10\r\"\xbb\x01\n\x1b\x46\x65tchSystemMetadataResponse\x12\x32\n\x08response\x18\x01 \x01(\x0b\x32 .xg.cmdcomp.ConfirmationResponse\x12/\n\x0eresult_set_val\x18\x02 \x01(\x0b\x32\x15.xg.cmdcomp.ResultSetH\x00\x12\x14\n\nstring_val\x18\x03 \x01(\tH\x00\x12\x11\n\x07int_val\x18\x04 \x01(\x0fH\x00\x42\x0e\n\x0cresult_oneof\"\x10\n\x0e\x43loseResultSet\"w\n\x0c\x45xecuteQuery\x12\x0b\n\x03sql\x18\x01 \x01(\t\x12\r\n\x05\x66orce\x18\x02 \x01(\x08\x12\x15\n\rforceRedirect\x18\x03 \x01(\x08\x12\x34\n\x0fperformanceMode\x18\x04 \x01(\x0e\x32\x1b.xg.cmdcomp.PerformanceMode\"\xb3\x01\n\x14\x45xecuteQueryResponse\x12\x32\n\x08response\x18\x01 \x01(\x0b\x32 .xg.cmdcomp.ConfirmationResponse\x12\x10\n\x08redirect\x18\x02 \x01(\x08\x12\x14\n\x0credirectHost\x18\x03 \x01(\t\x12\x14\n\x0credirectPort\x18\x04 \x01(\x07\x12\x0f\n\x07queryId\x18\x05 \x01(\t\x12\x18\n\x10numClientThreads\x18\x06 \x01(\x07\"+\n\rExecuteUpdate\x12\x0b\n\x03sql\x18\x01 \x01(\t\x12\r\n\x05\x66orce\x18\x02 \x01(\x08\"\xa1\x01\n\x15\x45xecuteUpdateResponse\x12\x32\n\x08response\x18\x01 \x01(\x0b\x32 .xg.cmdcomp.ConfirmationResponse\x12\x16\n\x0eupdateRowCount\x18\x02 \x01(\x0f\x12\x10\n\x08redirect\x18\x03 \x01(\x08\x12\x14\n\x0credirectHost\x18\x04 \x01(\t\x12\x14\n\x0credirectPort\x18\x05 \x01(\x07\"W\n\x0e\x45xecuteExplain\x12\x0b\n\x03sql\x18\x01 \x01(\t\x12\r\n\x05\x66orce\x18\x02 \x01(\x08\x12)\n\x06\x66ormat\x18\x03 \x01(\x0e\x32\x19.xg.cmdcomp.ExplainFormat\"\xdc\x01\n\x16\x45xecuteExplainForSpark\x12\x0b\n\x03sql\x18\x01 \x01(\t\x12\x41\n\x04type\x18\x02 \x01(\x0e\x32\x33.xg.cmdcomp.ExecuteExplainForSpark.PartitioningType\x12\x19\n\x11partitioningParam\x18\x03 \x01(\x0f\x12\r\n\x05\x66orce\x18\x04 \x01(\x08\"H\n\x10PartitioningType\x12\x18\n\x14INVALID_PARTITIONING\x10\x00\x12\x0b\n\x07\x42Y_SIZE\x10\x01\x12\r\n\tBY_NUMBER\x10\x02\"\x9b\x01\n\x19\x45xplainResponseStringPlan\x12\x32\n\x08response\x18\x01 \x01(\x0b\x32 .xg.cmdcomp.ConfirmationResponse\x12\x0c\n\x04plan\x18\x02 \x01(\t\x12\x10\n\x08redirect\x18\x03 \x01(\x08\x12\x14\n\x0credirectHost\x18\x04 \x01(\t\x12\x14\n\x0credirectPort\x18\x05 \x01(\x07\"N\n\x18QueryConcurrencyResponse\x12\x32\n\x08response\x18\x01 \x01(\x0b\x32 .xg.cmdcomp.ConfirmationResponse\"\x13\n\x11SystemWideQueries\"x\n\x19SystemWideQueriesResponse\x12\x32\n\x08response\x18\x01 \x01(\x0b\x32 .xg.cmdcomp.ConfirmationResponse\x12\'\n\x04rows\x18\x02 \x03(\x0b\x32\x19.xg.cmdcomp.SysQueriesRow\"\x87\x02\n\x0cLocalQueries\x12\x14\n\x08identity\x18\x01 \x01(\x05\x42\x02\x18\x01\x12\x1b\n\ruuid_identity\x18\x02 \x01(\x0c\x42\x02\x18\x01H\x00\x12\x10\n\x08\x64\x61tabase\x18\x03 \x01(\t\x12\r\n\x05token\x18\x04 \x01(\x0c\x12\x15\n\tsignature\x18\x05 \x01(\x0c\x42\x02\x18\x01\x12\x1e\n\x12issuer_certificate\x18\x06 \x01(\x0c\x42\x02\x18\x01\x12\x1a\n\x12issuer_fingerprint\x18\x07 \x01(\x0c\x12\x14\n\x08username\x18\x08 \x01(\x0c\x42\x02\x18\x01\x12\x11\n\tcompleted\x18\t \x01(\x08\x12\x10\n\x04user\x18\n \x01(\x0c\x42\x02\x18\x01\x42\x15\n\x13one_identity_option\"s\n\x14LocalQueriesResponse\x12\x32\n\x08response\x18\x01 \x01(\x0b\x32 .xg.cmdcomp.ConfirmationResponse\x12\'\n\x04rows\x18\x02 \x03(\x0b\x32\x19.xg.cmdcomp.SysQueriesRow\"\xd7\x03\n\rSysQueriesRow\x12\x10\n\x08query_id\x18\x01 \x01(\t\x12\x1a\n\x12\x65\x66\x66\x65\x63tive_priority\x18\x02 \x01(\x02\x12\x1a\n\x12\x65stimated_time_sec\x18\x03 \x01(\x05\x12\x0e\n\x06userid\x18\x04 \x01(\t\x12\x10\n\x08sql_text\x18\x05 \x01(\t\x12\x18\n\x10\x65lapsed_time_sec\x18\x06 \x01(\x05\x12\x0e\n\x06status\x18\x07 \x01(\t\x12\x14\n\x0cquery_server\x18\x08 \x01(\t\x12\x10\n\x08\x64\x61tabase\x18\t \x01(\t\x12\x10\n\x08remoteIP\x18\n \x01(\t\x12\x15\n\rservice_class\x18\x0b \x01(\t\x12\x1d\n\x15\x65stimated_result_rows\x18\x0c \x01(\x03\x12\x1d\n\x15\x65stimated_result_size\x18\r \x01(\x03\x12\x11\n\tsent_rows\x18\x0e \x01(\x03\x12\x12\n\nsent_bytes\x18\x0f \x01(\x03\x12\x18\n\x10initial_priority\x18\x10 \x01(\x02\x12\"\n\x1ainitial_effective_priority\x18\x11 \x01(\x02\x12\x1e\n\x16priority_adjust_factor\x18\x12 \x01(\x02\x12\x1c\n\x14priority_adjust_time\x18\x13 \x01(\r\"\x1c\n\x1aSystemWideCompletedQueries\"}\n\x18\x43ompletedQueriesResponse\x12\x32\n\x08response\x18\x01 \x01(\x0b\x32 .xg.cmdcomp.ConfirmationResponse\x12-\n\x04rows\x18\x02 \x03(\x0b\x32\x1f.xg.cmdcomp.CompletedQueriesRow\"\xc0\x05\n\x13\x43ompletedQueriesRow\x12\x0c\n\x04user\x18\x01 \x01(\t\x12\x31\n\x0b\x64\x61tabase_id\x18\x02 \x01(\x0b\x32\x1c.google.protobuf.StringValue\x12\x16\n\x0e\x63lient_version\x18\x03 \x01(\t\x12\x11\n\tclient_ip\x18\x04 \x01(\t\x12\x0b\n\x03sql\x18\x05 \x01(\t\x12\x17\n\x0ftimestamp_start\x18\x06 \x01(\x04\x12\x12\n\ntime_start\x18\x07 \x01(\t\x12\x1a\n\x12timestamp_complete\x18\x08 \x01(\x04\x12\x15\n\rtime_complete\x18\t \x01(\t\x12\x0c\n\x04\x63ode\x18\n \x01(\x05\x12\r\n\x05state\x18\x0b \x01(\t\x12\x0e\n\x06reason\x18\x0c \x01(\t\x12\x1c\n\x14timestamp_exec_start\x18\r \x01(\x04\x12\x17\n\x0ftime_exec_start\x18\x0e \x01(\t\x12\x0c\n\x04uuid\x18\x0f \x01(\t\x12 \n\x18\x66inal_effective_priority\x18\x10 \x01(\x01\x12\x15\n\rcost_estimate\x18\x11 \x01(\x01\x12\x18\n\x10plan_parallelism\x18\x12 \x01(\r\x12\x16\n\x0eheuristic_cost\x18\x13 \x01(\x01\x12\x15\n\rpso_threshold\x18\x14 \x01(\x03\x12\x15\n\rrows_returned\x18\x15 \x01(\x04\x12\x16\n\x0e\x62ytes_returned\x18\x16 \x01(\x04\x12\x0f\n\x07runtime\x18\x17 \x01(\x04\x12 \n\x18temp_disk_space_consumed\x18\x18 \x01(\x04\x12\x1e\n\x16priority_adjust_factor\x18\x19 \x01(\x02\x12\x1c\n\x14priority_adjust_time\x18\x1a \x01(\r\x12\x18\n\x10initial_priority\x18\x1b \x01(\x02\x12\"\n\x1ainitial_effective_priority\x18\x1c \x01(\x02\"\x1f\n\nClearCache\x12\x11\n\tall_nodes\x18\x01 \x01(\x08\"\xc3\x19\n\x07Request\x12-\n\x04type\x18\x01 \x01(\x0e\x32\x1f.xg.cmdcomp.Request.RequestType\x12\x39\n\x11\x63lient_connection\x18\x02 \x01(\x0b\x32\x1c.xg.cmdcomp.ClientConnectionH\x00\x12;\n\x12\x63lient_connection2\x18\x03 \x01(\x0b\x32\x1d.xg.cmdcomp.ClientConnection2H\x00\x12+\n\nget_schema\x18\x04 \x01(\x0b\x32\x15.xg.cmdcomp.GetSchemaH\x00\x12\x37\n\x10\x63lose_connection\x18\x05 \x01(\x0b\x32\x1b.xg.cmdcomp.CloseConnectionH\x00\x12+\n\nset_schema\x18\x06 \x01(\x0b\x32\x15.xg.cmdcomp.SetSchemaH\x00\x12\x35\n\x0ftest_connection\x18\x07 \x01(\x0b\x32\x1a.xg.cmdcomp.TestConnectionH\x00\x12+\n\nfetch_data\x18\x08 \x01(\x0b\x32\x15.xg.cmdcomp.FetchDataH\x00\x12\x33\n\x0e\x66\x65tch_metadata\x18\t \x01(\x0b\x32\x19.xg.cmdcomp.FetchMetadataH\x00\x12\x36\n\x10\x63lose_result_set\x18\n \x01(\x0b\x32\x1a.xg.cmdcomp.CloseResultSetH\x00\x12\x31\n\rexecute_query\x18\x0b \x01(\x0b\x32\x18.xg.cmdcomp.ExecuteQueryH\x00\x12\x35\n\x0f\x65xecute_explain\x18\x0c \x01(\x0b\x32\x1a.xg.cmdcomp.ExecuteExplainH\x00\x12G\n\x19\x65xecute_explain_for_spark\x18\r \x01(\x0b\x32\".xg.cmdcomp.ExecuteExplainForSparkH\x00\x12\x33\n\x0e\x65xecute_update\x18\x0e \x01(\x0b\x32\x19.xg.cmdcomp.ExecuteUpdateH\x00\x12@\n\x15\x66\x65tch_system_metadata\x18\x10 \x01(\x0b\x32\x1f.xg.cmdcomp.FetchSystemMetadataH\x00\x12/\n\x0c\x63\x61ncel_query\x18\x11 \x01(\x0b\x32\x17.xg.cmdcomp.CancelQueryH\x00\x12<\n\x13system_wide_queries\x18\x12 \x01(\x0b\x32\x1d.xg.cmdcomp.SystemWideQueriesH\x00\x12\x31\n\rlocal_queries\x18\x13 \x01(\x0b\x32\x18.xg.cmdcomp.LocalQueriesH\x00\x12O\n\x1dsystem_wide_completed_queries\x18\x1f \x01(\x0b\x32&.xg.cmdcomp.SystemWideCompletedQueriesH\x00\x12/\n\x0c\x65xecute_plan\x18\x14 \x01(\x0b\x32\x17.xg.cmdcomp.ExecutePlanH\x00\x12/\n\x0c\x65xplain_plan\x18\x15 \x01(\x0b\x32\x17.xg.cmdcomp.ExplainPlanH\x00\x12)\n\tlist_plan\x18\x16 \x01(\x0b\x32\x14.xg.cmdcomp.ListPlanH\x00\x12+\n\nkill_query\x18\x17 \x01(\x0b\x32\x15.xg.cmdcomp.KillQueryH\x00\x12<\n\x13\x65xecute_inline_plan\x18\x18 \x01(\x0b\x32\x1d.xg.cmdcomp.ExecuteInlinePlanH\x00\x12\x37\n\x0e\x66orce_external\x18\x19 \x01(\x0b\x32\x19.xg.cmdcomp.ForceExternalB\x02\x18\x01H\x00\x12\x33\n\x0e\x65xecute_export\x18\x1a \x01(\x0b\x32\x19.xg.cmdcomp.ExecuteExportH\x00\x12%\n\x07set_pso\x18\x1b \x01(\x0b\x32\x12.xg.cmdcomp.SetPSOH\x00\x12\x34\n\x0f\x61ttach_to_query\x18\x1e \x01(\x0b\x32\x19.xg.cmdcomp.AttachToQueryH\x00\x12\x31\n\rset_parameter\x18# \x01(\x0b\x32\x18.xg.cmdcomp.SetParameterH\x00\x12>\n\x10\x65xplain_pipeline\x18$ \x01(\x0b\x32\".xg.cmdcomp.ExplainPipelineRequestH\x00\x12@\n\x15\x63lient_connection_gcm\x18% \x01(\x0b\x32\x1f.xg.cmdcomp.ClientConnectionGCMH\x00\x12\x42\n\x16\x63lient_connection_gcm2\x18& \x01(\x0b\x32 .xg.cmdcomp.ClientConnectionGCM2H\x00\x12\x36\n\ncheck_data\x18\' \x01(\x0b\x32\x1c.xg.cmdcomp.CheckDataRequestB\x02\x18\x01H\x00\x12-\n\x0b\x63lear_cache\x18) \x01(\x0b\x32\x16.xg.cmdcomp.ClearCacheH\x00\x12@\n\x15\x63lient_connection_sso\x18* \x01(\x0b\x32\x1f.xg.cmdcomp.ClientConnectionSSOH\x00\x12\x42\n\x16\x63lient_connection_sso2\x18+ \x01(\x0b\x32 .xg.cmdcomp.ClientConnectionSSO2H\x00\x12U\n client_connection_security_token\x18, \x01(\x0b\x32).xg.cmdcomp.ClientConnectionSecurityTokenH\x00\x12W\n!client_connection_refresh_session\x18- \x01(\x0b\x32*.xg.cmdcomp.ClientConnectionRefreshSessionH\x00\x12S\n\x1f\x63lient_connection_refresh_token\x18. \x01(\x0b\x32(.xg.cmdcomp.ClientConnectionRefreshTokenH\x00\x12?\n\x14\x66\x65tch_authenticators\x18\x33 \x01(\x0b\x32\x1f.xg.cmdcomp.FetchAuthenticatorsH\x00\"\x8f\x07\n\x0bRequestType\x12\x0b\n\x07INVALID\x10\x00\x12\x15\n\x11\x43LIENT_CONNECTION\x10\x01\x12\x16\n\x12\x43LIENT_CONNECTION2\x10\x02\x12\x0e\n\nGET_SCHEMA\x10\x03\x12\x14\n\x10\x43LOSE_CONNECTION\x10\x04\x12\x0e\n\nSET_SCHEMA\x10\x05\x12\x13\n\x0fTEST_CONNECTION\x10\x06\x12\x0e\n\nFETCH_DATA\x10\x07\x12\x12\n\x0e\x46\x45TCH_METADATA\x10\x08\x12\x14\n\x10\x43LOSE_RESULT_SET\x10\t\x12\x11\n\rEXECUTE_QUERY\x10\n\x12\x13\n\x0f\x45XECUTE_EXPLAIN\x10\x0b\x12\x1d\n\x19\x45XECUTE_EXPLAIN_FOR_SPARK\x10\x0c\x12\x12\n\x0e\x45XECUTE_UPDATE\x10\r\x12\x19\n\x15\x46\x45TCH_SYSTEM_METADATA\x10\x0f\x12\x10\n\x0c\x43\x41NCEL_QUERY\x10\x10\x12\x17\n\x13SYSTEM_WIDE_QUERIES\x10\x11\x12\x11\n\rLOCAL_QUERIES\x10\x12\x12!\n\x1dSYSTEM_WIDE_COMPLETED_QUERIES\x10\x1e\x12\x10\n\x0c\x45XECUTE_PLAN\x10\x13\x12\x10\n\x0c\x45XPLAIN_PLAN\x10\x14\x12\r\n\tLIST_PLAN\x10\x15\x12\x0e\n\nKILL_QUERY\x10\x16\x12\x17\n\x13\x45XECUTE_INLINE_PLAN\x10\x17\x12\x12\n\x0e\x46ORCE_EXTERNAL\x10\x18\x12\x12\n\x0e\x45XECUTE_EXPORT\x10\x19\x12\x0b\n\x07SET_PSO\x10\x1a\x12\x13\n\x0f\x41TTACH_TO_QUERY\x10\x1d\x12\x11\n\rSET_PARAMETER\x10\"\x12\x14\n\x10\x45XPLAIN_PIPELINE\x10#\x12\x19\n\x15\x43LIENT_CONNECTION_GCM\x10$\x12\x1a\n\x16\x43LIENT_CONNECTION_GCM2\x10%\x12\x0e\n\nCHECK_DATA\x10&\x12\x0f\n\x0b\x43LEAR_CACHE\x10(\x12\x19\n\x15\x43LIENT_CONNECTION_SSO\x10)\x12\x1a\n\x16\x43LIENT_CONNECTION_SSO2\x10*\x12$\n CLIENT_CONNECTION_SECURITY_TOKEN\x10+\x12%\n!CLIENT_CONNECTION_REFRESH_SESSION\x10,\x12#\n\x1f\x43LIENT_CONNECTION_REFRESH_TOKEN\x10-\x12\x18\n\x14\x46\x45TCH_AUTHENTICATORS\x10\x32\x42\x0f\n\rrequest_oneof\"\xe0\x01\n\x14\x43onfirmationResponse\x12;\n\x04type\x18\x01 \x01(\x0e\x32-.xg.cmdcomp.ConfirmationResponse.ResponseType\x12\x0e\n\x06reason\x18\x02 \x01(\t\x12\x11\n\tsql_state\x18\x03 \x01(\t\x12\x13\n\x0bvendor_code\x18\x04 \x01(\x0f\"S\n\x0cResponseType\x12\x0b\n\x07INVALID\x10\x00\x12\x0f\n\x0bRESPONSE_OK\x10\x01\x12\x11\n\rRESPONSE_WARN\x10\x02\x12\x12\n\x0eRESPONSE_ERROR\x10\x03\")\n\x0b\x45xecutePlan\x12\x0b\n\x03sql\x18\x01 \x01(\t\x12\r\n\x05\x66orce\x18\x02 \x01(\x08\"/\n\x11\x45xecuteInlinePlan\x12\x0b\n\x03sql\x18\x01 \x01(\t\x12\r\n\x05\x66orce\x18\x02 \x01(\x08\"T\n\x0b\x45xplainPlan\x12\x0b\n\x03sql\x18\x01 \x01(\t\x12\r\n\x05\x66orce\x18\x02 \x01(\x08\x12)\n\x06\x66ormat\x18\x03 \x01(\x0e\x32\x19.xg.cmdcomp.ExplainFormat\"\"\n\rForceExternal\x12\r\n\x05\x66orce\x18\x01 \x01(\x08:\x02\x18\x01\"\n\n\x08ListPlan\"\x96\x01\n\x10ListPlanResponse\x12\x32\n\x08response\x18\x01 \x01(\x0b\x32 .xg.cmdcomp.ConfirmationResponse\x12\x10\n\x08planName\x18\x02 \x03(\t\x12\x10\n\x08redirect\x18\x03 \x01(\x08\x12\x14\n\x0credirectHost\x18\x04 \x01(\t\x12\x14\n\x0credirectPort\x18\x05 \x01(\x07\"\x1a\n\x0b\x43\x61ncelQuery\x12\x0b\n\x03sql\x18\x01 \x01(\t\"I\n\x13\x43\x61ncelQueryResponse\x12\x32\n\x08response\x18\x01 \x01(\x0b\x32 .xg.cmdcomp.ConfirmationResponse\"\x18\n\tKillQuery\x12\x0b\n\x03sql\x18\x01 \x01(\t\"G\n\x11KillQueryResponse\x12\x32\n\x08response\x18\x01 \x01(\x0b\x32 .xg.cmdcomp.ConfirmationResponse\"+\n\rExecuteExport\x12\x0b\n\x03sql\x18\x01 \x01(\t\x12\r\n\x05\x66orce\x18\x02 \x01(\x08\"\xa2\x01\n\x15\x45xecuteExportResponse\x12\x32\n\x08response\x18\x01 \x01(\x0b\x32 .xg.cmdcomp.ConfirmationResponse\x12\x17\n\x0f\x65xportStatement\x18\x02 \x01(\t\x12\x10\n\x08redirect\x18\x03 \x01(\x08\x12\x14\n\x0credirectHost\x18\x04 \x01(\t\x12\x14\n\x0credirectPort\x18\x05 \x01(\x07\"4\n\x16\x45xplainPipelineRequest\x12\x0b\n\x03sql\x18\x01 \x01(\t\x12\r\n\x05\x66orce\x18\x02 \x01(\x08\"\xa6\x01\n\x17\x45xplainPipelineResponse\x12\x32\n\x08response\x18\x01 \x01(\x0b\x32 .xg.cmdcomp.ConfirmationResponse\x12\x19\n\x11pipelineStatement\x18\x02 \x01(\t\x12\x10\n\x08redirect\x18\x03 \x01(\x08\x12\x14\n\x0credirectHost\x18\x04 \x01(\t\x12\x14\n\x0credirectPort\x18\x05 \x01(\x07\".\n\x10\x43heckDataRequest\x12\x0b\n\x03sql\x18\x01 \x01(\t\x12\r\n\x05\x66orce\x18\x02 \x01(\x08\"\xa1\x01\n\x11\x43heckDataResponse\x12\x32\n\x08response\x18\x01 \x01(\x0b\x32 .xg.cmdcomp.ConfirmationResponse\x12\x1a\n\x12\x63heckDataStatement\x18\x02 \x01(\t\x12\x10\n\x08redirect\x18\x03 \x01(\x08\x12\x14\n\x0credirectHost\x18\x04 \x01(\t\x12\x14\n\x0credirectPort\x18\x05 \x01(\x07\"*\n\x06SetPSO\x12\x11\n\tthreshold\x18\x01 \x01(\x03\x12\r\n\x05reset\x18\x02 \x01(\x08\"\xf0\n\n\x0cSetParameter\x12\r\n\x05reset\x18\x01 \x01(\x08\x12\x35\n\rpso_threshold\x18\x02 \x01(\x0b\x32\x1c.xg.cmdcomp.SetParameter.PSOH\x00\x12\x36\n\trow_limit\x18\x03 \x01(\x0b\x32!.xg.cmdcomp.SetParameter.RowLimitH\x00\x12\x38\n\ntime_limit\x18\x04 \x01(\x0b\x32\".xg.cmdcomp.SetParameter.TimeLimitH\x00\x12\x44\n\x0ftemp_disk_limit\x18\x05 \x01(\x0b\x32).xg.cmdcomp.SetParameter.MaxTempDiskLimitH\x00\x12\x35\n\x08priority\x18\x06 \x01(\x0b\x32!.xg.cmdcomp.SetParameter.PriorityH\x00\x12;\n\x0b\x63oncurrency\x18\x07 \x01(\x0b\x32$.xg.cmdcomp.SetParameter.ConcurrencyH\x00\x12\x34\n\x08pso_seed\x18\x08 \x01(\x0b\x32 .xg.cmdcomp.SetParameter.PSOSeedH\x00\x12P\n\x17result_set_column_limit\x18\t \x01(\x0b\x32-.xg.cmdcomp.SetParameter.ResultSetColumnLimitH\x00\x12@\n\x0e\x66orce_external\x18\n \x01(\x0b\x32&.xg.cmdcomp.SetParameter.ForceExternalH\x00\x12O\n\x16priority_adjust_factor\x18\x0b \x01(\x0b\x32-.xg.cmdcomp.SetParameter.PriorityAdjustFactorH\x00\x12K\n\x14priority_adjust_time\x18\x0c \x01(\x0b\x32+.xg.cmdcomp.SetParameter.PriorityAdjustTimeH\x00\x12G\n\x12service_class_name\x18\r \x01(\x0b\x32).xg.cmdcomp.SetParameter.ServiceClassNameH\x00\x12@\n\x0ememory_tracing\x18\x0e \x01(\x0b\x32&.xg.cmdcomp.SetParameter.MemoryTracingH\x00\x1a\x18\n\x03PSO\x12\x11\n\tthreshold\x18\x01 \x01(\x03\x1a\x1c\n\x08RowLimit\x12\x10\n\x08rowLimit\x18\x01 \x01(\x03\x1a\x1e\n\tTimeLimit\x12\x11\n\ttimeLimit\x18\x01 \x01(\x03\x1a)\n\x10MaxTempDiskLimit\x12\x15\n\rtempDiskLimit\x18\x01 \x01(\x03\x1a\x34\n\x14ResultSetColumnLimit\x12\x1c\n\x14resultSetColumnLimit\x18\x01 \x01(\x03\x1a\x1c\n\x08Priority\x12\x10\n\x08priority\x18\x01 \x01(\x01\x1a\"\n\x0b\x43oncurrency\x12\x13\n\x0b\x63oncurrency\x18\x01 \x01(\x03\x1a\x17\n\x07PSOSeed\x12\x0c\n\x04seed\x18\x01 \x01(\x04\x1a\x1e\n\rForceExternal\x12\r\n\x05is_on\x18\x01 \x01(\x08\x1a\x36\n\x14PriorityAdjustFactor\x12\x1e\n\x16priority_adjust_factor\x18\x01 \x01(\x01\x1a\x32\n\x12PriorityAdjustTime\x12\x1c\n\x14priority_adjust_time\x18\x01 \x01(\r\x1a.\n\x10ServiceClassName\x12\x1a\n\x12service_class_name\x18\x01 \x01(\t\x1a\x1e\n\rMemoryTracing\x12\r\n\x05is_on\x18\x01 \x01(\x08\x42\x0b\n\tParameter*4\n\x0fPerformanceMode\x12\x07\n\x03OFF\x10\x00\x12\x18\n\x14ROOT_OP_INST_DISCARD\x10\x01*/\n\rExplainFormat\x12\t\n\x05PROTO\x10\x00\x12\x08\n\x04JSON\x10\x01\x12\t\n\x05\x44\x45\x42UG\x10\x02*1\n\x0cServerSignal\x12\x0b\n\x07INVALID\x10\x00\x12\x14\n\x07QUIESCE\x10\xff\xff\xff\xff\xff\xff\xff\xff\xff\x01\x42\x17\n\x15\x63om.ocient.jdbc.protob\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'sharedMessages.clientWireProtocol_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\025com.ocient.jdbc.proto'
  _FETCHMETADATARESPONSE_COLS2POSENTRY._options = None
  _FETCHMETADATARESPONSE_COLS2POSENTRY._serialized_options = b'8\001'
  _FETCHMETADATARESPONSE_COLS2TYPESENTRY._options = None
  _FETCHMETADATARESPONSE_COLS2TYPESENTRY._serialized_options = b'8\001'
  _LOCALQUERIES.fields_by_name['identity']._options = None
  _LOCALQUERIES.fields_by_name['identity']._serialized_options = b'\030\001'
  _LOCALQUERIES.fields_by_name['uuid_identity']._options = None
  _LOCALQUERIES.fields_by_name['uuid_identity']._serialized_options = b'\030\001'
  _LOCALQUERIES.fields_by_name['signature']._options = None
  _LOCALQUERIES.fields_by_name['signature']._serialized_options = b'\030\001'
  _LOCALQUERIES.fields_by_name['issuer_certificate']._options = None
  _LOCALQUERIES.fields_by_name['issuer_certificate']._serialized_options = b'\030\001'
  _LOCALQUERIES.fields_by_name['username']._options = None
  _LOCALQUERIES.fields_by_name['username']._serialized_options = b'\030\001'
  _LOCALQUERIES.fields_by_name['user']._options = None
  _LOCALQUERIES.fields_by_name['user']._serialized_options = b'\030\001'
  _REQUEST.fields_by_name['force_external']._options = None
  _REQUEST.fields_by_name['force_external']._serialized_options = b'\030\001'
  _REQUEST.fields_by_name['check_data']._options = None
  _REQUEST.fields_by_name['check_data']._serialized_options = b'\030\001'
  _FORCEEXTERNAL._options = None
  _FORCEEXTERNAL._serialized_options = b'\030\001'
  _globals['_PERFORMANCEMODE']._serialized_start=14372
  _globals['_PERFORMANCEMODE']._serialized_end=14424
  _globals['_EXPLAINFORMAT']._serialized_start=14426
  _globals['_EXPLAINFORMAT']._serialized_end=14473
  _globals['_SERVERSIGNAL']._serialized_start=14475
  _globals['_SERVERSIGNAL']._serialized_end=14524
  _globals['_CLIENTCONNECTION']._serialized_start=88
  _globals['_CLIENTCONNECTION']._serialized_end=278
  _globals['_CLIENTCONNECTIONGCM']._serialized_start=281
  _globals['_CLIENTCONNECTIONGCM']._serialized_end=495
  _globals['_CLIENTCONNECTIONSSO']._serialized_start=498
  _globals['_CLIENTCONNECTIONSSO']._serialized_end=675
  _globals['_CLIENTCONNECTIONSECURITYTOKEN']._serialized_start=678
  _globals['_CLIENTCONNECTIONSECURITYTOKEN']._serialized_end=954
  _globals['_CLIENTCONNECTIONRESPONSE']._serialized_start=956
  _globals['_CLIENTCONNECTIONRESPONSE']._serialized_end=1062
  _globals['_CLIENTCONNECTIONGCMRESPONSE']._serialized_start=1064
  _globals['_CLIENTCONNECTIONGCMRESPONSE']._serialized_end=1173
  _globals['_CLIENTCONNECTIONSSORESPONSE']._serialized_start=1175
  _globals['_CLIENTCONNECTIONSSORESPONSE']._serialized_end=1292
  _globals['_CLIENTCONNECTIONSECURITYTOKENRESPONSE']._serialized_start=1295
  _globals['_CLIENTCONNECTIONSECURITYTOKENRESPONSE']._serialized_end=1546
  _globals['_CLIENTCONNECTION2']._serialized_start=1548
  _globals['_CLIENTCONNECTION2']._serialized_end=1628
  _globals['_CLIENTCONNECTIONGCM2']._serialized_start=1630
  _globals['_CLIENTCONNECTIONGCM2']._serialized_end=1734
  _globals['_CLIENTCONNECTIONSSO2']._serialized_start=1736
  _globals['_CLIENTCONNECTIONSSO2']._serialized_end=1792
  _globals['_SECURITYTOKEN']._serialized_start=1794
  _globals['_SECURITYTOKEN']._serialized_end=1869
  _globals['_SESSIONINFO']._serialized_start=1871
  _globals['_SESSIONINFO']._serialized_end=1959
  _globals['_CLIENTCONNECTIONREFRESHSESSION']._serialized_start=1961
  _globals['_CLIENTCONNECTIONREFRESHSESSION']._serialized_end=1993
  _globals['_CLIENTCONNECTIONREFRESHSESSIONRESPONSE']._serialized_start=1996
  _globals['_CLIENTCONNECTIONREFRESHSESSIONRESPONSE']._serialized_end=2134
  _globals['_CLIENTCONNECTIONREFRESHTOKEN']._serialized_start=2136
  _globals['_CLIENTCONNECTIONREFRESHTOKEN']._serialized_end=2219
  _globals['_CLIENTCONNECTIONREFRESHTOKENRESPONSE']._serialized_start=2222
  _globals['_CLIENTCONNECTIONREFRESHTOKENRESPONSE']._serialized_end=2365
  _globals['_SECONDARYINTERFACELIST']._serialized_start=2367
  _globals['_SECONDARYINTERFACELIST']._serialized_end=2408
  _globals['_CLIENTCONNECTION2RESPONSE']._serialized_start=2411
  _globals['_CLIENTCONNECTION2RESPONSE']._serialized_end=2700
  _globals['_CLIENTCONNECTIONGCM2RESPONSE']._serialized_start=2703
  _globals['_CLIENTCONNECTIONGCM2RESPONSE']._serialized_end=2995
  _globals['_CLIENTCONNECTIONSSO2RESPONSE']._serialized_start=2998
  _globals['_CLIENTCONNECTIONSSO2RESPONSE']._serialized_end=3315
  _globals['_OPENIDAUTHENTICATOR']._serialized_start=3317
  _globals['_OPENIDAUTHENTICATOR']._serialized_end=3387
  _globals['_AUTHENTICATOR']._serialized_start=3389
  _globals['_AUTHENTICATOR']._serialized_end=3486
  _globals['_FETCHAUTHENTICATORS']._serialized_start=3488
  _globals['_FETCHAUTHENTICATORS']._serialized_end=3527
  _globals['_FETCHAUTHENTICATORSRESPONSE']._serialized_start=3530
  _globals['_FETCHAUTHENTICATORSRESPONSE']._serialized_end=3661
  _globals['_GETSCHEMA']._serialized_start=3663
  _globals['_GETSCHEMA']._serialized_end=3674
  _globals['_GETSCHEMARESPONSE']._serialized_start=3676
  _globals['_GETSCHEMARESPONSE']._serialized_end=3763
  _globals['_SETSCHEMA']._serialized_start=3765
  _globals['_SETSCHEMA']._serialized_end=3792
  _globals['_CLOSECONNECTION']._serialized_start=3794
  _globals['_CLOSECONNECTION']._serialized_end=3831
  _globals['_TESTCONNECTION']._serialized_start=3833
  _globals['_TESTCONNECTION']._serialized_end=3849
  _globals['_ATTACHTOQUERY']._serialized_start=3851
  _globals['_ATTACHTOQUERY']._serialized_end=3883
  _globals['_FETCHDATA']._serialized_start=3885
  _globals['_FETCHDATA']._serialized_end=3916
  _globals['_RESULTSET']._serialized_start=3918
  _globals['_RESULTSET']._serialized_end=3983
  _globals['_FETCHDATARESPONSE']._serialized_start=3985
  _globals['_FETCHDATARESPONSE']._serialized_end=4099
  _globals['_FETCHMETADATA']._serialized_start=4101
  _globals['_FETCHMETADATA']._serialized_end=4116
  _globals['_FETCHMETADATARESPONSE']._serialized_start=4119
  _globals['_FETCHMETADATARESPONSE']._serialized_end=4432
  _globals['_FETCHMETADATARESPONSE_COLS2POSENTRY']._serialized_start=4334
  _globals['_FETCHMETADATARESPONSE_COLS2POSENTRY']._serialized_end=4381
  _globals['_FETCHMETADATARESPONSE_COLS2TYPESENTRY']._serialized_start=4383
  _globals['_FETCHMETADATARESPONSE_COLS2TYPESENTRY']._serialized_end=4432
  _globals['_FETCHSYSTEMMETADATA']._serialized_start=4435
  _globals['_FETCHSYSTEMMETADATA']._serialized_end=5041
  _globals['_FETCHSYSTEMMETADATA_SYSTEMMETADATACALL']._serialized_start=4600
  _globals['_FETCHSYSTEMMETADATA_SYSTEMMETADATACALL']._serialized_end=5041
  _globals['_FETCHSYSTEMMETADATARESPONSE']._serialized_start=5044
  _globals['_FETCHSYSTEMMETADATARESPONSE']._serialized_end=5231
  _globals['_CLOSERESULTSET']._serialized_start=5233
  _globals['_CLOSERESULTSET']._serialized_end=5249
  _globals['_EXECUTEQUERY']._serialized_start=5251
  _globals['_EXECUTEQUERY']._serialized_end=5370
  _globals['_EXECUTEQUERYRESPONSE']._serialized_start=5373
  _globals['_EXECUTEQUERYRESPONSE']._serialized_end=5552
  _globals['_EXECUTEUPDATE']._serialized_start=5554
  _globals['_EXECUTEUPDATE']._serialized_end=5597
  _globals['_EXECUTEUPDATERESPONSE']._serialized_start=5600
  _globals['_EXECUTEUPDATERESPONSE']._serialized_end=5761
  _globals['_EXECUTEEXPLAIN']._serialized_start=5763
  _globals['_EXECUTEEXPLAIN']._serialized_end=5850
  _globals['_EXECUTEEXPLAINFORSPARK']._serialized_start=5853
  _globals['_EXECUTEEXPLAINFORSPARK']._serialized_end=6073
  _globals['_EXECUTEEXPLAINFORSPARK_PARTITIONINGTYPE']._serialized_start=6001
  _globals['_EXECUTEEXPLAINFORSPARK_PARTITIONINGTYPE']._serialized_end=6073
  _globals['_EXPLAINRESPONSESTRINGPLAN']._serialized_start=6076
  _globals['_EXPLAINRESPONSESTRINGPLAN']._serialized_end=6231
  _globals['_QUERYCONCURRENCYRESPONSE']._serialized_start=6233
  _globals['_QUERYCONCURRENCYRESPONSE']._serialized_end=6311
  _globals['_SYSTEMWIDEQUERIES']._serialized_start=6313
  _globals['_SYSTEMWIDEQUERIES']._serialized_end=6332
  _globals['_SYSTEMWIDEQUERIESRESPONSE']._serialized_start=6334
  _globals['_SYSTEMWIDEQUERIESRESPONSE']._serialized_end=6454
  _globals['_LOCALQUERIES']._serialized_start=6457
  _globals['_LOCALQUERIES']._serialized_end=6720
  _globals['_LOCALQUERIESRESPONSE']._serialized_start=6722
  _globals['_LOCALQUERIESRESPONSE']._serialized_end=6837
  _globals['_SYSQUERIESROW']._serialized_start=6840
  _globals['_SYSQUERIESROW']._serialized_end=7311
  _globals['_SYSTEMWIDECOMPLETEDQUERIES']._serialized_start=7313
  _globals['_SYSTEMWIDECOMPLETEDQUERIES']._serialized_end=7341
  _globals['_COMPLETEDQUERIESRESPONSE']._serialized_start=7343
  _globals['_COMPLETEDQUERIESRESPONSE']._serialized_end=7468
  _globals['_COMPLETEDQUERIESROW']._serialized_start=7471
  _globals['_COMPLETEDQUERIESROW']._serialized_end=8175
  _globals['_CLEARCACHE']._serialized_start=8177
  _globals['_CLEARCACHE']._serialized_end=8208
  _globals['_REQUEST']._serialized_start=8211
  _globals['_REQUEST']._serialized_end=11478
  _globals['_REQUEST_REQUESTTYPE']._serialized_start=10550
  _globals['_REQUEST_REQUESTTYPE']._serialized_end=11461
  _globals['_CONFIRMATIONRESPONSE']._serialized_start=11481
  _globals['_CONFIRMATIONRESPONSE']._serialized_end=11705
  _globals['_CONFIRMATIONRESPONSE_RESPONSETYPE']._serialized_start=11622
  _globals['_CONFIRMATIONRESPONSE_RESPONSETYPE']._serialized_end=11705
  _globals['_EXECUTEPLAN']._serialized_start=11707
  _globals['_EXECUTEPLAN']._serialized_end=11748
  _globals['_EXECUTEINLINEPLAN']._serialized_start=11750
  _globals['_EXECUTEINLINEPLAN']._serialized_end=11797
  _globals['_EXPLAINPLAN']._serialized_start=11799
  _globals['_EXPLAINPLAN']._serialized_end=11883
  _globals['_FORCEEXTERNAL']._serialized_start=11885
  _globals['_FORCEEXTERNAL']._serialized_end=11919
  _globals['_LISTPLAN']._serialized_start=11921
  _globals['_LISTPLAN']._serialized_end=11931
  _globals['_LISTPLANRESPONSE']._serialized_start=11934
  _globals['_LISTPLANRESPONSE']._serialized_end=12084
  _globals['_CANCELQUERY']._serialized_start=12086
  _globals['_CANCELQUERY']._serialized_end=12112
  _globals['_CANCELQUERYRESPONSE']._serialized_start=12114
  _globals['_CANCELQUERYRESPONSE']._serialized_end=12187
  _globals['_KILLQUERY']._serialized_start=12189
  _globals['_KILLQUERY']._serialized_end=12213
  _globals['_KILLQUERYRESPONSE']._serialized_start=12215
  _globals['_KILLQUERYRESPONSE']._serialized_end=12286
  _globals['_EXECUTEEXPORT']._serialized_start=12288
  _globals['_EXECUTEEXPORT']._serialized_end=12331
  _globals['_EXECUTEEXPORTRESPONSE']._serialized_start=12334
  _globals['_EXECUTEEXPORTRESPONSE']._serialized_end=12496
  _globals['_EXPLAINPIPELINEREQUEST']._serialized_start=12498
  _globals['_EXPLAINPIPELINEREQUEST']._serialized_end=12550
  _globals['_EXPLAINPIPELINERESPONSE']._serialized_start=12553
  _globals['_EXPLAINPIPELINERESPONSE']._serialized_end=12719
  _globals['_CHECKDATAREQUEST']._serialized_start=12721
  _globals['_CHECKDATAREQUEST']._serialized_end=12767
  _globals['_CHECKDATARESPONSE']._serialized_start=12770
  _globals['_CHECKDATARESPONSE']._serialized_end=12931
  _globals['_SETPSO']._serialized_start=12933
  _globals['_SETPSO']._serialized_end=12975
  _globals['_SETPARAMETER']._serialized_start=12978
  _globals['_SETPARAMETER']._serialized_end=14370
  _globals['_SETPARAMETER_PSO']._serialized_start=13863
  _globals['_SETPARAMETER_PSO']._serialized_end=13887
  _globals['_SETPARAMETER_ROWLIMIT']._serialized_start=13889
  _globals['_SETPARAMETER_ROWLIMIT']._serialized_end=13917
  _globals['_SETPARAMETER_TIMELIMIT']._serialized_start=13919
  _globals['_SETPARAMETER_TIMELIMIT']._serialized_end=13949
  _globals['_SETPARAMETER_MAXTEMPDISKLIMIT']._serialized_start=13951
  _globals['_SETPARAMETER_MAXTEMPDISKLIMIT']._serialized_end=13992
  _globals['_SETPARAMETER_RESULTSETCOLUMNLIMIT']._serialized_start=13994
  _globals['_SETPARAMETER_RESULTSETCOLUMNLIMIT']._serialized_end=14046
  _globals['_SETPARAMETER_PRIORITY']._serialized_start=14048
  _globals['_SETPARAMETER_PRIORITY']._serialized_end=14076
  _globals['_SETPARAMETER_CONCURRENCY']._serialized_start=14078
  _globals['_SETPARAMETER_CONCURRENCY']._serialized_end=14112
  _globals['_SETPARAMETER_PSOSEED']._serialized_start=14114
  _globals['_SETPARAMETER_PSOSEED']._serialized_end=14137
  _globals['_SETPARAMETER_FORCEEXTERNAL']._serialized_start=14139
  _globals['_SETPARAMETER_FORCEEXTERNAL']._serialized_end=14169
  _globals['_SETPARAMETER_PRIORITYADJUSTFACTOR']._serialized_start=14171
  _globals['_SETPARAMETER_PRIORITYADJUSTFACTOR']._serialized_end=14225
  _globals['_SETPARAMETER_PRIORITYADJUSTTIME']._serialized_start=14227
  _globals['_SETPARAMETER_PRIORITYADJUSTTIME']._serialized_end=14277
  _globals['_SETPARAMETER_SERVICECLASSNAME']._serialized_start=14279
  _globals['_SETPARAMETER_SERVICECLASSNAME']._serialized_end=14325
  _globals['_SETPARAMETER_MEMORYTRACING']._serialized_start=14327
  _globals['_SETPARAMETER_MEMORYTRACING']._serialized_end=14357
# @@protoc_insertion_point(module_scope)

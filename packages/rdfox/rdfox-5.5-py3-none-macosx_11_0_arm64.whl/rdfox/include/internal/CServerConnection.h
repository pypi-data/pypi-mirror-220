// Copyright 2021 by Oxford Semantic Technologies Limited.

CRDFOX void CServerConnection_destroy(CServerConnection* serverConnection);

CRDFOX const CException* CServerConnection_newServerConnection(const char* roleName, const char* password, CServerConnection** serverConnection);

CRDFOX const CException* CServerConnection_newDataStoreConnection(CServerConnection* serverConnection, const char* dataStoreName, CDataStoreConnection** dataStoreConnection);

CRDFOX const CException* CServerConnection_createDataStore(CServerConnection* serverConnection, const char* dataStoreName, const CParameters* dataStoreParameters);

CRDFOX const CException* CServerConnection_deleteDataStore(CServerConnection* serverConnection, const char* dataStoreName);

CRDFOX const CException* CServerConnection_getNumberOfThreads(CServerConnection* serverConnection, size_t* numberOfThreads);

CRDFOX const CException* CServerConnection_setNumberOfThreads(CServerConnection* serverConnection, size_t numberOfThreads);

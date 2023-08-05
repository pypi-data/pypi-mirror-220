// Copyright 2021 by Oxford Semantic Technologies Limited.

CRDFOX const CException* CServer_startLocalServer(const CParameters* parameters);

CRDFOX const CException* CServer_getNumberOfLocalServerRoles(size_t* numberOfRoles);

CRDFOX const CException* CServer_createFirstLocalServerRole(const char* firstRoleName, const char* password);

CRDFOX void CServer_stopLocalServer();

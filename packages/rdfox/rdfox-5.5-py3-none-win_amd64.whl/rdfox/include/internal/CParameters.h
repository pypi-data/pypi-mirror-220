// Copyright 2021 by Oxford Semantic Technologies Limited.

CRDFOX const CParameters* CParameters_getEmptyParameters();

CRDFOX void CParameters_destroy(CParameters* parameters);

CRDFOX const CException* CParameters_newEmptyParameters(CParameters** parameters);

CRDFOX const CException* CParameters_setString(CParameters* parameters, const char* key, const char* value);

CRDFOX const CException* CParameters_getString(const CParameters* parameters, const char* key, const char* const defaultValue, const char** string);

// Copyright 2021 by Oxford Semantic Technologies Limited.

typedef enum { PREFIXES_INVALID_PREFIX_NAME, PREFIXES_NO_CHANGE, PREFIXES_REPLACED_EXISTING, PREFIXES_DECLARED_NEW } CPrefixes_DeclareResult;

CRDFOX const CPrefixes* CPrefixes_getEmptyPrefixes();

CRDFOX const CPrefixes* CPrefixes_getDefaultPrefixes();

CRDFOX void CPrefixes_destroy(CPrefixes* prefixes);

CRDFOX const CException* CPrefixes_newEmptyPrefixes(CPrefixes** prefixes);

CRDFOX const CException* CPrefixes_newDefaultPrefixes(CPrefixes** prefixes);

CRDFOX const CException* CPrefixes_declareStandardPrefixes(CPrefixes* prefixes);

CRDFOX const CException* CPrefixes_declarePrefix(CPrefixes* prefixes, const char* prefixName, const char* prefixIRI, CPrefixes_DeclareResult* declareResult);

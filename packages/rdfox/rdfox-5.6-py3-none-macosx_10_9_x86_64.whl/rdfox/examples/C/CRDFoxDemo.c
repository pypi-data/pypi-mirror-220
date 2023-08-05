// Copyright 2021 by Oxford Semantic Technologies Limited.

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdbool.h>

#include "CRDFox.h"

static size_t getTriplesCount(CDataStoreConnection* dataStoreConnection, const char* queryDomain, CPrefixes* prefixes) {
    CParameters* parameters = NULL;
    CParameters_newEmptyParameters(&parameters);
    CParameters_setString(parameters, "fact-domain", queryDomain);

    CCursor* cursor = NULL;
    CDataStoreConnection_createCursor(dataStoreConnection, NULL, prefixes, "SELECT ?X ?Y ?Z WHERE { ?X ?Y ?Z }", 34, parameters, &cursor);
    CParameters_destroy(parameters);
    CDataStoreConnection_beginTransaction(dataStoreConnection, TRANSACTION_TYPE_READ_ONLY);
    size_t result = 0;
    size_t multiplicity;
    for (CCursor_open(cursor, &multiplicity); multiplicity != 0; CCursor_advance(cursor, &multiplicity))
        result += multiplicity;
    CCursor_destroy(cursor);
    CDataStoreConnection_rollbackTransaction(dataStoreConnection);
    return result;
}

void handleException(const CException* exception) {
    if (exception) {
        const char* exceptionName = CException_getExceptionName(exception);
        const char* what = CException_what(exception);
        printf("Exception:\n");
        printf("Name: %s\n", exceptionName);
        printf("What: %s\n", what);
        exit(1);
    }
}

bool stdoutOutputStreamFlush(void* context) {
    return fflush(stdout) == 0;
}

bool stdoutOutputStreamWrite(void* context, const void* data, size_t numberOfBytesToWrite) {
    return fwrite(data, sizeof(char), numberOfBytesToWrite, stdout) == numberOfBytesToWrite;
}

int main() {
    handleException(CServer_startLocalServer(CParameters_getEmptyParameters()));

    CServer_createFirstLocalServerRole("", "");

    CServerConnection* serverConnection = NULL;
    handleException(CServerConnection_newServerConnection("", "", &serverConnection));

    // We next specify how many threads the server should use during import of data and reasoning.
    printf("Setting the number of threads...\n");
    handleException(CServerConnection_setNumberOfThreads(serverConnection, 2));

    // We the default value for the "type" perameter, which is "par-complex-nn".
    handleException(CServerConnection_createDataStore(serverConnection, "example", CParameters_getEmptyParameters()));

    // We connect to the data store.
    CDataStoreConnection* dataStoreConnection = NULL;
    handleException(CServerConnection_newDataStoreConnection(serverConnection, "example", &dataStoreConnection));

    // We next import the RDF data into the store. At present, only Turtle/N-triples files are supported.
    // At the moment, please convert RDF/XML files into Turtle format to load into CRDFox.
    printf("Importing RDF data...\n");

    CPrefixes* emptyPrefixes = NULL;
    CPrefixes_newEmptyPrefixes(&emptyPrefixes);

    CPrefixes* defaultPrefixes = NULL;
    CPrefixes_newDefaultPrefixes(&defaultPrefixes);

    // To show how to handle exceptions, try to import a file that does not exist.
    printf("To show how to handle exceptions, try to import a file that does not exist.\n");
    const CException* exception = CDataStoreConnection_importDataFromFile(dataStoreConnection, NULL, UPDATE_TYPE_ADDITION, emptyPrefixes, "no_file.ttl", "text/turtle");
    if (exception) {
        const char* exceptionName = CException_getExceptionName(exception);
        const char* what = CException_what(exception);
        printf("Exception:\n");
        printf("Name: %s\n", exceptionName);
        printf("What: %s\n", what);
    }

    handleException(CDataStoreConnection_importDataFromFile(dataStoreConnection, NULL, UPDATE_TYPE_ADDITION, emptyPrefixes, "lubm1.ttl", "text/turtle"));

    // RDFox manages data in several fact domains.
    //
    // - The 'all' domain contains all facts -- that is, both the explicitly given and the derived facts.
    //
    // - The 'derived' domain contains the facts that were derived by reasoning, but were not explicitly given in the input.
    //
    // - The 'explicit' domain contains the facts that were explicitly given in the input.
    //
    // The domain must be specified in various places where queries are evaluated. If a query domain is not
    // specified, the 'all' domain is used.
    printf("Number of tuples after import: %zu\n", getTriplesCount(dataStoreConnection, "all", emptyPrefixes));

    // SPARQL queries can be evaluated in several ways. One option is to have the query result be written to
    // an output stream in one of the supported formats.
    struct COutputStream outputStream = { NULL, &stdoutOutputStreamFlush, &stdoutOutputStreamWrite };
    CStatementResult statementResult;
    handleException(CDataStoreConnection_evaluateStatement(dataStoreConnection, NULL, emptyPrefixes, "SELECT DISTINCT ?Y WHERE { ?X ?Y ?Z }", 37, CParameters_getEmptyParameters(), &outputStream, "application/sparql-results+json", statementResult));

    // We now add the ontology and the custom rules to the data.

    // In this example, the rules are kept in a file separate from the ontology. JRDFox supports
    // SWRL rules, so it is possible to store the rules into the OWL ontology.

    printf("Adding the ontology to the store...\n");
    handleException(CDataStoreConnection_importDataFromFile(dataStoreConnection, NULL, UPDATE_TYPE_ADDITION, defaultPrefixes, "univ-bench.owl", "text/owl-functional"));

    printf("Importing rules from a file...\n");
    handleException(CDataStoreConnection_importDataFromFile(dataStoreConnection, NULL, UPDATE_TYPE_ADDITION, emptyPrefixes, "additional-rules.txt", ""));

    printf("Number of tuples after materialization: %zu\n", getTriplesCount(dataStoreConnection, "all", emptyPrefixes));

    // We now evaluate the same query as before, but we do so using a cursor, which provides us with
    // programmatic access to individual query results.

    CCursor* cursor = NULL;
    CDataStoreConnection_createCursor(dataStoreConnection, NULL, emptyPrefixes, "SELECT DISTINCT ?Y WHERE { ?X ?Y ?Z }", 37, CParameters_getEmptyParameters(), &cursor);

    int numberOfRows = 0;
    printf("\n=======================================================================================\n");

    size_t arity;
    CCursor_getArity(cursor, &arity);

    size_t multiplicity;
    const CResourceID* argumentsBuffer;
    CCursor_getArgumentsBuffer(cursor, &argumentsBuffer);

    const CArgumentIndex* argumentIndexes;
    CCursor_getArgumentIndexes(cursor, &argumentIndexes);
    // We iterate trough the result tuples.
    for (CCursor_open(cursor, &multiplicity); multiplicity != 0; CCursor_advance(cursor, &multiplicity)) {
        // We iterate through the terms of each tuple.
        for (size_t termIndex = 0; termIndex < arity; ++termIndex) {
            if (termIndex != 0)
                printf("  ");
            // For each term, we retrieve the lexical form and the data type of the term.
            const CResourceID resourceID = argumentsBuffer[argumentIndexes[termIndex]];
            CDatatypeID datatypeID;
            char lexicalFormBuffer[1024];
            size_t lexicalFormSize = 0;
            bool resourceResolved = false;
            CCursor_getResourceLexicalForm(cursor, resourceID, lexicalFormBuffer, sizeof(lexicalFormBuffer), &lexicalFormSize, &datatypeID, &resourceResolved);
            if (lexicalFormSize >= sizeof(lexicalFormBuffer)) {
                printf("Warning: the lexical form for resourceID %"PRIu64" was truncated from %zu to %zu characters.\n", resourceID, lexicalFormSize, sizeof(lexicalFormBuffer) - 1);
                lexicalFormBuffer[sizeof(lexicalFormBuffer) - 1] = '\0';
            }
            else
                lexicalFormBuffer[lexicalFormSize] = '\0';
            printf("%s", lexicalFormBuffer);
        }
        printf(" * ");
        printf("%zu\n", multiplicity);
        ++numberOfRows;
    }
    printf("---------------------------------------------------------------------------------------\n");
    printf("  The number of rows returned: %d\n", numberOfRows);
    printf("=======================================================================================\n\n");

    // RDFox supports incremental reasoning. One can import facts into the store incrementally by
    // calling importDataFromFileName(dataStoreConnection, ...) with additional argument UPDATE_TYPE_ADDITION.
    printf("Importing triples for incremental reasoning...\n");
    CDataStoreConnection_importDataFromFile(dataStoreConnection, NULL, UPDATE_TYPE_ADDITION, defaultPrefixes, "lubm1-new.ttl", "text/turtle");

    // Adding the rules/facts changes the number of triples. Note that the store is updated incrementally.
    printf("Number of tuples after addition: %zu\n", getTriplesCount(dataStoreConnection, "all", emptyPrefixes));

    // One can export the facts from the current store into a file as follows.
    printf("Exporting facts to file 'final-facts.ttl'...\n");
    fflush(stdout);
    CParameters* parameters = NULL;
    CParameters_newEmptyParameters(&parameters);
    CParameters_setString(parameters, "fact-domain", "all");
    CDataStoreConnection_exportDataToFile(dataStoreConnection, defaultPrefixes, "final-facts.ttl", "application/n-triples", parameters);
    CParameters_destroy(parameters);

    CDataStoreConnection_destroy(dataStoreConnection);

    printf("This is the end of the example!\n");
    return 0;
}

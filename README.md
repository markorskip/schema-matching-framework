# schema-matching-framework

Migrating data from a source database to a destination database is a common problem.

The process involves 2 steps.

1. Identifying which fields in the source database goes to which fields in the destination database.
2. Writing the code that will read from the source database, transform the data to match the destination database, and insert the date into the destination database.

The code that does work can be in many languages, including sql assuming cross database connections are possible.

This framework will attempt to solve both these problems.

Some possible interfaces will be:

defineMappingsBasedOnSchemas(sourceSchema DataSchema, destinationSchema DataSchema) -> DataMappingFile:

defineMappingsBasedOnSchemaAndData(sourceDatabase SchemaWithData, destinationDatabase SchemaWithData) -> DataMappingFile:

defineMappingsBasedOnSchemaAndDataAndMetadata(sourceDatabaseWithMeta SchemaDataMetaModel, destinationDatabaseWithMeta SchemaDataMetaModel) -> DataMappingFile:

generateMappingCode(dataMappingFile)-> DataMappingCode


# Expectations

The abilitity for code to generate a complete mapping without human assistance is unlikely.  I expect the data mapping file to be incomplete and only perhaps 70 percent correct.   However it could still assist and a humaan analyst could fill in the gaps.

A complete dataMappingFile should be able to generate almost complete data mapping code when dealing with simple types such as strings and ints.  However when the data type is different across datasources, human analyst/programmer may have to complete the code as well.

That being said, this framework should be able to reduce the type of data migration dramatically.



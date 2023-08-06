from jpype.types import JInt
from jpype.types import JClass, JObject
from org.ohdsi.circe.cohortdefinition import CohortExpressionQueryBuilder as \
    JavaCohortExpressionQueryBuilder
from org.ohdsi.circe.cohortdefinition.CohortExpressionQueryBuilder import \
    BuildExpressionQueryOptions as JavaBuildExpressionQueryOptions


def CohortExpressionQueryBuilder() -> JClass:
    """
    Return the CohortExpressionQueryBuilder class.

    Returns
    -------
    _JClass
        A org.ohdsi.circe.cohortdefinition.CohortExpressionQueryBuilder class.
    """
    return JavaCohortExpressionQueryBuilder


def create_generate_options(
        chohort_id_field_name: str = None, cohort_id: int = None,
        cdm_schema: str = None, target_table: str = None,
        result_schema: str = None, vocabulary_schema: str = None,
        generate_stats: bool = None) -> JObject:
    """
    Create Generation Options

    Creates the generation options object for use in ``build_cohort_query``.

    Parameters
    ----------
    chohort_id_field_name : str, optional
        The field that contains the cohortId in the cohort table, by default
        None
    cohort_id : int, optional
        The generated cohort ID, by default None
    cdm_schema : str, optional
        The value of the CDM schema, by default None
    target_table : str, optional
        The cohort table name, by default None
    result_schema : str, optional
        The schema the cohort table belongs to, by default None
    vocabulary_schema : str, optional
        The schema of the vocabulary tables (defaults to cdmSchema),
        by default None
    generate_stats : bool, optional
        A boolean representing if the query should include inclusion rule
        statistics calculation, by default None

    TODO
    ----
    Somehow the class expect a $ in the name of the class, weirdness..
    TypeError: No matching overloads found for *static* org.ohdsi.circe.cohortdefinition.CohortExpressionQueryBuilder.buildExpressionQuery(org.ohdsi.circe.cohortdefinition.CohortExpression,org.ohdsi.circe.cohortdefinition.CohortExpressionQueryBuilder.BuildExpressionQueryOptions), options are:
        public java.lang.String org.ohdsi.circe.cohortdefinition.CohortExpressionQueryBuilder.buildExpressionQuery(org.ohdsi.circe.cohortdefinition.CohortExpression,org.ohdsi.circe.cohortdefinition.CohortExpressionQueryBuilder$BuildExpressionQueryOptions)
        public java.lang.String org.ohdsi.circe.cohortdefinition.CohortExpressionQueryBuilder.buildExpressionQuery(java.lang.String,org.ohdsi.circe.cohortdefinition.CohortExpressionQueryBuilder$BuildExpressionQueryOptions)

    Returns
    -------
    _JObject
        _description_
    """
    options = JavaBuildExpressionQueryOptions()

    if chohort_id_field_name:
        options.cohortIdFieldName = chohort_id_field_name
    if cohort_id:
        options.cohortId = JInt(cohort_id)
    if cdm_schema:
        options.cdmSchema = cdm_schema
    if target_table:
        options.targetTable = target_table
    if result_schema:
        options.resultSchema = result_schema
    if vocabulary_schema:
        options.vocabularySchema = vocabulary_schema
    if generate_stats:
        options.generateStats = generate_stats

    return options


def build_cohort_query(cohort_expression: JObject | str,
                       options: JObject = None) -> str:
    """
    Build Cohort SQL

    Generates the OMOP CDM Sql to generate the cohort expression

    Parameters
    ----------
    cohort_expression : _JObject | str
        A java instance of
        ``org.ohdsi.circe.cohortdefinition.CohortExpression`` or a JSON
        string representing a cohort expression.
    options : _JObject, optional
        The options object from ``create_generate_options``, by default None
    """
    # expression can be a org.ohdsi.circe.cohortdefinition.CohortExpression
    # or a String (it’s an overload method)
    if not options:
        options = create_generate_options()

    sql = JavaCohortExpressionQueryBuilder().buildExpressionQuery(
        cohort_expression, options)

    return sql

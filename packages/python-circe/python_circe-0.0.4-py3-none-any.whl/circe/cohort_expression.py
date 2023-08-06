import json

from jpype.types import JClass, JObject
from org.ohdsi.circe.cohortdefinition import CohortExpression as \
    JavaCohortExpression


def CohortExpression() -> JClass:
    """
    Return the CohortExpression class.

    Returns
    -------
    _JClass
        A org.ohdsi.circe.cohortdefinition.CohortExpression class.
    """
    return JavaCohortExpression


def cohort_expression_from_json(cohort: str | dict) -> JObject:
    """
    Render read JSON into a CohortExpression instance.

    Reads a String (json) and deserializes it into a
    org.ohdsi.circe.cohortdefinition.CohortExpression

    Parameters
    ----------
    json : str | dict
        A JSON string representing a cohort expression. Or a dictionary
        representing a cohort expression.

    Returns
    -------
    _JObject
        A java instance of
        ``org.ohdsi.circe.cohortdefinition.CohortExpression``.
    """
    if isinstance(cohort, dict):
        cohort = json.dumps(cohort)

    return JavaCohortExpression.fromJson(cohort)

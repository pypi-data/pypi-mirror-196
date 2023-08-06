import json

from jpype.types import JClass
from org.ohdsi.circe.vocabulary import ConceptSetExpressionQueryBuilder as \
    JavaConceptSetExpressionQueryBuilder

from circe.concept_set_expression import concept_set_expression_from_json


def ConceptSetExpressionQueryBuilder() -> JClass:
    """
    Return the ConceptSetExpressionQueryBuilder class.

    Returns
    -------
    JClass
        A org.ohdsi.circe.vocabulary.ConceptSetExpressionQueryBuilder class.
    """
    return JavaConceptSetExpressionQueryBuilder


def build_concept_set_query(concept_set_expression: str | dict) -> str:
    """
    Build a query from a ConceptSetExpression instance.

    Parameters
    ----------
    concept_set_expression : ConceptSetExpression
        A java instance of
        ``org.ohdsi.circe.vocabulary.ConceptSetExpression``.

    Returns
    -------
    str
        A query string.
    """
    if isinstance(concept_set_expression, dict):
        concept_set_expression = json.dumps(concept_set_expression)

    return JavaConceptSetExpressionQueryBuilder.buildExpressionQuery(
        concept_set_expression_from_json(concept_set_expression)
    )

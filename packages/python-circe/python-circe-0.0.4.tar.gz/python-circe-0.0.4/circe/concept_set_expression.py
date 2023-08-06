import json

from org.ohdsi.circe.vocabulary import ConceptSetExpression as \
    JavaConceptSetExpression
from jpype.types import JClass, JObject


def ConceptSetExpression() -> JClass:
    """
    Return the ConceptSetExpression class.

    Returns
    -------
    JClass
        A org.ohdsi.circe.vocabulary.ConceptSetExpression class.
    """
    return JavaConceptSetExpression


def concept_set_expression_from_json(concept_set: str | dict) -> JObject:
    """
    Render read JSON into a ConceptSetExpression instance.

    Reads a String (json) and deserializes it into a
    org.ohdsi.circe.vocabulary.ConceptSetExpression

    Parameters
    ----------
    concept_set : str | dict
        A JSON string representing a concept set expression. Or a dictionary
        representing a concept set expression.

    Returns
    -------
    JObject
        A java instance of
        ``org.ohdsi.circe.vocabulary.ConceptSetExpression``.
    """
    if isinstance(concept_set, dict):
        concept_set = json.dumps(concept_set)

    return JavaConceptSetExpression.fromJson(concept_set)

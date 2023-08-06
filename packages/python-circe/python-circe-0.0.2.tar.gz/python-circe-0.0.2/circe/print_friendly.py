from org.ohdsi.circe.cohortdefinition.printfriendly import MarkdownRender

from jpype.types import JObject, JArray


def cohort_print(expression: JObject):
    """
    Create a print friendly version of a cohort expression.

    Parameters
    ----------
    expression : JObject
        A character vector or result of ``cohort_expression_from_json``
        containing the cohort expression.

    Returns
    -------
    str
        A character vector containing the print friendly version of the
        cohort expression.
    """
    return MarkdownRender().renderCohort(expression)


def concept_set_print(expression: JObject):
    """
    Create a print friendly version of a concept set expression.

    Parameters
    ----------
    expression : JObject
        A character vector or result of ``concept_set_expression_from_json``
        containing the concept set expression.

    Returns
    -------
    str
        A character vector containing the print friendly version of the
        concept set expression.
    """
    return MarkdownRender().renderConceptSet(expression)


def concept_set_list_print(expression: JObject | list[JObject] | JArray):
    """
    Render conceptSet array for print-friendly

    Generates a print-friendly (human-readable) representation of an array of
    concept sets. This can for example be used in a study protocol.

    Parameters
    ----------
    expression : JObject | list[JObject] | JArray
        A character vector or result of ``concept_set_expression_from_json``
        containing the concept set expression.


    Returns
    -------
    str
        A character vector containing the print friendly version of the
        concept set expression.
    """
    return MarkdownRender().renderConceptSetList(expression)

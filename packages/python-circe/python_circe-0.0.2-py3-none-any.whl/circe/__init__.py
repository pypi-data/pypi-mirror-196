import jpype
import jpype.imports

from importlib.resources import files


# start the JVM if it hasn't been started yet
jar_folder = files('circe.java')
if not jpype.isJVMStarted():
    jpype.startJVM(classpath=[str(jar_folder.joinpath('*'))])


if __name__ == '__main__':

    from circe.cohort_expression import cohort_expression_from_json
    from circe.print_friendly import cohort_print, concept_set_print, concept_set_list_print
    cohort_json = files('circe.data').joinpath('simpleCohort.json').read_text()
    exp = cohort_expression_from_json(cohort_json)
    print(cohort_print(exp))
    print('*'*80)

    from circe.cohort_sql_builder import build_cohort_query, create_generate_options

    query = build_cohort_query(exp)
    print(query)
    print('*'*80)
    from circe.concept_set_expression import concept_set_expression_from_json

    concept_set_json = files('circe.data').joinpath('conceptSet.json').read_text()
    concept = concept_set_expression_from_json(concept_set_json)
    print(concept_set_print(concept_set_json))
    print('*'*80)

    concept_set_list_json = files('circe.data').joinpath('conceptSetList.json').read_text()
    print(concept_set_list_print(concept_set_list_json))


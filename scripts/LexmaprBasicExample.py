import lexmapr
import argparse
import lexmapr.pipeline

#minimal examples
#RUNNING LEXMAPR AS IS
lexmapr.pipeline.run(argparse.Namespace(input_file='temp.csv', config='sample_config.json',
                                                full=None, output=None, version=False,
                                                bucket=False, no_cache=False, profile=None))


#FULL MATCH ON A SINGLE PHRASE
from  lexmapr import pipeline_helpers
import lexmapr.pipeline_resources
lookup_table = lexmapr.pipeline_resources.get_predefined_resources()
resources = lexmapr.pipeline_resources.get_config_resources('sample_config.json',False)
lookup_table =  pipeline_helpers.merge_lookup_tables(lookup_table,resources)

print(pipeline_helpers.map_term('chicken meat', lookup_table))


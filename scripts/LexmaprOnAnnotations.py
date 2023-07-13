import os
import lexmapr.pipeline
import pandas as pd
from typing import List
from tqdm import tqdm
import argparse
from Annotation import Annotation


def create_document_colletion() -> List[Annotation]:
    document_iterator = Annotation.iterate_over_files(Annotation.BASE_DIR)
    document_set = []
    for document in document_iterator:
        filename = os.path.join(Annotation.BASE_DIR,document)
        with open(filename) as file:
            lines = [line.strip()  for line in file.readlines()]
            accepted_lines = []
            for line in lines:
                tokens = line.split('\t')
                # if tokens[1].startswith('food'): accepted_lines.append(tokens[-1])
                if tokens[1].startswith('unit'): accepted_lines.append(tokens[-1])
                
            document_set.append(Annotation(filename, accepted_lines))
    return document_set
def main():
    all_data = pd.DataFrame(columns=['input_file', 'sample', 'processed_sample', 'processed_sample_(scientific)', 'status', 'matched_component'])
    for document in tqdm(create_document_colletion()):
        document.to_df().to_csv('temp.csv')
        lexmapr.pipeline.run(argparse.Namespace(input_file='temp.csv', config='sample_config.json',
                                                        full=None, output='output_temp.tsv', version=False,
                                                        bucket=False, no_cache=False, profile=None))

        out_df = pd.read_csv('output_temp.tsv',sep='\t')
        out_df = out_df.assign(matched_component = out_df['Matched_Components'].str.strip("[]").str.split(',')).explode('matched_component')
        out_df['input_file'] = document.filename
        out_df.drop(columns=['Sample_Id','Matched_Components'],inplace=True)
        out_df.columns = ['sample','processed_sample','processed_sample_(scientific)','status','matched_component','input_file']
        all_data = pd.concat([all_data, out_df])
    all_data.to_csv('extracted_from_AL_annotations_Unit.csv')


if __name__=="__main__":
    main()

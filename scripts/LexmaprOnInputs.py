import os
import lexmapr.pipeline
import pandas as pd
from typing import List
from tqdm import tqdm
import argparse
from Annotation import Annotation, Document


def create_document_colletion() -> List[Document]:
    document_iterator = Document.iterate_over_files(Document.BASE_DIR)
    document_set = []
    for document in document_iterator:
        filename = os.path.join(Document.BASE_DIR,document)
        with open(filename) as file:
            lines = [line.strip()  for line in file.readlines()]
            document_set.append(Document(filename, lines))
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
    # all_data.to_csv('extracted_from_input_files.csv')


if __name__=="__main__":
    main()

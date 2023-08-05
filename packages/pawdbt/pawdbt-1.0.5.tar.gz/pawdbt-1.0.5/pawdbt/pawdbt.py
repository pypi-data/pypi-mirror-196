#!/usr/bin/env python
# coding: utf-8

from pawdbt.pawdbt_helper_modules import *

def main_yaml():
    if is_dbt_project_healthy():

        clear_terminal()

        cd = get_current_dir()
        dry_arr = get_all_dry_doc_blocks(cd)
        flag_values = return_flag_values(flag_list)
        selector = flag_values.get('select', None)
        doc_blocks_in_relation = flag_values.get('save-doc-blocks-in', None)
        always_overwrite = flag_values.get('always-overwrite', False)
        run_models = flag_values.get('run-models', False)

        header_and_info(selector, doc_blocks_in_relation, always_overwrite, run_models)

        if run_models:
            for i in tqdm(range(1), total=1, desc="Running selector to create models", colour="green"):
                run_selector(selector)

        spinner = Halo(text="Gathering Models...", spinner=pong)
        spinner.start()

        selected_models = get_models_by_identifier_type('name', selector)
        selected_paths = get_models_by_identifier_type('path', selector)

        spinner.stop()

        ymls = []
        mds = []

        for i, relation in tqdm(enumerate(selected_models), total=len(selected_models), desc="Processing relations",
                                colour="green"):
            tqdm.write(f"Processing {relation}...")
            columns, types = get_relation_columns_and_datatype(relation)
            yml = create_relation_yml(relation, selected_paths[i], columns, dry_arr, types)
            md = create_relation_md(relation, selected_paths[i], selected_models, selected_paths, dry_arr,
                                    doc_blocks_in_relation)
            ymls.append(yml)
            mds.append(md)

        for i, relation in tqdm(enumerate(selected_models), total=len(selected_models), desc="Writing YAML & MD Files",
                                colour="green"):
            create_file(selected_paths[i], 'yml', ymls[i], always_overwrite)
            create_file(selected_paths[i], 'md', mds[i], always_overwrite)
    else:
        raise RuntimeError('You are not currently ')


if __name__ == "__main__":
    main_yaml()

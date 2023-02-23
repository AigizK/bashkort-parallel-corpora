import argparse
import json
import os

uniq_mhr = set()


def prepare_sentences():
    mhr_lines = []
    ru_lines = []

    with open(f"mhr.txt", "rt") as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            mhr_lines.append(line)
    with open(f"rus.txt", "rt") as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            ru_lines.append(line)
    print(len(mhr_lines))
    print(len(ru_lines))
    assert len(mhr_lines) == len(ru_lines)

    return mhr_lines, ru_lines


def write_to_file(f, mhr_lines, ru_lines):
    assert len(mhr_lines) == len(ru_lines)
    global uniq_mhr
    added = 0
    skipped = 0
    for i in range(len(mhr_lines)):
        line_key=f'{mhr_lines[i]}|||{ru_lines[i]}'
        if line_key not in uniq_mhr:
            f.write(json.dumps({'mhr': mhr_lines[i], 'rus': ru_lines[i]},
                               ensure_ascii=False) + "\n")
            added += 1
            uniq_mhr.add(line_key)
        else:
            skipped += 1
    print(
        f'Всего {len(mhr_lines)} предложений, добавлено {added},пропущено {skipped} предл.')


def push_to_hf():
    from datasets import load_dataset
    from huggingface_hub import notebook_login

    mhr_dataset = load_dataset("json", data_files="mhr_rus.jsonl")
    notebook_login()
    mhr_dataset.push_to_hub("mari-russian-parallel-corpora")


if __name__ == '__main__':
    result_jsonl = []
    with open("mhr_rus.jsonl", "wt") as f:
        mhr_lines, ru_lines = prepare_sentences()
        write_to_file(f, mhr_lines, ru_lines)

    push_to_hf()




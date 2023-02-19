import argparse
import json
import os


def prepare_1000_sentences():
    ba_lines = []
    ru_lines = []

    for i in range(1, 11):
        with open(f"1000-sentences/ba/{i}.txt", "rt") as f:
            while True:
                line = f.readline().strip()
                if not line:
                    break
                line = line[line.index('.') + 1:].strip()
                ba_lines.append(line)
        with open(f"1000-sentences/ru/{i}.txt", "rt") as f:
            while True:
                line = f.readline().strip()
                if not line:
                    break
                ru_lines.append(line)
        assert len(ba_lines) == len(ru_lines)

    return ba_lines, ru_lines


def prepare_bash_encyclopedia():
    ba_lines = []
    ru_lines = []

    with open(f"bash_encyclopedia/ba/___BashEncycl_all.tmx.txt", "rt") as f:
        while True:
            line = f.readline().strip()
            if not line:
                break
            ba_lines.append(line.replace(" ", " "))
    with open(f"bash_encyclopedia/ru/___BashEncycl_all.tmx.txt", "rt") as f:
        while True:
            line = f.readline().strip()
            if not line:
                break
            ru_lines.append(line.replace(" ", " "))
    assert len(ba_lines) == len(ru_lines)

    return ba_lines, ru_lines


def prepare_bashinform():
    ba_lines = []
    ru_lines = []

    files_names = os.listdir("bashinform/ba/")

    for i in files_names:
        with open(f"bashinform/ba/{i}", "rt") as f:
            while True:
                line = f.readline().strip()
                if not line:
                    break
                ba_lines.append(line)
        with open(f"bashinform/ru/{i}", "rt") as f:
            while True:
                line = f.readline().strip()
                if not line:
                    break
                ru_lines.append(line)
        assert len(ba_lines) == len(ru_lines)

    return ba_lines, ru_lines


def prepare_little_prince():
    ba_lines = []
    ru_lines = []

    with open(f"little_prince/ba/Princ_2018.tmx.txt", "rt") as f:
        while True:
            line = f.readline().strip()
            if not line:
                break
            ba_lines.append(line.replace(" ", " "))
    with open(f"little_prince/ru/Princ_2018.tmx.txt", "rt") as f:
        while True:
            line = f.readline().strip()
            if not line:
                break
            ru_lines.append(line.replace(" ", " "))
    assert len(ba_lines) == len(ru_lines)

    return ba_lines, ru_lines


def prepare_bashkortsoft_corpus():
    ba_lines = []
    ru_lines = []

    return ba_lines, ru_lines

uniq_ba=set()

def prepare_tmx():
    from xml.dom.minidom import parse

    ba_lines = []
    ru_lines = []

    files_names = os.listdir("tmx")

    for file in files_names:
        # print(file)
        with open(f"tmx/{file}", 'rb') as fin:
            document = parse(fin)

        tu_items = document.getElementsByTagName("tu")
        for tu in tu_items:
            # print(tu)
            ru = ''
            ba = ''
            tuvs = tu.childNodes

            for tuv in tuvs:
                if tuv.nodeName == "tuv":
                    try:
                        if tuv.attributes.items()[0][1] == "ru":
                            seg = tuv.getElementsByTagName("seg")[0]
                            ru = seg.childNodes[0].data
                        elif tuv.attributes.items()[0][1] == "ba":
                            seg = tuv.getElementsByTagName("seg")[0]
                            ba = seg.childNodes[0].data
                    except:
                        # print(tuv)
                        pass
            if ba != '' and ru != '':
                ba_lines.append(ba)
                ru_lines.append(ru)

        # for node in tmx_file.unit_iter():
        #     print(node.source, node.target)

    return ba_lines, ru_lines

def prepare_tg_bot():
    ba_lines = []
    ru_lines = []

    with open("translated_books/ba-ru.tsv","rt") as f:
        lines = f.readlines()
        lines=lines[1:]
        for line in lines:
            line=line.strip()
            cells = line.split('\t')
            ba_lines.append(cells[1])
            ru_lines.append(cells[2])
    return ba_lines, ru_lines


def write_to_file(f, ba_lines, ru_lines, corpus_name):
    assert len(ba_lines) == len(ru_lines)
    global uniq_ba
    for i in range(len(ba_lines)):
        if ba_lines[i] not in uniq_ba:
            f.write(json.dumps({'ba': ba_lines[i], 'ru': ru_lines[i],
                                'corpus': corpus_name},
                               ensure_ascii=False) + "\n")
            uniq_ba.add(ba_lines[i])
    print(corpus_name, " - ", len(ba_lines))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--corpus', type=str, nargs="+")
    args = parser.parse_args()

    if args.corpus is not None:
        corpuses = args.corpus
    else:
        corpuses = ['translated_books', '1000-sentences', 'bash_encyclopedia', 'bashinform',
                    'little_prince', 'raw-1000000', 'tmx']
        # corpuses = [ 'translated_books']

    result_jsonl = []
    with open("ba_ru.jsonl", "wt") as f:
        for corpus in corpuses:
            if corpus == '1000-sentences':
                ba_lines, ru_lines = prepare_1000_sentences()
                write_to_file(f, ba_lines, ru_lines, '1000 sentences')

            elif corpus == "bash_encyclopedia":
                ba_lines, ru_lines = prepare_bash_encyclopedia()
                write_to_file(f, ba_lines, ru_lines, 'bashkir encyclopedia')
            elif corpus == "bashinform":
                ba_lines, ru_lines = prepare_bashinform()
                write_to_file(f, ba_lines, ru_lines,
                              'https://www.bashinform.ru/')
            elif corpus == "little_prince":
                ba_lines, ru_lines = prepare_little_prince()
                write_to_file(f, ba_lines, ru_lines, 'little prince')
            # elif corpus=="raw-1000000":
            #     ba_lines, ru_lines = prepare_bashkortsoft_corpus()
            #     write_to_file(f,ba_lines, ru_lines,'first corpus of http://baskortsoft.ru/')
            elif corpus == "tmx":
                ba_lines, ru_lines = prepare_tmx()
                write_to_file(f, ba_lines, ru_lines, 'tmx corpus')
            elif corpus=="translated_books":
                ba_lines, ru_lines = prepare_tg_bot()
                write_to_file(f, ba_lines, ru_lines, 'https://t.me/bashkort_translate_bot')

    print(len(corpuses))
    print(corpuses)

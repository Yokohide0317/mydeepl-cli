import deepl
from pathlib import Path
import time, datetime
import argparse
import os
import json
import sys

class Mydeepl:

    def __init__(self, args, order):
        self.auth_file = Path(os.environ["HOME"], ".mydeepl_auth.json")

        if order == "init":
            pass
        elif order == "text":
            self.text = " ".join(args.inp)
            self.auth_key = self.get_auth()
            self.translator = deepl.Translator(self.auth_key)
        elif order == "doc":
            self.input_path = Path(args.inp)
            self.output_path = self.def_path()
            self.auth_key = self.get_auth()
            self.translator = deepl.Translator(self.auth_key)
        return

    def get_auth(self):
        if not self.auth_file.exists():
            print(f".mydeepl_auth.json does not exist. run \"mydl init\" to create it.")
            sys.exit()
        auth_key = json.load(open(self.auth_file, 'r'))["auth_key"]
        return auth_key

    # 出力ファイル名を作成
    def get_exp_name(self) -> str:
        # filename.txt -> filename_translated.txt
        result_id = str(self.input_path).replace(self.input_path.suffix, "") + "_translated" + self.input_path.suffix
        return result_id

    def def_path(self):
        # Define path 
        output_dir = "./"
        filename = self.get_exp_name()
        output_path = str(Path(output_dir, filename))
        return output_path

    def trans_doc(self):
        translator = self.translator

    # ======https://github.com/DeepLcom/deepl-python#configuration==========
        try:
            translator.translate_document_from_filepath(
                self.input_path,
                self.output_path,
                target_lang="JA"
            )

            with open(self.input_path, "rb") as in_file, open(self.output_path, "wb") as out_file:
                translator.translate_document(
                    in_file,
                    out_file,
                    target_lang="JA"
                )

        except deepl.DocumentTranslationException as error:
            # If an error occurs during document translation after the document was
            # already uploaded, a DocumentTranslationException is raised. The
            # document_handle property contains the document handle that may be used to
            # later retrieve the document from the server, or contact DeepL support.
            doc_id = error.document_handle.id
            doc_key = error.document_handle.key
            print(f"Error after uploading ${error}, id: ${doc_id} key: ${doc_key}")
        except deepl.DeepLException as error:
            # Errors during upload raise a DeepLException
            print(error)
        return str(self.output_path)
    # ================================================

    def trans_text(self): 
        translator = self.translator
        result = translator.translate_text(str(self.text), target_lang="JA")
        return result

    def init_auth(self):
        inp = str(input("Enter Your Key: ")).strip()

        if self.auth_file.exists():
            print(f"authkey is already exist: {str(self.auth_file)}")
            y_n = str(input("Do you want to overwrite? [y|n] "))
            if y_n != "y":
                print("Abort")
                sys.exit()
        
        # 作成
        with open(self.auth_file, mode='w') as f:
            f.write('{"auth_key": "%s"}' %(inp))
        return

def init_main(args):
    mydeepl = Mydeepl(args, order="init")
    result = mydeepl.init_auth()
    return

def text_main(args):
    mydeepl = Mydeepl(args, order="text")
    result = mydeepl.trans_text()
    print(result)
    return

def doc_main(args):
    mydeepl = Mydeepl(args, order="doc")
    result = mydeepl.trans_doc()
    print(f"Exported to... {result}")
    return


def command_help(args):
    print(parser.parse_args([args.command, '--help']))

def main():
    parser = argparse.ArgumentParser(description="")
    subparsers = parser.add_subparsers()

    # init
    parser_init = subparsers.add_parser("init", help='see `add -h`')
    parser_init.set_defaults(handler=init_main)

    # document
    parser_doc = subparsers.add_parser('doc', help='see `add -h`')
    parser_doc.add_argument("inp")
    parser_doc.set_defaults(handler=doc_main)

    # text
    parser_text = subparsers.add_parser("text", help='see `add -h`')
    parser_text.add_argument("inp", nargs='*')
    parser_text.set_defaults(handler=text_main)

    # help コマンドの parser を作成
    parser_help = subparsers.add_parser('help', help='see `help -h`')
    parser_help.add_argument('command', help='command name which help is shown')
    parser_help.set_defaults(handler=command_help)

    args = parser.parse_args()
    if hasattr(args, 'handler'):
        args.handler(args)
    else:
        # 未知のサブコマンドの場合はヘルプを表示
        parser.print_help()
    return

if __name__ == "__main__":
    main()

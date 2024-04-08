# Author: Okafor Obinna

import os
import json
import argparse
from pprint import pprint
import io
import sys
import multiprocessing as mp
import requests
from pyoparser import ResumeParser
import tempfile


def print_cyan(text):
    print("\033[96m {}\033[00m" .format(text))


class ResumeParserCli(object):

    def __init__(self):
        self.__parser = argparse.ArgumentParser()
        self.__parser.add_argument(
            '-f',
            '--file',
            help="resume file to be extracted")
        self.__parser.add_argument(
            '-d',
            '--directory',
            help="directory containing all the resumes to be extracted")
        self.__parser.add_argument(
            '-r',
            '--remotefile',
            help="remote path for resume file to be extracted")
        self.__parser.add_argument(
            '-re',
            '--custom-regex',
            help="custom regex for parsing mobile numbers")
        self.__parser.add_argument(
            '-sf',
            '--skillsfile',
            help="custom skills CSV file against \
                  which skills are searched for")
        self.__parser.add_argument(
            '-e',
            '--export-format',
            help="the information export format (json)")
        self.__parser.add_argument(
            '-o',
            '--export-filepath',
            help="the export file path")

    def __banner(self):
        banner_string = r'''
              ____ __  __ ____   ____   ___     ____  _____  ______ ____ 
            / __ \\ \/ // __ \ / __ \ /   |   / __ \/ ___/ / ____// __ \
           / /_/ / \  // / / // /_/ // /| |  / /_/ /\__ \ / __/  / /_/ /
          / ____/  / // /_/ // ____// ___ | / _, _/___/ // /___ / _, _/ 
         /_/      /_/ \____//_/    /_/  |_|/_/ |_|/____//_____//_/ |_|  
                                                               
           - By Okafor Obinna (kingsloob1@gmail.com)
        '''
        print(banner_string)

    def export_data(self, exported_data, args):
        '''function to export resume data in specified format
        '''
        if args.export_format:
            if args.export_format == 'json':
                with open(args.export_filepath, 'w') as fd:
                    json.dump(exported_data, fd, sort_keys=True, indent=4)
                    abs_path = os.path.abspath(args.export_filepath)
                    print('Data exported successfully at: ' + abs_path)
                    sys.exit(0)
        else:
            return exported_data

    def extract_resume_data(self):
        args = self.__parser.parse_args()

        if args.export_format and not args.export_filepath:
            print('Please specify output file path using -o option')
            sys.exit(1)

        if args.remotefile:
            return self.export_data(
                self.__extract_from_remote_file(
                    args.remotefile,
                    args.skillsfile,
                    args.custom_regex
                ),
                args
            )

        if args.file and not args.directory:
            return self.export_data(
                self.__extract_from_file(
                    args.file,
                    args.skillsfile,
                    args.custom_regex
                ),
                args
            )
        elif args.directory and not args.file:
            return self.export_data(
                self.__extract_from_directory(
                    args.directory,
                    args.skillsfile,
                    args.custom_regex
                ),
                args
            )
        else:
            self.__parser.print_help()

    def __extract_from_file(self, file, skills_file=None, custom_regex=None):
        if os.path.exists(file):
            print_cyan('Extracting data from: {}'.format(file))
            resume_parser = ResumeParser(file, skills_file, custom_regex)
            return [resume_parser.get_extracted_data()]
        else:
            print('File not found. Please provide a valid file name')
            sys.exit(1)

    def __extract_from_directory(
        self,
        directory,
        skills_file=None,
        custom_regex=None
    ):
        if os.path.exists(directory):
            pool = mp.Pool(mp.cpu_count())

            resumes = []
            for root, _, filenames in os.walk(directory):
                for filename in filenames:
                    file = os.path.join(root, filename)
                    resumes.append([file, skills_file, custom_regex])
            results = pool.map(resume_result_wrapper, resumes)
            pool.close()
            pool.join()

            return results
        else:
            print('Directory not found. Please provide a valid directory')
            sys.exit(1)

    def __extract_from_remote_file(
        self,
        remote_file,
        skills_file,
        custom_regex
    ):
        try:
            print_cyan('Extracting data from: {}'.format(remote_file))
            headers={'User-Agent': 'Mozilla/5.0'}
            headResp = requests.head(remote_file, headers=headers)
            contentLength = int(headResp.headers['content-length'])
            
            if contentLength > 104857600: 
                raise Exception("Remote file must be less than 100 Mega Bytes")
            
            filename = remote_file.split('/')[-1]
            fileResp = requests.get(remote_file, headers=headers)
            fileBuffer = io.BytesIO()
            fileBuffer.write(fileResp.content)
            fileBuffer.seek(0)
            fileBuffer.name = filename

            resume_parser = ResumeParser(fileBuffer, skills_file, custom_regex)
            return [resume_parser.get_extracted_data()]
        
        except Exception as e:
            print(e)
            sys.exit(1)
        except:
            print('File not found. Please provide correct URL for resume file')
            sys.exit(1)


def resume_result_wrapper(args):
    print_cyan('Extracting data from: {}'.format(args[0]))
    parser = ResumeParser(args[0], args[1], args[2])
    return parser.get_extracted_data()


def main():
    cli_obj = ResumeParserCli()
    pprint(cli_obj.extract_resume_data())
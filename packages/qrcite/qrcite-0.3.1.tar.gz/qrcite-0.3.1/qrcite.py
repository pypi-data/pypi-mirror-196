#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 31 13:27:19 2022

@author: @M@nerdculture.de
"""

import argparse
import re

import bibtexparser
from bibtexparser.bibdatabase import BibDatabase
import qrcode
from PIL import Image, ImageDraw, ImageFont
from fonts.ttf import FredokaOne
from habanero import Crossref
import pandas as pd


def strip_leading_doi_url(doi: str) -> str:
    doi = re.sub(r'^(https?://)?(dx.|www.)?doi.org/', '', doi)
    return doi


def strip_curly_braces(text: str) -> str:
    return re.sub(r'{|}', '', text)


def get_wrapped_text(text: str, font: ImageFont.ImageFont, line_length: int):
    lines = ['']
    for word in text.split():
        line = f'{lines[-1]} {word}'.strip()
        if font.getlength(line) <= line_length:
            lines[-1] = line
        else:
            lines.append(word)
    return '\n'.join(lines)

def complete_reference(bib_entry):
    # Fetching misssing bib-entrys from crrossref. Updating only if entry is empty.
    if 'doi' in bib_entry:  #Fetch Data by doi.
        cr = Crossref()
        cr_id = strip_leading_doi_url(bib_entry['doi'])
        ##Try fetching crossref data:
        try:
            cross_rawdata = cr.works(ids = cr_id)
            print('hier')
            cross_data = cross_rawdata['message']
            ## Adding Authors
            if 'autor' not in bib_entry:
                autors_str = ''
                for author_entry in cross_data['author']:
                    if autors_str == '':
                        autors_str = f"{author_entry['family']}, {author_entry['given']}"
                    else:
                        autors_str += f" and {author_entry['family']}, {author_entry['given']}"
                bib_entry.update(author = autors_str)
            ## Adding Title
            if 'title' not in bib_entry:
                bib_entry.update(title=cross_data['title'][0])
            ## Adding Year
            if 'year' not in bib_entry:
                bib_entry.update(year=cross_data['created']['date-parts'][0][0])
                
        except:
            print('No entry found on crossref.org. Trying openaire.eu')
            requesturl = 'http://api.openaire.eu/search/researchProducts?format=csv&doi=' + bib_entry['doi']
            print(requesturl)
            openaireData = pd.read_csv(requesturl)
            print(openaireData)
                
            if len(openaireData) == 0:
                return bib_entry
            ## Adding Authors
            if 'autor' not in bib_entry:
                bib_entry.update(author = re.sub(';',' and ',openaireData['Authors'][0]))
            ## Adding Title
            if 'title' not in bib_entry:
                bib_entry.update(title=re.sub('\t','',openaireData['Title'][0]))
            ## Adding Year
            if 'year' not in bib_entry:
                bib_entry.update(year=openaireData['Publication Year'][0]) ## YYYY-MM-DD
        return bib_entry
        
    else:
        print('Neither doi nor url to fetch data. Aborting.')
        return bib_entry


def __main__():
    ### Handling Parameters
    parser = argparse.ArgumentParser(description='Handle parameters')

    ### file argument
    parser.add_argument('file', type=str, nargs='?', help='Bibfile to process')
    parser.add_argument("-S", "--sci-hub", action="store_true", dest="sci",
                        help="Change Reference Link to shadow library")
    parser.add_argument("-c", "--color", action="store", default='#000000', dest="qrcolor", help="Color of QR pixels")
    parser.add_argument("-t", "--type", action="store", default="png", dest="filetype",
                        help="output type, png is default")
    parser.add_argument("-v", "--verbose", action="store_true", dest="verbose", help="Verbose output")
    parser.add_argument("-s", "--style", action="store", default="withtext", dest="style",
                        help="Style of QR code, e.g. 'withtext' or 'qrcode'")
    parser.add_argument("-d", "--doi", action="store", default="", dest="doiInput",
                        help="Give a single DOI instead of a bib file. Will be ignored when bibfile is given.")
    args = parser.parse_args()

    ### Definitions
    bib_kwargs = {
        "font_size": 24,
        "qr_border_size": 2,
        "qr_pixel_size": 5,
        "qrcode_file_extension": args.filetype,
        "qrcolor": args.qrcolor,
        "ref_url": "https://sci-hub.st/" if args.sci else "https://doi.org/",
        "style": args.style,
        "doiInput": args.doiInput,
        "verbose": args.verbose
    }

    file = args.file  # 'Examples.bib' as default
    if args.doiInput == "" and file is None:
        print("No *.bib file or doi string given, nothing to do.")
        raise SystemExit()

    process_bibfile(file, **bib_kwargs)

def process_bibfile(bibfile: str,
                    qrcode_file_extension: str = 'png',
                    qrcolor: str = '#000000',
                    qr_border_size: int = 1,
                    qr_pixel_size: int = 20,
                    font_size: int = 24,
                    ref_url: str = 'https://doi.org/',
                    style: str = 'withtext',
                    doiInput: str = '',
                    verbose: bool = False) -> None:

    if bibfile is None:
        if verbose:
            print(f'Processing doi {doiInput}')
        bib_database = BibDatabase()
        bib_database.entries = [{
            'ID': re.sub(r'/', '|', doiInput),
            'doi': doiInput}]
    else:
        if verbose:
            print(f'Processing bibfile {bibfile}')
        with open(bibfile) as bibtex_file:
            bib_database = bibtexparser.load(bibtex_file)

    if verbose:
        print(f'Found {len(bib_database.entries)} entries in bibfile {bibfile}')

    ### Iterate through all entries in the file
    for entry, key in zip(bib_database.entries, bib_database.entries_dict):
        if 'doi' not in entry and 'url' not in entry:
            # print error message and skip entry
            print(f'Entry {key} does not have a DOI or URL')
            print('skipping entry')
            continue
        
        # In case entrys are missing:
        if ('title' not in entry) or ('title' not in entry) or ('title' not in entry):
            if verbose:
                print(f'Fetching missing data for {doiInput}')
            if style != 'qrcode':
                entry = complete_reference(entry)

        title = entry['title'] if 'title' in entry else "No Title"
        author = entry['author'] if 'author' in entry else ''
        year = entry['year'] if 'year' in entry else ''
        journal = entry['journal'] if 'journal' in entry else ''


        ### Modifications in case we use an DOI:
        if 'doi' in entry:
            ### Check that it's just the doi and not the whole link:
            doi = strip_leading_doi_url(entry['doi'])
            ### make it a link
            link = ref_url + doi  # Example: "https://doi.org/10.1002/andp.19053220607"
        else:
            ### Just use given url as backup.
            link = entry['url']


        ### Create QR code
        qr = qrcode.QRCode(
            version=1,  # number from 1-40, corresponds to size
            error_correction=qrcode.constants.ERROR_CORRECT_L,  # L 7%, M 15%, Q 25%, H 30 % of errors can be corrected
            box_size=qr_pixel_size,  # Pixelsize of one dot
            border=qr_border_size,  # Free space around
        )
        qr.add_data(link)  # text to qr
        qr.make()  # fit=True determines size automatically

        qr_img = qr.make_image(fill_color=qrcolor, back_color="white")#, size=(500, 500) #Parameter not needed?

        if style == 'withtext':
            pixel_border_size = qr_border_size * qr_pixel_size

            text_width = qr_img.size[0] * 5 - 2 * pixel_border_size

            back_size = (
                qr_img.size[0] + text_width + pixel_border_size,
                qr_img.size[1],
            )

            full_img = Image.new('RGBA', back_size, color=(0, 0, 0, 0))
            full_img.paste(qr_img, (0, 0))
            draw = ImageDraw.Draw(full_img)
            font = ImageFont.truetype(FredokaOne, font_size)
            fill_color = (24, 24, 24)

            local_get_wrapped_text = lambda text: get_wrapped_text(text, font, text_width)

            wrapped_text = f'{local_get_wrapped_text(strip_curly_braces(title))}\n' \
                           f'{journal}{", " if journal else ""}{year}\n' \
                           f'{local_get_wrapped_text(author)}'

            text_position = (
                qr_img.size[0] + pixel_border_size,
                pixel_border_size
            )

            draw.text(text_position, wrapped_text, font=font, fill=fill_color)

            img = full_img
        elif style == 'qrcode':
            img = qr_img
        else:
            raise ValueError(f'Unknown style {style}')

        qr_filename = f'{key}.{qrcode_file_extension}'

        if verbose:
            print(f'Writing QR code to {qr_filename}, link: {link}')

        img.save(qr_filename)


def test_strip_leading_doi_url():
    assert strip_leading_doi_url('http://www.doi.org/10.1002/andp.19053220607') == '10.1002/andp.19053220607'
    assert strip_leading_doi_url('http://dx.doi.org/10.1002/andp.19053220607') == '10.1002/andp.19053220607'
    assert strip_leading_doi_url('http://doi.org/10.1002/andp.19053220607') == '10.1002/andp.19053220607'

    assert strip_leading_doi_url('https://www.doi.org/10.1002/andp.19053220607') == '10.1002/andp.19053220607'
    assert strip_leading_doi_url('https://dx.doi.org/10.1002/andp.19053220607') == '10.1002/andp.19053220607'
    assert strip_leading_doi_url('https://doi.org/10.1002/andp.19053220607') == '10.1002/andp.19053220607'

    assert strip_leading_doi_url('www.doi.org/10.1002/andp.19053220607') == '10.1002/andp.19053220607'
    assert strip_leading_doi_url('dx.doi.org/10.1002/andp.19053220607') == '10.1002/andp.19053220607'
    assert strip_leading_doi_url('doi.org/10.1002/andp.19053220607') == '10.1002/andp.19053220607'

    assert strip_leading_doi_url('10.1002/andp.19053220607') == '10.1002/andp.19053220607'
    assert strip_leading_doi_url('') == ''


def test_strip_curly_braces():
    assert strip_curly_braces('{foo}') == 'foo'
    assert strip_curly_braces('{foo} bar') == 'foo bar'
    assert strip_curly_braces('{foo} {bar}') == 'foo bar'
    assert strip_curly_braces('{foo} {bar} {baz}') == 'foo bar baz'

    assert strip_curly_braces('foo') == 'foo'
    assert strip_curly_braces('foo bar') == 'foo bar'
    assert strip_curly_braces('foo bar baz') == 'foo bar baz'

    assert strip_curly_braces('') == ''


def test_get_wrapped_text():
    font = ImageFont.truetype(FredokaOne, 20)
    assert get_wrapped_text('foo bar', font, 0) == '\nfoo\nbar'
    assert get_wrapped_text('foo bar', font, 1000) == 'foo bar'


if __name__ == '__main__':
    __main__()

#! /usr/bin/env python3

import sys
import re

def fdier(in_stream, target_regex,
             start_regex = None,
             stop_regex = None):
    """
    -------------------------------------------------------------------------
    Parameters
    -------------------------------------------------------------------------
    in_stream : A file object
        Input
    target_regex : A regular expression object
        Search item in `in_stream`
    start_regex : A regular expression object
        Where the targeted regular expression object can begin to be searched for
        in `in_stream`
    stop_regex :
        Where the targeted regular expression object can no longer be searched for
        in `in_stream`
    """
    search_has_started = False
    if not start_regex:
        search_has_started = True
    for line_index, line in enumerate(in_stream):
        if stop_regex and stop_regex.match(line):
            break
        if start_regex and (not search_has_started):
            if start_regex.match(line):
                search_has_started = True
            continue
        for match_object in target_regex.finditer(line):
            yield line_index, match_object

def record_occurrences(in_stream, out_stream,
        target_regex,
        start_regex = None,
        stop_regex = None):
    """
    Counts the occurrences of words matching the targeted regular expression
    and records the line number it occurs on.
    ------------------------------------------------------------------------
    Parameters
    ------------------------------------------------------------------------
    in_stream : A file object
        Input, in this case, 'On the Origin of Species'
    out_stream : A file object
        Output containing line number and words matching regular expression
    target_regex : A regular expression object
        Search item in `in_stream`
    start_regex : A regular expression object
        Where the targeted regular expression object can begin to be searched for
        in `in_stream`
    stop_regex :
        Where the targeted regular expression object can no longer be searched for
        in `in_stream`
    """
    occurrences = 0
    for line_index, match_obj in fdier(in_stream, target_regex,
            start_regex, stop_regex):
        occurrences += 1
        for target_str in match_obj.groups():
            out_stream.write("{line_num}\t{string}\n".format(
                    line_num = line_index + 1,
                    string = target_str))
    return occurrences



if __name__ == '__main__':
    target_pattern = re.compile(r'(^\w*herit\w*)', re.IGNORECASE)
    start_pattern = re.compile(r'^\*\*\*\s*START.*$')
    stop_pattern = re.compile(r'^\*\*\*\s*END.*$')
    in_path = 'origin.txt'
    out_path = 'origin-output.txt'
    with open(in_path, 'r') as in_stream:
        with open(out_path, 'w') as out_stream:
            occurrences = record_occurrences(in_stream=in_stream,
            out_stream=out_stream,
            target_regex=target_pattern,
            start_regex=start_pattern,
            stop_regex=stop_pattern)
    message = "Chucky D referred to heritability {0} times!".format(
            occurrences)
    print(message)

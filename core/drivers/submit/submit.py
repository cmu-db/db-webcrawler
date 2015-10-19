import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))

import mechanize
import cookielib
import string
import random

from patterns import patterns, match_any_pattern
import extract

def get_form_index(br, form):
    index = 0
    for f in br.forms():
        if str(f.attrs.get('name', '')) != '':
            if str(f.attrs.get('name', '')) == form['name']:
                break
            else:
                continue
        if str(f.attrs.get('action', '')) == form['action']:
            break
        if str(f.attrs.get('method', '')).lower() == form['method']:
            break
        index = index + 1
    return index

def submit_form(form, inputs, br = None):
    if br == None:
        br = mechanize.Browser()
        cj = cookielib.LWPCookieJar() 
        br.set_cookiejar(cj)

    br.open(form['url'])
    br.select_form(nr=get_form_index(br, form))

    for input in form['inputs']:
        if input['name'] in inputs:
            if input['type'] == 'file':
                flag = True
                filename = inputs[input['name']]
                br.form.add_file(open(filename), 'text/plain', filename)
                br.form.set_all_readonly(False)
            else:
                if input['name'] in br.form:
                    br.form[input['name']] = inputs[input['name']]

    response = br.submit().read()

    return response, br

def gen_random_value(chars = string.ascii_letters + string.digits, length = 0):
    if length == 0:
        length = random.choice(range(8, 21))
    return ''.join(random.choice(chars) for x in range(length))

def fill_form(form, matched_patterns = {}, br = None):
    inputs = {}
    for input in form['inputs']:
        for pattern_name in patterns:
            pattern, value = patterns[pattern_name]
            if match_any_pattern(input['name'], pattern) or match_any_pattern(input['type'], pattern):
                if pattern_name in matched_patterns:
                    inputs[input['name']] = matched_patterns[pattern_name]
                else:
                    inputs[input['name']] = value[0]
                    matched_patterns[pattern_name] = value[0]
                break
            else :
                inputs[input['name']] = gen_random_value()

    response, br = submit_form(form, inputs, br)

    return matched_patterns, inputs, response, br

def fill_form_random(deploy_path, form, br):
    inputs = {}
    for input in form['inputs']:
        if input['type'] == 'file':
            filename = os.path.join(deploy_path, gen_random_value())
            with open(filename, 'w') as f:
                f.write(gen_random_value(length = 1000))
            f.close()
            inputs[input['name']] = filename
        else:
            inputs[input['name']] = gen_random_value()

    response, br = submit_form(form, inputs, br)

    return inputs

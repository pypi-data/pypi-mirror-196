def timeout(function_module, seconds):
    import os
    from subprocess import check_output
    value = check_output(["python", os.path.dirname(os.path.realpath(__file__))+'\\function_timeout.py',seconds,function_module])
    return value.strip()[-5:]
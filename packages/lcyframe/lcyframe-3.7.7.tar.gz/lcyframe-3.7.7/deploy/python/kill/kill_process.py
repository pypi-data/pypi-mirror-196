import psutil

def kills(pid):
    """Kills all process"""
    try:
        parent = psutil.Process(int(pid))
    except:
        return False
    for child in parent.children(recursive=True):
        try:
            child.kill()
        except:
            continue
    parent.kill()
    return True
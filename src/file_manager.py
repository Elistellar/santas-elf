from pathlib import Path


BASE_DIR = Path(__file__).parent.parent

def path(_path: str) -> str:
    """
    1. Check if the given path exist
    2. If not, create it
    3. Return the file's absolute path
    """
    
    _path = BASE_DIR / _path
    
    if not _path.exists():
        
        if not _path.parent.exists():
            _path.parent.mkdir(parents=True)
        
        _path.touch()
    
    return str(_path)
    
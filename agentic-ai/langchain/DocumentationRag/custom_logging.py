class Colors:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def log_info(message:str, color:str=Colors.CYAN):
    """Logs an informational message with a consistent format."""
    print(f"{color}ℹ️{message}{Colors.END}")

def log_error(message:str, color:str=Colors.RED):
    """Logs an error message with a consistent format."""
    print(f"{color}❌ {message}{Colors.END}")

def log_warning(message:str, color:str=Colors.YELLOW):
    """Logs a warning message with a consistent format."""
    print(f"{color}⚠️ {message}{Colors.END}")

def log_success(message:str, color:str=Colors.GREEN):
    """Logs a success message with a consistent format."""
    print(f"{color}✅ {message}{Colors.END}")

def log_header(message:str):
    """Logs a header message with a consistent format."""
    print(f"{Colors.BOLD}{Colors.PURPLE}{'*'*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.PURPLE}🚀{message}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.PURPLE}{'*'*60}{Colors.END}")


import logging
from functools import wraps

# --------------------------------------------------------------------
# 1️⃣  Configure a module‑level logger (you can tweak level / handler)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s [%(module)s:%(lineno)d] %(message)s",
)
log = logging.getLogger(__name__)

# --------------------------------------------------------------------
def log_call(func):
    """
    Decorator that logs:

        * function / method name
        * all input arguments (positional + keyword)
        * the return value

    Usage is identical to a normal decorator – just add `@log_call` above your
    function or method definition.
    """

    @wraps(func)               # preserves __name__, __doc__, etc.
    def wrapper(*args, **kwargs):
        # ---- Build a human‑readable argument list --------------------
        arg_parts = [repr(a) for a in args]
        kw_parts  = [f"{k}={v!r}" for k, v in kwargs.items()]
        all_args_str = ", ".join(arg_parts + kw_parts)

        # ---- Log the call --------------------------------------------
        log.info(f"Calling {func.__qualname__}({all_args_str})")

        try:
            result = func(*args, **kwargs)
        except Exception as exc:                # keep the exception for the caller
            log.exception(f"{func.__qualname__} raised an exception")
            raise

        # ---- Log the return value -------------------------------------
        log.info(f"{func.__qualname__} returned {result!r}")

        return result

    return wrapper

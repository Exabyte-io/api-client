from typing import Dict, Tuple

# Mapping of HTTP status codes to (display_text, suggestion)
HTTP_ERROR_MAP: Dict[int, Tuple[str, str]] = {
    400: (
        "Bad Request",
        "Check your request parameters and data.",
    ),
    401: (
        "Unauthorized",
        "Check your authentication credentials or run `mat3ra login` to re-authenticate.",
    ),
    402: (
        "Payment Required",
        "Insufficient account balance. Please make a payment or reduce the job time limit.",
    ),
    403: (
        "Forbidden",
        "You do not have permission. Ensure the correct project is set and your account has the required permissions.",
    ),
    404: (
        "Not Found",
        "The requested resource does not exist. Verify the ID or path, and ensure the correct project is set.",
    ),
    409: (
        "Conflict",
        "A resource with this identifier already exists.",
    ),
    422: (
        "Unprocessable Entity",
        "The request data is invalid. Check your input.",
    ),
    429: (
        "Too Many Requests",
        "You have exceeded your quota. Update your quota or try again later.",
    ),
    500: (
        "Internal Server Error",
        "An error occurred on the server. Contact support if the problem persists.",
    ),
    503: (
        "Service Unavailable",
        "The service is temporarily unavailable. Try again later.",
    ),
}

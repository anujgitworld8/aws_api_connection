# Method containing response headers.
def add_headers(response):
    response.headers["server"] = "False"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; frame-ancestors 'self'; object-src 'none'; script-src 'self' 'unsafe-inline'; connect-src 'self'; img-src 'self'; style-src 'self' 'unsafe-inline'; form-action 'self'; frame-ancestors 'self';"
    )
    response.headers["Cross-Origin-Opener-Policy"] = "same-origin"
    response.headers["Content-Type-Options"] = "nosniff"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Strict-Transport-Security"] = (
        "max-age=31556926; includeSubDomains; preload"
    )
    response.headers["Frame-Options"] = "DENY"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Access-Control-Max-Age"] = "86400"
    response.headers["Access-Control-Allow-Origin"] = "same-origin"
    response.headers["Access-Control-Allow-Headers"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "*"
    response.headers["Access-Control-Request-Headers"] = "*"
    response.headers["Access-Control-Request-Method"] = "*"
    response.headers["Cache-Control"] = "no-cache; no-store; must-revalidate"


file_headers = {
    "server": "False",
    "Content-Security-Policy": "default-src 'self'; frame-ancestors 'self'; object-src 'none'; script-src 'self' 'unsafe-inline'; connect-src 'self'; img-src 'self'; style-src 'self' 'unsafe-inline'; form-action 'self'; frame-ancestors 'self'",
    "Cross-Origin-Opener-Policy": "same-origin",
    "Content-Type-Options": "nosniff",
    "X-Content-Type-Options": "nosniff",
    "Strict-Transport-Security": "max-age:31536000; includeSubDomains; preload",
    "Frame-Options": "DENY",
    "X-Frame-Options": "DENY",
    "XSS-Protection": "1; mode:block",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "Access-Control-Max-Age": "86400",
    "Access-Control-Allow-Origin": "same-origin",
    "Access-Control-Allow-Headers": "*",
    "Access-Control-Allow-Methods": "*",
    "Access-Control-Request-Headers": "*",
    "Access-Control-Request-Method": "*",
    "Cache-Control": "no-cache; no-store; must-revalidate",
}

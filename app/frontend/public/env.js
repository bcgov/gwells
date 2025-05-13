(function (window) {
    window.env = window.env || {};
    window.env.DEBUG = "{$PATH}"; // Use Caddy's env var syntax
    window.env.AXIOS_BASE_URL = "{$AXIOS_BASE_URL}";
    window.env.API_BASE_URL = "{$API_BASE_TEST}";
})(window);
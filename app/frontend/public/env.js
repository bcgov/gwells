(function (window) {
    window.env = window.env || {};
    window.env.AXIOS_BASE_URL = "{{.Env.AXIOS_BASE_URL}}";
})(window);
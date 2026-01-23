(function (window) {
    window.env = window.env || {};
    window.env.VITE_AXIOS_BASE_URL = "{{.Env.VITE_AXIOS_BASE_URL}}";
})(window);
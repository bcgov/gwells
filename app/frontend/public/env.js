(function (window) {
    window.env = window.env || {};
    window.env.BACKEND_URL = "{{.Env.BACKEND_URL}}";
    window.env.VITE_BACKEND_URL = "{{.Env.VITE_BACKEND_URL}}";
    window.env.VITE_AXIOS_BASE_URL = "{{.Env.VITE_AXIOS_BASE_URL}}";
})(window);
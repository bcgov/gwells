(function (window) {
    window.env = window.env || {};
    window.env.DEBUG = "Template system is: {{.Env.PATH}}"; // PATH should always exist
    window.env.AXIOS_BASE_URL = "{{.Env.AXIOS_BASE_URL}}";
    window.env.API_BASE_URL = "{{.Env.API_BASE_URL}}";
})(window);
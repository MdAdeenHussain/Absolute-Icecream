(function () {
    "use strict";

    const STORAGE_KEY = "absolute-theme";

    const root = document.documentElement;

    function getSystemTheme() {
        return window.matchMedia(
            "(prefers-color-scheme: dark)"
        ).matches
            ? "dark"
            : "light";
    }

    function getStoredTheme() {
        const stored = localStorage.getItem(
            STORAGE_KEY
        );

        if (
            stored === "light" ||
            stored === "dark"
        ) {
            return stored;
        }

        return null;
    }

    function applyTheme(theme) {
        root.setAttribute(
            "data-theme",
            theme
        );
    }

    function initializeTheme() {
        const storedTheme = getStoredTheme();

        applyTheme(
            storedTheme || getSystemTheme()
        );
    }

    function toggleTheme() {
        const currentTheme =
            root.getAttribute("data-theme") ||
            getSystemTheme();

        const nextTheme =
            currentTheme === "dark"
                ? "light"
                : "dark";

        applyTheme(nextTheme);

        localStorage.setItem(
            STORAGE_KEY,
            nextTheme
        );
    }

    initializeTheme();

    document.addEventListener(
        "DOMContentLoaded",
        function () {

            const toggleButtons =
                document.querySelectorAll(
                    "[data-theme-toggle]"
                );

            toggleButtons.forEach(
                function (button) {
                    button.addEventListener(
                        "click",
                        toggleTheme
                    );
                }
            );

            const mediaQuery =
                window.matchMedia(
                    "(prefers-color-scheme: dark)"
                );

            mediaQuery.addEventListener(
                "change",
                function () {

                    if (!getStoredTheme()) {
                        applyTheme(
                            getSystemTheme()
                        );
                    }

                }
            );

        }
    );

})();
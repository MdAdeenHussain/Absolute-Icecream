(function () {
    "use strict";

    document.addEventListener(
        "DOMContentLoaded",
        function () {

            initializeMobileMenu();
            initializeScrollProgress();
            initializeRevealAnimations();
            initializeCookieBanner();
            initializeCartDrawer();
            initializeModalSystem();
            refreshIcons();

        }
    );


    /* =====================================================
       ICONS
       ===================================================== */

    function refreshIcons() {

        if (
            typeof lucide !== "undefined"
        ) {
            lucide.createIcons();
        }

    }


    /* =====================================================
       MOBILE MENU
       ===================================================== */

    function initializeMobileMenu() {

        const menu =
            document.querySelector(
                "[data-mobile-menu]"
            );

        const backdrop =
            document.querySelector(
                "[data-mobile-menu-backdrop]"
            );

        const openButton =
            document.querySelector(
                "[data-mobile-menu-open]"
            );

        const closeButton =
            document.querySelector(
                "[data-mobile-menu-close]"
            );

        if (
            !menu ||
            !backdrop ||
            !openButton
        ) {
            return;
        }

        function openMenu() {

            menu.classList.add(
                "is-open"
            );

            backdrop.classList.add(
                "is-visible"
            );

            menu.setAttribute(
                "aria-hidden",
                "false"
            );

            openButton.setAttribute(
                "aria-expanded",
                "true"
            );

            document.body.style.overflow =
                "hidden";
        }

        function closeMenu() {

            menu.classList.remove(
                "is-open"
            );

            backdrop.classList.remove(
                "is-visible"
            );

            menu.setAttribute(
                "aria-hidden",
                "true"
            );

            openButton.setAttribute(
                "aria-expanded",
                "false"
            );

            document.body.style.overflow =
                "";
        }

        openButton.addEventListener(
            "click",
            openMenu
        );

        if (closeButton) {
            closeButton.addEventListener(
                "click",
                closeMenu
            );
        }

        backdrop.addEventListener(
            "click",
            closeMenu
        );

        menu
            .querySelectorAll("a")
            .forEach(function (link) {

                link.addEventListener(
                    "click",
                    closeMenu
                );

            });

        document.addEventListener(
            "keydown",
            function (event) {

                if (
                    event.key === "Escape" &&
                    menu.classList.contains(
                        "is-open"
                    )
                ) {
                    closeMenu();
                }

            }
        );

    }


    /* =====================================================
       SCROLL PROGRESS
       ===================================================== */

    function initializeScrollProgress() {

        const progress =
            document.querySelector(
                "#scroll-progress"
            );

        if (!progress) {
            return;
        }

        function updateProgress() {

            const scrollTop =
                window.scrollY;

            const documentHeight =
                document.documentElement
                    .scrollHeight -
                window.innerHeight;

            if (documentHeight <= 0) {
                progress.style.width = "0%";
                return;
            }

            const percentage =
                Math.min(
                    100,
                    Math.max(
                        0,
                        (scrollTop /
                            documentHeight) *
                            100
                    )
                );

            progress.style.width =
                `${percentage}%`;
        }

        window.addEventListener(
            "scroll",
            updateProgress,
            {
                passive: true
            }
        );

        updateProgress();
    }


    /* =====================================================
       SCROLL REVEAL
       ===================================================== */

    function initializeRevealAnimations() {

        const elements =
            document.querySelectorAll(
                "[data-reveal]"
            );

        if (!elements.length) {
            return;
        }

        if (
            window.matchMedia(
                "(prefers-reduced-motion: reduce)"
            ).matches
        ) {
            elements.forEach(
                element =>
                    element.classList.add(
                        "is-visible"
                    )
            );

            return;
        }

        const observer =
            new IntersectionObserver(
                function (entries) {

                    entries.forEach(
                        function (entry) {

                            if (
                                entry.isIntersecting
                            ) {

                                entry.target.classList.add(
                                    "is-visible"
                                );

                                observer.unobserve(
                                    entry.target
                                );
                            }

                        }
                    );

                },
                {
                    threshold: 0.12,
                    rootMargin: "0px 0px -50px 0px"
                }
            );

        elements.forEach(
            element =>
                observer.observe(element)
        );

    }


    /* =====================================================
       COOKIE CONSENT
       ===================================================== */

    function initializeCookieBanner() {

        const banner =
            document.querySelector(
                "[data-cookie-banner]"
            );

        if (!banner) {
            return;
        }

        const STORAGE_KEY =
            "absolute-cookie-consent";

        const stored =
            localStorage.getItem(
                STORAGE_KEY
            );

        if (!stored) {

            window.setTimeout(
                function () {

                    banner.classList.add(
                        "is-visible"
                    );

                    banner.setAttribute(
                        "aria-hidden",
                        "false"
                    );

                },
                900
            );

        }

        function saveConsent(value) {

            localStorage.setItem(
                STORAGE_KEY,
                value
            );

            banner.classList.remove(
                "is-visible"
            );

            banner.setAttribute(
                "aria-hidden",
                "true"
            );

            /*
             * Analytics initialization will be
             * connected here in Step 10.
             */

        }

        const accept =
            banner.querySelector(
                "[data-cookie-accept]"
            );

        const reject =
            banner.querySelector(
                "[data-cookie-reject]"
            );

        if (accept) {
            accept.addEventListener(
                "click",
                function () {
                    saveConsent("analytics");
                }
            );
        }

        if (reject) {
            reject.addEventListener(
                "click",
                function () {
                    saveConsent("essential");
                }
            );
        }

    }


    /* =====================================================
       CART DRAWER
       ===================================================== */

    function initializeCartDrawer() {

        const drawer =
            document.querySelector(
                "[data-cart-drawer]"
            );

        if (!drawer) {
            return;
        }

        const openButtons =
            document.querySelectorAll(
                "[data-cart-open]"
            );

        const closeButtons =
            document.querySelectorAll(
                "[data-cart-close]"
            );

        function openCart() {

            drawer.classList.add(
                "is-open"
            );

            drawer.setAttribute(
                "aria-hidden",
                "false"
            );

            document.body.style.overflow =
                "hidden";
        }

        function closeCart() {

            drawer.classList.remove(
                "is-open"
            );

            drawer.setAttribute(
                "aria-hidden",
                "true"
            );

            document.body.style.overflow =
                "";
        }

        openButtons.forEach(
            button =>
                button.addEventListener(
                    "click",
                    openCart
                )
        );

        closeButtons.forEach(
            button =>
                button.addEventListener(
                    "click",
                    closeCart
                )
        );

        document.addEventListener(
            "keydown",
            function (event) {

                if (
                    event.key === "Escape" &&
                    drawer.classList.contains(
                        "is-open"
                    )
                ) {
                    closeCart();
                }

            }
        );

    }


    /* =====================================================
       MODAL SYSTEM
       ===================================================== */

    function initializeModalSystem() {

        const modals =
            document.querySelectorAll(
                ".modal"
            );

        modals.forEach(
            function (modal) {

                const closeButtons =
                    modal.querySelectorAll(
                        "[data-modal-close]"
                    );

                closeButtons.forEach(
                    function (button) {

                        button.addEventListener(
                            "click",
                            function () {
                                closeModal(modal);
                            }
                        );

                    }
                );

            }
        );

        document.addEventListener(
            "keydown",
            function (event) {

                if (
                    event.key !== "Escape"
                ) {
                    return;
                }

                document
                    .querySelectorAll(
                        ".modal.is-open"
                    )
                    .forEach(closeModal);

            }
        );

    }


    function openModal(modal) {

        if (!modal) {
            return;
        }

        modal.classList.add(
            "is-open"
        );

        modal.setAttribute(
            "aria-hidden",
            "false"
        );

        document.body.style.overflow =
            "hidden";
    }


    function closeModal(modal) {

        if (!modal) {
            return;
        }

        modal.classList.remove(
            "is-open"
        );

        modal.setAttribute(
            "aria-hidden",
            "true"
        );

        document.body.style.overflow =
            "";
    }


})();

/* =========================================================
   HOMEPAGE
========================================================= */

document.addEventListener("DOMContentLoaded", () => {

    /*
     * Hero parallax
     */

    const heroProduct = document.querySelector(".hero-product");

    if (heroProduct &&
        !window.matchMedia("(prefers-reduced-motion: reduce)").matches) {

        window.addEventListener("mousemove", (event) => {

            const x =
                (event.clientX / window.innerWidth - 0.5) * 2;

            const y =
                (event.clientY / window.innerHeight - 0.5) * 2;

            heroProduct.style.transform = `
                translate3d(
                    ${x * 8}px,
                    ${y * 8}px,
                    0
                )
            `;

        });

    }


    /*
     * Sugar target count-up
     */

    const target = document.querySelector(".target-value strong");

    if (target) {

        const observer = new IntersectionObserver(
            (entries, observer) => {

                if (!entries[0].isIntersecting) {
                    return;
                }

                let current = 0;
                const end = 0.5;
                const duration = 1000;
                const startTime = performance.now();

                function animate(time) {

                    const progress = Math.min(
                        (time - startTime) / duration,
                        1
                    );

                    current = end * progress;

                    target.textContent =
                        `≤${current.toFixed(1)}`;

                    if (progress < 1) {
                        requestAnimationFrame(animate);
                    }

                }

                requestAnimationFrame(animate);

                observer.disconnect();

            },
            {
                threshold: 0.5
            }
        );

        observer.observe(target);
    }


});
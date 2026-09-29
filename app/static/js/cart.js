class AbsoluteCart {

    constructor() {

        this.drawer =
            document.querySelector("#cart-drawer");

        this.itemsContainer =
            document.querySelector("#cart-items");

        this.subtotalElement =
            document.querySelector("#cart-subtotal");

        this.countElements =
            document.querySelectorAll(
                "[data-cart-count]"
            );

        this.bindEvents();

        this.refresh();

    }


    async request(
        url,
        options = {}
    ) {

        const response = await fetch(
            url,
            {
                headers: {
                    "Content-Type":
                        "application/json",
                    ...(options.headers || {})
                },
                ...options
            }
        );

        const data =
            await response.json();

        if (!response.ok) {

            throw new Error(
                data.error ||
                "Something went wrong."
            );

        }

        return data;

    }


    async refresh() {

        try {

            const data =
                await this.request(
                    "/api/cart"
                );

            this.render(data);

        } catch (error) {

            console.error(
                "Cart error:",
                error
            );

        }

    }


    async add(
        variantId,
        quantity = 1
    ) {

        try {

            const data =
                await this.request(
                    "/api/cart/add",
                    {
                        method: "POST",
                        body: JSON.stringify({
                            variant_id: variantId,
                            quantity: quantity
                        })
                    }
                );

            this.render(data);

            this.open();

            this.showMessage(
                "Added to cart"
            );

        } catch (error) {

            this.showMessage(
                error.message,
                true
            );

        }

    }


    async update(
        variantId,
        quantity
    ) {

        try {

            const data =
                await this.request(
                    "/api/cart/update",
                    {
                        method: "PATCH",
                        body: JSON.stringify({
                            variant_id: variantId,
                            quantity: quantity
                        })
                    }
                );

            this.render(data);

        } catch (error) {

            this.showMessage(
                error.message,
                true
            );

            this.refresh();

        }

    }


    async remove(variantId) {

        try {

            const data =
                await this.request(
                    `/api/cart/remove/${variantId}`,
                    {
                        method: "DELETE"
                    }
                );

            this.render(data);

        } catch (error) {

            this.showMessage(
                error.message,
                true
            );

        }

    }


    render(data) {

        const items =
            data.items || [];

        const count =
            data.item_count || 0;

        const subtotal =
            Number(
                data.subtotal || 0
            );


        this.countElements.forEach(
            element => {

                element.textContent =
                    count;

                element.hidden =
                    count === 0;

            }
        );


        if (this.subtotalElement) {

            this.subtotalElement.textContent =
                this.money(subtotal);

        }


        if (!this.itemsContainer) {
            return;
        }


        if (!items.length) {

            this.itemsContainer.innerHTML = `
                <div class="cart-empty">

                    <div class="cart-empty-mark">
                        ○
                    </div>

                    <h3>
                        Your freezer is empty.
                    </h3>

                    <p>
                        Add an Absolute flavour to begin.
                    </p>

                    <a
                        href="/shop"
                        class="btn btn-primary">
                        Explore flavours
                    </a>

                </div>
            `;

            return;
        }


        this.itemsContainer.innerHTML =
            items.map(
                item => this.itemHTML(item)
            ).join("");


        this.bindItemEvents();

    }


    itemHTML(item) {

        const image =
            item.image
                ? `
                    <img
                        src="/static/${this.escape(
                            item.image
                        )}"
                        alt="${this.escape(
                            item.name
                        )}">
                  `
                : `
                    <div class="cart-item-placeholder">
                        ${this.escape(
                            item.name
                        )}
                    </div>
                  `;


        return `
            <article
                class="cart-item"
                data-variant-id="${item.variant_id}">

                <div class="cart-item-image">
                    ${image}
                </div>

                <div class="cart-item-content">

                    <div class="cart-item-heading">

                        <div>

                            <span>
                                ${this.escape(
                                    item.flavour
                                )}
                            </span>

                            <h3>
                                ${this.escape(
                                    item.name
                                )}
                            </h3>

                            <small>
                                ${this.escape(
                                    item.size
                                )}
                            </small>

                        </div>

                        <button
                            type="button"
                            class="cart-item-remove"
                            data-remove-item
                            aria-label="Remove item">

                            ×

                        </button>

                    </div>


                    <div class="cart-item-bottom">

                        <div class="quantity-control">

                            <button
                                type="button"
                                data-quantity-minus>
                                −
                            </button>

                            <span>
                                ${item.quantity}
                            </span>

                            <button
                                type="button"
                                data-quantity-plus>
                                +
                            </button>

                        </div>


                        <strong>
                            ${this.money(
                                item.line_total
                            )}
                        </strong>

                    </div>

                </div>

            </article>
        `;

    }


    bindItemEvents() {

        document
            .querySelectorAll(
                "[data-remove-item]"
            )
            .forEach(button => {

                button.addEventListener(
                    "click",
                    () => {

                        const item =
                            button.closest(
                                ".cart-item"
                            );

                        const id =
                            item.dataset.variantId;

                        this.remove(id);

                    }
                );

            });


        document
            .querySelectorAll(
                "[data-quantity-minus]"
            )
            .forEach(button => {

                button.addEventListener(
                    "click",
                    () => {

                        const item =
                            button.closest(
                                ".cart-item"
                            );

                        const id =
                            item.dataset.variantId;

                        const quantity =
                            Number(
                                item.querySelector(
                                    ".quantity-control span"
                                ).textContent
                            );

                        this.update(
                            id,
                            quantity - 1
                        );

                    }
                );

            });


        document
            .querySelectorAll(
                "[data-quantity-plus]"
            )
            .forEach(button => {

                button.addEventListener(
                    "click",
                    () => {

                        const item =
                            button.closest(
                                ".cart-item"
                            );

                        const id =
                            item.dataset.variantId;

                        const quantity =
                            Number(
                                item.querySelector(
                                    ".quantity-control span"
                                ).textContent
                            );

                        this.update(
                            id,
                            quantity + 1
                        );

                    }
                );

            });

    }


    bindEvents() {

        document
            .querySelectorAll(
                "[data-cart-open]"
            )
            .forEach(button => {

                button.addEventListener(
                    "click",
                    () => this.open()
                );

            });


        document
            .querySelectorAll(
                "[data-cart-close]"
            )
            .forEach(button => {

                button.addEventListener(
                    "click",
                    () => this.close()
                );

            });

    }


    open() {

        if (!this.drawer) {
            return;
        }

        this.drawer.classList.add(
            "is-open"
        );

        this.drawer.setAttribute(
            "aria-hidden",
            "false"
        );

        document.body.classList.add(
            "cart-open"
        );

    }


    close() {

        if (!this.drawer) {
            return;
        }

        this.drawer.classList.remove(
            "is-open"
        );

        this.drawer.setAttribute(
            "aria-hidden",
            "true"
        );

        document.body.classList.remove(
            "cart-open"
        );

    }


    showMessage(
        message,
        error = false
    ) {

        const element =
            document.createElement(
                "div"
            );

        element.className =
            `cart-toast ${
                error ? "is-error" : ""
            }`;

        element.textContent =
            message;

        document.body.appendChild(
            element
        );

        requestAnimationFrame(() => {

            element.classList.add(
                "is-visible"
            );

        });

        setTimeout(() => {

            element.classList.remove(
                "is-visible"
            );

            setTimeout(
                () => element.remove(),
                250
            );

        }, 2200);

    }


    money(value) {

        return new Intl.NumberFormat(
            "en-IN",
            {
                style: "currency",
                currency: "INR",
                maximumFractionDigits: 0
            }
        ).format(value);

    }


    escape(value) {

        return String(value)
            .replaceAll("&", "&amp;")
            .replaceAll("<", "&lt;")
            .replaceAll(">", "&gt;")
            .replaceAll('"', "&quot;")
            .replaceAll("'", "&#039;");

    }

}


document.addEventListener(
    "DOMContentLoaded",
    () => {

        window.AbsoluteCart =
            new AbsoluteCart();

    }
);
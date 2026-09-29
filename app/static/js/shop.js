document.addEventListener("DOMContentLoaded", () => {

    /*
     * SHOP FILTERS
     */

    const filterButtons =
        document.querySelectorAll(".filter-button");

    const products =
        document.querySelectorAll(".shop-product");

    filterButtons.forEach(button => {

        button.addEventListener("click", () => {

            filterButtons.forEach(item => {
                item.classList.remove("active");
            });

            button.classList.add("active");

            const filter =
                button.dataset.filter;

            products.forEach(product => {

                const name =
                    product.dataset.productName || "";

                let show = true;

                if (filter === "dark-chocolate") {
                    show = name.includes("dark chocolate");
                }

                if (filter === "coffee") {
                    show = name.includes("coffee");
                }

                if (filter === "vanilla") {
                    show = name.includes("vanilla");
                }

                product.hidden = !show;

            });

        });

    });


    /*
     * PRODUCT VARIANTS
     */

    const variantButtons =
        document.querySelectorAll(".variant-option");

    const priceElement =
        document.querySelector("#product-price");

    const selectedSize =
        document.querySelector("#selected-size");

    const addButton =
        document.querySelector("#add-product-to-cart");


    let selectedVariant = null;


    variantButtons.forEach(button => {

        const stock =
            Number(button.dataset.stock || 0);

        if (stock <= 0) {

            button.disabled = true;

            button.insertAdjacentHTML(
                "beforeend",
                `<small class="variant-coming-soon">
                    Coming soon
                </small>`
            );

        }


        button.addEventListener("click", () => {

            if (button.disabled) {
                return;
            }

            variantButtons.forEach(item => {
                item.classList.remove("selected");
            });

            button.classList.add("selected");

            selectedVariant = {
                id: button.dataset.variantId,
                price: button.dataset.price,
                size: button.dataset.size
            };

            if (priceElement) {

                priceElement.textContent =
                    `₹${Number(
                        selectedVariant.price
                    ).toLocaleString("en-IN")}`;

            }

            if (selectedSize) {

                selectedSize.textContent =
                    selectedVariant.size;

            }

            if (addButton) {

                addButton.disabled = false;
                addButton.textContent =
                    "Add to cart";

            }

        });

    });


    /*
     * ADD TO CART
     *
     * The actual persistent cart API is connected
     * in Step 6.
     */

    if (addButton) {

    addButton.addEventListener(
        "click",
        async () => {

            if (!selectedVariant) {
                return;
            }

            if (
                window.AbsoluteCart &&
                typeof window.AbsoluteCart.add === "function"
            ) {

                await window.AbsoluteCart.add(
                    selectedVariant.id,
                    1
                );

                addButton.textContent =
                    "Added to cart ✓";

                setTimeout(() => {

                    addButton.textContent =
                        "Add to cart";

                }, 1500);

            }

        }
    );

}
});
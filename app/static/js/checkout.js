document.addEventListener(
    "DOMContentLoaded",
    () => {

        const form =
            document.querySelector(
                "#checkout-form"
            );

        if (!form) {
            return;
        }


        const submitButton =
            document.querySelector(
                "#checkout-submit"
            );

        const errorElement =
            document.querySelector(
                "#checkout-error"
            );


        form.addEventListener(
            "submit",
            async event => {

                event.preventDefault();

                errorElement.textContent =
                    "";

                submitButton.disabled =
                    true;

                submitButton.textContent =
                    "Creating order…";


                const formData =
                    new FormData(form);


                const payload =
                    Object.fromEntries(
                        formData.entries()
                    );


                try {

                    const response =
                        await fetch(
                            "/api/checkout/create",
                            {
                                method: "POST",

                                headers: {
                                    "Content-Type":
                                        "application/json"
                                },

                                body:
                                    JSON.stringify(
                                        payload
                                    )
                            }
                        );


                    const data =
                        await response.json();


                    if (!response.ok) {

                        throw new Error(
                            data.error ||
                            "Unable to create order."
                        );

                    }


                    /*
                     * Payment gateway integration
                     * will happen after order creation.
                     */

                    window.location.href =
                        `/checkout/payment/${data.order_id}`;

                } catch (error) {

                    errorElement.textContent =
                        error.message;

                    submitButton.disabled =
                        false;

                    submitButton.textContent =
                        "Continue to payment";

                }

            }
        );

    }
);
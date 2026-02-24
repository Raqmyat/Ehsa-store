/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { ControlButtons } from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";
import { NumberPopup } from "@point_of_sale/app/utils/input_popups/number_popup";
import { makeAwaitable } from "@point_of_sale/app/store/make_awaitable_dialog";
import { _t } from "@web/core/l10n/translation";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";

patch(ControlButtons.prototype, {
    async clickFixedDiscount() {
        const order = this.pos.get_order();
        const selectedLine = order.get_selected_orderline();

        if (!selectedLine) {
            this.dialog.add(AlertDialog, {
                title: _t("No line selected"),
                body: _t("Please select a product line to apply the discount."),
            });
            return;
        }

        const discountValue = await makeAwaitable(this.dialog, NumberPopup, {
            title: _t("Fixed Discount Amount"),
            startingValue: 0,
        });

        if (discountValue !== undefined && discountValue !== null) {
            const amount = parseFloat(discountValue);
            if (isNaN(amount) || amount < 0) {
                return;
            }

            const price = selectedLine.price_unit;
            const qty = selectedLine.qty;
            const totalBeforeDiscount = price * qty;

            if (totalBeforeDiscount <= 0) {
                return;
            }

            // Calculate percentage: (amount / totalBeforeDiscount) * 100
            // Odoo's discount field is a percentage.
            const discountPercentage = (amount / totalBeforeDiscount) * 100;

            if (discountPercentage > 100) {
                this.dialog.add(AlertDialog, {
                    title: _t("Invalid Discount"),
                    body: _t("Discount cannot exceed the total amount of the line."),
                });
                return;
            }

            selectedLine.set_discount(discountPercentage);

            if (this.props.close) {
                this.props.close();
            }
        }
    }
});

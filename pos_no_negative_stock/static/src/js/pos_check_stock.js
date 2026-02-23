/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { PosStore } from "@point_of_sale/app/store/pos_store";
import { PosOrderline } from "@point_of_sale/app/models/pos_order_line";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { _t } from "@web/core/l10n/translation";

patch(PosStore.prototype, {
    async addLineToOrder(vals, order, opts = {}, configure = true) {
        let product = vals.product_id;
        if (typeof product === "number") {
            product = this.data.models["product.product"].get(product);
        }

        if (product && (product.is_storable || product.type === 'product')) {
            const stockQty = product.qty_available !== undefined ? product.qty_available : product.free_qty;

            if (stockQty !== undefined) {
                let alreadyOrdered = 0;
                const currentOrder = order || this.get_order();
                const orderLines = currentOrder ? currentOrder.get_orderlines() : [];
                for (const line of orderLines) {
                    if (line.product_id && line.product_id.id === product.id) {
                        alreadyOrdered += line.qty || 0;
                    }
                }

                const addingQty = vals.qty !== undefined ? vals.qty : 1;
                const totalQty = alreadyOrdered + addingQty;

                if (totalQty > stockQty) {
                    const remaining = Math.max(0, stockQty - alreadyOrdered);
                    this.dialog.add(AlertDialog, {
                        title: _t("Insufficient Stock"),
                        body: _t(
                            "Insufficient stock for %s. You can only add %s more unit(s). Available: %s, in order: %s.",
                            product.display_name, remaining, stockQty, alreadyOrdered
                        ),
                    });
                    return;
                }
            }
        }
        return super.addLineToOrder(...arguments);
    },
});

patch(PosOrderline.prototype, {
    set_quantity(quantity, keep_price) {
        const product = this.product_id;
        if (product && (product.is_storable || product.type === 'product')) {
            const stockQty = product.qty_available !== undefined ? product.qty_available : product.free_qty;
            if (stockQty !== undefined) {
                const quant = typeof quantity === "number" ? quantity : parseFloat("" + (quantity ? quantity : 0));

                // Don't block if reducing quantity
                if (quant <= this.qty) {
                    return super.set_quantity(...arguments);
                }

                // Sum other lines of the same product
                let otherLinesQty = 0;
                const orderLines = this.order_id ? this.order_id.get_orderlines() : [];
                for (const line of orderLines) {
                    if (line !== this && line.product_id && line.product_id.id === product.id) {
                        otherLinesQty += line.qty || 0;
                    }
                }

                const totalQty = otherLinesQty + quant;
                if (totalQty > stockQty) {
                    const remaining = Math.max(0, stockQty - otherLinesQty);
                    // Returning an object is the standard Odoo 18 way for models to report errors to UI
                    return {
                        title: _t("Insufficient Stock"),
                        body: _t(
                            "Insufficient stock for %s. Max allowed for this line: %s (Available: %s, other lines: %s).",
                            product.display_name, remaining, stockQty, otherLinesQty
                        ),
                    };
                }
            }
        }
        return super.set_quantity(...arguments);
    }
});

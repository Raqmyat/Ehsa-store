/** @odoo-module */
import { PosOrderline } from "@point_of_sale/app/models/pos_order_line";
import { patch } from "@web/core/utils/patch";
import { _t } from "@web/core/l10n/translation";

patch(PosOrderline.prototype, {
    set_discount(discount) {
        /** Add Popup error when Discount Limit is applied for POS Orderline **/
        const order = this.order_id;
        if (order) {
            const product = this.get_product();
            const rounded = Math.round(discount);
            const pos_categ = product.pos_categ_ids && product.pos_categ_ids.length > 0 ? product.pos_categ_ids[0] : null;

            if (order.config.apply_discount_limit === 'product_category' && pos_categ) {
                if (pos_categ.discount_limit && rounded > pos_categ.discount_limit) {
                    return {
                        title: _t("Discount Not Possible"),
                        body: _t("You cannot apply discount above the discount limit."),
                    };
                }
            } else if (order.config.apply_discount_limit === 'product') {
                if (product.product_discount_limit && rounded > product.product_discount_limit) {
                    return {
                        title: _t("Discount Not Possible"),
                        body: _t("You cannot apply discount above the discount limit."),
                    };
                }
            }
        }
        return super.set_discount(discount);
    },
});

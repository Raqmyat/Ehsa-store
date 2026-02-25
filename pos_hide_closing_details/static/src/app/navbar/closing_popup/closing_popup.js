import { ClosePosPopup } from "@point_of_sale/app/navbar/closing_popup/closing_popup";
import { patch } from "@web/core/utils/patch";

patch(ClosePosPopup, {
    props: [
        ...ClosePosPopup.props,
        "can_show_closing_details?",
    ],
});

patch(ClosePosPopup.prototype, {
    canShowClosingDetails() {
        return this.props.can_show_closing_details;
    },
});

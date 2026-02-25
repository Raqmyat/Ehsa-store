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
        console.log("POS Hide Debug - can_show_closing_details:", this.props.can_show_closing_details);
        console.log("POS Hide Debug - is_manager:", this.props.is_manager);
        return this.props.can_show_closing_details;
    },
});

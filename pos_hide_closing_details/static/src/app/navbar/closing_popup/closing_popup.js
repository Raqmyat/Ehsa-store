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
        const canShow = this.props.can_show_closing_details;
        console.log("POS Hide Debug - Final Decision (can_show):", canShow);
        return canShow;
    },
    get dialogProps() {
        const props = super.dialogProps;
        if (!this.canShowClosingDetails()) {
            console.log("POS Hide Debug - Applying CSS Class 'pos-hide-details'");
            props.contentClass = (props.contentClass || "") + " pos-hide-details";
        }
        return props;
    },
    async confirm() {
        // Bypass all difference checks and warning messages
        await this.closeSession();
    },
});

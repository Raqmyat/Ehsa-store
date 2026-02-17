from odoo import models
import requests

class StockPicking(models.Model):
    _inherit = 'stock.picking'


    def update_product_qty_in_salla(self):
        for picking in self:

            for move_line in picking.move_line_ids:
                product = move_line.product_id
                product.invalidate_recordset(['qty_available'])
                current_qty = int(product.qty_available)

                for mapping in product.channel_mapping_ids:
                    if mapping.channel_id.channel != 'salla':
                        continue

                    salla_variant_id = getattr(mapping, 'store_variant_id', False)
                    access_token = mapping.channel_id.access_token
                    branch_id = mapping.channel_id.salla_branch_id

                    if not salla_variant_id or not access_token:
                        continue

                    url = f"https://api.salla.dev/admin/v2/products/variants/{salla_variant_id}"

                    headers = {
                        "Authorization": f"Bearer {access_token}",
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                    }
                    if not branch_id:
                        branch_id = 1680270783

                    payload = {
                        "quantities": [
                            {
                                "branch": int(branch_id),
                                "quantity": current_qty
                            }
                        ]
                    }

                    try:
                        response = requests.put(url=url, json=payload, headers=headers, timeout=15)

                        if response.status_code in [200, 201]:
                            print(
                                f"[SALLA SUCCESS] Variant {product.name} updated in branch {branch_id} to {current_qty}")
                        else:
                            print(f"[SALLA ERROR] {response.status_code}: {response.text}")

                    except Exception as e:
                        print(f"[SALLA EXCEPTION] {str(e)}")

    def button_validate(self):
        res = super().button_validate()

        self.update_product_qty_in_salla()

        return res